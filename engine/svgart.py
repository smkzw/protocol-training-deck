"""Fallback illustrations in plain SVG, for when no image generator is available (or its output is not usable).

Style contract (same as the deck): flat shapes, warm neutral fills, 2 px strokes in #B9AE9C, brand orange #FF9900 for
the thing being taught, red #C00000 only for "blocked / wrong", green #2F8A57 only for "allowed / correct".
No realistic anatomy, no faces, no skin tones — schematic shapes with labels read better on a projector.

Every function returns an <svg> string with its own viewBox; place it with p.el(x, y, w, h, svg, '') and keep the box
aspect ratio close to the viewBox ratio. To reveal parts step by step, use the *_layers() functions: they return
several SVGs with the same viewBox that you stack in the same box with different s= / o=.
"""
from html import escape

LINE, FILL, SOFT, INK = '#B9AE9C', '#F3EDE3', '#FBF8F3', '#3D4046'
BRAND, BAD, OK, CRA = '#FF9900', '#C00000', '#2F8A57', '#4A6D8C'


def _svg(vb, body):
    return f'<svg viewBox="{vb}" style="width:100%;height:100%;overflow:visible" aria-hidden="true">{body}</svg>'


def _label(x, y, text, color=INK, size=13, anchor='middle', weight=700):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>'


# ------------------------------------------------------------------ people and body regions
ZONES = {  # front view, viewBox 0 0 200 420
    'abdomen': (70, 170, 60, 56), 'thigh_l': (66, 262, 30, 70), 'thigh_r': (104, 262, 30, 70),
    'arm_l': (30, 112, 22, 62), 'arm_r': (148, 112, 22, 62), 'chest': (66, 100, 68, 56),
}


def person(zones=(), blocked=(), labels=True):
    """Front-view schematic figure. zones = region keys to highlight in orange (e.g. injection sites);
    blocked = regions to hatch red (e.g. 5 cm around the navel → pass 'navel')."""
    body = (f'<circle cx="100" cy="44" r="28" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M62 86 Q100 74 138 86 L150 112 L172 180 L156 186 L140 128 L138 250 L132 400 L106 400 L100 268 L94 400 L68 400 L62 250 L60 128 L44 186 L28 180 L50 112 Z" '
            f'fill="{FILL}" stroke="{LINE}" stroke-width="2" stroke-linejoin="round"/>')
    for z in zones:
        x, y, w, h = ZONES[z]
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="rgba(255,153,0,.28)" stroke="{BRAND}" stroke-width="2"/>'
    if 'navel' in blocked:
        body += ('<defs><pattern id="sa-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                 f'<line x1="0" y1="0" x2="0" y2="6" stroke="{BAD}" stroke-width="2"/></pattern></defs>'
                 f'<circle cx="100" cy="198" r="14" fill="url(#sa-hatch)" stroke="{BAD}" stroke-width="1.5"/>')
    if labels:
        names = {'abdomen': '腹部', 'thigh_l': '大腿', 'thigh_r': '大腿', 'arm_l': '上臂', 'arm_r': '上臂', 'chest': '胸部'}
        for z in zones:
            x, y, w, h = ZONES[z]
            body += _label(x + w / 2, y + h + 14, names[z], BRAND, 12)
    return _svg('0 0 200 420', body)


# ------------------------------------------------------------------ tissue / organ schematics
def skin_section(highlight='dermis'):
    """Skin cross-section: epidermis, dermis, subcutis; highlight one layer (e.g. where an SC injection goes)."""
    layers = [('epidermis', '表皮', 0, 30, '#F6E3CF'), ('dermis', '真皮', 30, 80, '#F1D3B8'), ('subcutis', '皮下组织', 110, 90, '#F8EAD2')]
    body = ''
    for key, name, y, h, col in layers:
        stroke = BRAND if key == highlight else LINE
        body += f'<rect x="0" y="{y}" width="320" height="{h}" fill="{col}" stroke="{stroke}" stroke-width="{3 if key == highlight else 1.5}"/>'
        body += _label(330, y + h / 2 + 5, name, BRAND if key == highlight else INK, 13, 'start')
    for cx in (60, 150, 240):
        body += f'<ellipse cx="{cx}" cy="160" rx="22" ry="14" fill="#FFF6E6" stroke="{LINE}" stroke-width="1.5"/>'
    return _svg('0 0 400 200', body)


def lungs():
    """Two lungs with trachea and bronchi, for spirometry / asthma context."""
    body = (f'<path d="M100 10 L100 70 M100 70 L70 100 M100 70 L130 100" stroke="{LINE}" stroke-width="8" stroke-linecap="round" fill="none"/>'
            f'<path d="M86 60 C40 60 18 120 20 190 C22 230 60 236 86 220 Z" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M114 60 C160 60 182 120 180 190 C178 230 140 236 114 220 Z" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>')
    return _svg('0 0 200 240', body)


# ------------------------------------------------------------------ drug, mechanism
def antibody(color=BRAND, label=None):
    """Y-shaped IgG antibody."""
    body = (f'<path d="M60 150 L60 90 L20 40 M60 90 L100 40" stroke="{color}" stroke-width="14" stroke-linecap="round" fill="none"/>'
            f'<path d="M60 150 L60 90 L20 40 M60 90 L100 40" stroke="#fff" stroke-width="3" stroke-linecap="round" fill="none" opacity=".55"/>')
    if label:
        body += _label(60, 172, label, color, 14)
    return _svg('0 0 120 180', body)


