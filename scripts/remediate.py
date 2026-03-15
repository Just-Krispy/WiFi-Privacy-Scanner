#!/usr/bin/env python3
"""
WiFi Privacy Scanner - Remediation Scripts
Generates platform-specific scripts to mitigate detected WiFi privacy threats.
"""

import io
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# Platform-specific remediation commands
REMEDIATIONS = {
    "mac_randomization": {
        "title": "Enable MAC Address Randomization",
        "severity": "HIGH",
        "description": "Prevents tracking across WiFi networks by randomizing your hardware address.",
        "windows": {
            "info": "Windows 10/11 supports random hardware addresses per network.",
            "steps": [
                "Open Settings > Network & Internet > WiFi",
                "Click your connected network",
                "Set 'Random hardware addresses' to ON",
                "Or enable globally: Settings > Network & Internet > WiFi > Random hardware addresses = ON",
            ],
            "script": """@echo off
echo ============================================
echo   MAC Address Randomization - Windows
echo ============================================
echo.
echo Enabling random hardware addresses via registry...
echo.
reg add "HKLM\\SOFTWARE\\Microsoft\\WlanSvc\\Interfaces" /v RandomMacState /t REG_DWORD /d 1 /f 2>nul
echo.
echo NOTE: You can also enable this per-network in:
echo   Settings ^> Network ^& Internet ^> WiFi ^> [Your Network] ^> Random hardware addresses
echo.
echo Restart your WiFi adapter for changes to take effect.
echo.
netsh interface set interface "Wi-Fi" disable
timeout /t 2 /nobreak >nul
netsh interface set interface "Wi-Fi" enable
echo.
echo Done! Your MAC address will now be randomized.
pause
""",
            "filename": "enable_mac_randomization.bat"
        },
        "linux": {
            "info": "NetworkManager supports MAC randomization natively.",
            "steps": [
                "Edit /etc/NetworkManager/conf.d/mac-random.conf",
                "Add [device] and wifi.scan-rand-mac-address=yes",
                "Restart NetworkManager",
            ],
            "script": """#!/bin/bash
echo "============================================"
echo "  MAC Address Randomization - Linux"
echo "============================================"
echo ""

# Create NetworkManager config for MAC randomization
sudo tee /etc/NetworkManager/conf.d/mac-random.conf > /dev/null << 'CONF'
[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
CONF

echo "Config written to /etc/NetworkManager/conf.d/mac-random.conf"
echo "Restarting NetworkManager..."
sudo systemctl restart NetworkManager
echo ""
echo "Done! Your MAC address will now be randomized on every connection."
""",
            "filename": "enable_mac_randomization.sh"
        },
        "darwin": {
            "info": "macOS randomizes MAC by default since Sonoma. For older versions:",
            "steps": [
                "Open System Settings > WiFi",
                "Click (i) next to your network",
                "Enable 'Private Wi-Fi Address'",
            ],
            "script": """#!/bin/bash
echo "============================================"
echo "  MAC Address Randomization - macOS"
echo "============================================"
echo ""
echo "macOS 14+ (Sonoma) randomizes MAC addresses by default."
echo ""
echo "To verify or enable manually:"
echo "  1. Open System Settings > WiFi"
echo "  2. Click the (i) icon next to your network"
echo "  3. Enable 'Private Wi-Fi Address'"
echo ""
echo "For temporary randomization on current session:"
sudo ifconfig en0 ether $(openssl rand -hex 6 | sed 's/\\(..\\)/\\1:/g; s/.$//')
echo "MAC address randomized for this session."
""",
            "filename": "enable_mac_randomization.sh"
        }
    },
    "disable_wps": {
        "title": "Disable WPS (WiFi Protected Setup)",
        "severity": "MEDIUM",
        "description": "WPS has known vulnerabilities that allow brute-force attacks on your router PIN.",
        "windows": {
            "info": "WPS must be disabled in your router's admin panel.",
            "steps": [
                "Open a browser and go to your router admin page (usually 192.168.1.1 or 192.168.0.1)",
                "Login with admin credentials",
                "Navigate to WiFi/Wireless settings",
                "Find WPS and set it to DISABLED",
                "Save and reboot router",
            ],
            "script": """@echo off
echo ============================================
echo   Disable WPS - Router Admin
echo ============================================
echo.
echo Finding your router gateway address...
for /f "tokens=3" %%i in ('route print ^| findstr "0.0.0.0.*0.0.0.0"') do (
    echo Your router admin page is likely: http://%%i
    start http://%%i
    goto :done
)
:done
echo.
echo Steps:
echo   1. Login to your router admin panel
echo   2. Go to WiFi / Wireless settings
echo   3. Find WPS and set to DISABLED
echo   4. Save and reboot
echo.
pause
""",
            "filename": "disable_wps.bat"
        },
        "linux": {
            "info": "Disable WPS in your router admin panel.",
            "steps": ["Login to your router admin page", "Disable WPS in wireless settings"],
            "script": """#!/bin/bash
echo "============================================"
echo "  Disable WPS - Router Admin"
echo "============================================"
echo ""
GW=$(ip route | grep default | awk '{print $3}')
echo "Your router admin page is likely: http://$GW"
echo "Opening in browser..."
xdg-open "http://$GW" 2>/dev/null || echo "Open http://$GW in your browser"
echo ""
echo "Steps:"
echo "  1. Login to router admin panel"
echo "  2. Go to WiFi/Wireless settings"
echo "  3. Disable WPS"
echo "  4. Save and reboot"
""",
            "filename": "disable_wps.sh"
        },
        "darwin": {
            "info": "Disable WPS in your router admin panel.",
            "steps": ["Login to your router admin page", "Disable WPS in wireless settings"],
            "script": """#!/bin/bash
echo "============================================"
echo "  Disable WPS - Router Admin"
echo "============================================"
GW=$(netstat -rn | grep default | awk '{print $2}' | head -1)
echo "Your router admin page is likely: http://$GW"
open "http://$GW"
echo "Disable WPS in WiFi/Wireless settings."
""",
            "filename": "disable_wps.sh"
        }
    },
    "disable_xfinity_motion": {
        "title": "Disable Xfinity Motion Sensing",
        "severity": "HIGH",
        "vendor": "Xfinity",
        "description": "Xfinity XB6/7/8 gateways have built-in motion sensing. This disables it.",
        "windows": {
            "info": "Motion sensing is controlled via the Xfinity app or web portal.",
            "steps": [
                "Open the Xfinity app on your phone",
                "Go to More > WiFi > Advanced Security",
                "Find 'Xfinity xFi Advanced Security' settings",
                "Disable 'Motion Sensing' or 'Home Presence'",
                "Alternatively: login to xfinity.com/myxfi",
            ],
            "script": """@echo off
echo ============================================
echo   Disable Xfinity Motion Sensing
echo ============================================
echo.
echo Xfinity motion sensing is controlled via the Xfinity app.
echo.
echo Option 1 - Xfinity App:
echo   1. Open the Xfinity app
echo   2. Go to More ^> WiFi
echo   3. Tap Advanced Security
echo   4. Disable Motion Sensing / Home Presence
echo.
echo Option 2 - Web Portal:
start https://www.xfinity.com/myxfi
echo   Opening xfinity.com/myxfi in your browser...
echo   Navigate to Advanced Security and disable motion features.
echo.
echo Option 3 - Replace the Xfinity gateway:
echo   Use your own router in bridge mode to bypass all Xfinity sensing.
echo   Call Xfinity: 1-800-934-6489 to enable bridge mode.
echo.
pause
""",
            "filename": "disable_xfinity_motion.bat"
        },
        "linux": {
            "info": "Xfinity motion sensing must be disabled via the Xfinity app or web portal.",
            "steps": ["Use Xfinity app or visit xfinity.com/myxfi", "Disable motion sensing"],
            "script": """#!/bin/bash
echo "Opening Xfinity portal..."
xdg-open "https://www.xfinity.com/myxfi" 2>/dev/null
echo "Disable Motion Sensing in Advanced Security settings."
echo "Or use your own router in bridge mode to bypass Xfinity sensing."
""",
            "filename": "disable_xfinity_motion.sh"
        },
        "darwin": {
            "info": "Same as above — use Xfinity app or web portal.",
            "steps": ["Use Xfinity app or visit xfinity.com/myxfi"],
            "script": """#!/bin/bash
open "https://www.xfinity.com/myxfi"
echo "Disable Motion Sensing in Advanced Security settings."
""",
            "filename": "disable_xfinity_motion.sh"
        }
    },
    "disable_upnp": {
        "title": "Disable UPnP (Universal Plug and Play)",
        "severity": "MEDIUM",
        "description": "UPnP allows devices to automatically open ports, creating security vulnerabilities.",
        "windows": {
            "info": "UPnP can be disabled both on Windows and on your router.",
            "steps": [
                "On Windows: Services > SSDP Discovery > Stop and Disable",
                "On Router: Admin panel > Advanced > UPnP > Disable",
            ],
            "script": """@echo off
echo ============================================
echo   Disable UPnP - Windows + Router
echo ============================================
echo.
echo Disabling SSDP Discovery service (Windows UPnP)...
net stop SSDPSRV 2>nul
sc config SSDPSRV start= disabled
echo.
echo Windows UPnP client disabled.
echo.
echo IMPORTANT: You should also disable UPnP on your router:
for /f "tokens=3" %%i in ('route print ^| findstr "0.0.0.0.*0.0.0.0"') do (
    echo   Router admin: http://%%i
    echo   Navigate to Advanced ^> UPnP ^> Disable
)
echo.
pause
""",
            "filename": "disable_upnp.bat"
        },
        "linux": {
            "info": "Disable UPnP client and check router settings.",
            "steps": ["Remove miniupnpc if installed", "Disable UPnP on router"],
            "script": """#!/bin/bash
echo "Removing UPnP client tools..."
sudo apt remove -y miniupnpc 2>/dev/null
echo "UPnP client removed."
echo ""
GW=$(ip route | grep default | awk '{print $3}')
echo "Also disable UPnP on your router: http://$GW"
echo "Navigate to Advanced > UPnP > Disable"
""",
            "filename": "disable_upnp.sh"
        },
        "darwin": {
            "info": "macOS doesn't have UPnP enabled by default. Check your router.",
            "steps": ["Disable UPnP on your router admin panel"],
            "script": """#!/bin/bash
GW=$(netstat -rn | grep default | awk '{print $2}' | head -1)
echo "Disable UPnP on your router: http://$GW"
open "http://$GW"
""",
            "filename": "disable_upnp.sh"
        }
    },
    "dns_privacy": {
        "title": "Switch to Privacy-Focused DNS",
        "severity": "MEDIUM",
        "description": "Your ISP can see every domain you visit via DNS. Switching to encrypted DNS prevents this.",
        "windows": {
            "info": "Windows 11 supports DNS-over-HTTPS natively.",
            "steps": [
                "Settings > Network > WiFi > Hardware properties",
                "Set DNS to: 1.1.1.1 (Cloudflare) or 9.9.9.9 (Quad9)",
                "Enable DNS over HTTPS",
            ],
            "script": """@echo off
echo ============================================
echo   Privacy DNS Setup - Windows
echo ============================================
echo.
echo Setting DNS to Cloudflare (1.1.1.1) with encryption...
echo.
netsh interface ip set dns "Wi-Fi" static 1.1.1.1 primary
netsh interface ip add dns "Wi-Fi" 1.0.0.1 index=2
echo.
echo DNS set to Cloudflare (1.1.1.1, 1.0.0.1)
echo.
echo To enable DNS-over-HTTPS (Windows 11):
echo   Settings ^> Network ^> WiFi ^> Hardware properties
echo   Set DNS encryption to "Encrypted only (DNS over HTTPS)"
echo.
echo Alternative privacy DNS providers:
echo   Quad9:    9.9.9.9 / 149.112.112.112
echo   Mullvad:  194.242.2.2
echo.
pause
""",
            "filename": "setup_privacy_dns.bat"
        },
        "linux": {
            "info": "Use systemd-resolved with DoT or install stubby for DoH.",
            "steps": ["Set DNS in /etc/systemd/resolved.conf", "Enable DNS over TLS"],
            "script": """#!/bin/bash
echo "============================================"
echo "  Privacy DNS Setup - Linux"
echo "============================================"
echo ""
echo "Setting DNS to Cloudflare with DNS-over-TLS..."
sudo tee /etc/systemd/resolved.conf > /dev/null << 'CONF'
[Resolve]
DNS=1.1.1.1 1.0.0.1
FallbackDNS=9.9.9.9 149.112.112.112
DNSOverTLS=yes
CONF
sudo systemctl restart systemd-resolved
echo "Done! DNS set to Cloudflare with TLS encryption."
echo ""
echo "Verify: resolvectl status"
resolvectl status | grep "DNS Server" | head -4
""",
            "filename": "setup_privacy_dns.sh"
        },
        "darwin": {
            "info": "macOS supports encrypted DNS via configuration profiles.",
            "steps": [
                "System Settings > Network > WiFi > Details > DNS",
                "Add 1.1.1.1 and 1.0.0.1",
                "For DoH, install Cloudflare 1.1.1.1 app",
            ],
            "script": """#!/bin/bash
echo "Setting DNS to Cloudflare..."
networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1
echo "DNS set. Verify:"
networksetup -getdnsservers Wi-Fi
echo ""
echo "For encrypted DNS, install the 1.1.1.1 app from the App Store."
""",
            "filename": "setup_privacy_dns.sh"
        }
    },
    "wifi_auto_connect": {
        "title": "Disable Auto-Connect to Open Networks",
        "severity": "HIGH",
        "description": "Prevents your device from automatically connecting to unknown or rogue WiFi networks.",
        "windows": {
            "info": "Disable auto-connect for saved networks and open hotspots.",
            "steps": [
                "Settings > Network > WiFi > Manage known networks",
                "For each network, disable 'Connect automatically'",
            ],
            "script": """@echo off
echo ============================================
echo   Disable WiFi Auto-Connect - Windows
echo ============================================
echo.
echo Listing saved WiFi profiles...
netsh wlan show profiles
echo.
echo Disabling auto-connect for all saved profiles...
for /f "tokens=2 delims=:" %%a in ('netsh wlan show profiles ^| findstr "Profile"') do (
    set "profile=%%a"
    setlocal enabledelayedexpansion
    set "profile=!profile:~1!"
    netsh wlan set profileparameter name="!profile!" connectionmode=manual 2>nul
    echo   Disabled auto-connect: !profile!
    endlocal
)
echo.
echo Done! Networks will no longer auto-connect.
echo You'll need to manually select and connect each time.
pause
""",
            "filename": "disable_auto_connect.bat"
        },
        "linux": {
            "info": "Disable auto-connect in NetworkManager.",
            "steps": ["nmcli connection modify <name> autoconnect no"],
            "script": """#!/bin/bash
echo "Disabling auto-connect for all saved WiFi networks..."
for conn in $(nmcli -t -f NAME,TYPE connection show | grep wireless | cut -d: -f1); do
    nmcli connection modify "$conn" autoconnect no
    echo "  Disabled: $conn"
done
echo "Done! You'll need to manually connect to WiFi networks."
""",
            "filename": "disable_auto_connect.sh"
        },
        "darwin": {
            "info": "Disable auto-join in WiFi settings.",
            "steps": ["System Settings > WiFi > (i) next to network > Auto-Join OFF"],
            "script": """#!/bin/bash
echo "To disable auto-connect on macOS:"
echo "  System Settings > WiFi"
echo "  Click (i) next to each saved network"
echo "  Toggle OFF 'Auto-Join'"
open "x-apple.systempreferences:com.apple.wifi-settings"
""",
            "filename": "disable_auto_connect.sh"
        }
    }
}


