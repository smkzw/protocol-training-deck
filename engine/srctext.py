"""Copy protocol text for the "方案原文" drill-down without retyping it.

    P = Source('src/protocol.md')
    P.line('2. 筛选期和基线时')            → the whole line that starts with these words
    P.lines('## 3.5.1', 6)                 → the 6 non-empty lines after the heading line
A prefix that is not found stops the build, so a changed protocol never silently shows stale text.
"""
from pathlib import Path


class Source:
    def __init__(self, path, start=0):
        root = Path(__file__).resolve().parents[1]
        self.rows = (root / path).read_text(encoding='utf-8').split('\n')
        self.start, self.path = start, path

    def index(self, prefix, after=None):
        for i in range(self.start if after is None else after, len(self.rows)):
            if self.rows[i].strip().startswith(prefix):
                return i
        raise SystemExit(f'ERROR {self.path}: anchor not found: {prefix}')

    def line(self, prefix, after=None):
        return self.rows[self.index(prefix, after)].strip()

    def lines(self, prefix, n, after=None):
        i, out = self.index(prefix, after) + 1, []
        while len(out) < n and i < len(self.rows):
            if self.rows[i].strip():
                out.append(self.rows[i].strip())
            i += 1
        return out
