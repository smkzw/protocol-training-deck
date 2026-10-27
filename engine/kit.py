"""Page kit for the v2 SOP deck: a 1168×564 canvas, step attributes for sop2.js, and reusable pieces.

Text markup inside strings: **bold**  !!dark red!!  ==brand chip==  __underline__  ^^marker highlight^^  [建议] [操作建议] → muted suggestion tags.
"""
from html import escape
import json
import re

W, H = 1168, 564


def md(s):
    if s is None:
        return ''
    s = escape(str(s), quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'!!(.+?)!!', r'<span class="kr">\1</span>', s)
    s = re.sub(r'==(.+?)==', r'<span class="k">\1</span>', s)
    s = re.sub(r'__(.+?)__', r'<span class="ku">\1</span>', s)
    s = re.sub(r'\^\^(.+?)\^\^', r'<span class="hl">\1</span>', s)
    s = s.replace('\n', '<br>')
    s = s.replace('[操作建议]', '<span class="sug">（操作建议）</span>').replace('[建议]', '<span class="sug">（建议）</span>')
    return s


def icon(name, cls=''):
    return f'<svg class="ico {cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def A(s=None, o=None, k=None, fx=None, d=None, count=None, move=None):
    """Step attributes."""
    out = ''
    if s is not None:
        out += f' data-s="{s}"'
    if o is not None:
        out += f' data-o="{o}"'
    if fx:
        out += f' data-fx="{fx}"'
    if d:
        out += f' data-d="{d}"'
    if k:
        out += " data-k='" + escape(json.dumps({str(a): b for a, b in k.items()}, ensure_ascii=False), quote=False).replace("'", '&#39;') + "'"
    if count:
        out += " data-count='" + json.dumps({str(a): b for a, b in count.items()}) + "'"
    if move:
        out += " data-move='" + json.dumps({str(a): b for a, b in move.items()}) + "'"
    return out


ROLE = {'crc': ('CRC', 'user', 'rc-crc'), 'cra': ('CRA', 'search', 'rc-cra'), 'mm': ('MM', 'shield', 'rc-mm'),
        'pi': ('研究者', 'doctor', 'rc-pi'), 'sub': ('受试者', 'user', 'rc-sub'), 'pv': ('PV', 'alert', 'rc-pv'),
        'nurse': ('研究护士', 'nurse', 'rc-pi'), 'sys': ('系统', 'monitor', 'rc-sys'), 'lab': ('中心实验室', 'flask', 'rc-sys'),
        'read': ('中心阅片', 'eye', 'rc-sys'), 'iwrs': ('IWRS', 'shuffle', 'rc-sys'), 'ec': ('伦理委员会', 'hospital', 'rc-pi'),
        'pharm': ('药物管理员', 'pill', 'rc-pi')}


def role(key, label=None, cls='f13'):
    name, ic, rc = ROLE[key]
    return f'<span class="role {rc} {cls}"><span class="av">{icon(ic)}</span>{escape(label or name)}</span>'


