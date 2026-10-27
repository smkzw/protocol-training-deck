#!/usr/bin/env python3
"""Static checks for a deck project: wording, emphasis density, speaker scripts, drill-downs, font sizes.

    python3 -I scripts/check_project.py [project_dir]        (default: the current directory)

ERROR lines must be fixed (exit code 1). WARN lines are fixed or consciously accepted (write why in plan/TASK.md).
A word that is legitimate in your study (e.g. a disease term containing a listed word) can be allowed with
DECK['allow_words'] = ['…'] in content/project.py.
"""
from html import unescape
from pathlib import Path
import hashlib
import importlib
import re
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
CONTENT, ENGINE = ROOT / 'content', ROOT / 'engine'
if not (CONTENT / 'meta.py').exists():
    sys.exit(f'not a deck project (no content/meta.py): {ROOT}')
for p in (ENGINE, ENGINE / 'brand', CONTENT, CONTENT / 'pages'):
    sys.path.insert(0, str(p))

from project import DECK  # noqa: E402
from meta import META, ORDER, CHAPTERS  # noqa: E402
from notes import NOTES, HERO_NOTES  # noqa: E402
try:
    from orig import SRC  # noqa: E402
except ImportError:
    SRC = {}

# ---- word lists (keep in sync with reference/copy-rules.md)
BANNED = {
    '工程化用语': ['闸门', '关卡', '锚点', 'token', 'Token', '放行', '闭环', '动线', '泳道', '节点', '流转', '抓手', '颗粒度', '赋能',
               '链路', '打通', '落地', '兜底', '触达', 'SOP化', 'SOP 化', '卡点', '路由', '回流', '拉齐', '心智'],
    '口语': ['有些事还没完', '后面全错', '一样不能省', '千万', '别忘了', '搞定', '踩坑', '坑', '翻车', '很简单', '大家都知道', '说白了',
           '其实就是', '一定要', '记住', '注意了'],
    '合规敏感': ['预筛', '是否可以签署知情'],
    '指挥性措辞': ['你需要', '你要', '务必', '必须提前', '请CRC', '请 CRC', '请CRA', '请 CRA', 'CRC应当', 'CRC 应当', 'CRA应当', 'CRA 应当',
              'PM应当', 'PM 应当', '建议大家', '大家要'],
}
ALLOW = set(DECK.get('allow_words', []))
EMPH = re.compile(r'<b>|class="kr"|class="ku"|class="hl"')
RULE_WORDS = re.compile(r'入选|排除|入排|窗口|洗脱|筛选期|时限|阈值')

errors, warns = [], []
err = lambda m: errors.append(m)
warn = lambda m: warns.append(m)

# ---- brand and runtime integrity (Kangzhe: official logo / header mark unaltered; vendored html-ppt files are not edited)
STOCK = ['这一页讲', '这一页展示了', '可以看到', '值得关注的是', '接下来我们将']   # Kangzhe speaker-script rule: no stock phrases
PINNED = {   # sha256 of the files shipped with the skill; when maintaining the skill and changing one, update it here too
    'static/vendor/html-ppt/assets/runtime.js': ('69e6fb4e3272bc0a82283071f106b97319a9f0b3f90f8012442fb728d6f7b04c', err,
        'vendored html-ppt runtime was edited — restore it with new_project.py --update-engine'),
    'static/vendor/html-ppt/assets/base.css': ('786791775484fbec5e4e74b3c3280ad8955a848251520008fb9c9d0d5669a9a4', err,
        'vendored html-ppt base.css was edited — restore it with new_project.py --update-engine'),
    'static/assets/logo_bot.svg': ('8d16d3ae8353dd31f46a50d401e66f9e62af40be6cc42cdf5050866a4e6e1cae', warn,
        'logo is not the official Kangzhe logo_bot.svg (fine only if the deck was deliberately rebranded, see README)'),
    'brand/header-mark.svg': ('df7d12a9f9e053f3178dc365af68aaf865d04eab50c038c69cdebb057464aa95', warn,
        'header mark is not the official Kangzhe double-diamond asset (fine only if deliberately rebranded)'),
}
for rel, (want, report, msg) in PINNED.items():
    f = ENGINE / rel
    if not f.exists():
        err(f'engine/{rel} missing — run new_project.py --update-engine')
    elif hashlib.sha256(f.read_bytes()).hexdigest() != want:
        report(f'engine/{rel}: {msg}')
if not re.fullmatch(r'产品中心-医学部｜\d{4}年\d{1,2}月', DECK.get('footer', '')) and '【' not in DECK.get('footer', ''):
    warn(f"footer「{DECK.get('footer', '')}」is not the Kangzhe format 产品中心-医学部｜YYYY年M月 (fine only for another department)")


def visible(html):
    html = re.sub(r'<aside class="notes">.*?</aside>', '', html, flags=re.S)
    html = re.sub(r"data-k='[^']*'", lambda m: ' ' + re.sub(r'<[^>]+>', ' ', unescape(m.group(0))) + ' ', html)  # keyframe texts
    return unescape(re.sub(r'<[^>]+>', ' ', html))


def scan(where, text):
    flat = text.replace('\n', ' ')
    if '【' in flat:                         # template placeholders 【…】 left unfilled
        i = flat.index('【')
        err(f'{where}: unfilled template placeholder … {flat[i:i + 20]}')
    # a rule that quotes the word it forbids (不出现“预筛”或“…”) is not a use of the word
    flat = re.sub(r'(不出现|不写|不用|不使用|避免|禁用)((?:[^“”]{0,4}“[^”]*”)+)', r'\1', flat)
    for kind, words in BANNED.items():
        for w in words:
            if w in ALLOW or w not in flat:
                continue
            if w == '坑' and re.search(r'坑[洼道]', flat):
                continue
            i = flat.index(w)
            err(f'{where}: {kind}「{w}」… {flat[max(0, i - 12):i + 14].strip()}')


