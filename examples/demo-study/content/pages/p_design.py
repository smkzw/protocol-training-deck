"""Chapter 01: disease background as a causal chain (P1), the drug, study identity card and the whole-study timeline
(fictional DEMO-301)."""
from components import Page, icon, md, kv_card, alert, piecewise_axis, OK, BRAND
import svgart


def bg_disease():
    """P1: one column per step, the arrow arrives with the next column; the last step closes the loop and states the need."""
    p = Page('bg_disease', '')
    cols = [('皮肤屏障受损', 'shield', ['过敏原、微生物更易侵入', '激活皮肤免疫反应']),
            ('2 型炎症', 'virus', ['以 IL-X、IL-Y 为主', 'XB-101 作用在这一环（见下页）']),
            ('剧烈瘙痒', 'alert', ['炎症介质刺激感觉神经', '与湿疹样皮损同为主要表现']),
            ('搔抓', 'bolt', ['进一步破坏皮肤屏障', '回到第 1 环，形成循环'])]
    for i, (title, ico, lines) in enumerate(cols):
        x = i * 302
        body = ''.join(f'<div class="f14" style="margin-top:4px">{md(t)}</div>' for t in lines)
        p.el(x, 0, 262, 170, f'<div class="t-brand" style="font-size:calc(40px * var(--kz-un));line-height:1">{icon(ico)}</div>'
             f'<div class="f18 b ink" style="margin:10px 0 4px">{"①②③④"[i]} {title}</div>{body}',
             'pn c', style='display:flex;flex-direction:column;justify-content:center;align-items:center', s=i + 1, fx='up', d=200 if i else 0)
        if i:
            p.wire(f'M{x - 36} 85 L{x - 4} 85', 'brand', s=i + 1)
    # step 4 also closes the loop back to column 1
    p.wire('M1037 174 C 1037 250 131 250 131 178', 'brand dash', s=4, d_ms=500)
    p.wlabel(584, 254, '瘙痒—搔抓循环', s=4)
    p.node(0, 296, 740, 92, '中重度患者的治疗需求', '外用药物控制不佳时需要系统治疗；现有系统治疗存在疗效不足或长期安全性方面的顾虑', 'star', 'on', s=5)
    alert(p, 770, 296, 398, 92, 'warn', '“中重度”按评分判定', '本研究以 EASI ≥16、IGA ≥3、BSA ≥10% 界定（入选 2～4）', s=5, d=200)
    p.narr(0, 414, 1168, 106, [
        '起点是皮肤屏障受损：过敏原和微生物更容易进入皮肤，激活免疫反应。',
        '随后是以 IL-X、IL-Y 为主的 2 型炎症，XB-101 作用在这一环。',
        '炎症介质刺激感觉神经，引起剧烈瘙痒。',
        '搔抓又破坏屏障，回到第一环，形成瘙痒—搔抓循环。',
        '中重度患者外用药物控制不佳时需要系统治疗。本研究的“中重度”以入选 2～4 的评分界定。',
    ])
    return p


def bg_drug():
    """No generated image: the mechanism and the injection sites are drawn with engine/svgart.py."""
    p = Page('bg_drug', '')
    L = svgart.moa_layers(('IL-X', 'IL-Y'), 'IL-X 受体 α 亚基', 'XB-101', '人源化单抗（虚构）')
    # step 1: the disease pathway; step 2: what the drug blocks
    p.el(0, 0, 560, None, f'<span class="f15 b ink">{icon("virus")} 作用机制</span>', '', s=1)
    for key, st in (('base', 1), ('ligand', 1), ('signal', 1), ('drug', 2)):
        p.el(0, 34, 560, 323, L[key], '', s=st, fx='fade', d=0 if key != 'signal' else 400)
    p.tag(0, 368, 'IL-X 与 IL-Y 共用同一受体亚基', 'brand', s=1, o=2, d=600)
    p.tag(0, 368, '阻断受体 → 两条通路同时被抑制', 'cra', s=2, d=300)
    # step 3: how it is given
    p.el(610, 0, 558, None, f'<span class="f15 b ink">{icon("syringe")} 给药方式</span>', '', s=3)
    p.el(610, 34, 170, 357, svgart.person(zones=('abdomen', 'thigh_l', 'arm_r'), blocked=('navel',)), '', s=3, fx='fade')
    p.el(800, 40, 368, 113, svgart.pen_injector(), '', s=3, fx='left', d=200)
    kv_card(p, 800, 170, 368, 190, '规格与给药', [('规格', '300 mg / 2 mL 预充注射器'), ('首剂', '600 mg（2 支，不同部位）'),
                                                 ('之后', '300 mg，每 4 周 1 次'), ('部位', '腹部（脐周 5 cm 外）、大腿、上臂')], s=3, d=300)
    p.narr(0, 414, 1168, 106, [
        'IL-X 和 IL-Y 是两种炎症因子，结合同一个受体亚基后把炎症信号传进细胞。',
        'XB-101 是结合这个受体亚基的抗体，受体被占住后，两种因子的信号都传不进去。',
        'XB-101 皮下注射：首剂 600 mg 分两支打在不同部位，之后每 4 周 300 mg；可选腹部、大腿或上臂，避开肚脐周围。',
    ])
    return p


