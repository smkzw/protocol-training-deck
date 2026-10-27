"""Chapter 02: the diary card drawn as the real form and filled cell by cell (P16), then the baseline weekly mean worked
as a calculator (P10). Both use the same participant and the same seven days as screen_cal."""
from components import Page, icon, md, Verbatim, quote_card, kv_card, alert

q = Verbatim('src/protocol.md')
DATES = ['11/24', '11/25', '11/26', '11/27', '11/28', '11/29', '11/30']


def diary_form():
    p = Page('diary_form', '')
    COLS, TOP, RH = [16, 116, 266, 386, 584], 100, 38
    p.el(0, 0, 600, 400, f'<div class="dh">{icon("diary")}瘙痒日志卡（示例）</div><div class="f12">受试者编号 S01003 · 每日睡前记录过去 24 小时最严重瘙痒（0～10 的整数）</div>',
         'doc', s=1, fx='fade')
    # step 1: the form's own grid — header row + 7 days
    for y in [64, TOP] + [TOP + (i + 1) * RH for i in range(7)]:
        p.el(16, y, 568, 1, '', '', style='background:#DED7CC', s=1)
    for x in COLS:
        p.el(x, 64, 1, TOP + 7 * RH - 64, '', '', style='background:#DED7CC', s=1)
    for c, h in enumerate(['日期', '瘙痒评分', '记录时间', '备注']):
        p.el(COLS[c] + 8, 72, COLS[c + 1] - COLS[c] - 16, None, h, 'f13 b ink', s=1)
    for i, d in enumerate(DATES):
        p.el(COLS[0] + 8, TOP + i * RH + 9, 84, None, d, 'f13 num', s=1)
    cell = lambda c, i, html, st, o=None, cls='f14 num ink': p.el(COLS[c] + 8, TOP + i * RH + 8, COLS[c + 1] - COLS[c] - 16, None, html, cls, s=st, o=o)
    row = lambda i: (16, TOP + i * RH + 2, 568, RH - 4)
    # step 2: two ordinary days
    cell(1, 0, '5', 2); cell(2, 0, '21:30', 2)
    cell(1, 1, '6', 2); cell(2, 1, '22:05', 2)
    # step 3: 11/26 back-filled the next day (wrong) → step 4: left blank with a reason
    cell(1, 2, '4', 3, 4); cell(3, 2, '11/27 补填', 3, 4, 'f13 t-bad')
    p.ring(*row(2), 'bad', s=3, o=4)
    cell(3, 2, '漏记：当晚忘记记录', 4, cls='f13')
    cell(1, 3, '4', 4); cell(2, 3, '21:40', 4)
    # step 5: a correction made the way 4.3 describes
    cell(1, 4, '<span style="text-decoration:line-through;text-decoration-thickness:2px;color:#5B6068">7</span>　4', 5); cell(2, 4, '21:50', 5)
    cell(3, 4, '更正 ZW 11/28', 5, cls='f13')
    p.ring(*row(4), 'ok', s=5, o=6)
    # step 6: the rest of the week and the check at the next visit
    cell(3, 5, '漏记：外出', 6, cls='f13')
    cell(1, 6, '7', 6); cell(2, 6, '21:15', 6)
    p.el(16, 372, 568, None, '研究者核对：李医生　12/1（V2）', 'f13 ink', s=6)
    kv_card(p, 630, 0, 538, 214, '方案 4.3 · 日志卡', [('记录', '每日睡前，过去 24 小时最严重瘙痒，0～10 整数'), ('漏记', '**保持空白**，不得补填，备注可写原因'),
                                                      ('更正', '原值**划一横线**，旁写正确值，签缩写和日期'), ('回收', '研究者每次访视回收并核对')],
            s=1, ico='file', label_w='3.5em')
    alert(p, 630, 230, 538, 170, 'bad', '11/26 漏记，第二天回忆补填', '方案规定漏记的日期保持空白，不得事后补填。', s=3, o=4)
    alert(p, 630, 230, 538, 170, 'ok', '漏记的日期保持空白', '分数格留空，备注栏写明原因。', s=4, o=5)
    alert(p, 630, 230, 538, 170, 'ok', '划一横线，旁写正确值', '签姓名缩写和日期；不涂抹，不用修正液。', s=5, o=6)
    alert(p, 630, 230, 538, 170, 'ok', '回收时核对：5 天有评分', '11/24、25、27、28、30 有评分，满足入选 5 的“至少 4 天”。', s=6)
    p.narr(0, 414, 1168, 106, [
        '日志卡按天一行：日期、瘙痒评分、记录时间、备注。受试者每天睡前记录过去 24 小时最严重的瘙痒。',
        '正常的两天：11/24 记 5 分，11/25 记 6 分，都写了记录时间。',
        '反例：11/26 忘了记，第二天凭回忆补了 4 分。方案规定漏记的日期保持空白，不得补填。',
        '正确做法：11/26 的分数格留空，备注写明原因；11/27 照常记录。',
        '11/28 先写了 7，发现写错。原值划一横线，旁边写 4，签姓名缩写和日期。',
        'V2 时研究者回收并核对：这一周 5 天有评分，满足至少 4 天的要求。',
    ])
    return p


