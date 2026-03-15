# WiFi Privacy Scanner - Quick Start

**Detect CSI-capable surveillance routers in your WiFi environment.**

## What This Does

Scans WiFi networks and identifies routers capable of:
- 🎯 Motion sensing and presence detection
- 💓 Vital signs monitoring (heart rate, breathing)
- 🚶 Biometric tracking (95.5% accuracy)
- 🏃 Full body pose estimation through walls

**Threat Level:** Detects Xfinity, Origin AI, WhoFi, DensePose, and other CSI surveillance systems.

## Installation

```bash
# No dependencies required - uses Python 3 standard library
cd ~/.openclaw/workspace/skills/wifi-privacy-scanner
```

## Usage

### 1. Run a Scan

```bash
python3 scripts/scanner.py
```

**Output:**
```
🔍 Scanning WiFi networks...
   Found 4 networks

🛡️  Analyzing privacy threats...

✅ Scan complete! Results saved to: output/scan_20260315_140956.json

📊 Threat Score: 90/100
   Threats Found: 3
```

### 2. Generate Human-Readable Report

```bash
# Find latest scan
LATEST=$(ls -t output/scan_*.json | head -1)

# Generate report
python3 scripts/report_generator.py "$LATEST"
```

**Output:** Markdown report saved to `output/scan_*_report.md`

### 3. View Results

```bash
# View JSON results
cat output/scan_*.json | jq .

# View Markdown report
cat output/scan_*_report.md
```

## Example Output

### Console
```
📊 Threat Score: 90/100
   Threats Found: 3

🔴 CRITICAL: OriginWireless_Mesh
   - Full CSI extraction
   - Vital signs monitoring
   - Breathing/heart rate detection

🟠 HIGH: xfinitywifi
   - Motion Sensing
   - Room-level occupancy tracking
```

### Markdown Report
```markdown
# WiFi Privacy Scan Report

**Scan Date:** 2026-03-15
**Networks Scanned:** 4
**Threats Detected:** 3

## 🎯 Overall Threat Assessment
### Threat Score: 90/100
**Status:** 🔴 CRITICAL - Severe privacy risks detected

**Threat Breakdown:**
- 🔴 Critical: 1
- 🟠 High: 2
- 🟡 Medium: 0
- 🟢 Low/Safe: 1
```

## Risk Levels

| Emoji | Level | Score | What It Means |
|-------|-------|-------|---------------|
| 🔴 | CRITICAL | 80-100 | Full CSI, biometric tracking - **AVOID** |
| 🟠 | HIGH | 60-79 | Motion sensing - **DISABLE OR REPLACE** |
| 🟡 | MEDIUM | 40-59 | Basic presence - **REVIEW SETTINGS** |
| 🟢 | LOW | 0-39 | Standard WiFi - **SAFE** |

## Known Threats Detected

- **Xfinity (XB6/XB7/XB8)** - Motion Sensing
- **Origin AI** - Vital Signs Monitoring
- **WhoFi** - 95.5% Biometric Accuracy
- **DensePose** - Full Body Pose Tracking
- **Cognitive Systems** - Motion Detection
- **Google Nest** - Soli Presence Sensing
- **TP-Link CSI** - Select models with motion features

## Privacy Protection Tips

1. **Enable MAC Randomization** - Prevents device tracking
2. **Use VPN** - Encrypts traffic
3. **Disable WiFi When Not Needed** - Limits exposure
4. **Replace CSI Routers** - Use standard models
5. **Check Router Settings** - Disable motion/presence features

## Testing

The scanner includes mock data for testing if you don't have `nmcli` (Linux) or `airport` (macOS):

```bash
# Will automatically fall back to mock data
python3 scripts/scanner.py
```

## Directory Structure

```
wifi-privacy-scanner/
├── SKILL.md              # Full documentation
├── README.md             # This file
├── scripts/
│   ├── scanner.py        # Network scanning & analysis
│   └── report_generator.py  # Markdown report generation
├── references/
│   └── csi-routers-db.json  # Threat database
└── output/               # Scan results & reports
    ├── scan_*.json
    └── scan_*_report.md
```

## Adding New Routers

Edit `references/csi-routers-db.json` to add routers to the threat database.

## Use Cases

- **Home Privacy Audit** - Check your own WiFi
- **Office Security** - Identify workplace surveillance
- **Public Spaces** - Scan cafes, hotels, airports
- **IoT Protection** - Secure smart home networks

## Learn More

See `SKILL.md` for complete documentation including:
- Detection methodology
- Router database structure
- Output format specifications
- Extension and contribution guidelines

---

**⚠️ Privacy Note:** This detects *known* surveillance routers. It cannot guarantee complete privacy. Always use encryption and follow security best practices.

**Built for Privacy Tech AI Agency**
