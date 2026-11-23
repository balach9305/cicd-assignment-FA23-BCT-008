#!/usr/bin/env python3
"""Insert the student's roll number into the webpage and Selenium expectations."""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 scripts/configure.py FA23-BCT-XXX")
roll = sys.argv[1].strip().upper()
if not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{2,39}", roll):
    raise SystemExit("Use letters, numbers, hyphens or underscores for your roll number")
root = Path(__file__).resolve().parents[1]
for relative in ("index.html", "tests/test_site.py"):
    file = root / relative
    content = file.read_text(encoding="utf-8")
    if "YOUR_ROLL_NUMBER" not in content:
        print(f"{relative}: already configured; verify your roll number manually")
        continue
    file.write_text(content.replace("YOUR_ROLL_NUMBER", roll), encoding="utf-8")
    print(f"Configured {relative}: {roll}")
