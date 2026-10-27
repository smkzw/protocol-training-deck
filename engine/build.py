#!/usr/bin/env python3
"""Build a protocol-training HTML deck.

    python3 -I engine/build.py            (run from the project root; engine/ sits inside the project)

Inputs (all in content/, written by you):
    project.py   DECK settings: cover title, subtitle, footer, drill-down source note, hero images
    meta.py      CHAPTERS, ORDER, META — chapter list, slide order, page header attributes + lead sentence
    notes.py     NOTES[pid] = (opening, [one paragraph per step]); HERO_NOTES for cover / toc / chapter pages
    orig.py      SRC[pid] = [(heading, [protocol paragraphs])] for the "方案原文" drill-down (optional)
    pages/p_*.py page builders; every module exports PAGES = [function, ...]; function name == page id
    assets/      your own images (copied to deck/assets/)
Output: deck/ (index.html + runtime files). deck/ is generated — never edit files there by hand.
Exit code 1 on a structural error; WARN lines are things to fix or consciously accept.
"""
from pathlib import Path
from html import escape
import importlib
import json
import re
import shutil
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent
CONTENT, DECK, STATIC = ROOT / 'content', ROOT / 'deck', HERE / 'static'
for p in (HERE, HERE / 'brand', CONTENT, CONTENT / 'pages'):
    sys.path.insert(0, str(p))
from header_mark import facets  # noqa: E402
from hero_layout import html_fluid_fragment  # noqa: E402
from icons import sprite  # noqa: E402
from kit import md  # noqa: E402
from project import DECK as CFG  # noqa: E402
import meta  # noqa: E402
from meta import CHAPTERS, ORDER, META  # noqa: E402
from notes import NOTES, HERO_NOTES  # noqa: E402
try:
    from orig import SRC  # noqa: E402
except ImportError:
    SRC = {}

FOOT = CFG['footer']
LOGO = 'assets/logo_bot.svg'
LEAD_H, KY = 40, (564 - 40) / 564
# Pages are laid out in 0..524 below the lead line. Legacy decks may list such pages in meta.NATIVE and lay out the
# others in 0..564, which is then squeezed by KY; without NATIVE every page is native.
NATIVE = getattr(meta, 'NATIVE', None)
native = lambda pid: NATIVE is None or pid in NATIVE
HERO_IMG = {'cover': 'assets/hero/cover.webp', 'toc': 'assets/hero/toc.webp', 'section': 'assets/hero/section.webp',
            'ending': 'assets/hero/ending.webp'}
HERO_IMG.update(CFG.get('hero_images', {}))

makers = {}
for f in sorted((CONTENT / 'pages').glob('p_*.py')):
    for make in importlib.import_module(f.stem).PAGES:
        if make.__name__ in makers:
            sys.exit(f'ERROR page id {make.__name__} defined twice ({f.name})')
        makers[make.__name__] = make

warn = []


