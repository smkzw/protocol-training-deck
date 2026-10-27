"""Dump a .docx to plain text in body order, tables rendered as pipe rows with merged-cell dedupe."""
import sys
import zipfile
import re
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def text_of(el):
    out = []
    for node in el.iter():
        if node.tag == W + 't' and node.text:
            out.append(node.text)
        elif node.tag == W + 'tab':
            out.append('\t')
        elif node.tag in (W + 'br', W + 'cr'):
            out.append('\n')
        elif node.tag == W + 'sym':
            out.append('□')
    return ''.join(out)


def para_style(p):
    ppr = p.find(W + 'pPr')
    if ppr is not None:
        ps = ppr.find(W + 'pStyle')
        if ps is not None:
            return ps.get(W + 'val') or ''
    return ''


def dump_table(tbl, lines, depth=0):
    for tr in tbl.findall(W + 'tr'):
        cells = []
        for tc in tr.findall(W + 'tc'):
            tcpr = tc.find(W + 'tcPr')
            span = 1
            vmerge_cont = False
            if tcpr is not None:
                gs = tcpr.find(W + 'gridSpan')
                if gs is not None:
                    span = int(gs.get(W + 'val'))
                vm = tcpr.find(W + 'vMerge')
                if vm is not None and vm.get(W + 'val') != 'restart':
                    vmerge_cont = True
            parts = []
            for child in tc:
                if child.tag == W + 'p':
                    parts.append(text_of(child))
                elif child.tag == W + 'tbl':
                    sub = []
                    dump_table(child, sub, depth + 1)
                    parts.append(' / '.join(sub))
            t = ' '.join(x.strip() for x in parts if x.strip())
            if vmerge_cont:
                t = '^'
            cells.append(t + (' <span%d>' % span if span > 1 else ''))
        lines.append('  ' * depth + '| ' + ' | '.join(cells) + ' |')


def main(path, out):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W + 'body')
    lines = []
    for child in body:
        if child.tag == W + 'p':
            t = text_of(child).strip()
            if t:
                st = para_style(child)
                prefix = '#' * int(m.group(1)) + ' ' if (m := re.search(r'(\d)', st)) and 'eading' in st else ''
                lines.append(prefix + t)
        elif child.tag == W + 'tbl':
            lines.append('[TABLE]')
            dump_table(child, lines)
            lines.append('[/TABLE]')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    # footnotes
    if 'word/footnotes.xml' in z.namelist():
        fr = ET.fromstring(z.read('word/footnotes.xml'))
        fn = [text_of(f).strip() for f in fr.findall(W + 'footnote')]
        open(out.replace('.md', '_footnotes.md'), 'w', encoding='utf-8').write('\n'.join(x for x in fn if x))
    print(len(lines), 'lines')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
