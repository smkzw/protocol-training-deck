"""Protocol originals for the "方案原文" drill-down: SRC[pid] = [(heading, [paragraph, ...])].
Copy by anchor from src/protocol.md (never retype); a missing anchor stops the build.

    from srctext import Source
    P = Source('src/protocol.md')
    SRC = {'incl_lab': [('排除标准（3.5.2）', [P.line('1. 筛选期丙氨酸')])]}
"""
SRC = {}
