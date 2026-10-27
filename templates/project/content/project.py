"""Deck-level settings. Everything printed on the cover / in the footer / in the drill-down source note lives here."""
DECK = {
    'cover_title': ['【研究简称或方案编号】', '研究方案及操作培训'],     # 1–2 lines; too long → hero layout capacity error
    'cover_subtitle': '临床试验方案 【版本】（【日期】）',
    'footer': '产品中心-医学部｜【YYYY】年【M】月',
    'html_title': '【研究简称】 研究方案及操作培训',
    'source_note': '摘自 【方案编号】 临床试验方案 【版本】（【日期】）。',
    # 'hero_images': {'cover': 'assets/hero/my-cover.webp'},     # optional; files go to content/assets/
    # 'ending_title': '谢谢', 'ending_subtitle': '…',              # only when ORDER ends with ('ending',)
    # 'allow_words': [],                                         # words check_project.py should accept in this study
}
