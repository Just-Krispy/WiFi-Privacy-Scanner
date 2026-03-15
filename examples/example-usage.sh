#!/bin/bash
# Example: Complete WiFi Privacy Scan Workflow

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/wifi-privacy-scanner"
cd "$SKILL_DIR"

echo "🦞 WiFi Privacy Scanner - Example Workflow"
echo "==========================================="
echo ""

# Step 1: Run scan
echo "📡 Step 1: Scanning WiFi networks..."
python3 scripts/scanner.py
echo ""

# Step 2: Find latest scan
LATEST=$(ls -t output/scan_*.json | head -1)
echo "📄 Latest scan: $LATEST"
echo ""

# Step 3: Generate report
echo "📊 Step 2: Generating report..."
python3 scripts/report_generator.py "$LATEST"
echo ""

# Step 4: Show summary
echo "📋 Step 3: Quick Summary"
echo "----------------------"
THREAT_SCORE=$(cat "$LATEST" | grep -o '"threat_score": [0-9]*' | grep -o '[0-9]*')
THREATS_FOUND=$(cat "$LATEST" | grep -o '"threats_found": [0-9]*' | grep -o '[0-9]*')

echo "Threat Score: $THREAT_SCORE/100"
echo "Threats Found: $THREATS_FOUND"
echo ""

# Step 5: Show report location
REPORT="${LATEST%.json}_report.md"
echo "✅ Complete! View full report:"
echo "   $REPORT"
echo ""

# Optional: Display report excerpt
echo "📖 Report Preview (first 30 lines):"
echo "-----------------------------------"
head -30 "$REPORT"
echo ""
echo "... (see full report for details)"
