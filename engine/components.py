"""Shared scene components, generalized from the reference deck. Every function draws onto a kit.Page in canvas units
(1168 × 564; y 0..524 on NATIVE pages, 0..564 otherwise) and takes the usual step arguments s= (appear at step),
o= (disappear at step), d= (delay ms inside the step).

Use components to save effort, not to make every page look the same: a page should combine one or two of them with
its own diagram (see reference/patterns.md). All text goes through kit.md(), so **bold**, !!red!!, __underline__,
^^highlight^^, ==chip== and [建议] work everywhere.
"""
from datetime import date, timedelta
from pathlib import Path
import re

from kit import Page, icon, md, role, A, ROLE  # noqa: F401  (re-exported for page modules)

OK, BAD, WARN = '#2F8A57', '#C00000', '#D98E00'
BRAND, CRA, MM, GREY = '#FF9900', '#4A6D8C', '#E98A00', '#9A948A'
KIND = {'ok': OK, 'bad': BAD, 'warn': WARN, 'brand': BRAND, 'cra': CRA, 'mm': MM, 'grey': GREY}
KIND_ICON = {'ok': 'check', 'bad': 'x', 'warn': 'alert', 'brand': 'star', 'cra': 'search', 'mm': 'shield', 'grey': 'file'}
LINE = 'border-bottom:1px dashed #E6DFD3'


# ------------------------------------------------------------------ source fidelity
class Verbatim:
    """Guard for protocol text shown on a slide: q = Verbatim('src/protocol.md'); q('…') returns the text unchanged
    and stops the build if it is not found word for word (whitespace-insensitive). Use for every on-screen quote."""

    def __init__(self, *paths):
        root = Path(__file__).resolve().parents[1]
        self.text = re.sub(r'\s+', '', ''.join((root / p).read_text(encoding='utf-8') for p in paths))

    def __call__(self, s):
        if re.sub(r'\s+', '', s) not in self.text:
            raise SystemExit(f'ERROR on-screen quote not found verbatim in the source: {s[:40]}…')
        return s


# ------------------------------------------------------------------ cards
def note_html(kind, title, body=''):
    """Small verdict block: coloured icon + title, then body. kind: ok | bad | warn."""
    c = KIND[kind]
    return (f'<div class="f13 b" style="color:{c};display:flex;gap:5px;align-items:flex-start">{icon(KIND_ICON[kind])}<span>{md(title)}</span></div>'
            + (f'<div class="f12" style="margin-top:3px">{md(body)}</div>' if body else ''))


def alert(p, x, y, w, h, kind, title, body='', s=1, o=None, d=0, fx='right', cover=True):
    """Example card. kind 'bad' = 反例 (a mistake), 'ok' = 正例, 'warn' = needs the investigator's judgement.
    Lay several on the same spot with s=k, o=k+1 to swap examples step by step. cover=True gives it an opaque
    background so it may sit on top of the scene (QA then skips collisions under it)."""
    p.el(x, y, w, h, note_html(kind, title, body), 'pn tone' + (' cover' if cover else ''), style=f'--tone:{KIND[kind]};', s=s, o=o, d=d, fx=fx)


def case_card(p, x, y, w, h, head, rows, verdict, kind, s=1, o=None, avatar='sub', fx='right'):
    """Participant / case card: avatar + head, (label, value) rows, verdict line coloured by kind."""
    c = KIND[kind]
    body = ''.join(f'<div style="display:flex;gap:8px;padding:3px 0;{LINE}"><span class="mut nw" style="flex:none;width:6.2em">{md(a)}</span><span>{md(b)}</span></div>' for a, b in rows)
    av = f'<span class="role {ROLE[avatar][2]}"><span class="av">{icon(ROLE[avatar][1])}</span></span>'
    html = (f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">{av}<span class="f16 b ink">{md(head)}</span></div>'
            f'<div class="f13">{body}</div>'
            f'<div class="f14 b" style="margin-top:8px;color:{c};display:flex;gap:6px;align-items:flex-start">{icon(KIND_ICON[kind])}<span>{md(verdict)}</span></div>')
    p.el(x, y, w, h, html, 'pn tone cover', style=f'--tone:{c};', s=s, o=o, fx=fx)