def nrs_calc():
    p = Page('nrs_calc', '')
    A = ['5', '6', '—', '4', '4', '—', '7']   # S01003, same week as diary_form: 26 ÷ 5 = 5.2
    B = ['3', '4', '—', '3', '—', '—', '5']   # another participant: 15 ÷ 4 = 3.75
    C = ['4', '4', '3', '5', '—', '—', '4']   # boundary: 20 ÷ 5 = 4.0
    # step 1: the inputs
    p.el(0, 0, 1168, 146, '', 'pn', s=1, fx='up')
    p.el(18, 12, 900, None, f'<span class="f15 b ink">{icon("diary")} S01003 · 基线前 7 天（11/24～11/30）每日最严重瘙痒评分</span>', '', s=1,
         k={5: {'html': f'<span class="f15 b ink">{icon("diary")} S01012 · 另一位受试者的基线前 7 天</span>'},
            6: {'html': f'<span class="f15 b ink">{icon("diary")} S01015 · 恰好落在阈值上的一周</span>'}})
    miss = lambda v: 'mut' if v == '—' else ''
    for i, d in enumerate(DATES):
        x = 18 + i * 162
        p.el(x, 48, 140, 86, '', 'pn flat', s=1, d=i * 80)
        p.el(x, 54, 140, None, d, 'f12 mut c num', s=1, d=i * 80)
        p.el(x, 76, 140, None, A[i], 'f28 b c num', s=1, d=i * 80,
             k={1: {'c': miss(A[i])}, 5: {'t': B[i], 'c': miss(B[i])}, 6: {'t': C[i], 'c': miss(C[i])}})
    # step 2: the formula; values roll with the inputs
    boxes = [(0, 300, '有评分各日之和', {2: [0, 26, 0], 5: [26, 15, 0], 6: [15, 20, 0]}, None),
             (360, 240, '有评分的天数', {2: [0, 5, 0], 4: [5, 7, 0], 5: [7, 4, 0], 6: [4, 5, 0]}, {4: {'c': 't-bad'}, 5: {'c': ''}}),
             (660, 240, '周平均', {3: [0, 5.2, 1], 4: [5.2, 3.71, 2], 5: [3.71, 3.75, 2], 6: [3.75, 4.0, 1]}, {4: {'c': 't-bad'}, 6: {'c': ''}})]
    for x, w, label, count, k in boxes:
        p.el(x, 166, w, 96, f'<div class="f13 mut c">{label}</div>', 'pn flat', style='display:block;padding:8px', s=2)
        p.el(x, 196, w, None, '?', 'f32 b c num ink', s=2, count=count, k=k)
    p.el(304, 188, 52, None, '÷', 'f28 mut c', s=2)
    p.el(604, 188, 52, None, '=', 'f28 mut c', s=2)
    # steps 3–6: the verdict, one per input set
    p.el(930, 166, 238, 96, '', 'pn flat', s=3)
    for st, kind, text in [(3, 'ok', '5.2 ≥ 4，5 天有评分\n**符合入选 5**'), (4, 'bad', '3.71 < 4\n**误判为不符合**'),
                           (5, 'bad', '3.75 < 4\n**不符合入选 5**'), (6, 'ok', '4.0 = 4\n**符合（≥4 分）**')]:
        p.stamp(946, 190, 48, kind, s=st, o=st + 1 if st < 6 else None)
        p.text(1006, 184, 156, text, 'f14 lh15', s=st, o=st + 1 if st < 6 else None)
    i5 = q('基线前7天每日最严重瘙痒数字评分（NRS）的周平均值≥4分，且7天中至少4天有评分。')
    avg = q('周平均值为7天中有评分各日的评分之和除以有评分的天数。')
    quote_card(p, 0, 282, 560, 120, '入选 5 与周平均 · 方案 3.5.1、5.1',
               i5.replace('≥4分', '__≥4分__').replace('至少4天', '__至少4天__') + '\n' + avg.replace('除以有评分的天数', '__除以有评分的天数__'), s=1)
    alert(p, 600, 282, 568, 120, 'bad', '反例：除以 7 天', '26 ÷ 7 = 3.71，会把符合的受试者误判为不符合。周平均只除以有评分的天数。', s=4, o=5)
    alert(p, 600, 282, 568, 120, 'bad', '15 ÷ 4 = 3.75', '有评分的天数够 4 天，但周平均低于 4 分，不符合入选 5。', s=5, o=6)
    alert(p, 600, 282, 568, 120, 'ok', '恰好 4.0 分', '原文是“≥4分”，等于 4 分符合。', s=6)
    p.narr(0, 414, 1168, 106, [
        '还是 S01003 那一周：5 天有评分，11/26 和 11/29 空白。',
        '周平均的算法在方案 5.1：有评分各日的分数加起来，除以有评分的天数。',
        '26 除以 5 等于 5.2，不低于 4 分，且 5 天有评分，符合入选 5。',
        '反例：除以 7 天得到 3.71，把一个符合的受试者误判为不符合。',
        '另一位受试者 4 天有评分，合计 15 分，周平均 3.75，不到 4 分，不符合。',
        '边界情况：合计 20 分、5 天有评分，周平均正好 4.0。原文是“大于或等于 4 分”，符合。',
    ])
    return p


PAGES = [diary_form, nrs_calc]
