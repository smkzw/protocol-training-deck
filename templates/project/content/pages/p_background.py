"""Chapter 01 starter page (pattern P2). Replace the STUDY values with facts from plan/facts.md, then add the other
chapter-01 pages (F01 bg_disease, F02 bg_drug, F04 picos, …) as functions in this module and list them in PAGES."""
from components import Page, icon, kv_card

STUDY = {
    'title': '【方案完整题目】',
    'ids': [('方案编号', '【编号】'), ('方案版本', '【版本 · 日期】'), ('申办者', '【申办者】')],
    'facts': [('试验分期', '【Ⅲ期】'), ('研究设计', '【多中心 · 随机 · 双盲 · 安慰剂对照】'), ('计划入组', '【N 例（比例）】'),
              ('组长单位', '【组长单位】'), ('主要研究者', '【PI】'), ('研究周期', '【每例最长约 W 周】')],
    'arms': [('【试验组】', 160, 'rgba(255,153,0,.30)'), ('【对照组】', 80, 'rgba(15,17,21,.08)')],   # (name, n, colour)
    'primary': [('时间点', '**【Wxx】**（【Vx】）'), ('指标', '【主要终点】')],
}


def study_info():
    p = Page('study_info', '')
    # step 1: full title and identifiers
    p.el(0, 0, 1168, 74, f'<div class="f12 mut">方案名称</div><div class="f18 b ink" style="line-height:1.45;margin-top:2px">{STUDY["title"]}</div>',
         'pn tint', style='padding:8px 16px', s=1)
    for i, (a, b) in enumerate(STUDY['ids']):
        p.el(i * 396, 84, 376, 40, f'<span class="f12 mut">{a}</span>　<span class="f14 b ink num">{b}</span>', 'pn flat',
             style='display:flex;align-items:center;padding:4px 14px', s=1, fx='left', d=200 + i * 150)
    # step 2: nature and size
    for i, (a, b) in enumerate(STUDY['facts']):
        p.el((i % 3) * 396, 142 + (i // 3) * 62, 376, 54, f'<div class="f12 mut">{a}</div><div class="f15 b ink">{b}</div>', 'pn flat',
             style='padding:6px 14px', s=2, fx='left', d=(i % 3) * 120 + (i // 3) * 200)
    # step 3: the arms drawn to scale (longest bar = 560 units), then the primary endpoint
    top = max(n for _, n, _ in STUDY['arms'])
    p.el(0, 280, 300, None, f'<span class="f15 b ink">{icon("users")} 分组与样本量</span>', '', s=3)
    for i, (name, n, col) in enumerate(STUDY['arms']):
        p.el(0, 312 + i * 44, 130, None, f'<span class="f13 b ink">{name}</span>', '', s=3, d=i * 200)
        p.el(140, 308 + i * 44, 560 * n / top, 34, f'<span class="f14 b ink num">{n} 例</span>', 'bar', style=f'background:{col}', s=3, fx='wipe', d=i * 200)
    kv_card(p, 760, 280, 408, 112, '主要终点', STUDY['primary'], s=3, ico='star', d=300)
    p.narr(0, 414, 1168, 106, ['【第 1 步旁白，一句】', '【第 2 步旁白，一句】', '【第 3 步旁白，一句】'])
    return p


PAGES = [study_info]