def kv_card(p, x, y, w, h, title, rows, s=1, o=None, d=0, cls='pn flat', label_w='6.5em', ico=None):
    """Titled card with (label, value) rows — study facts, time points, sample specs."""
    body = ''.join(f'<div class="f13" style="display:flex;gap:8px;padding:3px 0;{LINE}"><span class="mut nw" style="flex:none;width:{label_w}">{md(a)}</span><span>{md(b)}</span></div>' for a, b in rows)
    p.panel(x, y, w, h, title, body, ico, cls.replace('pn', '').strip(), s=s, o=o, d=d)


def quote_card(p, x, y, w, h, title, text, s=1, o=None, d=0):
    """Protocol original on screen (tint card). Mark thresholds with __…__; pass text through a Verbatim guard first."""
    p.el(x, y, w, h, f'<div class="f12 b t-brand" style="display:flex;gap:5px;align-items:center">{icon("file")}{md(title)}</div>'
                     f'<div class="f13" style="margin-top:4px;line-height:1.55">{md(text)}</div>', 'pn tint', s=s, o=o, d=d, fx='up')


def doc_mock(p, x, y, w, h, title, lines, s=1, o=None, d=0, cls='', extra='', ico='file', fx='drop', k=None):
    """A paper document (record, form, report, ICF). lines: short strings; extra: raw html appended."""
    html = f'<div class="dh">{icon(ico)}{md(title)}</div>' + ''.join(f'<div class="f12">{md(t)}</div>' for t in lines) + extra
    p.el(x, y, w, h, html, ('doc ' + cls).strip(), s=s, o=o, d=d, fx=fx, k=k)


def screen_mock(p, x, y, w, h, title, body_html, s=1, o=None, d=0):
    """A system screen (EDC, IWRS, e-mail). body_html is raw html (use md() for text)."""
    p.el(x, y, w, h, f'<div class="bar">{icon("monitor")} {md(title)}</div><div class="bd">{body_html}</div>', 'screen', s=s, o=o, d=d, fx='up')


def verdict_board(p, x, y, w, rows, title='判定结果', row_h=34, s=1):
    """Running verdicts: rows = [(label, {step: (value, kind)})]; the tag on each row changes with the step."""
    p.panel(x, y, w, 40 + len(rows) * row_h, title, '', 'list', s=s)
    for i, (lab, frames) in enumerate(rows):
        k = {st: {'html': f'<span class="tag {kind}">{md(v)}</span>'} for st, (v, kind) in frames.items()}
        p.el(x + 14, y + 40 + i * row_h, w - 28, row_h - 6, f'<span class="f13 b ink">{md(lab)}</span>', '', style=f'display:flex;align-items:center;{LINE}', s=s)
        p.el(x + w - 200, y + 42 + i * row_h, 186, row_h - 10, '', 'r', style='display:flex;justify-content:flex-end;align-items:center', s=min(frames), k=k)


def visit_checklist(p, title, sub, groups, skip=(), x=0, y=0, w=380, h=None, skip_label='本次不做'):
    """Visit checklist that ticks in step with the demo beside it.
    groups = [(group title, [(text, frames)])]; frames = step it turns done (int) or {step: 'done'|'fail'|'now'|''}.
    Use 'fail' at the trap step and 'done' one step later, so the list shows the mistake before the fix."""
    body = f'<div class="f12 mut" style="margin:-2px 0 2px">{md(sub)}</div>' if sub else ''
    for g, items in groups:
        body += f'<div class="ck-g">{md(g)}</div>'
        for text, fr in items:
            if isinstance(fr, int):
                fr = {fr: 'done'}
            k = {st: {'c': c} for st, c in fr.items()} if fr else None
            body += f'<div class="ck"{A(k=k) if k else ""}><span class="bx">{icon("check", "i-ck")}{icon("x", "i-x")}</span><span class="ct">{md(text)}</span></div>'
    if skip:
        body += f'<div class="ck-g">{md(skip_label)}</div><div style="display:flex;flex-wrap:wrap;gap:4px">' + ''.join(
            f'<span class="tag" style="text-decoration:line-through;color:#8B8478">{md(t)}</span>' for t in skip) + '</div>'
    return p.panel(x, y, w, h or (524 - y), title, body, 'list', 'stretch')


def report_table(p, rows, x=0, y=404, w=540, h=120, title='方案规定的报告对象与时限', s=1):
    """Who reports to whom, what, by when — only what the protocol states. rows = [(who → whom, what, deadline)]."""
    body = ''.join(f'<div style="display:grid;grid-template-columns:31% 41% 28%;gap:6px;padding:3px 0;border-top:1px dashed #E6DFD3;line-height:1.35" class="f12">'
                   f'<b class="ink">{md(a)}</b><span>{md(b)}</span><b class="t-brand">{md(c)}</b></div>' for a, b, c in rows)
    p.panel(x, y, w, h, title, body, 'phone', 'flat stretch', s=s)


