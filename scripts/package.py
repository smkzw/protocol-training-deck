#!/usr/bin/env python3
"""Package deck/ for delivery.

    python3 -I scripts/package.py [name]      → dist/<name>_<YYYYMMDD>.zip   (name defaults to DECK['html_title'])

Before zipping: every src/href in index.html must resolve to a file inside deck/ (no broken image, no absolute path,
no http resource — the deck must work offline), and deck/MANIFEST.sha256 is (re)written for later integrity checks.
"""
from datetime import date
from pathlib import Path
import hashlib
import re
import sys
import zipfile

ROOT = Path.cwd()
DECK = ROOT / 'deck'
if not (DECK / 'index.html').exists():
    sys.exit('deck/index.html not found — run python3 -I engine/build.py first (from the project root)')
sys.path.insert(0, str(ROOT / 'content'))
from project import DECK as CFG  # noqa: E402

html = (DECK / 'index.html').read_text(encoding='utf-8')
bad = []
for ref in sorted(set(re.findall(r'\s(?:src|href)="([^"#]+)"', html))):
    if ref.startswith(('data:', 'mailto:')):
        continue
    if re.match(r'(https?:)?//', ref) or ref.startswith('/'):
        bad.append(f'external or absolute reference: {ref}')
    elif not (DECK / ref.split('?')[0]).exists():
        bad.append(f'missing file: {ref}')
for f in sorted(DECK.rglob('*')):   # CSS/JS must not pull anything from the network either (fonts, @import, scripts)
    if f.suffix in ('.css', '.js') and f.is_file():
        t = f.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'https?://[^\s\'")]+|@import[^;]*;', t):
            bad.append(f'network reference in {f.relative_to(DECK)}: {m.group(0)[:60]}')
if bad:
    sys.exit('ERROR\n  ' + '\n  '.join(bad))

files = sorted(f for f in DECK.rglob('*') if f.is_file() and f.name != 'MANIFEST.sha256' and not f.name.startswith('.'))
(DECK / 'MANIFEST.sha256').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(DECK)}\n' for f in files))

name = sys.argv[1] if len(sys.argv) > 1 else re.sub(r'[\\/:*?"<>|\s]+', '_', CFG.get('html_title', 'deck')).strip('_')
out = ROOT / 'dist' / f'{name}_{date.today():%Y%m%d}.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files + [DECK / 'MANIFEST.sha256']:
        z.write(f, f'{name}/{f.relative_to(DECK)}')
print(f'wrote {out} ({out.stat().st_size // 1024} KB, {len(files)} files); open {name}/index.html after unzipping')
