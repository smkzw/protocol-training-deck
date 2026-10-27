"""Kangzhe header mark (the double rhombus top-left on body pages), from the approved SVG asset.

Each slide needs its own id prefix, otherwise gradients/filters of different slides collide.
"""
from pathlib import Path
import re

_SVG = (Path(__file__).resolve().parent / 'header-mark.svg').read_text(encoding='utf-8')
_INNER = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', _SVG.strip())


def facets(prefix='kz'):
    s = _INNER.replace('id="kz-', f'id="{prefix}-').replace('url(#kz-', f'url(#{prefix}-')
    return re.sub(r'(<g data-kz-header-mark="[^"]*")', r'\1 class="kz-mark-float"', s, count=1)
