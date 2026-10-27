"""Deck structure. Fill CHAPTERS / ORDER / META from plan/outline.md (see reference/page-catalog.md).
Header (标题区) = where the page sits; lead (强调句) = the one protocol rule to remember on the page."""
from datetime import date
from components import StudyDates

DAY = StudyDates(date(2026, 12, 1))   # fictional participant: D1 (first dose) — every example date derives from it

# (number, TOC title ≤7 字, one-line description ≤14 字, header stage label ≤6 字) — longer TOC text raises the
# hero layout capacity error (固定文字框横向容量不足): shorten it, never shrink the font
# Delete chapters the study does not need (e.g. no run-in → drop 03) and renumber.
CHAPTERS = [
    ('01', '研究背景与设计', '疾病、药物、研究概要与终点', '研究背景'),
    ('02', '筛选期', '受试者识别、V1、入排与审核', '筛选期'),
    ('03', '导入期与基线', '日志卡、基线判定与随机', '基线'),
    ('04', '治疗期', '给药访视与当天安排', '治疗期'),
    ('05', '随访与研究结束', '随访访视与提前终止', '随访'),
    ('06', '特殊情况处理', '退出、补救、安全性、揭盲', '特殊情况'),
]

ORDER = [
    ('cover',), ('toc',),
    ('chapter', 0), 'study_info',
    # ('chapter', 1), 'v1_flow', ...    add pages chapter by chapter from plan/outline.md
    # ('ending',),                      optional Kangzhe closing page (ending_title / ending_subtitle in project.py, HERO_NOTES['ending'])
]

# pid: (chapter index, title, small = time/visit/clause attributes, lead sentence with **emphasis**)
# chapter index = position in CHAPTERS, starting at 0 (chapter '02' → 1); HERO_NOTES alone uses the '01' strings
META = {
    'study_info': (0, '研究基本信息', '方案摘要 · 【方案编号】 · 【版本】', '【设计关键词】Ⅲ期研究，计划入组 **【N】 例（【比例】）**'),
}