def autofit(pg, ky):
    """Narration cards shrink to their longest caption and dock to the bottom of their slot. Everything above the card
    in its column (boxes, keyframed y/h, wires, motion paths, wire labels) is stretched vertically into the freed
    height, so the space goes to content instead of a tall, sparse caption box. Pages with hand-drawn SVG groups
    (clock faces, arcs) are left alone — they would distort."""
    num = r'-?\d*\.?\d+(?:e-?\d+)?'

    def geo(part):
        m = re.search(r'style="([^"]*)"', part)
        if not m:
            return None
        g = {k: float(v) for k, v in re.findall(r'--([xywh]):(' + num + ')', m.group(1))}
        return g if 'x' in g and 'y' in g else None

    def setg(part, **kv):
        for k, v in kv.items():
            part = re.sub(r'--' + k + ':' + num, f'--{k}:{v:.1f}'.replace('.0;', ';').rstrip('0').rstrip('.'), part, count=1)
        return part

    for i, part in enumerate(pg.parts):
        if 'class="narr ab"' not in part:
            continue
        n = geo(part)
        txts = re.findall(r'<div class="tx">(.*?)</div></div>', part)
        lines = max(-(-width(t) * 14 // (n['w'] - 66)) for t in txts)
        need = round(max(48, lines * 20.5 + 24) / ky + 4)
        slack = n['h'] - need
        if slack < 10:
            return
        Y = n['y']
        boxes = [(j, geo(q)) for j, q in enumerate(pg.parts) if j != i and geo(q)]
        band = [g for _, g in boxes if g['y'] >= Y - 1 or g['y'] + g.get('h', 0) > Y + 1]
        top = [(j, g) for j, g in boxes if g['y'] < Y - 1 and g['y'] + g.get('h', 0) <= Y + 1]
        s = (Y + slack) / Y
        ov = lambda a, b: min(a['x'] + a.get('w', 0), b['x'] + b.get('w', 0)) - max(a['x'], b['x']) > 0
        for _, e in top:
            eb = e['y'] + e.get('h', 16)
            for b in band:
                if ov(e, b) and b['y'] >= eb - 1:
                    s = min(s, max(1, (b['y'] - max(6, b['y'] - eb)) / eb))
        if s < 1.015:
            warn.append(f'{pg.id}: autofit skipped (neighbours leave no room)')
            return
        slack = round(Y * s - Y, 1)
        need = n['h'] - slack
        if any('<circle' in w or '<g' in w for w in pg.wires):
            warn.append(f'{pg.id}: autofit skipped (hand-drawn svg)')
            return
        inreg = lambda x: True

        def remap_d(d):
            toks = re.findall(r'[A-Za-z]|' + num, d)
            arity = {'M': 2, 'L': 2, 'T': 2, 'C': 6, 'S': 4, 'Q': 4, 'H': 1, 'V': 1, 'A': 7}
            out, cmd, buf = [], None, []
            for t in toks:
                if t.isalpha():
                    if t not in 'Zz' and t.islower():
                        raise ValueError('relative path')
                    cmd = t.upper()
                    out.append(t)
                    continue
                buf.append(float(t))
                if len(buf) < arity[cmd]:
                    continue
                if cmd == 'V':
                    buf = [buf[0] * s if buf[0] <= Y + 2 else buf[0]]
                elif cmd != 'H':
                    for q in range(5 if cmd == 'A' else 0, len(buf), 2):
                        if buf[q + 1] <= Y + 2:
                            buf[q + 1] *= s
                out.append(' '.join(f'{v:g}' for v in buf))
                buf = []
            return ' '.join(out)

        try:
            wires = []
            for w in pg.wires:
                w = re.sub(r' d="([^"]+)"', lambda m: f' d="{remap_d(m.group(1))}"', w)
                w = re.sub(r'<text([^>]*) x="(' + num + r')" y="(' + num + r')"',
                           lambda m: f'<text{m.group(1)} x="{m.group(2)}" y="{float(m.group(3)) * s if inreg(float(m.group(2))) and float(m.group(3)) <= Y + 2 else float(m.group(3)):g}"', w)
                if '<polygon' in w:
                    raise ValueError('polygon')
                wires.append(w)
        except ValueError as e:
            warn.append(f'{pg.id}: autofit skipped ({e})')
            return
        parts = list(pg.parts)
        for j, g in top:
            q = parts[j]
            kv = {'y': g['y'] * s}
            if 'h' in g:
                kv['h'] = g['h'] * s
            q = setg(q, **kv)

            def fr(m):
                d = json.loads(m.group(1).replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'))
                for f in d.values():
                    if isinstance(f, dict):
                        for key in ('y', 'h'):
                            if isinstance(f.get(key), (int, float)):
                                f[key] = round(f[key] * s, 1)
                return "data-k='" + escape(json.dumps(d, ensure_ascii=False), quote=False).replace("'", '&#39;') + "'"
            q = re.sub(r"data-k='([^']*)'", fr, q)
            parts[j] = q
        parts[i] = setg(part, y=Y + slack, h=need)
        pg.parts, pg.wires = parts, wires
        return




def width(s):
    s = re.sub(r'<[^>]+>|\*\*', '', s)
    return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .55 for c in s)


def notes_html(pid, steps):
    intro, parts = NOTES.get(pid, ('', []))
    if not intro and not parts:
        warn.append(f'{pid}: no speaker script')
        return ''
    if len(parts) != steps:
        warn.append(f'{pid}: script has {len(parts)} step paragraphs, page has {steps} steps')
    out = f'<p data-k="0">{md(intro)}</p>' if intro else ''
    out += ''.join(f'<p data-k="{i}">【{i}】{md(t)}</p>' for i, t in enumerate(parts, 1))
    return f'<aside class="notes">{out}</aside>'


def hero(kind, content, image, notes, title):
    return (f'<section class="slide kz-hero" data-chrome="hero" data-steps="0" data-title="{escape(title)}">'
            + html_fluid_fragment(kind, content, image, LOGO)
            + f'<aside class="notes"><p data-k="0">{md(notes)}</p></aside></section>')


# ---- structural checks before any rendering
errors = []
pids = [i for i in ORDER if isinstance(i, str)]
for pid in pids:
    if pid not in META:
        errors.append(f'{pid}: in ORDER but has no META entry')
    if pid not in makers:
        errors.append(f'{pid}: in ORDER but no page function named {pid} in content/pages/')
for pid in set(META) - set(pids):
    errors.append(f'{pid}: META entry but not in ORDER')
for pid in set(makers) - set(pids):
    warn.append(f'{pid}: page function exists but is not in ORDER (not built)')
if len(pids) != len(set(pids)):
    errors.append('ORDER lists a page id twice')
for key in ['cover', 'toc'] + [c[0] for c in CHAPTERS]:
    if key not in HERO_NOTES:
        warn.append(f'HERO_NOTES has no entry for {key!r}')
if errors:
    for e in errors:
        print('ERROR', e)
    sys.exit(1)

# ---- assemble
total = len(ORDER)
slides, late = [], []   # late = errors found while rendering pages
for n, item in enumerate(ORDER, 1):
    if item == ('cover',):
        slides.append(hero('cover', {'title': '\n'.join(CFG['cover_title']), 'subtitle': CFG.get('cover_subtitle', ''),
                                     'meta': FOOT}, HERO_IMG['cover'], HERO_NOTES.get('cover', ''), '封面'))
        continue
    if item == ('toc',):
        slides.append(hero('toc', {'title': CFG.get('toc_title', '培训章节'), 'items': [{'title': t, 'description': d} for _, t, d, _ in CHAPTERS]},
                           HERO_IMG['toc'], HERO_NOTES.get('toc', ''), '目录'))
        continue
    if item == ('ending',):   # optional Kangzhe closing page: ('ending',) as the last ORDER entry
        slides.append(hero('ending', {'title': CFG.get('ending_title', '谢谢'), 'subtitle': CFG.get('ending_subtitle', ''), 'meta': FOOT},
                           HERO_IMG['ending'], HERO_NOTES.get('ending', ''), '尾页'))
        continue
    if item[0] == 'chapter':
        num, t, d, _ = CHAPTERS[item[1]]
        slides.append(hero('section', {'number': num, 'title': t}, HERO_IMG['section'], HERO_NOTES.get(num, ''), f'{num} {t}'))
        continue
    pid = item
    ch, title, small, lead = META[pid]
    pg = makers[pid]()
    if pg.id != pid:
        sys.exit(f'ERROR function {pid}() returned Page({pg.id!r}); the id must equal the function name')
    autofit(pg, 1 if native(pid) else KY)
    body, steps = pg.render()
    if steps == 0:
        warn.append(f'{pid}: page has no steps (nothing is revealed on key press)')
    stage = CHAPTERS[ch][3]
    if width(stage) * 14 + 24 + width(title) * 32 + 12 + width(small) * 16 > 925:
        warn.append(f'{pid}: header may overflow ({title} / {small})')
    src = SRC.get(pid)
    if width(lead) * 18 > 1168 - (130 if src else 10):   # Kangzhe TYPE-03: no ellipsis, so an overlong lead is an error
        late.append(f'{pid}: lead longer than one line ({width(lead):.0f} em): shorten it')
    btn = (f'<button class="src-btn" type="button" data-src="{pid}">方案原文<svg class="ico" aria-hidden="true"><use href="#i-file"/></svg></button>'
           if src else '')
    data = (f'<script type="application/json" class="src-data">'
            + json.dumps({'title': f'方案原文 · {title}', 'sections': [{'h': h, 'p': ps} for h, ps in src]}, ensure_ascii=False).replace('</', '<\\/')
            + '</script>') if src else ''
    ky = 1 if native(pid) else KY
    mark = f'<svg class="kz-mark" viewBox="0 0 100 90" aria-hidden="true">{facets(prefix=f"kz{n}")}</svg>'
    slides.append(
        f'<section class="slide" data-scene="{pid}" data-steps="{steps}" data-title="{escape(title)}">'
        f'<img class="kz-bg" src="assets/body-quiet.webp" alt="">'
        f'<div class="kz-chrome">{mark}<div class="kz-rule"></div><img class="kz-logo" src="{LOGO}" alt="康哲药业">'
        f'<div class="kz-foot"><span>{FOOT}</span><span class="right">'
        f'<span class="kz-page-number">{n} / {total}</span></span></div></div>'
        f'<h2 class="kz-body-title"><span class="stage">{escape(stage)}</span>{escape(title)}<small>{escape(small)}</small></h2>'
        f'<div class="cv" style="--y0:{LEAD_H};--ky:{ky:.4f}"><div class="lead"><p class="lead-tx">{md(lead)}</p>{btn}</div>{body}</div>'
        f'{data}{notes_html(pid, steps)}</section>')

# ---- hover page index (sop2.js marks the current page; links are plain #/n hashes)
groups, cur = [], None
for n, item in enumerate(ORDER, 1):
    if item in (('cover',), ('toc',), ('ending',)):
        continue
    if isinstance(item, tuple):
        cur = (item[1], n, [])
        groups.append(cur)
    elif cur is not None:
        cur[2].append((n, META[item][1]))
nav = ('<nav class="sop-nav" aria-label="页面目录"><button class="sop-nav-tab" type="button" aria-expanded="false">'
       '<svg class="ico" aria-hidden="true"><use href="#i-list"/></svg><span>目录</span></button><div class="sop-nav-panel">'
       '<div class="sop-nav-chs"><div class="sop-nav-top"><a href="#/1" data-n="1">封面</a><a href="#/2" data-n="2">培训章节</a></div>')
for ch, n, pages in groups:
    num, t, _, _ = CHAPTERS[ch]
    rng = f'{pages[0][0]}–{pages[-1][0]}' if pages else f'{n}'
    nav += f'<a class="sop-nav-ch" href="#/{n}" data-n="{n}" data-ch="{ch}"><b>{num}</b><span>{escape(t)}</span><em>{rng}</em></a>'
nav += '</div><div class="sop-nav-pages">'
for ch, n, pages in groups:
    nav += f'<ol data-ch="{ch}">' + ''.join(f'<li><a href="#/{p}" data-n="{p}"><i>{p}</i>{escape(t)}</a></li>' for p, t in pages) + '</ol>'
nav += '</div></div></nav>'

# ---- write deck/: runtime files from engine/static, then the project's own assets, then index.html
DECK.mkdir(exist_ok=True)
shutil.copytree(STATIC, DECK, dirs_exist_ok=True)
if (CONTENT / 'assets').is_dir():
    shutil.copytree(CONTENT / 'assets', DECK / 'assets', dirs_exist_ok=True)
if late:
    for e in late:
        print('ERROR', e)
    sys.exit(1)
html = ('<!DOCTYPE html>\n<!-- Generated by engine/build.py from content/; do not edit by hand. Runtime: html-ppt-skill (MIT) + Kangzhe brand layer. -->\n'
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>{escape(CFG.get("html_title", " ".join(CFG["cover_title"])))}</title>\n<link rel="icon" href="data:,">\n'
        '<link rel="stylesheet" href="vendor/html-ppt/assets/base.css">\n<link rel="stylesheet" href="kz/kz-tokens.css">\n'
        '<link rel="stylesheet" href="kz/kz-subset.css">\n<link rel="stylesheet" href="sop2.css">\n</head>\n'
        f'<body class="kz" data-fit="fluid" data-src-note="{escape(CFG.get("source_note", ""))}">\n' + sprite() + '\n<div class="deck">\n' + '\n'.join(slides) + '\n</div>\n' + nav + '\n'
        '<script src="vendor/html-ppt/assets/runtime.js"></script>\n<script src="kz/kz-tokens.js"></script>\n'
        '<script src="kz/kz-drilldown.js"></script>\n'
        '<script src="kz/html-ppt-bridge.js"></script>\n<script src="sop2.js"></script>\n<script src="kz/kz-audience.js"></script>\n</body></html>\n')
# suggestion markers written straight into HTML (bypassing md()) get the same styling
SUG = lambda q: lambda s: s.replace('[操作建议]', f'<span class={q}sug{q}>（操作建议）</span>').replace('[建议]', f'<span class={q}sug{q}>（建议）</span>')
html = re.sub(r"data-k='[^']*'", lambda m: SUG('\\"')(m.group(0)), html)   # inside keyframe JSON the quotes must be escaped
html = SUG('"')(html)
(DECK / 'index.html').write_text(html, encoding='utf-8')
print('wrote', DECK / 'index.html', total, 'slides')
for w in warn:
    print('WARN', w)
