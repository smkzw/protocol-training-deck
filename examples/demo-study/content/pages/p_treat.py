"""Chapter 03: one dosing visit (checklist ticked in step with a demo that contains a trap) and the dosing-day timeline."""
from components import (Page, icon, md, A, visit_checklist, tube_html, alert, time_axis, OK, BAD, BRAND)
from meta import DAY          # the one fictional D1 of the deck (content/meta.py)


def v4():
    p = Page('v4', '')
    visit_checklist(p, 'V4 清单', '按方案流程表；日期按 D1 = 12/01 举例', [
        ('给药前', [('核对访视窗口 D26～D32', 1), ('EASI · IGA · BSA 评估', 2), ('血常规、血生化采血', 2),
                   ('PK 血样：给药前 1 小时内', {3: 'fail', 4: 'done'})]),
        ('给药与留观', [('皮下注射 300 mg（1 支）', 5), ('留观至少 30 分钟', 5)]),
        ('收尾', [('预约 V5 · W8', 5)]),
    ])
    R = 400
    # step 1: the window on real dates
    p.el(R, 0, 768, None, f'<span class="f15 b ink">{icon("calendar")} 访视窗口：D29 ± 3</span>', '', s=1)
    for i, n in enumerate(range(25, 34)):
        inwin = 26 <= n <= 32
        cls = 'tag ok' if n == 29 else ('tag' if inwin else 'tag bad')
        p.el(R + i * 84, 32, 78, 50, f'<div class="f12 b num">D{n}</div><div class="f12 num">{DAY(n)}</div>', 'pn flat c',
             style=f'padding:4px;{"" if inwin else "filter:opacity(.45)"}', s=1, fx='up', d=i * 50)
    p.el(R + 84, 88, 7 * 84 - 6, 8, '', 'band', style='background:rgba(47,138,87,.55)', s=1, fx='wipe', d=500)
    # step 2: tube rack for this visit
    p.el(R, 112, 360, None, f'<span class="f15 b ink">{icon("tube")} 本次采血</span>', '', s=2)
    tubes = [('#8E5BB5', 'rgba(192,0,0,.45)', '血常规', ''), ('#E2B300', 'rgba(192,0,0,.4)', '血生化', ''), ('#C9302C', 'rgba(192,0,0,.4)', 'PK', '给药前')]
    p.el(R, 144, 360, 112, ''.join(tube_html(*t) for t in tubes), 'pn flat', style='display:flex;justify-content:space-around;align-items:center', s=2, fx='up')
    # steps 3–4: the trap and the fix, on the same spot
    alert(p, R + 380, 112, 388, 144, 'bad', 'PK 在给药后 20 分钟才采', '时间点不符合“给药前 1 小时内”，该 PK 样本不符合方案要求，按偏离记录。', s=3, o=4)
    alert(p, R + 380, 112, 388, 144, 'ok', 'PK 08:50 采集，09:30 给药', '采血到给药 40 分钟，在给药前 1 小时内。', s=4)
    p.ring(R + 4, 140, 116, 120, 'bad', s=3, o=4)
    # step 5: dosing, observation and the next window
    ring = ('<svg viewBox="0 0 120 120" style="width:100%;height:100%"><circle cx="60" cy="60" r="48" stroke="#EFE7DB"/>'
            '<circle class="fg" cx="60" cy="60" r="48" pathLength="100" transform="rotate(-90 60 60)"/></svg>')
    p.el(R, 290, 130, 130, ring, 'tmr', s=5, fx='pop', k={5: {'c': 'full'}})
    p.el(R, 340, 130, None, '<div class="f20 b num c">30′</div>', '', s=5, d=300)
    p.el(R + 150, 290, 618, 110, f'<div class="f13 b ink">{icon("calendar")} 下次 V5 · W8 · D57 ± 3</div><div class="f13" style="margin-top:4px">举例 <b class="num">{DAY.window(57, 3)}</b>，仍按 D1 推算，不随本次实际日期顺延。</div>',
         'pn tint', s=5, fx='up', d=300)
    p.narr(R + 150, 424, 618, 100, [
        'V4 的目标日是 D29，窗口正负 3 天，按 D1 等于 12 月 1 日举例就是 12/26 到 01/01。',
        '本次采三管血：血常规、血生化和 PK。PK 只能在给药前 1 小时内采。',
        '反例：先给药、给药后 20 分钟才采 PK。时间点不符合方案，清单上这一项是红叉。',
        '正确做法：08:50 采 PK，09:30 给药，间隔 40 分钟。',
        '给药后留观至少 30 分钟。下次 V5 仍按 D1 推算窗口。',
    ])
    return p