# ------------------------------------------------------------------ axes and time
def day_axis(L, R, d0, d1):
    """Linear day → x mapping: X = day_axis(40, 1128, -28, 1); X(-14)."""
    return lambda d: L + (d - d0) * (R - L) / (d1 - d0)


def piecewise_axis(segments):
    """Week → x with stretched short phases: segments = [(w0, w1, x0, x1), ...] in order."""
    def f(w):
        for w0, w1, x0, x1 in segments:
            if w <= w1:
                return x0 + (max(w, w0) - w0) * (x1 - x0) / (w1 - w0)
        w0, w1, x0, x1 = segments[-1]
        return x1
    return f


def time_axis(p, L, R, y, h0, h1, s=1, step=30):
    """Clock ticks h0:00..h1:00 at height y; returns T(h, m) → x."""
    T = lambda h, m: L + ((h * 60 + m) - h0 * 60) * (R - L) / ((h1 - h0) * 60)
    t = h0 * 60
    while t <= h1 * 60:
        p.el(T(0, t) - 22, y, 44, None, f'{t // 60:02d}:{t % 60:02d}', 'f12 mut c num', s=s)
        t += step
    return T


class StudyDates:
    """Example dates for a fictional participant: dates = StudyDates(date(2026, 12, 1)); dates(29) → '12/29' for Day 29.
    Day 1 = first dose; D-1 is the day before D1 and there is no Day 0 (protocol convention). Keep ONE instance in
    content/meta.py (DAY) and import it in page modules: from meta import DAY."""

    def __init__(self, d1):
        self.d1 = d1

    def date(self, n):
        if n == 0:
            raise ValueError('there is no Day 0: D-1 is the day before D1')
        return self.d1 + timedelta(n - 1 if n > 0 else n)

    def __call__(self, n):
        d = self.date(n)
        return f'{d.month:02d}/{d.day:02d}'

    def window(self, n, w):
        return f'{self(n - w)}～{self(n + w)}'


class Calendar:
    """Month grid (Monday first) for constraint-on-real-dates scenes.
    cal = Calendar(p, date(2026, 11, 2), weeks=6); cal.band(a, b, colour, s); cal.mark(day, '文字', 'ok', s)."""

    def __init__(self, p, start, x=0, y=30, cw=78, ch=56, weeks=6, s=1, dim_month=None):
        self.p, self.start, self.x, self.y, self.cw, self.ch = p, start, x, y, cw, ch
        for i, w in enumerate('一二三四五六日'):
            p.el(x + i * cw, y - 26, cw, None, '周' + w, 'f12 b c mut', s=s)
        for n in range(weeks * 7):
            d = start + timedelta(n)
            cx, cy = self.pos(d)
            col = '#B0A797' if dim_month and d.month == dim_month else '#3D4046'
            p.el(cx + 2, cy + 2, cw - 4, ch - 4, f'<span class="f13 b num" style="color:{col}">{d.month}/{d.day}</span>', '',
                 style='padding:3px 6px;border-radius:8px;background:rgba(255,255,255,.7);border:1px solid #EEE6DA', s=s, fx='fade', d=n * 8)

    def pos(self, d):
        n = (d - self.start).days
        return self.x + n % 7 * self.cw, self.y + n // 7 * self.ch

    def band(self, a, b, color, s, o=None, d=0):
        """Coloured strip along the bottom of each day cell from a to b (wraps across weeks)."""
        cur = a
        while cur <= b:
            x, y = self.pos(cur)
            run = min(7 - (cur - self.start).days % 7, (b - cur).days + 1)
            self.p.el(x + 2, y + self.ch - 14, run * self.cw - 4, 10, '', 'band', style=f'background:{color}', s=s, o=o, fx='wipe', d=d)
            cur += timedelta(run)

    def mark(self, day, text, kind, s, o=None, d=0):
        x, y = self.pos(day)
        self.p.el(x + 4, y + 20, self.cw - 8, None, f'<span class="tag {kind}" style="width:100%;justify-content:center">{md(text)}</span>', '', s=s, o=o, fx='pop', d=d)

    def ring(self, day, s, o=None, kind='bad'):
        x, y = self.pos(day)
        self.p.ring(x - 2, y - 2, self.cw + 4, self.ch + 4, kind, s=s, o=o)


