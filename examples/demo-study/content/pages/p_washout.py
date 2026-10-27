"""Chapter 02: washout clauses read line by line (P7 text / reading) and the same clauses worked on a countdown axis (P8)."""
from datetime import date, timedelta
from components import Page, icon, md, Verbatim, quote_card, kv_card, alert, day_axis, BRAND

q = Verbatim('src/protocol.md')


def excl_prior():
    p = Page('excl_prior', '')
    # step 1: the three protocol sentences, left column
    e2 = q('基线前4周内使用过系统性免疫抑制剂或系统性糖皮质激素。')
    e3 = q('基线前8周或5个半衰期内（以时间较长者为准）使用过任何生物制剂。')
    t0 = q('基线访视（V2）即首次给药日（D1），排除标准中的“基线前”均自D1起倒推。')
    Y = [(0, 112), (130, 124), (272, 112)]
    quote_card(p, 0, Y[0][0], 540, Y[0][1], '排除 2 · 方案 3.5.2', '2. ' + e2.replace('基线前4周内', '__基线前4周内__').replace('系统性免疫', '__系统性__免疫', 1), s=1)
    quote_card(p, 0, Y[1][0], 540, Y[1][1], '排除 3 · 方案 3.5.2', '3. ' + e3.replace('8周或5个半衰期内（以时间较长者为准）', '__8周或5个半衰期内（以时间较长者为准）__'), s=1, d=150)
    quote_card(p, 0, Y[2][0], 540, Y[2][1], '起算点 · 方案 4.2', t0.replace('首次给药日（D1）', '__首次给药日（D1）__'), s=1, d=300)
    # steps 2–4: one reading per sentence, joined to its source by a line
    rows = [('pill', '系统性免疫抑制剂、系统性糖皮质激素', '末次用药须在 D1 前 **4 周（28 天）**以外', ['4 周', '起算点 D1']),
            ('syringe', '任何生物制剂', '8 周与 5 个半衰期，**取较长者**', ['8 周 = 56 天', '5 × 半衰期']),
            ('calendar', '起算点是 D1（首剂日）', '不是 V1，也不是签署知情同意书的日期', ['D1 = V2'])]
    for i, ((y, h), (ico, head, line, tags)) in enumerate(zip(Y, rows)):
        tag_html = '<div>' + ''.join(f'<span class="tag {"warn" if i == 2 else "brand"}" style="margin-right:6px">{md(t)}</span>' for t in tags) + '</div>'
        p.el(600, y, 568, h, f'<div class="f15 b ink">{icon(ico)} {md(head)}</div><div class="f14" style="margin:6px 0 8px">{md(line)}</div>{tag_html}',
             'pn flat' if i < 2 else 'pn tone', style='display:flex;flex-direction:column;justify-content:center;padding:0 calc(16 * var(--kz-u))'
             + (';--tone:#D98E00' if i == 2 else ''), s=i + 2, fx='left')
        p.wire(f'M544 {y + h / 2:.0f} L596 {y + h / 2:.0f}', 'brand', s=i + 2)
    # step 5: the phrase most often misread, over the biologics row
    alert(p, 600, Y[1][0], 568, Y[1][1], 'warn', '“以时间较长者为准”',
          '半衰期 14 天的药物：5 个半衰期 = 70 天，长于 8 周，按 70 天算；只看 8 周会把洗脱期算短。', s=5)
    p.narr(0, 404, 1168, 116, [
        '洗脱期涉及方案的三句话：排除 2、排除 3，以及 4.2 对“基线前”起算点的规定。',
        '排除 2：系统性免疫抑制剂和系统性糖皮质激素，末次用药要在 D1 前 4 周以外。',
        '排除 3：任何生物制剂，看 8 周和 5 个半衰期两个时长，取较长的那个。',
        '起算点是 D1，也就是首剂日，不是 V1，也不是签署知情同意书的那天。',
        '容易读错的是“以时间较长者为准”：5 个半衰期长于 8 周时，按 5 个半衰期算。',
    ])
    return p


