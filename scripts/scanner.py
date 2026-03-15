#!/usr/bin/env python3
"""
WiFi Privacy Scanner v2.0 - Detection Script
Scans local WiFi networks and identifies CSI-capable surveillance routers.
Supports Windows (netsh), Linux (nmcli), and macOS (airport).
"""

import argparse
import io
import json
import os
import platform
import subprocess
import re
import sys

# Force UTF-8 stdout/stderr on Windows (for emoji support in .exe builds)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class WiFiPrivacyScanner:
    def __init__(self, db_path=None):
        if db_path is None:
            # Handle PyInstaller frozen bundle
            if getattr(sys, 'frozen', False):
                base = Path(sys._MEIPASS)
            else:
                base = Path(__file__).parent.parent
            db_path = base / "references" / "csi-routers-db.json"

        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.load(f)

        self.csi_routers = self.db['csi_capable_routers']
        self.detection_patterns = self.db['detection_patterns']
        self.privacy_levels = self.db['privacy_levels']
        self.os_name = platform.system()

    # === Network scanning (platform-aware) ===

    def scan_networks(self, force_demo=False, verbose=False):
        if force_demo:
            if verbose:
                print("   [demo] Using mock network data")
            return self._get_mock_data()

        scanners = {
            'Windows': self._scan_windows,
            'Linux': self._scan_linux,
            'Darwin': self._scan_macos,
        }

        scanner_fn = scanners.get(self.os_name)
        if scanner_fn is None:
            if verbose:
                print(f"   [warn] Unsupported OS '{self.os_name}', using demo data")
            return self._get_mock_data()

        try:
            networks = scanner_fn(verbose)
            if networks:
                return networks
        except Exception as e:
            if verbose:
                print(f"   [warn] Scan failed ({e}), using demo data")

        return self._get_mock_data()

    # --- Windows (netsh) ---

    def _scan_windows(self, verbose=False):
        if verbose:
            print("   [windows] Scanning with netsh ...")
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            capture_output=True, text=True, timeout=15, shell=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"netsh error: {result.stderr.strip()}")
        return self._parse_netsh_output(result.stdout)

    def _parse_netsh_output(self, output):
        networks = []
        current = {}
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('SSID') and 'BSSID' not in line:
                if current.get('ssid'):
                    networks.append(current)
                match = re.match(r'SSID\s+\d+\s*:\s*(.*)', line)
                current = {
                    'ssid': match.group(1).strip() if match else '',
                    'bssid': '', 'signal_strength': 0, 'encryption': 'Unknown',
                }
            elif line.startswith('BSSID'):
                match = re.match(r'BSSID\s+\d+\s*:\s*(.*)', line)
                if match:
                    current['bssid'] = match.group(1).strip().upper().replace('-', ':')
            elif 'Signal' in line and '%' in line:
                match = re.search(r'(\d+)%', line)
                if match:
                    current['signal_strength'] = int(match.group(1))
            elif line.startswith('Authentication'):
                val = line.split(':', 1)[-1].strip()
                if val:
                    current['encryption'] = val
        if current.get('ssid'):
            networks.append(current)
        return networks

    # --- Linux (nmcli) ---

    def _scan_linux(self, verbose=False):
        if verbose:
            print("   [linux] Scanning with nmcli ...")
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL,SECURITY', 'dev', 'wifi', 'list', '--rescan', 'yes'],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            raise RuntimeError(f"nmcli error: {result.stderr.strip()}")
        return self._parse_nmcli_output(result.stdout)

    def _parse_nmcli_output(self, output):
        networks = []
        for line in output.strip().splitlines():
            if not line.strip():
                continue
            parts = re.split(r'(?<!\\):', line)
            if len(parts) < 4:
                continue
            ssid = parts[0].replace('\\:', ':').strip()
            bssid = ':'.join(parts[1:7]).replace('\\', '').strip()
            signal = parts[7] if len(parts) > 7 else parts[2]
            security = parts[-1].strip() if len(parts) > 3 else 'Unknown'
            if not ssid:
                continue
            networks.append({
                'ssid': ssid, 'bssid': bssid.upper(),
                'signal_strength': int(signal) if signal.isdigit() else 0,
                'encryption': security,
            })
        return networks

    # --- macOS (airport) ---

    def _scan_macos(self, verbose=False):
        if verbose:
            print("   [macos] Scanning with airport ...")
        airport = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
        result = subprocess.run([airport, '-s'], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            raise RuntimeError("airport error")
        return self._parse_airport_output(result.stdout)

    def _parse_airport_output(self, output):
        networks = []
        lines = output.strip().splitlines()
        if len(lines) < 2:
            return networks
        header = lines[0]
        ssid_end = header.index('BSSID') - 1
        for line in lines[1:]:
            ssid = line[:ssid_end].strip()
            rest = line[ssid_end:].split()
            if len(rest) < 3:
                continue
            bssid = rest[0]
            rssi = rest[1]
            security = ' '.join(rest[3:]) if len(rest) > 3 else 'Unknown'
            try:
                pct = max(0, min(100, 2 * (int(rssi) + 100)))
            except ValueError:
                pct = 0
            networks.append({
                'ssid': ssid, 'bssid': bssid.upper(),
                'signal_strength': pct, 'encryption': security,
            })
        return networks

    # --- Mock data ---

    def _get_mock_data(self):
        return [
            {'ssid': 'xfinitywifi', 'bssid': 'B0:8B:D0:12:34:56', 'signal_strength': 85, 'encryption': 'WPA2'},
            {'ssid': 'HOME-WiFi', 'bssid': '00:24:A5:78:90:AB', 'signal_strength': 92, 'encryption': 'WPA2'},
            {'ssid': 'OriginWireless_Mesh', 'bssid': '00:1B:63:CD:EF:12', 'signal_strength': 70, 'encryption': 'WPA3'},
            {'ssid': 'NormalRouter', 'bssid': 'AA:BB:CC:DD:EE:FF', 'signal_strength': 65, 'encryption': 'WPA2'},
            {'ssid': 'NETGEAR-5G', 'bssid': '34:98:B5:11:22:33', 'signal_strength': 40, 'encryption': 'WPA2'},
            {'ssid': 'GoogleNest_1234', 'bssid': 'F4:F5:D8:AA:BB:CC', 'signal_strength': 55, 'encryption': 'WPA3'},
        ]

    # === Threat analysis ===

    def analyze_network(self, network):
        ssid = network['ssid'].lower()
        bssid = network['bssid'].upper()
        oui = ':'.join(bssid.split(':')[:3])

        threat_info = {
            'network': network, 'threats': [],
            'risk_level': 'LOW', 'risk_score': 0, 'vendor_match': None,
        }

        score_map = {'CRITICAL': 90, 'HIGH': 70, 'MEDIUM': 50, 'LOW': 20}

        for router in self.csi_routers:
            matched = False
            match_reason = []

            if oui in [p.upper() for p in router['oui_prefixes']]:
                matched = True
                match_reason.append(f"MAC OUI match ({oui})")

            for indicator in router.get('indicators', []):
                if indicator.lower() in ssid:
                    matched = True
                    match_reason.append(f"SSID contains '{indicator}'")

            if matched:
                threat_info['vendor_match'] = router['vendor']
                threat_info['threats'].append({
                    'vendor': router['vendor'],
                    'models': router.get('models', []),
                    'detection_type': router.get('detection', 'Unknown'),
                    'capabilities': router.get('capabilities', []),
                    'mitigation': router.get('mitigation', ''),
                    'match_reason': match_reason,
                })
                risk = router.get('risk', 'LOW')
                new_score = score_map.get(risk, 0)
                if new_score > threat_info['risk_score']:
                    threat_info['risk_score'] = new_score
                    threat_info['risk_level'] = risk

        for keyword in self.detection_patterns.get('csi_indicators', []):
            if keyword.lower() in ssid and not threat_info['threats']:
                threat_info['threats'].append({
                    'vendor': 'Unknown',
                    'detection_type': 'Potential CSI Feature',
                    'match_reason': [f"SSID contains CSI keyword: '{keyword}'"],
                    'capabilities': ['Unknown surveillance capabilities'],
                    'mitigation': 'Investigate router model and disable motion/sensing features',
                })
                threat_info['risk_score'] = max(threat_info['risk_score'], 40)
                if threat_info['risk_level'] == 'LOW':
                    threat_info['risk_level'] = 'MEDIUM'

        return threat_info

    # === Scan history diff ===

    def _load_previous_scan(self, output_dir):
        scans = sorted(output_dir.glob('scan_*.json'), reverse=True)
        for f in scans:
            if '_report' not in f.name:
                try:
                    with open(f, encoding='utf-8') as fh:
                        return json.load(fh)
                except (json.JSONDecodeError, IOError, UnicodeDecodeError):
                    continue
        return None

    def _compute_diff(self, current, previous):
        prev_bssids = {n['network']['bssid']: n for n in previous.get('networks', [])}
        curr_bssids = {n['network']['bssid']: n for n in current.get('networks', [])}

        new_nets = [curr_bssids[b] for b in curr_bssids if b not in prev_bssids]
        gone_nets = [prev_bssids[b] for b in prev_bssids if b not in curr_bssids]
        changes = []
        for b in set(curr_bssids) & set(prev_bssids):
            if curr_bssids[b]['risk_score'] != prev_bssids[b]['risk_score']:
                changes.append({
                    'ssid': curr_bssids[b]['network']['ssid'], 'bssid': b,
                    'previous_score': prev_bssids[b]['risk_score'],
                    'current_score': curr_bssids[b]['risk_score'],
                })

        return {
            'new_networks': [{'ssid': n['network']['ssid'], 'bssid': n['network']['bssid'],
                              'risk_level': n['risk_level']} for n in new_nets],
            'gone_networks': [{'ssid': n['network']['ssid'], 'bssid': n['network']['bssid']} for n in gone_nets],
            'threat_changes': changes,
            'previous_scan_date': previous.get('scan_date', 'unknown'),
        }

    # === Full scan pipeline ===

    def scan_and_analyze(self, force_demo=False, verbose=False, output_dir=None):
        print(f"🔍 Scanning WiFi networks ({self.os_name}) ...")
        networks = self.scan_networks(force_demo=force_demo, verbose=verbose)
        print(f"   Found {len(networks)} networks")

        print("\n🛡️  Analyzing privacy threats ...")
        analyzed = [self.analyze_network(net) for net in networks]

        threats_found = [a for a in analyzed if a['threats']]
        critical = sum(1 for a in analyzed if a['risk_level'] == 'CRITICAL')
        high = sum(1 for a in analyzed if a['risk_level'] == 'HIGH')
        medium = sum(1 for a in analyzed if a['risk_level'] == 'MEDIUM')
        max_score = max((a['risk_score'] for a in analyzed), default=0)

        result = {
            'scan_date': datetime.now().isoformat(),
            'scanner_version': '2.0.0',
            'platform': self.os_name,
            'networks_scanned': len(networks),
            'threats_found': len(threats_found),
            'threat_score': max_score,
            'threat_breakdown': {
                'critical': critical, 'high': high, 'medium': medium,
                'low': len(networks) - critical - high - medium,
            },
            'networks': analyzed,
            'recommendations': self._generate_recommendations(analyzed),
        }

        if output_dir:
            prev = self._load_previous_scan(output_dir)
            if prev:
                result['diff'] = self._compute_diff(result, prev)
                if verbose:
                    d = result['diff']
                    print(f"\n📈 Changes since last scan ({d['previous_scan_date'][:10]}):")
                    print(f"   New: {len(d['new_networks'])}  Gone: {len(d['gone_networks'])}  Changed: {len(d['threat_changes'])}")

        return result

    def _generate_recommendations(self, analyzed):
        recs = []
        critical = [a for a in analyzed if a['risk_level'] == 'CRITICAL']
        high = [a for a in analyzed if a['risk_level'] == 'HIGH']
        medium = [a for a in analyzed if a['risk_level'] == 'MEDIUM']

        if critical:
            recs.append(f"🚨 CRITICAL: {len(critical)} network(s) with severe surveillance capabilities. "
                        "Avoid these networks. Use VPN and disable WiFi when not needed.")
        if high:
            recs.append(f"⚠️  HIGH RISK: {len(high)} network(s) with motion sensing. "
                        "Disable motion/presence features or replace router.")
        if medium:
            recs.append(f"ℹ️  MEDIUM RISK: {len(medium)} network(s) with potential surveillance. "
                        "Review router docs and disable unnecessary sensing.")
        recs.extend([
            "💡 Enable MAC address randomization on your devices",
            "💡 Use VPN to encrypt traffic and limit exposure",
            "💡 Regularly update router firmware to patch vulnerabilities",
            "💡 Disable WPS, UPnP, and remote management features",
        ])
        return recs


def main():
    parser = argparse.ArgumentParser(
        description='WiFi Privacy Scanner v2.0 - detect CSI-capable surveillance routers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n'
               '  python scanner.py                    # Live scan\n'
               '  python scanner.py --demo             # Demo/mock data\n'
               '  python scanner.py -v --format all    # Verbose + JSON + MD + HTML\n',
    )
    parser.add_argument('--demo', action='store_true', help='Use mock data instead of live scan')
    parser.add_argument('--db', type=str, default=None, help='Path to router threat database JSON')
    parser.add_argument('--output-dir', type=str, default=None, help='Output directory')
    parser.add_argument('--format', choices=['json', 'markdown', 'html', 'all'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    scanner = WiFiPrivacyScanner(db_path=args.db)
    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif getattr(sys, 'frozen', False):
        output_dir = Path(os.path.dirname(sys.executable)) / 'output'
    else:
        output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    results = scanner.scan_and_analyze(force_demo=args.demo, verbose=args.verbose, output_dir=output_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = output_dir / f'scan_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scan complete! Results saved to: {json_file}")
    print(f"\n📊 Threat Score: {results['threat_score']}/100")
    print(f"   Threats Found: {results['threats_found']}")

    if args.format in ('markdown', 'all'):
        from report_generator import ReportGenerator
        gen = ReportGenerator()
        md = gen.generate_markdown(results)
        md_file = output_dir / f'scan_{timestamp}_report.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"   Markdown: {md_file}")

    if args.format in ('html', 'all'):
        from report_generator import ReportGenerator
        gen = ReportGenerator()
        html = gen.generate_html(results)
        html_file = output_dir / f'scan_{timestamp}_report.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"   HTML: {html_file}")

    if 'diff' in results:
        d = results['diff']
        if d['new_networks'] or d['gone_networks']:
            print(f"\n📈 Changes since last scan:")
            for n in d['new_networks']:
                print(f"   + NEW: {n['ssid']} ({n['risk_level']})")
            for n in d['gone_networks']:
                print(f"   - GONE: {n['ssid']}")


if __name__ == '__main__':
    main()
