"""Chapter 01: assessment scales (P3 card grid) and the visit × item matrix (P5 with focus questions)."""
from components import Page, icon, md

# SoA as data: every count or "which visits" statement on any page derives from this one dict (plan/facts.md §4)
VISITS = [('V1', 'D-28～D-1'), ('V2', 'D1'), ('V3', 'W2'), ('V4', 'W4'), ('V5', 'W8'), ('V6', 'W12'), ('V7', 'W16'), ('V8', 'W28')]
SOA = {
    '给药': 'V2 V4 V5 V6',
    'EASI / IGA / BSA': 'V1 V2 V4 V5 V6 V7 V8',
    'PK 血样': 'V2 V4 V6 V7',
    '血常规 / 血生化': 'V1 V2 V4 V6 V7 V8',
}


def scales():
    p = Page('scales', '')
    # (name, assessor tag, item lines, grading segments [(label, flex weight, colour)], threshold note)
    cards = [
        ('EASI 湿疹面积和严重程度指数', ('研究者', 'cra'), ['4 个部位：头颈、躯干、上肢、下肢', '4 项体征：红斑、水肿/丘疹、表皮剥脱、苔藓化，每项 0～3 分', '受累面积 0～6 分'],
         [('0', 16, '#F3EDE3'), ('16 入选下限', 56, 'rgba(255,153,0,.35)')], '总分 0～72；入选要求 ≥16'),
        ('IGA 研究者整体评估', ('研究者', 'cra'), ['对整体皮损做 5 级评估', '只取整数，不取中间值'],
         [('0 清除', 1, '#F3EDE3'), ('1 几乎清除', 1, '#F3EDE3'), ('2 轻度', 1, '#F3EDE3'), ('3 中度', 1, 'rgba(255,153,0,.35)'), ('4 重度', 1, 'rgba(255,153,0,.5)')], '入选要求 ≥3'),
        ('BSA 累及体表面积', ('研究者', 'cra'), ['皮损面积占全身体表面积的百分比'],
         [('0%', 10, '#F3EDE3'), ('10% 入选下限 → 100%', 90, 'rgba(255,153,0,.35)')], '入选要求 ≥10%'),
        ('瘙痒 NRS 数字评分', ('受试者自评', 'ok'), ['每日记录过去 24 小时最严重瘙痒', '0 = 无瘙痒，10 = 能想象的最严重瘙痒'],
         [('0', 4, '#F3EDE3'), ('4 入选下限 → 10', 6, 'rgba(255,153,0,.35)')], '基线前 7 天周平均 ≥4，且 ≥4 天有评分'),
    ]
    W, H = 572, 196
    for i, (name, (who, kind), items, segs, note) in enumerate(cards):
        x, y, st = (i % 2) * (W + 24), (i // 2) * (H + 16), i + 1
        dim = {k: {'c': 'on' if k == st else 'is-dim'} for k in range(1, 5)}       # card k is the focus at step k
        body = (f'<div style="display:flex;align-items:center;gap:8px"><span class="f16 b ink">{md(name)}</span><span class="tag {kind}">{md(who)}</span></div>'
                + ''.join(f'<div class="f13" style="margin-top:4px">· {md(t)}</div>' for t in items))
        p.el(x, y, W, H, body, 'pn', style='display:block', s=1, d=i * 120, k=dim)   # display:block = content starts at the top
        bar = ''.join(f'<div style="flex:{w};background:{c};display:flex;align-items:center;justify-content:center;border-right:2px solid #fff" class="f12 b ink nw">{md(t)}</div>'
                      for t, w, c in segs)
        p.el(x + 14, y + H - 66, W - 28, 30, bar, '', style='display:flex;border-radius:8px;overflow:hidden', s=st, fx='wipe')
        p.el(x + 14, y + H - 30, W - 28, None, f'<span class="f12 t-brand b">{md(note)}</span>', '', s=st, d=300)
    p.narr(0, 424, 1168, 100, [
        'EASI 由研究者评估 4 个部位、4 项体征的严重程度和受累面积，总分 0 到 72 分，入选要求不低于 16 分。',
        'IGA 是研究者对整体皮损的 5 级评估：0 清除到 4 重度，入选要求不低于 3 级。',
        'BSA 是皮损面积占全身体表面积的百分比，入选要求不低于 10%。',
        '瘙痒 NRS 由受试者每天自评，0 到 10 分；基线前 7 天的周平均不低于 4 分，且至少 4 天有评分。',
    ])
    return p


def matrix():
    p = Page('matrix', '')
    L, T, CW, CH = 170, 60, 84, 66
    for j, (v, t) in enumerate(VISITS):
        p.el(L + j * CW, 0, CW - 8, None, f'<div class="f14 b ink c">{v}</div><div class="f12 mut c num">{t}</div>', '', s=1, d=j * 40)
    focus = {2: ('row', '给药'), 3: ('row', 'PK 血样'), 4: ('col', 'V7')}   # what each step lights up
    for i, (item, visits) in enumerate(SOA.items()):
        y = T + i * CH
        p.el(0, y + 10, L - 12, None, f'<span class="f13 b ink">{md(item)}</span>', '', s=1)
        for j, (v, _) in enumerate(VISITS):
            on = v in visits.split()
            k = {st: {'c': '' if (kind == 'row' and key == item) or (kind == 'col' and key == v) else 'is-dim'} for st, (kind, key) in focus.items()}
            p.el(L + j * CW + 12, y + 8, CW - 32, CH - 16, '', 'cel' + (' on' if on else ''), s=1, fx='pop', d=j * 40 + i * 30, k=k)
    bottom = T + len(SOA) * CH
    p.el(L - 4, T - 4, len(VISITS) * CW, len(SOA) * CH, '', 'hl-ring', s=1, o=2)
    cards = [
        (1, '怎么读这张表', '每一行是一个项目，每一列是一次访视；橙色格表示方案流程表要求本次做。'),
        (2, '哪几次给药？', '**V2、V4、V5、V6**，共 4 次；V3 和 V7 不给药。'),
        (3, 'PK 在哪几次？', '**V2、V4、V6、V7**；给药访视的 PK 都在给药前 1 小时内采。'),
        (4, 'V7（主要终点）做什么？', '疗效评估、PK、血常规和血生化；**不给药**。'),
    ]
    for st, title, text in cards:
        p.panel(880, T, 288, 200, title, f'<div class="f14">{md(text)}</div>', 'search', 'tint', s=st, o=st + 1 if st < 4 else None)
    p.el(0, bottom + 20, 860, None, f'<span class="f12 mut">{icon("file")} 按方案 4.2 流程表整理；访视项目数和各页的“哪几次”都从同一份数据计算。</span>', '', s=1)
    p.narr(0, 424, 1168, 100, [
        '这张表按方案流程表整理：行是项目，列是访视，橙色格表示本次要做。',
        '先看给药：V2、V4、V5、V6 共 4 次，V3 和 V7 不给药。',
        'PK 在 V2、V4、V6、V7 采集，给药访视的 PK 都要在给药前 1 小时内完成。',
        'V7 是主要终点访视：做疗效评估、PK 和化验，但不给药。',
    ])
    return p


PAGES = [scales, matrix]
