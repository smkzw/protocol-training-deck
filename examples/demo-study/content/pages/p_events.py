"""Chapter 04: concomitant medication classes (P18 drop-in chips), the AE judgement funnel (P19), a decision flow walked by
case tokens (P13), the review document pack (P15) and a swimlane review flow with an envelope token (P14)."""
from components import (Page, icon, md, Verbatim, Flow, Lanes, quote_card, case_card, report_table, alert, screen_mock, chip,
                        doc_mock, OK, BAD, WARN, BRAND, KIND, KIND_ICON)

q = Verbatim('src/protocol.md')
g = Verbatim('src/review_guide.md')     # project (CRO) material, not the protocol


def conmed():
    p = Page('conmed', '')
    cols = [('ok', '允许使用', q('润肤剂（基线前7天起保持稳定）；基线前已稳定使用的口服抗组胺药。')),
            ('warn', '需与申办者讨论', q('研究期间新开始使用外用钙调磷酸酶抑制剂。')),
            ('bad', '禁止使用', q('系统性免疫抑制剂、系统性糖皮质激素、任何生物制剂、活疫苗。'))]
    X = [0, 398, 796]
    for (kind, title, text), x in zip(cols, X):
        p.el(x, 64, 372, 340, f'<div class="f16 b t-{kind}">{icon(KIND_ICON[kind])} {title}</div><div class="f13" style="margin-top:6px;line-height:1.5">{md(text)}</div>',
             'pn tone', style=f'--tone:{KIND[kind]};display:block', s=1, d=X.index(x) * 150)
    # chips start in the tray (y=0) and drop into a column; slot(c, r) = position of row r in column c
    slot = lambda c, r: {'x': X[c] + 24, 'y': 196 + r * 46}
    chip(p, 0, 0, 170, 36, '润肤剂', s=1, ico='drop', k={2: slot(0, 0)})
    chip(p, 190, 0, 170, 36, '口服抗组胺药', s=1, ico='pill', k={2: slot(0, 1)})
    chip(p, 380, 0, 240, 36, '外用钙调磷酸酶抑制剂', s=1, ico='spray', k={4: slot(1, 0)})
    chip(p, 640, 0, 170, 36, '另一种生物制剂', s=1, ico='syringe', k={3: {**slot(1, 1), 'c': 'err'}, 4: {**slot(2, 0), 'c': ''}})
    chip(p, 830, 0, 200, 36, '系统性糖皮质激素', s=1, ico='pill', k={4: slot(2, 1)})
    alert(p, 398, 300, 372, 96, 'bad', '生物制剂放进了“需讨论”', '方案已明确列为禁止使用，不属于讨论范围。', s=3, o=4)
    p.narr(0, 424, 1168, 100, [
        '方案把合并用药分成三类：允许、需与申办者讨论、禁止。类别名称和内容照抄方案 3.6。',
        '润肤剂和基线前已稳定使用的口服抗组胺药属于允许使用。',
        '反例：把另一种生物制剂放进“需讨论”。方案已明确禁止任何生物制剂，不需要讨论。',
        '生物制剂和系统性糖皮质激素归入禁止；只有研究期间新开始的外用钙调磷酸酶抑制剂需要与申办者讨论。',
    ])
    return p