# ------------------------------------------------------------------ measures
def threshold_bar(p, x, y, w, label, threshold, bad_side, value_pos, value_text, s=1, o=None, d=0, split=None):
    """Lab-style bar: red zone on bad_side ('low' | 'high'), a marker at value_pos (0..1) with its value.
    split = where the red zone ends/starts (0..1); default 0.4 for low, 0.6 for high."""
    cut = split if split is not None else (.4 if bad_side == 'low' else .6)
    grad = (f'linear-gradient(90deg,rgba(192,0,0,.2) 0 {cut:.0%},rgba(15,17,21,.06) {cut:.0%} 100%)' if bad_side == 'low' else
            f'linear-gradient(90deg,rgba(15,17,21,.06) 0 {cut:.0%},rgba(192,0,0,.2) {cut:.0%} 100%)')
    bad = (value_pos < cut) if bad_side == 'low' else (value_pos > cut)
    col = BAD if bad else OK
    p.el(x, y, w, None, f'<span class="f13 b ink">{md(label)}</span> <span class="f12 mut">{md(threshold)}</span>', '', s=s, o=o, d=d)
    p.el(x, y + 22, w, 12, '', '', style=f'border-radius:6px;background:{grad}', s=s, o=o, fx='wipe', d=d)
    p.el(x + w * value_pos - 5, y + 18, 10, 20, '', '', style=f'background:{col};border-radius:5px;border:2px solid #fff', s=s, o=o, fx='drop', d=d + 200)
    p.el(x + w * value_pos + 8, y + 18, 120, None, md(value_text), f'f12 b num {"t-bad" if bad else "t-ok"}', s=s, o=o, d=d + 250)


def gauge(p, x, y, n, total, color, s=1, o=None, d=0, name='', note='', r=54):
    """Ring meter n/total (diary days, doses, compliance) with a caption on the right. Box ≈ (x, y, 140+230, 2r+20)."""
    cx, cy = x + r + 16, y + r + 10
    arc = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EFE7DB" stroke-width="14"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round" pathLength="{total}" '
           f'stroke-dasharray="{n} {total}" transform="rotate(-90 {cx} {cy})"/>')
    p.svg_raw(f'<g{A(s=s, o=o, d=d, fx="pop")}>{arc}</g>')
    p.el(cx - 60, cy - 18, 120, None, f'<div class="f24 b num c" style="color:{color}">{n}/{total}</div>', '', s=s, o=o, d=d)
    if name or note:
        p.el(x + 2 * r + 46, cy - 30, 230, None, f'<div class="f14 b ink">{md(name)}</div><div class="f12">{md(note)}</div>', '', s=s, o=o, d=d)


def tube_html(cap, fill, label, sub=''):
    """A blood tube: cap colour, liquid colour, label under it. Put several in one p.el row (display:flex)."""
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px">'
            f'<div style="width:18px;height:10px;border-radius:3px 3px 0 0;background:{cap}"></div>'
            f'<div style="width:22px;height:64px;margin-top:-3px;border:2px solid #A9BCD0;border-radius:2px 2px 11px 11px;background:linear-gradient(transparent 28%,{fill} 28%)"></div>'
            f'<div class="f12 b ink nw">{md(label)}</div>' + (f'<div class="f12 mut nw" style="margin-top:-4px">{md(sub)}</div>' if sub else '') + '</div>')


def chip(p, x, y, w, h, text, s=1, o=None, d=0, k=None, cls='', ico=None, fx='drop'):
    """Movable item chip (a test, a document, a drug). Move/strike it with k={step: {'x':…, 'y':…, 'c': 'off'|'err'}}."""
    p.el(x, y, w, h, (icon(ico) if ico else '') + f'<span>{md(text)}</span>', ('chip ' + cls).strip(), s=s, o=o, d=d, k=k, fx=fx)


def switch_row(p, x, y, label, k, s=1, d=0, label_w=200):
    """Label + on/off switch; k = {step: {'c': 'on'}} or {'c': 'on err'}."""
    p.el(x, y + 4, label_w, None, f'<span class="f14 b ink">{md(label)}</span>', '', s=s, d=d)
    p.el(x + label_w + 36, y, 56, 28, '', 'sw', s=s, d=d, k=k)


