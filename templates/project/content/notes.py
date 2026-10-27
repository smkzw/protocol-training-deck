"""Speaker scripts (逐字稿), shown in the presenter window (S key). Rules: reference/speaker-notes.md.

NOTES[pid] = (opening, [one paragraph per step]). The opening is said when the page appears (header + lead visible,
nothing revealed yet); paragraph k is said right after the k-th key press. Paragraph count must equal page steps.
"""

HERO_NOTES = {
    'cover': '各位好。今天讲 【研究简称】 的方案要求和执行要点，依据方案 【版本】。',
    'toc': '整体分 【n】 章：【章节名依次列出】。每页左上角的标签提示当前阶段，标题写明访视和时间。',
    '01': '第一章，研究背景与设计：【本章讲什么】。',
    '02': '第二章，【…】。',
    '03': '第三章，【…】。',
    '04': '第四章，【…】。',
    '05': '第五章，【…】。',
    '06': '第六章，【…】。',
}

NOTES = {
    'study_info': ('先把研究的基本信息讲全，后面的内容都围绕它展开。', [
        '【第 1 步：题目、编号、版本、申办者】',
        '【第 2 步：分期、设计、例数、给药、周期】',
        '【第 3 步：分组比例与主要终点】',
    ]),
}