# ---- pages
makers = {}
for f in sorted((CONTENT / 'pages').glob('p_*.py')):
    src = f.read_text(encoding='utf-8')
    if 'quote_card(' in src and 'Verbatim(' not in src:
        warn(f'{f.name}: uses quote_card but no Verbatim guard — on-screen protocol text must go through q(...)')
    for m in re.finditer(r'font-size:\s*(?:calc\(\s*)?(\d+(?:\.\d+)?)px', src):
        if float(m.group(1)) < 12:
            err(f'{f.name}: font-size {m.group(1)}px < 12px')
    if re.search(r'\bf1[01]\b', src):
        err(f'{f.name}: class f10/f11 is below the 12px minimum')
    if re.search(r'border-(left|top)\s*:\s*(\d+)px', src) and any(int(w) >= 3 for w in re.findall(r'border-(?:left|top)\s*:\s*(\d+)px', src)):
        warn(f'{f.name}: thick border-left/top found — no full-height/full-width decorative bars')
    if re.search(r'（建议）|（操作建议）', src):
        warn(f'{f.name}: write [建议] / [操作建议] instead of plain （建议） so it gets the muted suggestion style')
    for make in importlib.import_module(f.stem).PAGES:
        makers[make.__name__] = make

for pid in [i for i in ORDER if isinstance(i, str)]:
    if pid not in makers or pid not in META:
        err(f'{pid}: missing page function or META entry (run engine/build.py for details)')
        continue
    ch, title, small, lead = META[pid]
    scan(f'{pid} 标题区', f'{title} {small}')
    scan(f'{pid} 强调句', lead)
    if re.search(r'[:：—]$|[:：]', title):
        warn(f'{pid}: title contains a colon/dash — titles name the content, without punctuation')
    pg = makers[pid]()
    body, steps = pg.render()
    scan(f'{pid} 页面', visible(body))
    raw = re.search(r'</?[a-zA-Z]+[^>]*>|\*\*|__|!!|\^\^', visible(body))
    if raw:
        err(f'{pid}: unrendered markup on the page「{raw.group(0)}」— md() escapes HTML: write \\n for a line break, and do not nest md markers inside raw HTML')
    # emphasis density: per card ≤2, per page ≤4 (narration cards and the lead are not counted)
    total = 0
    for part in pg.parts:
        if 'class="narr ab"' in part:
            continue
        n = len(EMPH.findall(part))
        if 'pn tint' in part:            # protocol quote cards: underlined thresholds are the convention, not emphasis
            n -= part.count('class="ku"')
        total += n
        if n > 2:
            warn(f'{pid}: a card has {n} emphasis marks (≤2): {visible(part).strip()[:30]}…')
    if total > 4:
        warn(f'{pid}: {total} emphasis marks on the page (≤4)')
    for i, t in enumerate(re.findall(r'<div class="tx">(.*?)</div></div>', body), 1):
        n = len(visible(t).strip())
        if n > 80:
            warn(f'{pid}: narration {i} is {n} chars (one sentence, 40–70)')
    if steps == 0:
        warn(f'{pid}: no steps')
    elif steps > 7:
        warn(f'{pid}: {steps} steps — more than 7 usually means the page should be split')
    intro, paras = NOTES.get(pid, ('', []))
    if not intro and not paras:
        err(f'{pid}: no speaker script in notes.py')
    else:
        if len(paras) != steps:
            err(f'{pid}: speaker script has {len(paras)} step paragraphs, page has {steps} steps')
        scan(f'{pid} 逐字稿', intro + ' '.join(paras))
        for w in STOCK:
            if w in intro + ''.join(paras):
                warn(f'{pid}: speaker script uses the stock phrase「{w}」— start with the content itself')
        if len(intro) > 60:
            warn(f'{pid}: script opening is {len(intro)} chars (aim 20–50)')
        for i, t in enumerate(paras, 1):
            if len(t) > 180:
                warn(f'{pid}: script paragraph {i} is {len(t)} chars (aim 60–150)')
            if re.match(r'\s*【\d+】', t):
                err(f'{pid}: script paragraph {i} starts with 【{i}】 — the build adds step numbers itself')
    if RULE_WORDS.search(title + small + lead) and pid not in SRC:
        warn(f'{pid}: rule/window page without a 方案原文 drill-down (add SRC[{pid!r}] in orig.py)')

for key in ['cover', 'toc'] + [c[0] for c in CHAPTERS] + (['ending'] if ('ending',) in ORDER else []):
    if key not in HERO_NOTES:
        warn(f'HERO_NOTES has no entry for {key!r}')
    else:
        scan(f'HERO_NOTES[{key}]', HERO_NOTES[key])
        for w in STOCK:
            if w in HERO_NOTES[key]:
                warn(f'HERO_NOTES[{key}]: stock phrase「{w}」')
for c in CHAPTERS:
    scan(f'章节 {c[0]}', ' '.join(c[1:]))
scan('封面', ' '.join(DECK.get('cover_title', [])) + ' ' + DECK.get('cover_subtitle', ''))
if re.search(r'面向|听众', ' '.join(DECK.get('cover_title', [])) + DECK.get('cover_subtitle', '')):
    warn('cover: the audience is the subtext, not cover text')

for e in errors:
    print('ERROR', e)
for w in warns:
    print('WARN ', w)
print(f'{len(errors)} error(s), {len(warns)} warning(s)')
sys.exit(1 if errors else 0)