# ------------------------------------------------------------------ flows
class Flow:
    """Decision flow drawn once at step 1; cases then walk through it as tokens, one case per step.

        f = Flow(p)
        f.node('ae', 0, 40, 150, 60, '发生不良事件', '任何时间', 'alert')
        f.diamond('q1', 190, 10, 160, 120, '是否严重？')
        f.node('sae', 400, 40, 170, 60, '按 SAE 报告', '获知后 24 小时内', 'bolt', 'bad')
        f.wire('ae', 'q1'); f.wire('q1', 'sae', 'bad', label='是')
        f.route('a', 'ae', 'q1', 'sae'); p.token({2: 'a'}, BAD, 'A', r=12)

    wire() connects the right edge of the first box to the left edge of the second (or pass an explicit SVG path
    with path=). route() builds an invisible token path through box centres (diamonds: top centre)."""

    def __init__(self, p, s=1):
        self.p, self.s, self.box, self.dia = p, s, {}, set()

    def node(self, key, x, y, w, h, title, sub=None, ico=None, cls='', s=None, d=0):
        self.box[key] = (x, y, w, h)
        self.p.node(x, y, w, h, title, sub, ico, cls, s=s or self.s, d=d)
        return self

    def diamond(self, key, x, y, w, h, text, s=None, d=0):
        self.box[key] = (x, y, w, h)
        self.dia.add(key)
        self.p.dia(x, y, w, h, text, s=s or self.s, d=d)
        return self

    def anchor(self, key, side):
        x, y, w, h = self.box[key]
        return {'l': (x, y + h / 2), 'r': (x + w, y + h / 2), 't': (x + w / 2, y), 'b': (x + w / 2, y + h), 'c': (x + w / 2, y + h / 2)}[side]

    def wire(self, a=None, b=None, cls='', label=None, path=None, s=None, sides='rl', curve=False):
        if path is None:
            (x1, y1), (x2, y2) = self.anchor(a, sides[0]), self.anchor(b, sides[1])
            if curve:
                path = f'M{x1:.0f} {y1:.0f} C {x1:.0f} {(y1 + y2) / 2:.0f} {x2:.0f} {(y1 + y2) / 2:.0f} {x2:.0f} {y2:.0f}'
            else:
                path = f'M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}'
        self.p.wire(path, cls, s=s or self.s)
        if label:
            nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', path)]
            mx, my = (nums[0] + nums[-2]) / 2, (nums[1] + nums[-1]) / 2
            self.p.el(mx - 15, my - 22, 30, None, md(label), 'f12 b mut c', s=s or self.s)
        return self

    def point(self, key, dx=0, dy=0):
        x, y, w, h = self.box[key]
        return (x + w / 2 + dx, y + 14 + dy) if key in self.dia else (x + w - 12 + dx, y + 4 + dy)

    def route(self, pid, *keys):
        """keys: box keys or (key, dx, dy) to offset parallel tokens."""
        pts = [self.point(*k) if isinstance(k, tuple) else self.point(k) for k in keys]
        self.p.path(pid, 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts))
        return self


class Lanes:
    """Swimlanes, one per role: lanes = Lanes(p, ['crc', 'pi', 'mm'], x=0, y=0, w=966, lane_h=84).
    lanes.box(1, 270, 170, '审核资料', '入组审核表签字', 'pen') returns the box (x, y, w, h)."""

    def __init__(self, p, roles, x=0, y=0, w=966, lane_h=84, gap=8, s=1, labels=None):
        self.p, self.x, self.y, self.lane_h, self.gap = p, x, y, lane_h, gap
        for i, r in enumerate(roles):
            ly = y + i * (lane_h + gap)
            p.el(x, ly, w, lane_h, '', '', style=f'background:{"rgba(255,255,255,.55)" if i % 2 == 0 else "rgba(246,242,236,.6)"};border-radius:12px', s=s, fx='fade')
            p.el(x + 10, ly + lane_h / 2 - 14, 110, None, role(r, (labels or {}).get(r)), '', s=s)

    def top(self, lane):
        return self.y + lane * (self.lane_h + self.gap)

    def box(self, lane, x, w, title, sub=None, ico=None, cls='', s=1, d=0, h=56):
        y = self.top(lane) + (self.lane_h - h) / 2
        self.p.node(x, y, w, h, title, sub, ico, cls, s=s, d=d)
        return (x, y, w, h)
