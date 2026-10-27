"""Chapter 02: the V1 visit as an S-shaped flow (P20), eligibility thresholds (rule text first, then measured examples)
and the screening calendar."""
from datetime import date
from components import (Page, icon, md, Verbatim, quote_card, threshold_bar, verdict_board, alert, kv_card,
                        Calendar, gauge, OK, BAD, BRAND)

q = Verbatim('src/protocol.md')


def v1_flow():
    """P20: 12 items in three rows (row 2 runs right to left); the number badges belong to the slots, so the swap at
    step 4 shows blood sampling sitting in slot 1."""
    p = Page('v1_flow', '')
    items = [('签署知情同意书', '先于一切研究操作', 'pen'), ('分配筛选号', None, 'key'), ('人口学资料', None, 'user'), ('病史与既往用药', '用于洗脱期判定', 'file'),
             ('合并用药', None, 'pill'), ('生命体征', None, 'ecg'), ('身高体重', None, 'scale'), ('体格检查', None, 'doctor'),
             ('EASI · IGA · BSA', '入选 2～4', 'clipboard'), ('血常规、血生化', '采血 · 排除 1', 'tube'), ('发放日志卡', '每日记录瘙痒评分', 'diary'),
             ('预约基线访视', '筛选期最长 28 天', 'calendar')]
    XS, YS, W, H = [40, 330, 620, 910], [10, 120, 230], 218, 56
    slot = lambda n: (XS[n % 4] if (n // 4) % 2 == 0 else XS[3 - n % 4], YS[n // 4])
    swap = {0: 9, 9: 0}     # step 4: ICF and blood sampling trade places
    for n, (title, sub, ico) in enumerate(items):
        x, y = slot(n)
        st = n // 4 + 1
        k = None
        if n in swap:
            tx, ty = slot(swap[n])
            k = {4: {'x': tx, 'y': ty, 'c': 'bad'}, 5: {'x': x, 'y': y, 'c': ''}}
        p.node(x, y, W, H, title, sub, ico, s=st, d=(n % 4) * 120, k=k)
        p.el(x - 11, y - 9, 22, 22, f'{n + 1}', 'f12 b c num', style=f'display:grid;place-items:center;background:{BRAND};color:#fff;border-radius:50%;z-index:3', s=st, d=(n % 4) * 120)
    for n in range(11):
        (x1, y1), (x2, y2) = slot(n), slot(n + 1)
        st = (n + 1) // 4 + 1
        if y1 == y2:
            a, b = (x1 + W + 4, x2 - 4) if x2 > x1 else (x1 - 4, x2 + W + 4)
            p.wire(f'M{a} {y1 + 28} L{b} {y2 + 28}', '', s=st)
        elif x1 > 500:
            p.wire(f'M{x1 + W} {y1 + 28} C 1162 {y1 + 28} 1162 {y2 + 28} {x2 + W + 4} {y2 + 28}', '', s=st)
        else:
            p.wire(f'M{x1} {y1 + 28} C 6 {y1 + 28} 6 {y2 + 28} {x2 - 4} {y2 + 28}', '', s=st)
    # red link between the swapped pair, threaded through the gap between boxes 8 and 7
    p.wire(f'M{XS[0] + W / 2} {YS[0] + H + 4} C {XS[0] + W / 2} 96 294 96 294 148 S {XS[1] + W / 2} 200 {XS[1] + W / 2} {YS[2] - 4}', 'bad dash', s=4, o=5)
    icf = q('任何研究相关操作均须在签署知情同意书之后进行。')
    quote_card(p, 40, 314, 520, 88, '方案 4.1', icf.replace('签署知情同意书之后', '__签署知情同意书之后__'), s=1)
    alert(p, 600, 314, 528, 88, 'bad', '受试者早到，先采血、后签知情同意书', '采血属于研究操作，发生在签署之前，不符合方案 4.1。', s=4, o=5)
    alert(p, 600, 314, 528, 88, 'ok', '先签署，再做第 2～12 项', '签署日期和时间早于第一项研究操作。', s=5)
    p.narr(0, 414, 1168, 106, [
        'V1 共 12 项。第一行：签署知情同意书、分配筛选号、人口学资料、病史与既往用药。',
        '第二行：合并用药、生命体征、身高体重、体格检查。既往用药和合并用药会用在洗脱期判定上。',
        '第三行：EASI、IGA、BSA 评估，血常规和血生化采血，发放日志卡，最后预约基线访视。',
        '反例：受试者来得早，先抽了血再签知情同意书。采血是研究操作，发生在签署之前，不符合方案。',
        '正确顺序：知情同意书永远排第一，签署时间早于任何研究操作。',
    ])
    return p


def incl_easi():
    p = Page('incl_easi', '')
    # step 1: the protocol text, thresholds underlined (quoted verbatim, then marked)
    inc = [q('筛选期和基线时湿疹面积和严重程度指数（EASI）评分≥16分。').replace('≥16分', '__≥16分__'),
           q('筛选期和基线时研究者整体评估（IGA）评分≥3分。').replace('≥3分', '__≥3分__'),
           q('筛选期和基线时特应性皮炎累及体表面积（BSA）≥10%。').replace('≥10%', '__≥10%__')]
    quote_card(p, 0, 0, 540, 176, '入选 2～4 · 方案原文', '\n'.join(f'{i + 2}. {t}' for i, t in enumerate(inc)), s=1, o=4)
    exc = q('筛选期丙氨酸氨基转移酶（ALT）或天门冬氨酸氨基转移酶（AST）>3×正常值上限（ULN）。').replace('>3×正常值上限（ULN）', '__>3×正常值上限（ULN）__')
    recheck = q('实验室检查不合格的允许在筛选期内复查一次。').replace('复查一次', '__复查一次__')
    quote_card(p, 0, 0, 540, 176, '排除 1 与复查 · 方案原文', '排除 1. ' + exc + '\n筛选期（4.1）：' + recheck, s=4)
    # steps 2–4: one participant measured twice, then the lab exclusion
    X, WB = 600, 520
    p.el(X, 0, WB, None, f'<span class="f15 b ink">{icon("user")} 受试者 S01003 · V1 筛选期</span>', '', s=2, o=3)
    p.el(X, 0, WB, None, f'<span class="f15 b ink">{icon("user")} 受试者 S01003 · V2 基线（首剂前）</span>', '', s=3, o=4)
    p.el(X, 0, WB, None, f'<span class="f15 b ink">{icon("flask")} 受试者 S01007 · V1 化验</span>', '', s=4)
    for i, (lab, th, pos, val) in enumerate([('EASI', '≥16 分', .72, '22 分'), ('IGA', '≥3 分', .64, '3 分'), ('BSA', '≥10%', .66, '12%')]):
        threshold_bar(p, X, 40 + i * 64, WB, lab, th, 'low', pos, val, s=2, o=3, d=i * 150)
    for i, (lab, th, pos, val) in enumerate([('EASI', '≥16 分', .36, '15 分'), ('IGA', '≥3 分', .64, '3 分'), ('BSA', '≥10%', .63, '11%')]):
        threshold_bar(p, X, 40 + i * 64, WB, lab, th, 'low', pos, val, s=3, o=4, d=i * 150)
    threshold_bar(p, X, 40, WB, 'ALT', '>3×ULN 排除', 'high', .74, '3.4×ULN', s=4)
    alert(p, X, 220, WB, 92, 'bad', '基线 EASI 15 分，低于 16 分', '筛选期达标不够，**基线时必须再次达标**，不符合入选 2。', s=3, o=4)
    alert(p, X, 120, WB, 92, 'warn', '允许在筛选期内复查一次', '复查仍 >3×ULN → 排除；复查须在筛选期 28 天内完成（方案 4.1）。', s=4)
    verdict_board(p, 0, 196, 540, [
        ('入选 2 · EASI', {2: ('V1 22 分 ✓', 'ok'), 3: ('基线 15 分 ✗', 'bad')}),
        ('入选 3 · IGA', {2: ('V1 3 分 ✓', 'ok'), 3: ('基线 3 分 ✓', 'ok')}),
        ('入选 4 · BSA', {2: ('V1 12% ✓', 'ok'), 3: ('基线 11% ✓', 'ok')}),
        ('排除 1 · ALT/AST', {4: ('3.4×ULN · 复查', 'warn')}),
    ])
    p.narr(0, 414, 1168, 106, [
        '先看原文：EASI 不低于 16 分、IGA 不低于 3 分、BSA 不低于 10%，三条都写着“筛选期**和基线时**”。',
        'S01003 在 V1 三项都达标，判定板上暂时全部符合。',
        '同一位受试者到基线时 EASI 降到 15 分。筛选期达标不能替代基线，这一条不符合入选 2。',
        '化验看排除 1：ALT 3.4 倍 ULN 超过 3 倍。方案允许筛选期内复查一次，复查仍超标即排除。',
    ])
    return p


def screen_cal():
    p = Page('screen_cal', '')
    D = lambda m, d: date(2026, m, d)
    cal = Calendar(p, D(11, 2), x=0, y=30, cw=78, ch=56, weeks=5, dim_month=12)
    # step 1: V1 = informed consent day
    cal.mark(D(11, 3), 'V1 · ICF', 'brand', 1, d=400)
    # step 2: screening window and the latest first dose
    cal.band(D(11, 3), D(11, 30), 'rgba(217,142,0,.45)', 2)
    cal.mark(D(12, 1), 'D1 最晚', 'ok', 2, d=400)
    p.el(0, 320, 546, None, '<span class="tag warn">筛选期 D-28～D-1：V1 在 11/03，首剂最晚 12/01</span>', '', s=2, d=500)
    # step 3: baseline diary window, 5 of 7 days scored
    cal.band(D(11, 24), D(11, 30), 'rgba(47,138,87,.55)', 3)
    for day in (24, 25, 27, 28, 30):
        cal.mark(D(11, day), '✓ NRS', 'ok', 3, o=4, d=200)
    gauge(p, 600, 186, 5, 7, OK, s=3, o=4, name='基线前 7 天 · 5 天有评分', note='≥4 天，可计算周平均', r=48)
    # step 4: only 3 days scored
    for day in (24, 28, 30):
        cal.mark(D(11, day), '✓ NRS', 'ok', 4, d=200)
    for day in (25, 26, 27, 29):
        cal.ring(D(11, day), 4)
    gauge(p, 600, 186, 3, 7, BAD, s=4, name='只有 3 天有评分', note='<4 天，不符合入选 5', r=48)
    # step 5: a re-test planned outside the window
    cal.ring(D(12, 3), 5)
    alert(p, 600, 318, 568, 80, 'bad', '复查约在 12/03', '已超出 28 天筛选期，复查结果不能用于入组判定。', s=5)
    kv_card(p, 600, 0, 568, 176, '方案规定', [('筛选期', '最长 **28 天**（D-28～D-1）'), ('日志卡', '筛选期发放，每日记录最严重瘙痒'),
                                          ('入选 5', '基线前 7 天周平均 ≥4，且 **≥4 天**有评分'), ('复查', '筛选期内允许一次')], s=1, ico='file')
    p.narr(600, 424, 568, 96, [
        '例子：受试者 11 月 3 日签署知情同意，当天就是 V1。',
        '筛选期最长 28 天，按 D-28 到 D-1 计，首剂最晚在 12 月 1 日。',
        '基线瘙痒评分取首剂前 7 天，11/24 到 11/30。这位受试者 5 天有评分，可以计算周平均。',
        '如果只有 3 天有评分，少于方案要求的 4 天，入选 5 就无法判定为符合。',
        '复查也要落在筛选期里。约在 12/03 复查，已经超出 28 天。',
    ])
    return p


PAGES = [v1_flow, incl_easi, screen_cal]
