# WiFi Privacy Scanner

**Detect CSI-capable surveillance routers in your WiFi environment.**

WiFi Privacy Scanner identifies routers and access points capable of Channel State Information (CSI) extraction — technology that can track your presence, motion, breathing rate, and even body position through walls, without cameras.

> **[Live Demo Report](https://just-krispy.github.io/WiFi-Privacy-Scanner/)** — See what a scan looks like

---

## What It Detects

| Vendor | Threat Level | Capabilities |
|--------|-------------|--------------|
| **Origin AI** | CRITICAL | Full CSI extraction, vital signs, breathing/heart rate, gait analysis |
| **WhoFi** | CRITICAL | 95.5% biometric accuracy, cross-venue tracking |
| **DensePose** | CRITICAL | Full body pose estimation through walls |
| **Xfinity** (XB6/7/8) | HIGH | Motion sensing, room-level occupancy |
| **Eero/Amazon** | HIGH | Motion detection, Amazon Sidewalk |
| **Linksys Aware** | HIGH | Whole-home motion detection |
| **Plume/HomePass** | HIGH | WiFi motion, ISP-level analytics |
| **Google Nest** | MEDIUM | Presence sensing, gesture recognition |
| **TP-Link** | MEDIUM | HomeShield motion detection |
| **ASUS** | MEDIUM | AiProtection device fingerprinting |
| **Netgear** | MEDIUM | Armor device fingerprinting |

**12 vendors, 52 OUI prefixes, 14 CSI keyword indicators**

---

## Quick Start

### Option 1: Python (all platforms)

```bash
# Clone the repo
git clone https://github.com/Just-Krispy/WiFi-Privacy-Scanner.git
cd WiFi-Privacy-Scanner

# Run a scan
python scan.py --format all
```

No dependencies required — uses Python standard library only.

### Option 2: Windows Executable

Download `WiFi-Privacy-Scanner.exe` from [Releases](https://github.com/Just-Krispy/WiFi-Privacy-Scanner/releases) — no Python needed.

```
WiFi-Privacy-Scanner.exe --format all
```

---

## Usage

```bash
python scan.py                      # Live scan, JSON output
python scan.py --format all         # JSON + Markdown + HTML reports
python scan.py --format html        # HTML report only
python scan.py --demo               # Demo mode (mock data)
python scan.py --demo --format all  # Demo with all report formats
python scan.py -v                   # Verbose output
python scan.py --help               # Full options
```

### Output

Reports are saved to the `output/` directory:
- **JSON** — Machine-readable scan data
- **Markdown** — Text report for documentation
- **HTML** — Interactive dashboard with animations, charts, and threat analysis

### Supported Platforms

| Platform | Scanner Tool | Status |
|----------|-------------|--------|
| **Windows** | `netsh wlan show networks` | Tested |
| **Linux** | `nmcli dev wifi list` | Tested |
| **macOS** | `airport -s` | Supported |
| **Headless/CI** | Mock data fallback | Auto-detected |

---

## HTML Report Features

The interactive HTML report includes:

- **Terminal boot sequence** with progress bar
- **Animated radar** with network blips positioned by signal strength
- **SVG threat gauge** with animated fill
- **Donut chart** threat breakdown
- **Signal strength bars** color-coded by threat level
- **Network topology** — force-directed graph with data-flow dots
- **Threat capability matrix** — heatmap of surveillance capabilities
- **Encryption analysis** with security grades (A+ through F)
- **Risk breakdown** showing what contributes to the score
- **Natural language summary** of findings
- **Smart recommendations** prioritized by severity
- **Network search & sort** — filter by name, vendor, or BSSID
- **Slide-out detail panel** — click any network for deep dive
- **Sound effects** — Web Audio synth (press M to mute)
- **Keyboard navigation** — J/K to navigate, Enter to open details
- **Export PDF** — one-click print-to-PDF
- **Shield activation** (score 0) or **threat alert** (threats found)

---

## How It Works

1. **Scan** — Detects all WiFi networks using platform-native tools
2. **Match** — Checks each network against a database of 52 OUI prefixes and SSID patterns
3. **Score** — Calculates a 0-100 risk score based on surveillance capabilities
4. **Report** — Generates interactive reports with actionable recommendations
5. **Diff** — Compares against previous scans to detect new/gone networks

---

## Project Structure

```
WiFi-Privacy-Scanner/
├── scan.py                          # Entry point
├── scripts/
│   ├── scanner.py                   # Core scanner + threat analysis
│   └── report_generator.py          # Markdown + HTML report generation
├── references/
│   └── csi-routers-db.json          # Threat database (12 vendors, 52 OUIs)
├── docs/
│   └── index.html                   # GitHub Pages demo report
└── output/                          # Scan results (gitignored)
```

---

## Contributing

To add a new router vendor to the threat database, edit `references/csi-routers-db.json`:

```json
{
  "vendor": "New Vendor",
  "models": ["Model X", "Model Y"],
  "detection": "Motion Sensing",
  "risk": "HIGH",
  "oui_prefixes": ["AA:BB:CC"],
  "indicators": ["vendor_ssid_keyword"],
  "capabilities": ["Motion detection", "Presence sensing"],
  "mitigation": "Steps to disable surveillance features"
}
```

---

## Privacy Note

This scanner runs **entirely locally** — no data is sent anywhere. It only reads WiFi network broadcast information (SSIDs, BSSIDs) that is publicly visible to any device with a WiFi adapter.

---

## License

MIT

---

Built by [Privacy Tech AI Agency](https://github.com/Just-Krispy)