def generate_remediation_scripts(scan_data, output_dir):
    """Generate platform-specific remediation scripts based on scan results."""
    os_name = platform.system().lower()
    os_key = {'windows': 'windows', 'linux': 'linux', 'darwin': 'darwin'}.get(os_name, 'windows')

    scripts_dir = Path(output_dir) / 'remediation'
    scripts_dir.mkdir(parents=True, exist_ok=True)

    generated = []

    # Always include general hardening scripts
    general_keys = ['mac_randomization', 'disable_wps', 'disable_upnp', 'dns_privacy', 'wifi_auto_connect']

    # Add vendor-specific scripts based on scan results
    vendor_keys = []
    for net in scan_data.get('networks', []):
        if net.get('vendor_match') == 'Xfinity':
            vendor_keys.append('disable_xfinity_motion')

    all_keys = list(dict.fromkeys(vendor_keys + general_keys))  # dedup, vendor first

    for key in all_keys:
        rem = REMEDIATIONS.get(key)
        if not rem:
            continue
        plat = rem.get(os_key)
        if not plat:
            continue

        # Write the script file
        filename = plat['filename']
        filepath = scripts_dir / filename
        with open(filepath, 'w', encoding='utf-8', newline='\n' if os_key != 'windows' else None) as f:
            f.write(plat['script'])

        # Make executable on Unix
        if os_key != 'windows':
            os.chmod(filepath, 0o755)

        generated.append({
            'key': key,
            'title': rem['title'],
            'severity': rem['severity'],
            'description': rem['description'],
            'filename': filename,
            'filepath': str(filepath),
            'steps': plat['steps'],
            'info': plat['info'],
            'vendor': rem.get('vendor'),
        })

    # Write a summary index
    summary = {
        'generated_at': datetime.now().isoformat(),
        'platform': os_key,
        'scripts_count': len(generated),
        'scripts': generated,
    }
    summary_file = scripts_dir / 'remediation_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return generated


def main():
    """CLI entry point — can run standalone or after a scan."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate WiFi privacy remediation scripts')
    parser.add_argument('scan_json', nargs='?', help='Path to scan results JSON (optional)')
    parser.add_argument('--output-dir', default='./output', help='Output directory')
    args = parser.parse_args()

    # Load scan data if provided
    scan_data = {}
    if args.scan_json:
        with open(args.scan_json, 'r', encoding='utf-8') as f:
            scan_data = json.load(f)
        print(f"Loaded scan data: {scan_data.get('threats_found', 0)} threats found")

    print(f"\n\U0001f6e0  Generating remediation scripts for {platform.system()}...\n")

    scripts = generate_remediation_scripts(scan_data, args.output_dir)

    for s in scripts:
        sev_icon = '\U0001f6a8' if s['severity'] == 'HIGH' else '\u26a0'
        print(f"  {sev_icon} {s['title']}")
        print(f"     Script: {s['filename']}")
        print(f"     {s['description']}")
        print()

    print(f"\u2705 Generated {len(scripts)} remediation scripts in: {args.output_dir}/remediation/")
    print(f"   Run each script to harden your network privacy.\n")


if __name__ == '__main__':
    main()
