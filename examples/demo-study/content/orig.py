"""Protocol originals for the "方案原文" drill-down: SRC[pid] = [(heading, [paragraph, ...])].
Text is copied by anchor from src/protocol.md (never retyped); a missing anchor stops the build."""
from srctext import Source

P = Source('src/protocol.md')

SRC = {
    'bg_disease': [('疾病背景（1.1）', P.lines('## 1.1 疾病背景', 1))],
    'v1_flow': [('筛选期（4.1）', [P.line('V1访视项目包括')])],
    'excl_prior': [('排除标准（3.5.2）', [P.line('2. 基线前4周内'), P.line('3. 基线前8周')]),
                   ('起算点（4.2）', [P.line('基线访视（V2）即首次给药日')])],
    'washout_calc': [('排除标准（3.5.2）', [P.line('2. 基线前4周内'), P.line('3. 基线前8周')]),
                     ('起算点（4.2）', [P.line('基线访视（V2）即首次给药日')])],
    'diary_form': [('日志卡（4.3）', P.lines('## 4.3 日志卡', 1))],
    'nrs_calc': [('入选标准（3.5.1）', [P.line('5. 基线前7天')]), ('瘙痒 NRS（5.1）', [P.line('瘙痒NRS：')])],
    'ae_judge': [('不良事件与实验室检查异常（6.3）', P.lines('## 6.3 不良事件与实验室检查异常', 1))],
    'scales': [('疗效评估量表（5.1）', P.lines('## 5.1 疗效评估量表', 4))],
    'conmed': [('合并用药（3.6）', P.lines('## 3.6 合并用药', 3))],
    'incl_easi': [('入选标准（3.5.1）', [P.line('2. 筛选期和基线时'), P.line('3. 筛选期和基线时'), P.line('4. 筛选期和基线时')]),
                  ('排除标准（3.5.2）', [P.line('1. 筛选期丙氨酸')]),
                  ('筛选期（4.1）', [P.line('试验参与者签署知情同意书后进入筛选期')])],
    'screen_cal': [('筛选期（4.1）', [P.line('试验参与者签署知情同意书后进入筛选期')]),
                   ('入选标准（3.5.1）', [P.line('5. 基线前7天')])],
    'v4': [('基线与给药访视（4.2）', [P.line('所有访视日期均以首次给药日')])],
    'dose_day': [('基线与给药访视（4.2）', [P.line('所有访视日期均以首次给药日')])],
    'ae_flow': [('严重不良事件（6.1、6.2）', [P.line('严重不良事件（SAE）是指'), P.line('研究者获知严重不良事件')])],
}
