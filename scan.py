#!/usr/bin/env python3
"""
WiFi Privacy Scanner - Quick Start
Run this script to scan your WiFi environment for surveillance-capable routers.

Usage:
    python scan.py                    # Live scan, JSON output
    python scan.py --format all       # Live scan + Markdown + HTML reports
    python scan.py --demo             # Demo mode with mock data
    python scan.py --help             # Full options
"""
import sys
import os

# Add scripts directory to path for both normal and frozen (PyInstaller) mode
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(base_dir, 'scripts'))
os.chdir(base_dir)

from scanner import main
main()
