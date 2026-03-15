# WiFi Privacy Scanner

**Detect CSI-capable routers and WiFi surveillance technologies in your environment.**

## Overview

The WiFi Privacy Scanner identifies routers and access points capable of Channel State Information (CSI) extraction and WiFi-based surveillance. These technologies can track presence, motion, vital signs, and even full body poses through WiFi signals—without cameras.

**Key Threats Detected:**
- **Xfinity Motion Sensing** (XB6/XB7/XB8) - Room-level occupancy tracking
- **Origin AI** - Vital signs monitoring, breathing/heart rate detection
- **WhoFi** - 95.5% biometric accuracy, cross-venue tracking
- **DensePose** - Full body pose estimation through walls
- **Cognitive Systems** - Motion and activity monitoring
- **Other CSI-capable routers** - Various motion sensing technologies

## How It Works

1. **Network Scanning** - Detects all WiFi networks in range
2. **Threat Analysis** - Matches against database of CSI-capable routers
3. **Risk Scoring** - Calculates privacy threat level (0-100)
4. **Report Generation** - Creates detailed Markdown reports with recommendations

## Components

### 1. Router Database (`references/csi-routers-db.json`)
Comprehensive database of CSI-capable routers including:
- Vendor and model information
- Detection capabilities
- MAC OUI prefixes
- SSID indicators
- Privacy risk levels
- Mitigation strategies

### 2. Scanner Script (`scripts/scanner.py`)
Python script that:
- Scans WiFi networks using system tools (nmcli/airport)
- Analyzes each network against threat database
- Generates risk scores
- Produces structured JSON output
- Falls back to mock data for testing

### 3. Report Generator (`scripts/report_generator.py`)
Converts scan JSON to human-readable reports:
- Markdown format with emoji indicators
- Grouped by risk level (CRITICAL/HIGH/MEDIUM/LOW)
- Detailed threat breakdowns
- Actionable mitigation strategies

## Usage

### Run a WiFi Privacy Scan

```bash
cd ~/.openclaw/workspace/skills/wifi-privacy-scanner
python3 scripts/scanner.py
```

**Output:**
- JSON results saved to `output/scan_YYYYMMDD_HHMMSS.json`
- Console summary with threat score

### Generate Human-Readable Report

```bash
python3 scripts/report_generator.py output/scan_YYYYMMDD_HHMMSS.json
```

**Output:**
- Markdown report saved to `output/scan_YYYYMMDD_HHMMSS_report.md`
- Detailed breakdown printed to console

### Quick Test (Mock Data)

```bash
# Scanner will use mock data if nmcli/airport not available
python3 scripts/scanner.py

# Example output:
# 🔍 Scanning WiFi networks...
#    Found 4 networks
# 
# 🛡️  Analyzing privacy threats...
# 
# ✅ Scan complete! Results saved to: output/scan_20260315_140730.json
# 
# 📊 Threat Score: 90/100
#    Threats Found: 3
```

## Risk Levels

| Level | Score | Description | Action |
|-------|-------|-------------|--------|
| 🔴 CRITICAL | 80-100 | Full CSI extraction, biometric tracking, DensePose | **AVOID** - Major privacy invasion |
| 🟠 HIGH | 60-79 | Motion sensing, room-level tracking | **CAUTION** - Disable or replace |
| 🟡 MEDIUM | 40-59 | Basic presence detection | **REVIEW** - Check settings |
| 🟢 LOW | 0-39 | Standard WiFi, no known CSI | **SAFE** - Normal operation |

## Output Format

### JSON Scan Results
```json
{
  "scan_date": "2026-03-15T14:07:00",
  "networks_scanned": 4,
  "threats_found": 3,
  "threat_score": 90,
  "threat_breakdown": {
    "critical": 1,
    "high": 2,
    "medium": 0,
    "low": 1
  },
  "networks": [
    {
      "network": {
        "ssid": "xfinitywifi",
        "bssid": "B0:8B:D0:12:34:56",
        "signal_strength": 85,
        "encryption": "WPA2"
      },
      "threats": [{
        "vendor": "Xfinity",
        "models": ["XB6", "XB7", "XB8"],
        "detection_type": "Motion Sensing",
        "capabilities": [
          "Presence detection",
          "Motion tracking",
          "Room-level occupancy"
        ],
        "mitigation": "Disable motion sensing in Xfinity app or use non-Xfinity router"
      }],
      "risk_level": "HIGH",
      "risk_score": 70,
      "vendor_match": "Xfinity"
    }
  ],
  "recommendations": [
    "🚨 CRITICAL: 1 network(s) with severe surveillance capabilities detected...",
    "💡 Enable MAC address randomization on your devices",
    "💡 Use VPN to encrypt traffic and limit exposure"
  ]
}
```