class Page:
    def __init__(self, pid, title, sub=None):
        self.id, self.title, self.sub = pid, title, sub
        self.parts, self.wires, self.defs, self.toks = [], [], [], []

    # ---- generic absolute element
    def el(self, x, y, w=None, h=None, inner='', cls='', tag='div', style='', **st):
        sty = f'--x:{x};--y:{y};' + (f'--w:{w};' if w is not None else '') + (f'--h:{h};' if h is not None else '')
        if h is None:
            cls += ' auto-h'
        if w is None:
            sty += 'width:auto;'
        self.parts.append(f'<{tag} class="ab {cls}" style="{sty}{style}"{A(**st)}>{inner}</{tag}>')
        return self

    def raw(self, html):
        self.parts.append(html)
        return self

    # ---- panels and text
    def panel(self, x, y, w, h, title=None, body='', ico=None, cls='', tcls='', **st):
        t = f'<div class="pn-t {tcls}">{icon(ico) if ico else ""}{md(title)}</div>' if title else ''
        return self.el(x, y, w, h, t + body, 'pn ' + cls, **st)

    def text(self, x, y, w, txt, cls='f14', h=None, **st):
        return self.el(x, y, w, h, md(txt).replace('\n', '<br>'), cls, **st)

    def node(self, x, y, w, h, title, sub=None, ico=None, cls='', **st):
        inner = f'<div class="h">{icon(ico) if ico else ""}{md(title)}</div>' + (f'<div class="s">{md(sub)}</div>' if sub else '')
        return self.el(x, y, w, h, inner, 'nd ' + cls, **st)

    def dia(self, x, y, w, h, text, cls='', **st):
        return self.el(x, y, w, h, f'<span>{md(text)}</span>', 'dia ' + cls, **st)

    def tag(self, x, y, text, kind='', **st):
        return self.el(x, y, None, None, f'<span class="tag {kind}">{md(text)}</span>', '', **st)

    def stamp(self, x, y, size, kind='ok', **st):
        ic = {'ok': 'check', 'bad': 'x', 'warn': 'alert'}[kind]
        return self.el(x, y, size, size, icon(ic), f'stamp {kind}', fx=st.pop('fx', 'pop'), **st)

    def ring(self, x, y, w, h, kind='', **st):
        return self.el(x, y, w, h, '', f'hl-ring {kind}', fx=st.pop('fx', 'pop'), **st)

    # ---- narration: list of strings (step 1..n) or dict {step: text}
    def narr(self, x, y, w, h, steps, start=1):
        items = steps.items() if isinstance(steps, dict) else [(start + i, t) for i, t in enumerate(steps)]
        items = sorted(items)
        out = []
        for i, (k, t) in enumerate(items):
            o = items[i + 1][0] if i + 1 < len(items) else None
            out.append(f'<div class="ne"{A(s=k, o=o, fx="fade")}><span class="no">{k}</span><div class="tx">{md(t)}</div></div>')
        self.parts.append(f'<div class="narr ab" style="--x:{x};--y:{y};--w:{w};--h:{h}">{"".join(out)}</div>')
        return self

    # ---- checklist
    def checklist(self, x, y, w, h, groups, title=None, ico='list'):
        """groups: [(group title, [(text, done_step, state)])], state 'ok'|'fail'; now = step it is highlighted."""
        body = ''
        for g, items in groups:
            body += f'<div class="ck-g">{md(g)}</div>'
            for it in items:
                text, ds = it[0], it[1]
                kind = it[2] if len(it) > 2 else 'ok'
                note = it[3] if len(it) > 3 else ''
                frames = {}
                if ds is not None:
                    frames[ds] = {'c': 'done' if kind == 'ok' else 'fail'}
                body += (f'<div class="ck"{A(k=frames) if frames else ""}><span class="bx">{icon("check" if kind == "ok" else "x")}</span>'
                         f'<span class="ct">{md(text)}{f" <em>{md(note)}</em>" if note else ""}</span></div>')
        return self.panel(x, y, w, h, title, body, ico)

    # ---- wires (canvas coordinates)
    def wire(self, d, cls='', s=None, o=None, arrow=True, pid=None, draw=True, d_ms=None):
        mk = ' marker-end="url(#ah-' + (cls.split()[0] if cls and cls.split()[0] in ('ok', 'bad', 'brand', 'cra', 'mm', 'pv') else 'n') + ')"' if arrow else ''
        idattr = f' id="{self.id}-{pid}"' if pid else ''
        dcls = ' draw' if draw and s is not None else ''
        self.wires.append(f'<path class="w {cls}{dcls}" d="{d}" pathLength="1"{mk}{idattr}{A(s=s, o=o, d=d_ms)}/>')
        return self

    def path(self, pid, d):
        """Invisible motion path for tokens."""
        self.wires.append(f'<path id="{self.id}-{pid}" d="{d}" fill="none" stroke="none"/>')
        return self

    def wlabel(self, x, y, text, cls='', s=None, anchor='middle'):
        self.wires.append(f'<text class="wl {cls}" x="{x}" y="{y}" text-anchor="{anchor}"{A(s=s)}>{escape(text)}</text>')
        return self

    def token(self, moves, color='#FF9900', label=None, r=9, ico=None, o=None):
        """moves: {step: pid}. Draw a dot (optionally with a short label) that travels along the paths."""
        mv = {k: f'{self.id}-{v}' for k, v in moves.items()}
        lab = f'<text y="4" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{escape(label)}</text>' if label else ''
        self.toks.append(f'<g class="tok"{A(move=mv, o=o)}><circle r="{r}" fill="{color}" stroke="#fff" stroke-width="2.5"/>{lab}</g>')
        return self

    def svg_raw(self, s):
        self.wires.append(s)
        return self

    # ---- render
    def render(self):
        markers = ''.join(f'<marker id="ah-{n}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                          f'<path d="M0 0 10 5 0 10z" fill="{c}"/></marker>' for n, c in
                          (('n', '#BDB4A6'), ('ok', '#2F8A57'), ('bad', '#C00000'), ('brand', '#FF9900'), ('cra', '#4A6D8C'), ('mm', '#E98A00'), ('pv', '#A85F34')))
        svg = (f'<svg class="wires" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs>{markers}{"".join(self.defs)}</defs>'
               + ''.join(self.wires) + '</svg>')
        top = f'<svg class="wires" viewBox="0 0 {W} {H}" preserveAspectRatio="none">{"".join(self.toks)}</svg>' if self.toks else ''
        body = svg + ''.join(self.parts) + top
        nums = [int(n) for n in re.findall(r'data-[so]="(\d+)"', body)]
        for blob in re.findall(r"data-(?:k|count|move)='([^']*)'", body):
            nums += [int(n) for n in re.findall(r'&quot;(\d+)&quot;|"(\d+)"\s*:', blob.replace('&quot;', '"')) for n in n if n]
        steps = max(nums) if nums else 0
        return body, steps
