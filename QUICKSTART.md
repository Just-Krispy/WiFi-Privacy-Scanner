# WiFi Privacy Scanner — Quick Start Guide

## What This Does

This tool scans your WiFi environment and tells you if any nearby routers are capable of **surveillance through WiFi signals** — things like motion tracking, breathing detection, and biometric monitoring. No cameras needed, just WiFi.

---

## Option 1: Windows EXE (Easiest — No Setup Required)

### Step 1: Download
- Go to: **https://github.com/Just-Krispy/WiFi-Privacy-Scanner/releases**
- Download **WiFi-Privacy-Scanner.exe**

### Step 2: Run It
- Open a terminal (search "cmd" or "PowerShell" in Start menu)
- Navigate to your Downloads folder:
  ```
  cd Downloads
  ```
- Run the scanner:
  ```
  WiFi-Privacy-Scanner.exe --format all --remediate
  ```

### Step 3: View Your Report
- The scanner creates an `output` folder next to the .exe
- Open the HTML file in your browser — it's the interactive report with:
  - Threat score (0-100)
  - Every network near you analyzed
  - Radar visualization
  - Remediation scripts to fix any issues

### Step 4: Run Cleanup Scripts (If Threats Found)
- Check the `output/remediation/` folder
- You'll find `.bat` scripts you can run to harden your privacy:
  - `enable_mac_randomization.bat` — Randomize your WiFi address
  - `disable_xfinity_motion.bat` — Turn off Xfinity surveillance
  - `setup_privacy_dns.bat` — Switch to encrypted DNS
  - `disable_auto_connect.bat` — Stop auto-joining unknown networks
  - And more

---

## Option 2: Python (Any Platform)

### Step 1: Install Python
- Download from **https://python.org/downloads** if you don't have it
- Make sure to check "Add Python to PATH" during install

### Step 2: Clone the Repo
```bash
git clone https://github.com/Just-Krispy/WiFi-Privacy-Scanner.git
cd WiFi-Privacy-Scanner
```

### Step 3: Run the Scanner
```bash
python scan.py --format all --remediate
```

### Step 4: View Results
- Open the HTML file in `output/` — it's the full interactive report
- Check `output/remediation/` for cleanup scripts

---

## What the Flags Mean

| Flag | What It Does |
|------|-------------|
| `--format all` | Generates JSON + Markdown + Interactive HTML reports |
| `--format html` | HTML report only |
| `--remediate` | Generates cleanup scripts for your platform |
| `--demo` | Uses fake data to preview the report (no WiFi scan) |
| `-v` | Verbose mode — shows extra details |

---

## Understanding Your Report

### Threat Score (0-100)
- **0** — All clear, no surveillance routers detected
- **1-39** — Low risk
- **40-59** — Medium — some routers have basic tracking
- **60-79** — High — motion sensing routers nearby
- **80-100** — Critical — full surveillance capabilities detected

### Risk Levels

| Level | Color | What It Means |
|-------|-------|--------------|
| **CRITICAL** | Red | Full body tracking, vital signs, biometrics |
| **HIGH** | Orange | Motion sensing, room-level occupancy tracking |
| **MEDIUM** | Yellow | Basic presence detection, analytics |
| **LOW** | Green | Standard WiFi, no known surveillance |

### Common Threats

- **Xfinity XB6/7/8** — Your Comcast router tracks motion in your home
- **Origin AI** — Can detect breathing and heart rate through walls
- **WhoFi** — 95.5% biometric accuracy, used in malls and airports
- **Eero/Amazon** — Motion detection + Amazon Sidewalk mesh
- **Google Nest** — Presence sensing via Soli radar

---

## Quick Privacy Wins (Do These Regardless)

1. **Enable MAC randomization** on your phone and laptop
   - iPhone: Settings > WiFi > tap (i) > Private Wi-Fi Address ON
   - Android: Settings > WiFi > gear icon > Privacy > Randomized MAC
   - Windows: Settings > Network > WiFi > Random hardware addresses ON

2. **Use a VPN** on public WiFi

3. **Disable auto-join** for networks you don't recognize

4. **Check your router settings** — disable WPS, UPnP, and any "motion" or "presence" features

---

## Need Help?

- **Live demo report:** https://just-krispy.github.io/WiFi-Privacy-Scanner/
- **Full docs:** https://github.com/Just-Krispy/WiFi-Privacy-Scanner
- **Issues:** https://github.com/Just-Krispy/WiFi-Privacy-Scanner/issues

---

*Built by Privacy Tech AI Agency*