## Dependencies

**System Requirements:**
- Python 3.7+
- Linux: `nmcli` (NetworkManager)
- macOS: `airport` (built-in)
- Windows: Falls back to mock data (real scanning TBD)

**Python Packages:**
- Standard library only (json, subprocess, pathlib, datetime)

## Privacy Mitigation Strategies

### Immediate Actions
1. **Enable MAC Randomization** - Prevents device tracking
2. **Use VPN** - Encrypts traffic, limits exposure
3. **Disable WiFi When Not Needed** - Reduces surveillance window

### Router-Specific
- **Xfinity:** Disable motion sensing in Xfinity app
- **Origin AI:** Avoid networks, use VPN
- **WhoFi:** MAC randomization essential
- **Google Nest:** Disable Soli features in Google Home

### Long-Term
- Replace CSI-capable routers with standard models
- Use wired connections when possible
- Regular firmware updates
- Disable WPS, UPnP, remote management

## Extending the Database

To add new routers to the threat database, edit `references/csi-routers-db.json`:

```json
{
  "vendor": "NewVendor",
  "models": ["Model1", "Model2"],
  "detection": "Detection Type",
  "risk": "HIGH|MEDIUM|LOW|CRITICAL",
  "oui_prefixes": ["AA:BB:CC"],
  "indicators": ["keyword1", "keyword2"],
  "capabilities": [
    "Capability 1",
    "Capability 2"
  ],
  "mitigation": "How to protect yourself"
}
```

## Testing

### Mock Data Test
```bash
# Scanner includes built-in mock data
python3 scripts/scanner.py
```

### Real Network Test
```bash
# Ensure nmcli (Linux) or airport (macOS) is available
which nmcli  # or: which airport
python3 scripts/scanner.py
```

### Validation
```bash
# Check output directory
ls output/

# Verify JSON structure
cat output/scan_*.json | jq .

# Generate report
python3 scripts/report_generator.py output/scan_*.json
```

## Roadmap

**Phase 1: Detection (Current)**
- ✅ Router database
- ✅ WiFi scanning
- ✅ Threat analysis
- ✅ Report generation

**Phase 2: Monitoring**
- [ ] Continuous monitoring mode
- [ ] Alert system for new threats
- [ ] Historical tracking
- [ ] Dashboard UI

**Phase 3: Active Defense**
- [ ] Auto-disable CSI features (where possible)
- [ ] Network isolation recommendations
- [ ] VPN auto-connect
- [ ] MAC randomization enforcement

**Phase 4: Research Integration**
- [ ] Real-time CSI detection
- [ ] Custom router firmware analysis
- [ ] Crowd-sourced threat database
- [ ] Academic research integration

## Use Cases

1. **Home Privacy Audit** - Check your home WiFi environment
2. **Office/Workplace** - Identify workplace surveillance
3. **Public Spaces** - Scan cafes, airports, hotels
4. **IoT Security** - Protect smart home devices
5. **Research** - Study WiFi surveillance deployment patterns

## Contributing

To contribute to the threat database:

1. Document router model and capabilities
2. Identify MAC OUI prefixes
3. Test detection accuracy
4. Submit pull request with references

## References

- Origin AI: WiFi-based vital signs monitoring
- WhoFi: 95.5% biometric accuracy research
- DensePose WiFi: Full body pose estimation papers
- Xfinity Motion Sensing: Official documentation
- Cognitive Systems: WiFi Motion technology

## License

Educational and privacy research purposes. Use responsibly.

---

**⚠️ Important:** This tool detects *known* surveillance routers. It cannot guarantee complete privacy. Always use encryption, VPN, and follow best security practices.

**Built for Privacy Tech AI Agency** - Empowering digital privacy through awareness and detection.