def study_info():
    p = Page('study_info', '')
    # step 1: full title and identifiers
    p.el(0, 0, 1168, 74, '<div class="f12 mut">方案名称</div><div class="f18 b ink" style="line-height:1.45;margin-top:2px">'
         '一项评价 XB-101 注射液治疗成人中重度特应性皮炎有效性和安全性的多中心、随机、双盲、安慰剂对照Ⅲ期研究</div>',
         'pn tint', style='padding:8px 16px', s=1, fx='up')
    for i, (a, b) in enumerate([('方案编号', 'DEMO-301'), ('方案版本', 'V1.0 · 2026 年 6 月 1 日'), ('申办者', '示例生物医药有限公司')]):
        p.el(i * 396, 84, 376, 40, f'<span class="f12 mut">{a}</span>　<span class="f14 b ink num">{b}</span>', 'pn flat',
             style='display:flex;align-items:center;padding:4px 14px', s=1, fx='left', d=200 + i * 150)
    # step 2: nature and size
    facts = [('试验分期', 'Ⅲ期'), ('研究设计', '多中心 · 随机 · 双盲 · 安慰剂对照'), ('计划入组', '240 例（2:1 随机）'),
             ('试验药物', 'XB-101 首剂 600 mg，之后 300 mg Q4W'), ('给药途径', '皮下注射，共 4 次'), ('研究周期', '每例最长约 32 周')]
    for i, (a, b) in enumerate(facts):
        p.el((i % 3) * 396, 142 + (i // 3) * 62, 376, 54, f'<div class="f12 mut">{a}</div><div class="f15 b ink">{b}</div>', 'pn flat',
             style='padding:6px 14px', s=2, fx='left', d=(i % 3) * 120 + (i // 3) * 200)
    # step 3: the two arms, drawn to scale
    p.el(0, 280, 300, None, f'<span class="f15 b ink">{icon("users")} 分组与样本量</span>', '', s=3)
    for i, (name, n, col) in enumerate([('XB-101 组', 160, 'rgba(255,153,0,.30)'), ('安慰剂组', 80, 'rgba(15,17,21,.08)')]):
        p.el(0, 312 + i * 44, 130, None, f'<span class="f13 b ink">{name}</span>', '', s=3, d=i * 200)
        p.el(140, 308 + i * 44, n * 3.4, 34, f'<span class="f14 b ink num">{n} 例</span>', 'bar', style=f'background:{col}', s=3, fx='wipe', d=i * 200)
    kv_card(p, 760, 280, 408, 112, '主要终点', [('时间点', '**W16**（V7）'), ('指标', 'EASI-75 应答率')], s=3, ico='star', d=300)
    p.narr(0, 414, 1168, 106, [
        '本研究是 XB-101 治疗成人中重度特应性皮炎的Ⅲ期研究，方案编号 DEMO-301，现行版本 V1.0。',
        '设计为多中心、随机、双盲、安慰剂对照。计划入组 240 例，首剂 600 mg，之后每 4 周 300 mg，皮下注射共 4 次；每例最长约 32 周。',
        '按 2:1 随机，XB-101 组 160 例、安慰剂组 80 例。主要终点在 W16，也就是 V7。',
    ])
    return p


def overview():
    p = Page('overview', '')
    X = piecewise_axis([(-4, 0, 40, 220), (0, 16, 220, 820), (16, 28, 820, 1128)])
    phases = [('筛选期', -4, 0, 'rgba(255,204,0,.22)', '≤28 天'), ('双盲治疗期', 0, 16, 'rgba(255,153,0,.16)', 'W0～W16'),
              ('安全性随访期', 16, 28, 'rgba(15,17,21,.06)', 'W16～W28')]
    # step 1: phases and the week axis
    for i, (n, a, b, c, sub) in enumerate(phases):
        p.el(X(a), 0, X(b) - X(a) - 3, 46, f'<div class="b ink f14 nw">{n}</div><div class="f12 mut nw">{sub}</div>', 'band',
             style=f'background:{c};padding:4px 8px', s=1, fx='wipe', d=i * 120)
    p.el(40, 70, 1088, 2, '', '', style='background:#CFC7BA', s=1, fx='wipe')
    for w in (-4, 0, 4, 8, 12, 16, 28):
        p.el(X(w) - 20, 76, 40, None, f'W{w}', 'f12 mut c num', s=1)
    # step 2: visits
    visits = [('V1', -3), ('V2', 0), ('V3', 2), ('V4', 4), ('V5', 8), ('V6', 12), ('V7', 16), ('V8', 28)]
    for i, (v, w) in enumerate(visits):
        big = v in ('V1', 'V2', 'V7')
        sz = 14 if big else 10
        p.el(X(w) - sz / 2, 71 - sz / 2, sz, sz, '', 'dot', style=f'background:{BRAND if big else "#fff"};border:2px solid {"#fff" if big else "#B0A797"}',
             s=2, fx='pop', d=i * 60)
        p.el(X(w) - 22, 96, 44, None, v, 'f12 c num ' + ('b ink' if big else 'mut'), s=2, d=i * 60)
    # step 3: dosing row
    p.text(0, 138, 40, '给药', 'f12 mut', s=3)
    for i, (w, n) in enumerate([(0, 2), (4, 1), (8, 1), (12, 1)]):
        p.el(X(w) - 13, 128, 26, 34, f'{icon("syringe")}<div class="f12 b num">{n}</div>', 'c', style=f'color:{"#C25E00" if n == 2 else "#8A8F96"}',
             s=3, fx='drop', d=i * 120)
    p.tag(X(0) + 20, 168, '首剂 600 mg（2 支）', 'brand', s=3, d=500)
    p.tag(X(16) - 60, 134, 'W16 不给药', 'bad', s=3, d=600)
    # step 4: assessments that drive site resources
    p.text(0, 212, 40, 'PK', 'f12 mut', s=4)
    for w in (0, 4, 12, 16):
        p.el(X(w) - 18, 208, 36, 22, 'PK', 'bar cra', style='justify-content:center', s=4, fx='pop')
    p.text(0, 244, 40, '评估', 'f12 mut', s=4)
    p.el(X(-3), 240, X(28) - X(-3), 22, 'EASI · IGA · BSA：V3 以外的每次访视', 'bar yel', s=4, fx='wipe', d=200)
    kpis = [('8', '次访视'), ('4', '次给药'), ('W16', '主要终点'), ('±3 天', 'V3～V7 窗口')]
    for i, (a, b) in enumerate(kpis):
        p.el(i * 292, 290, 276, 92, f'<div class="f28 b ink num">{a}</div><div class="f13 mut">{b}</div>', 'pn flat',
             style='display:flex;flex-direction:column;justify-content:center;padding:6px 16px', s=4, fx='up', d=400 + i * 120)
    p.narr(0, 414, 1168, 106, [
        '研究分三段：筛选期最长 28 天，16 周双盲治疗期，12 周安全性随访期。',
        '全程 8 次访视。橙色大点是项目最多的 3 次：V1 筛选、V2 基线首剂、V7 主要终点。',
        '共给药 4 次：V2 首剂 600 mg、两支，V4、V5、V6 各一支；V3 和 V7 不给药。',
        'PK 在 V2、V4、V6、V7 采集；EASI、IGA、BSA 除 V3 外每次评估。所有窗口都从 D1 推算，V3 到 V7 为正负 3 天。',
    ])
    return p


PAGES = [bg_disease, bg_drug, study_info, overview]