def ae_judge():
    """P19: four layers narrowing downwards; each case token stops in the layer that settles it."""
    p = Page('ae_judge', '')
    layers = [('签署知情同意书后新出现或加重？', '否 → 记为病史，不是 AE'), ('化验异常：有临床意义？', '无临床意义 → 写明理由，不记为 AE'),
              ('符合 SAE 标准？', '是 → 获知后 24 小时内报告申办者'), ('与研究药物的相关性', '研究者评估并记录')]
    LX = []
    for i, (qn, rule) in enumerate(layers):
        w = 540 - i * 70
        x, y = (560 - w) / 2, i * 94
        LX.append((x + w, y))
        k = {2: {'c': 'on'}, 3: {'c': ''}} if i == 0 else {3: {'c': 'on'}, 5: {'c': ''}} if i == 1 else {5: {'c': 'on'}}
        p.el(x, y, w, 82, f'<div class="f15 b ink">{md(qn)}</div><div class="f12 mut" style="margin-top:4px">{md(rule)}</div>', 'pn',
             style='display:flex;flex-direction:column;justify-content:center;padding-left:calc(58 * var(--kz-u))', s=1, d=i * 150, k=k)
        p.el(x + 14, y + 27, 28, 28, f'{i + 1}', 'f13 b c num', style='display:grid;place-items:center;border-radius:50%;background:rgba(15,17,21,.06)', s=1, d=i * 150)
    pt = lambda i: (LX[i][0] - 34, LX[i][1] + 41)     # tokens travel down the right edge, clear of text and numbers
    path = lambda n: 'M{:.0f} -6 '.format(pt(0)[0]) + ' '.join('L{:.0f} {:.0f}'.format(*pt(i)) for i in range(n))
    p.path('a', path(1)); p.path('b', path(2)); p.path('c', path(4))
    p.token({2: 'a'}, '#8A8F96', 'A', r=13)
    p.token({3: 'b'}, WARN, 'B', r=13)
    p.token({5: 'c'}, BAD, 'C', r=13)
    case_card(p, 600, 0, 568, 180, '例 A · 过敏性鼻炎', [('签署前', '已有，季节性发作'), ('研究期间', '程度未变')], '停在第 1 层：记为病史，不是 AE', 'ok', s=2, o=3)
    case_card(p, 600, 0, 568, 180, '例 B · V4 ALT 1.6×ULN', [('基线', 'ALT 1.5×ULN'), ('本次', '1.6×ULN，无症状')], '第 2 层：研究者判断有无临床意义', 'warn', s=3, o=5)
    case_card(p, 600, 0, 568, 180, '例 C · 带状疱疹', [('发生', 'V5 后新发'), ('处理', '门诊口服抗病毒药，未住院')], '不符合 SAE 标准 → 记为 AE，评估相关性', 'warn', s=5)
    alert(p, 600, 196, 568, 124, 'ok', '按方案 6.1 逐条对照', '未住院、未危及生命，不符合任何一条 SAE 标准，按 AE 记录并评估相关性。', s=5)
    alert(p, 600, 196, 568, 124, 'bad', '原始资料只写了“NCS”', '方案要求判断为无临床意义时写明理由，只写结论不符合要求。', s=3, o=4)
    alert(p, 600, 196, 568, 124, 'ok', '写明判断和理由', '“ALT 1.6×ULN，与基线 1.5×ULN 相当，无症状，判断无临床意义。”', s=4, o=5)
    lab = q('实验室检查异常由研究者判断是否有临床意义；有临床意义的异常记录为不良事件，判断为无临床意义时须在原始资料中写明理由。')
    quote_card(p, 0, 384, 560, 136, '方案 6.3', lab.replace('须在原始资料中写明理由', '__须在原始资料中写明理由__'), s=1)
    p.narr(600, 340, 568, 180, [
        '判断分四层，从上往下：是不是 AE、化验异常有没有临床意义、是不是 SAE、与研究药物的相关性。',
        '例 A：签署知情同意书前就有过敏性鼻炎，研究期间没有加重，停在第一层，记为病史。',
        '例 B：V4 的 ALT 是 1.6 倍 ULN，到第二层。反例：原始资料只写了“NCS”三个字母，没有理由。',
        '正确写法：写明数值、与基线的比较、有无症状，再给出无临床意义的判断。',
        '例 C：V5 后新发带状疱疹，门诊治疗、未住院，不符合 SAE 标准，记为 AE，再由研究者评估相关性。',
    ])
    return p