def moa_layers(ligands=('配体 A', '配体 B'), receptor='受体', drug='研究药物', target_note=''):
    """Mechanism of action in four stacked layers (same viewBox 0 0 520 300):
      'base'    cell membrane + receptor + cell label
      'ligand'  ligands arriving and binding (arrow)
      'signal'  downstream signal arrow into the cell
      'drug'    antibody bound to the receptor + red block marks on the ligand arrows and the signal
    Typical steps: base+ligand+signal at step 1 (the disease pathway), drug at step 2 (what the drug blocks)."""
    vb = '0 0 520 300'
    base = (f'<rect x="0" y="190" width="520" height="22" rx="11" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
            f'<rect x="0" y="212" width="520" height="88" fill="{SOFT}"/>'
            f'<path d="M240 190 L240 150 Q240 132 258 132 L262 132 Q280 132 280 150 L280 190 Z" fill="#E7DCCB" stroke="{LINE}" stroke-width="2"/>'
            f'<rect x="248" y="190" width="24" height="40" rx="6" fill="#E7DCCB" stroke="{LINE}" stroke-width="2"/>'
            + _label(292, 178, receptor, INK, 14, 'start') + _label(60, 260, '细胞', '#8A8F96', 13))
    lig = ''
    xs = [70, 450]
    for i, name in enumerate(ligands[:2]):
        x = xs[i]
        lig += (f'<circle cx="{x}" cy="60" r="20" fill="#FFE2B3" stroke="{BRAND}" stroke-width="2"/>' + _label(x, 30, name, INK, 13)
                + f'<path d="M{x} 82 Q{(x + 260) / 2} 110 {250 if i == 0 else 270} 136" stroke="{BRAND}" stroke-width="2.5" fill="none" stroke-dasharray="6 5"/>')
    signal = (f'<path d="M260 232 L260 282" stroke="{BRAND}" stroke-width="5" stroke-linecap="round"/>'
              f'<path d="M250 272 L260 288 L270 272" fill="none" stroke="{BRAND}" stroke-width="5" stroke-linejoin="round"/>'
              + _label(330, 270, '炎症信号', BRAND, 13, 'start'))
    x_mark = lambda x, y: f'<path d="M{x - 11} {y - 11} L{x + 11} {y + 11} M{x + 11} {y - 11} L{x - 11} {y + 11}" stroke="{BAD}" stroke-width="5" stroke-linecap="round"/>'
    drug_svg = (f'<g transform="translate(222 40) scale(.62)"><path d="M60 150 L60 90 L20 40 M60 90 L100 40" stroke="{CRA}" stroke-width="16" stroke-linecap="round" fill="none"/></g>'
                + _label(214, 44, drug, CRA, 14, 'end') + (_label(214, 62, target_note, '#5F6B76', 12, 'end', 400) if target_note else '')
                + x_mark(160, 110) + x_mark(360, 110) + x_mark(260, 258))
    return {'base': _svg(vb, base), 'ligand': _svg(vb, lig), 'signal': _svg(vb, signal), 'drug': _svg(vb, drug_svg)}


# ------------------------------------------------------------------ devices
def pen_injector(color=BRAND):
    body = (f'<rect x="10" y="30" width="250" height="44" rx="22" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
            f'<rect x="150" y="38" width="60" height="28" rx="6" fill="#FFF" stroke="{LINE}" stroke-width="1.5"/>'
            f'<rect x="260" y="40" width="40" height="24" rx="6" fill="{color}"/><path d="M300 52 L330 52" stroke="{LINE}" stroke-width="3"/>')
    return _svg('0 0 340 104', body)


def vial(fill_level=.6, color=BRAND, label=None):
    top = 40 + (1 - fill_level) * 100
    body = (f'<rect x="34" y="6" width="52" height="20" rx="4" fill="{color}"/>'
            f'<rect x="20" y="26" width="80" height="124" rx="12" fill="#FFF" stroke="{LINE}" stroke-width="2"/>'
            f'<rect x="24" y="{top:.0f}" width="72" height="{146 - top:.0f}" rx="9" fill="rgba(255,153,0,.25)"/>')
    if label:
        body += _label(60, 176, label, INK, 13)
    return _svg('0 0 120 184', body)


def tablet(color=BRAND, n=1):
    """Oral dose: n capsule-shaped tablets side by side (n ≤ 4)."""
    body = ''
    for i in range(n):
        x = 10 + i * 70
        body += (f'<rect x="{x}" y="20" width="60" height="28" rx="14" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M{x + 30} 20 L{x + 30} 48 L{x + 16} 48 A14 14 0 0 1 {x + 16} 20 Z" fill="{color}" opacity=".75"/>')
    return _svg(f'0 0 {20 + n * 70} 68', body)


def iv_bag(color=BRAND, label=None):
    """Intravenous infusion: bag, drip chamber and line."""
    body = (f'<path d="M30 10 L110 10 L110 120 Q110 140 90 140 L50 140 Q30 140 30 120 Z" fill="#FFF" stroke="{LINE}" stroke-width="2"/>'
            f'<rect x="36" y="60" width="68" height="74" rx="10" fill="rgba(255,153,0,.22)"/>'
            f'<rect x="62" y="140" width="16" height="26" rx="4" fill="{FILL}" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M70 166 L70 230" stroke="{color}" stroke-width="3"/>')
    if label:
        body += _label(70, 40, label, INK, 13)
    return _svg('0 0 140 240', body)