def washout_calc():
    p = Page('washout_calc', '')
    D1, LAST = date(2026, 12, 1), date(2026, 12, 8)     # planned first dose; latest first dose (V1 11/10 + 28 days)
    L, R = 200, 1128
    X0 = day_axis(L, R, -77, 11)
    X = lambda d: X0((d - D1).days)
    md_ = lambda d: f'{d.month}/{d.day}'
    # step 1: the date axis, the planned D1 and the end of screening
    p.el(L, 30, R - L, 2, '', '', style='background:#CFC7BA', s=1, fx='wipe')
    for d in (date(2026, 9, 15), date(2026, 10, 1), date(2026, 10, 15), date(2026, 11, 1), date(2026, 11, 15)):
        p.el(X(d) - 22, 6, 44, None, md_(d), 'f12 mut c num', s=1)
    p.el(X(D1) - 1, 24, 3, 232, '', '', style=f'background:{BRAND}', s=1, k={5: {'x': X(date(2026, 12, 4)) - 1}})
    p.el(X(D1) - 150, 0, 146, None, '<span class="tag brand">计划 D1 12/1</span>', 'r', s=1, o=5)
    p.el(X(date(2026, 12, 4)) - 150, 0, 146, None, '<span class="tag ok">D1 改为 12/4</span>', 'r', s=5)
    p.el(X(LAST) - 1, 24, 2, 232, '', '', style='border-left:2px dashed #8A8F96', s=1)
    p.el(X(LAST) + 4, 236, 70, None, '<span class="f12 mut">筛选期<br>最晚 12/8</span>', '', s=1)
    # steps 2–4: one row per drug; the bar runs from the last dose to the earliest D1 it allows
    rows = [('泼尼松（口服）', '系统性糖皮质激素 · 末次 10/20', date(2026, 10, 20), 28, '28 天'),
            ('甲氨蝶呤', '系统性免疫抑制剂 · 末次 11/6', date(2026, 11, 6), 28, '28 天'),
            ('生物制剂 Y', '半衰期 14 天（示例值）· 末次 9/20', date(2026, 9, 20), 70, '5 × 14 = 70 天')]
    for i, (name, sub, last, days, lab) in enumerate(rows):
        y, st = 52 + i * 66, i + 2
        end = last + timedelta(days)
        p.el(0, y + 4, 190, None, f'<div class="f14 b ink">{name}</div><div class="f12 mut">{sub}</div>', '', s=st)
        p.el(X(last) - 6, y + 16, 12, 12, '', 'dot', style='background:#5B6068;border-radius:50%', s=st, fx='pop')
        if i == 2:   # the 8-week reading, drawn first so the longer bar visibly runs past it
            p.el(X(last), y + 10, X(last + timedelta(56)) - X(last), 24, '8 周止于 11/15', 'bar grey', style='border:1.5px dashed #8A8F96', s=st, fx='wipe')
        k = {3: {'c': 'bad'}, 5: {'c': 'ok'}} if i == 1 else None
        p.el(X(last), y + 10 + (26 if i == 2 else 0), X(end) - X(last), 24, f'{lab} → {md_(end)}', 'bar ' + ('' if i == 1 else 'ok'), s=st, fx='wipe',
             d=500 if i == 2 else 0, k=k)
        p.stamp(1136, y + 8, 28, 'bad' if i == 1 else 'ok', s=st, o=5 if i == 1 else None, d=700)
    p.stamp(1136, 52 + 66 + 8, 28, 'ok', s=5, d=300)
    kv_card(p, 0, 278, 540, 116, '方案规定', [('排除 2', '系统性免疫抑制剂、糖皮质激素 **≥4 周**'), ('排除 3', '生物制剂 8 周或 5 个半衰期，**取较长**'),
                                             ('起算点', 'D1（首剂日）')], s=1, ico='file', label_w='4.5em')
    alert(p, 580, 278, 588, 116, 'ok', '泼尼松：10/20 + 28 天 = 11/17', '早于计划 D1 12/1，符合排除 2 的要求。', s=2, o=3)
    alert(p, 580, 278, 588, 116, 'bad', '甲氨蝶呤差 3 天', '11/6 + 28 天 = 12/4，晚于计划 D1 12/1；按 12/1 首剂不符合排除 2。', s=3, o=4)
    alert(p, 580, 278, 588, 116, 'ok', '生物制剂按 70 天算', '5 个半衰期 70 天长于 8 周，最早 D1 为 11/29。半衰期以该药说明书为准，此处为示例值。', s=4, o=5)
    alert(p, 580, 278, 588, 116, 'ok', '取最晚的日期：12/4', 'D1 改到 12/4，三种药物都满足，且仍在筛选期内（最晚 12/8）。', s=5)
    p.narr(0, 414, 1168, 106, [
        '受试者 S01009 在 11/10 完成 V1，计划 12/1 首剂；筛选期最长 28 天，首剂最晚 12/8。',
        '泼尼松属于系统性糖皮质激素，末次 10/20，加 28 天是 11/17，早于 D1，符合。',
        '甲氨蝶呤末次 11/6，加 28 天是 12/4，比计划 D1 晚 3 天。按 12/1 首剂，不符合排除 2。',
        '生物制剂取 8 周和 5 个半衰期中较长的一个。半衰期 14 天时是 70 天，最早 D1 为 11/29。',
        '几种药物同时存在时，取最晚的日期。D1 改到 12/4，三种药物都满足，仍在筛选期内。',
    ])
    return p


PAGES = [excl_prior, washout_calc]