def ae_flow():
    p = Page('ae_flow', '')
    f = Flow(p)
    f.node('ae', 0, 40, 160, 64, '发生不良事件', '签署 ICF 后至研究结束', 'alert')
    f.diamond('q1', 200, 4, 180, 136, '符合 SAE\n标准？')
    f.node('sae', 430, 0, 220, 64, '研究者报告申办者', '获知后 24 小时内', 'bolt', 'bad')
    f.node('rec', 430, 110, 220, 64, '记录原始资料与 CRF', '按 AE 随访', 'pen')
    f.node('fu', 700, 0, 230, 64, '随访 SAE', '至恢复、稳定或研究结束', 'search', 'warn')
    f.wire('ae', 'q1').wire('q1', 'sae', 'bad', label='是').wire('q1', 'rec', label='否', path='M335 100 C 380 130 400 142 430 142').wire('sae', 'fu', 'bad')
    f.route('a', 'ae', 'q1', 'sae', 'fu').route('b', ('ae', 0, 10), ('q1', 0, 10), 'rec').route('c', ('ae', 0, -10), ('q1', 0, -10), ('sae', -60, 0))
    p.token({2: 'a'}, BAD, 'A', r=12)
    p.token({3: 'b'}, OK, 'B', r=12)
    p.token({4: 'c'}, '#8A8F96', 'C', r=12)
    sae_def = q('严重不良事件（SAE）是指导致死亡、危及生命、需要住院或延长住院时间、导致永久或显著的功能丧失、先天性异常或出生缺陷的不良事件。')
    sae_rep = q('研究者获知严重不良事件（SAE）后应在24小时内报告申办者。')
    quote_card(p, 0, 200, 540, 160, 'SAE 定义与报告 · 方案 6.1、6.2',
               sae_def.replace('需要住院或延长住院时间', '__需要住院或延长住院时间__') + '\n' + sae_rep.replace('24小时内', '__24小时内__'), s=1)
    case_card(p, 580, 200, 588, 160, '例 A · 肺炎住院', [('获知', '周一 09:00 电话得知'), ('判断', '需要住院 → SAE')], '当天 24 小时内报告申办者，并持续随访', 'warn', s=2, o=3)
    case_card(p, 580, 200, 588, 160, '例 B · 注射部位红斑', [('程度', '轻度，2 天消退'), ('判断', '不符合 SAE 标准')], '记录为 AE，按常规随访', 'ok', s=3, o=4)
    alert(p, 580, 200, 588, 160, 'bad', '例 C · 周五晚获知，周一才报告', '获知时间就是计时起点，与工作日无关；超过 24 小时即不符合方案要求。', s=4)
    report_table(p, [('研究者 → 申办者', '严重不良事件', '获知后 24 小时内'), ('研究者', 'SAE 随访', '至恢复、稳定或研究结束')], x=0, y=376, w=540, h=130)
    p.narr(580, 376, 588, 130, [
        '先判断是否符合 SAE 标准：死亡、危及生命、住院或延长住院、永久功能丧失、先天异常。',
        '例 A：肺炎住院，符合 SAE。研究者获知后 24 小时内报告申办者，并随访到恢复、稳定或研究结束。',
        '例 B：轻度注射部位红斑，两天消退，不符合 SAE 标准，按 AE 记录。',
        '反例 C：周五晚上获知，周一才报告。24 小时从获知时开始算，不看是否工作日。',
    ])
    return p


def docs_pack():
    """P15: scattered records drop into the five folders, get their file names, then the identifiers are blacked out."""
    p = Page('docs_pack', '')
    cats = [('筛选期病历', ['V1 病程记录', '体格检查']), ('评分表', ['EASI / IGA / BSA', '研究者签名']), ('既往病历与用药记录', ['外院病历', '处方记录']),
            ('检验检查报告', ['血常规', '血生化']), ('入组审核表', ['研究者判定', '签字日期'])]
    SCATTER = [(10, 14), (196, 50), (372, 4), (60, 172), (282, 190)]
    for i, (name, lines) in enumerate(cats):
        y = i * 62
        p.el(580, y, 240, 54, '', 'pn flat', style='border:1.5px dashed #D9D0C3', s=1)
        p.el(594, y + 16, 220, None, f'<span class="f13 mut">{icon("folder")} {name}</span>', '', s=1, o=2)
        # on arrival the record folds to its title line, filed in the folder
        doc_mock(p, *SCATTER[i], 150, 110, name, lines, s=1, d=i * 100,
                 k={2: {'x': 584, 'y': y + 3, 'w': 232, 'h': 48, 'html': f'<div class="dh">{icon("folder")}{name}</div>'}})
        p.el(850, y + 15, 318, None, f'S01003-筛选期-{name}.pdf', 'f13 num ink', s=3, d=i * 100,
             k={5: {'html': '<span class="t-bad">张某某-既往病历.pdf</span>'}} if i == 2 else None)
    p.ring(842, 2 * 62 + 4, 326, 46, 'bad', s=5)
    # step 4: one record enlarged, identifiers blacked out, study number and date kept
    p.el(0, 0, 540, 300, f'<div class="dh">{icon("file")}筛选期病历（第 1 页）</div>', 'doc', s=4, fx='fade')
    for j, (a, b, red) in enumerate([('姓名', '张某某', True), ('身份证号', '110105 1990 0315 1234', True), ('联系电话', '138 0013 8000', True),
                                     ('受试者编号', 'S01003', False), ('就诊日期', '2026-11-10', False), ('诊断', '特应性皮炎', False)]):
        y = 44 + j * 40
        p.el(20, y, 110, None, a, 'f13 mut', s=4)
        p.el(130, y, 260, None, b, 'f14 num ink', s=4)
        if red:
            p.el(126, y - 3, 220, 28, '', 'redact', s=4, fx='wipe', d=500 + j * 200)
    rules = [(1, 3, '资料清单 · 项目流程（CRO）', g('筛选期病历、评分表（EASI/IGA/BSA）、既往病历与用药记录、检验检查报告、入组审核表，共5类，缺一类即退回补充。')),
             (3, 4, '文件命名 · 项目流程（CRO）', g('每类资料合并为一个PDF，按“受试者编号-访视-资料名称.pdf”命名，例如S01003-筛选期-筛选期病历.pdf。')),
             (4, None, '脱敏 · 项目流程（CRO）', g('上传前遮盖姓名、身份证号、联系电话等可识别个人身份的信息，保留受试者编号和日期。文件名中不得出现姓名。'))]
    for st, o, title, text in rules:
        quote_card(p, 0, 314, 540, 92, title, text, s=st, o=o)
    alert(p, 580, 326, 588, 80, 'bad', '文件名里出现了姓名', '既不符合命名规则，也没有脱敏；按“受试者编号-访视-资料名称”重新命名。', s=5)
    p.narr(0, 414, 1168, 106, [
        '这一部分来自项目的入组审核资料要求，不是方案条款。资料分 5 类，缺一类就退回补充。',
        '散在的原始资料按 5 个类别归档，每类合并成一个 PDF。',
        '文件名按“受试者编号-访视-资料名称”，例如 S01003-筛选期-筛选期病历.pdf。',
        '上传前遮盖姓名、身份证号和电话，保留受试者编号和日期。',
        '反例：文件名直接写了受试者姓名，既不符合命名规则，也泄露了身份信息。',
    ])
    return p