def dose_day():
    p = Page('dose_day', '')
    L, R = 150, 1150
    T = time_axis(p, L, R, 0, 8, 12, s=1)
    lanes = [('到达 · 生命体征', 'clock'), ('疗效评估', 'clipboard'), ('采血（含 PK）', 'tube'), ('给药与留观', 'syringe')]
    LY = [34, 82, 130, 178]
    for (t, ic), y in zip(lanes, LY):
        p.el(0, y + 6, 140, None, f'<span class="f13 b ink">{icon(ic)} {t}</span>', '', s=1)
        p.el(L, y, R - L, 36, '', '', style='border-bottom:1px dashed #E6DFD3', s=1)
    # step 1: dosing time and the PK window derived from it
    p.el(T(8, 30), 128, T(9, 30) - T(8, 30), 40, '', '', style='background:rgba(47,138,87,.10);border:1.5px dashed #2F8A57;border-radius:8px', s=1, fx='fade',
         k={3: {'x': T(9, 45), 'w': T(10, 45) - T(9, 45)}, 4: {'x': T(8, 30), 'w': T(9, 30) - T(8, 30)}})
    p.el(T(9, 30) - 1, 24, 3, 200, '', '', style=f'background:{BRAND}', s=1, k={3: {'x': T(10, 45) - 1}, 4: {'x': T(9, 30) - 1}})
    p.el(T(9, 30) + 6, 220, 220, None, '<span class="tag brand">给药 09:30</span>', '', s=1, o=3)
    p.el(T(10, 45) + 6, 220, 220, None, '<span class="tag bad">给药推迟到 10:45</span>', '', s=3, o=4)
    p.el(T(9, 30) + 6, 220, 220, None, '<span class="tag brand">给药 09:30</span>', '', s=4)
    # step 2: the normal day
    p.el(T(8, 10), LY[0] + 4, T(8, 25) - T(8, 10), 28, '', 'bar grey', s=2, fx='left')
    p.el(T(8, 25), LY[1] + 4, T(8, 50) - T(8, 25), 28, '', 'bar yel', s=2, fx='left', d=150)
    p.el(T(8, 50), LY[2] + 4, T(9, 5) - T(8, 50), 28, 'PK', 'bar cra', style='justify-content:center', s=2, fx='left', d=300, k={3: {'c': 'err'}, 4: {'c': ''}})
    p.el(T(9, 30), LY[3] + 4, T(10, 0) - T(9, 30), 28, '留观 30′', 'bar ok', style='justify-content:center', s=2, fx='left', d=450,
         k={3: {'x': T(10, 45)}, 4: {'x': T(9, 30), 'w': T(9, 45) - T(9, 30), 'c': 'err', 't': '15′'}, 5: {'x': T(9, 30), 'w': T(10, 0) - T(9, 30), 'c': '', 't': '留观 30′'}})
    # step 3/4 captions
    alert(p, 520, 262, 648, 104, 'bad', '给药推迟后，08:50 的 PK 已在给药前 1 小时 55 分', '不在“给药前 1 小时内”，该 PK 时间点不符合方案。', s=3, o=4)
    alert(p, 520, 262, 648, 104, 'bad', '留观 15 分钟即离院', '方案要求给药后在研究中心留观**至少 30 分钟**。', s=4, o=5)
    alert(p, 520, 262, 648, 104, 'ok', '回到正常安排', 'PK 在给药前 1 小时内，留观满 30 分钟。', s=5)
    p.checklist(0, 250, 500, 154, [('方案规定', [('PK 血样：给药前 1 小时内', 2), ('给药后留观至少 30 分钟', 2), ('窗口按 D1 推算，V3～V7 ±3 天', 5)])], '给药日要点')
    p.narr(520, 404, 648, 120, [
        '先定给药时刻。给药定在 09:30，PK 采血窗口就是 08:30 到 09:30。',
        '正常的一天：生命体征、疗效评估、采血，08:50 采 PK，09:30 给药，之后留观 30 分钟。',
        '反例一：给药推迟到 10:45，窗口跟着后移，08:50 采的 PK 就落到了窗口外。',
        '反例二：留观 15 分钟就离院，不满足至少 30 分钟。',
        '回到正常安排：所有给药前操作都围绕给药时刻排。',
    ])
    return p


PAGES = [v4, dose_day]
