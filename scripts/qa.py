#!/usr/bin/env python3
"""Automated visual QA through ego-browser (ego lite). Run from the project root:

    python3 -I scripts/qa.py              → qa/report.json + one final-state screenshot per slide (qa/shots/NN.png)
    python3 -I scripts/qa.py --shots 2    → also every step as qa/shots/NN-k.png (to check the animation)
    python3 -I scripts/qa.py --shots 0    → report only
    python3 -I scripts/qa.py --all-viewports --shots 0   → also the Kangzhe acceptance viewports (run once before G8)
    python3 -I scripts/qa.py --shots 0 --deck <unzipped folder>   → offline retest of the delivered zip (G8)

Exit code: 0 = summary empty (pass), 1 = problems found (listed below), 2 = QA could not run.
ego-browser does not forward the working directory or environment variables, so this script prepends the project path
to qa/run-ego.mjs and pipes it in. Works on macOS and Windows (ego lite: https://lite.ego.app/).
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import time

ROOT = Path.cwd()
ap = argparse.ArgumentParser()
ap.add_argument('--shots', type=int, choices=(0, 1, 2), default=1)
ap.add_argument('--all-viewports', action='store_true', help='1920×1080 plus 1280×720, 1536×730, 1920×940, 2560×1080')
ap.add_argument('--deck', help='folder holding index.html to test instead of deck/ (e.g. the unzipped delivery)')
args = ap.parse_args()

deck = Path(args.deck).resolve() if args.deck else ROOT / 'deck'
if not (deck / 'index.html').exists() or not (ROOT / 'qa' / 'run-ego.mjs').exists():
    sys.exit(f'{deck}/index.html or qa/run-ego.mjs not found: run from the project root, after python3 -I engine/build.py')
exe = shutil.which('ego-browser')
if not exe:
    print('ego-browser not found. Install ego lite from https://lite.ego.app/ and finish its first-run onboarding\n'
          '(it puts ego-browser on PATH). Without it, run the manual route in qa/README.md (browser console + DeckQA.all()).')
    sys.exit(2)

report = ROOT / 'qa' / 'report.json'
started = time.time()
vps = [[1920, 1080], [1280, 720], [1536, 730], [1920, 940], [2560, 1080]] if args.all_viewports else [[1920, 1080]]
script = f'const ROOT={json.dumps(ROOT.resolve().as_posix())}, SHOTS={args.shots}, DECK={json.dumps(deck.as_posix())}, VIEWPORTS={json.dumps(vps)};\n' + (ROOT / 'qa' / 'run-ego.mjs').read_text(encoding='utf-8')
r = subprocess.run([exe, 'nodejs'], input=script, text=True, encoding='utf-8', capture_output=True)
for line in (r.stdout + r.stderr).splitlines():
    if 'update is available' not in line:
        print(line)
if r.returncode or not report.exists() or report.stat().st_mtime < started:
    print('QA did not finish. If the error says "Inspected target navigated or closed", another QA run may be driving the '
          'same page: check for other "ego-browser nodejs" processes and run again.')
    sys.exit(2)

rep = json.loads(report.read_text(encoding='utf-8'))
print(f"{rep['slides']} slides, {rep['steps']} steps, summary {rep['summary'] or '{} (pass)'}")
for p in rep['problems'][:40]:
    print(f"  slide {p['slide']} step {p['step']} {p.get('scene', '')} {p['code']} {p['msg']}" + (f" @{p['viewport']}" if 'viewport' in p else ''))
if len(rep['problems']) > 40:
    print(f"  … {len(rep['problems']) - 40} more in qa/report.json")
if args.shots:
    print('screenshots: qa/shots/ — look at every one (reference/visual-qc.md §2); an empty summary is not the end of QA')
sys.exit(1 if rep['summary'] else 0)