def review_lanes():
    p = Page('review_lanes', '')
    lanes = Lanes(p, ['crc', 'pi', 'cra', 'mm'], x=0, y=0, w=860, lane_h=84, gap=8)
    B = {
        'v1': lanes.box(0, 130, 120, 'V1 完成', None, 'calendar'),
        'pack': lanes.box(0, 280, 170, '整理资料 · 提交', '原始资料扫描件', 'mail', d=100),
        'pi': lanes.box(1, 280, 170, '研究者判定合格', '审核表签字', 'pen', d=150),
        'cra': lanes.box(2, 480, 150, '复核资料完整', None, 'search', d=200),
        'mm': lanes.box(3, 480, 150, '医学审核', None, 'shield', d=250),
        'ok': lanes.box(3, 680, 160, '支持入组', '回复邮件', 'check', 'ok', d=300),
        'back': lanes.box(2, 680, 160, '资料不全 · 退回', '补充后再提交', 'upload', 'warn', d=350),
    }
    c = lambda k, dx=0: (B[k][0] + B[k][2] - 14 + dx, B[k][1] + 8)
    pts = lambda *ks: 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in (c(k) for k in ks))
    for a, b in (('v1', 'pack'), ('pack', 'pi'), ('pi', 'cra'), ('cra', 'mm'), ('mm', 'ok')):
        p.wire(f'M{B[a][0] + B[a][2]:.0f} {B[a][1] + 28:.0f} L{B[b][0]:.0f} {B[b][1] + 28:.0f}', 'brand' if b == 'ok' else '', s=1)
    p.wire(f'M{B["mm"][0] + 75:.0f} {B["mm"][1]:.0f} L{B["back"][0] + 20:.0f} {B["back"][1] + 56:.0f}', 'bad dash', s=1)
    p.path('m1', pts('v1', 'pack', 'pi', 'cra', 'mm', 'ok'))
    p.path('m2', pts('mm', 'back', 'pack'))
    p.token({2: 'm1'}, BRAND, '✉', r=13)
    p.token({3: 'm2'}, WARN, '✉', r=13)
    mail = [('主题', 'DEMO-301-S01003-入组审核'), ('受试者编号', 'S01003'), ('ICF 签署日期', '11/03'), ('预计基线日期', '12/01'),
            ('附件', '筛选期病历、评分表、既往病历、检验检查、入组审核表'), ('正文', 'S01003 已完成 V1，提交入组审核资料。')]
    screen_mock(p, 880, 0, 288, 172, '提交邮件（示例格式）', ''.join(f'<div><span class="b ink">{md(a)}</span>：<span class="{"hl" if "日期" in a else ""}">{md(b)}</span></div>' for a, b in mail), s=2)
    alert(p, 880, 192, 288, 120, 'warn', '缺少既往用药原始资料', '退回补充；审核方不根据口述代为判断。', s=3)
    p.narr(0, 384, 1168, 140, [
        '入组审核涉及四方：CRC 整理提交，研究者判定并签字，CRA 复核资料完整，医学审核后回复。这一流程来自项目的入组审核流程，不是方案条款。',
        '正常路径：V1 完成后提交，邮件写明受试者编号、ICF 日期和预计基线日期，审核通过后回复支持入组。',
        '资料不全时退回补充，补齐后重新提交；审核以原始资料为准，不以口述替代。',
    ])
    return p


PAGES = [conmed, ae_judge, ae_flow, docs_pack, review_lanes]
