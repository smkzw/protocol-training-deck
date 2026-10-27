# Page 与组件 API

页面模块统一这样导入：`from components import ...`。它会转出 kit 里的 `Page, icon, md, role, A, ROLE`。

坐标单位是画布单位：可用区 1168 × 524（总画布 1168 × 564，顶部 40 是强调句）。页面元素的 y 从 0（强调句下沿）到 524。

## 1. 步骤参数（所有元素通用）

| 参数 | 含义 | 例 |
|---|---|---|
| `s=k` | 第 k 步出现 | `s=2` |
| `o=k` | 第 k 步消失 | `s=2, o=3` 只在第 2 步可见 |
| `d=ms` | 本步内延迟出现，用于错峰 | `d=150` |
| `fx=` | 出场方式：`fade`、`up`（默认）、`pop`、`left`、`right`、`drop`、`wipe`（从左向右擦除展开，适合条、带、轴） | `fx='wipe'` |
| `k={步: {...}}` | 关键帧：`x y w h`（画布单位）、`c`（class，空字符串表示移除）、`t`（文字）、`html` | `k={3: {'x': 600, 'c': 'err'}, 4: {'x': 420, 'c': ''}}` |
| `count={步: [起, 止, 小数位]}` | 数字滚动 | `count={2: [0, 28, 0]}` |
| `move={步: pid}` | token 沿路径移动（用 `p.token`） | |

关键帧会一直保持到被覆盖。反例改动过的属性，在后面的步骤里要逐项写回。

## 2. Page 方法

| 方法 | 说明 |
|---|---|
| `Page(pid, '')` | pid 必须等于函数名 |
| `p.el(x, y, w, h, inner, cls, style='', **步骤参数)` | 通用绝对定位元素。`h=None` 表示自动高度，`w=None` 表示自动宽度 |
| `p.panel(x, y, w, h, title, body, ico, cls)` | 玻璃卡；`cls`：`flat`、`tint`、`stretch` |
| `p.text(x, y, w, txt, cls='f14')` | 文本，经过 `md()` |
| `p.node(x, y, w, h, title, sub, ico, cls)` | 流程节点；`cls`：`on`、`ok`、`bad`、`warn`、`term`（胶囊）、`dim` |
| `p.dia(x, y, w, h, text)` | 菱形判断节点（文字 ≤8 字，用 `\n` 换行） |
| `p.tag(x, y, text, kind)` | 标签；`kind`：`ok`、`bad`、`warn`、`brand`、`cra`、`mm`、`pv` 或空 |
| `p.stamp(x, y, size, kind)` | 圆形印章 ✓ ✗ ! |
| `p.ring(x, y, w, h, kind)` | 高亮圈，用于圈出出错处；`kind`：`bad`、`ok` 或空 |
| `p.narr(x, y, w, h, [第1步, 第2步, …])` | 旁白卡，每步一条；也可以传 `{步: 文本}` |
| `p.checklist(x, y, w, h, groups, title)` | 简单清单：`groups=[(组名, [(文本, 打勾步, 'ok'/'fail')])]` |
| `p.wire(d, cls, s=, o=)` | 画布坐标的 SVG 路径连线，带箭头；`cls`：`ok`、`bad`、`brand`、`cra`、`mm`、`dash`、`thick` |
| `p.wlabel(x, y, text)` | 连线标签 |
| `p.path(pid, d)` | 不可见的运动路径 |
| `p.token({步: pid}, color, label, r)` | 沿路径移动的圆点，可以带 1–2 字标签 |
| `p.svg_raw(svg)` | 往底层 SVG 里加原始片段（例如 `gauge` 的圆环） |
| `p.raw(html)` | 原始 HTML |

## 3. 文字标记（`md()`，所有组件的文本参数都会经过它）

`**加粗**`　`!!深红!!`　`__橙色下划线__`　`^^黄色高亮^^`　`==品牌 chip==`　`[建议]`　`[操作建议]`　换行写 `\n`

`[建议]` 在任何地方都可以写，包括关键帧 `k` 的 `html`/`t`：构建时统一替换成灰色小字“（建议）”。

`md()` 会转义 HTML，在文本里写 `<br>` 会原样显示出来。需要 HTML 时，用 `p.el` 的 `inner` 参数直接写 HTML，不要经过 `md()`。

## 4. 常用类（写在 `cls` 或 `inner` 的 HTML 里）

- 字号：`f12 f13 f14 f15 f16 f18 f20 f22 f24 f28 f32 f40 f56`
- 粗细与颜色：`b`、`ink`（深）、`mut`（灰）、`t-ok`、`t-bad`、`t-warn`、`t-brand`、`t-cra`、`t-mm`、`t-pv`
- 对齐与排版：`c`（居中）、`r`、`nw`（不换行）、`num`（等宽数字）、`lh12`、`lh15`
- 卡片：`pn`、`pn flat`、`pn tint`、`pn tone`（配合 `style="--tone:#C00000"`）、`pn on`（焦点）、`is-dim`（变淡）
- 条与带：`bar`（加 `ok`、`bad`、`cra`、`brand`、`grey`、`yel`、`stripe`）、`band`
- 其他：`doc`（纸质文档）、`screen`（系统界面）、`redact`（脱敏黑条）、`chip`（加 `off`、`err`）、`cel`（加 `on`、`miss`）、`tmr`（加 `full`、`short`）、`sw`（开关，加 `on`）、`err`
- 图标：`icon('名称')`。可用名称：alert arrowr baby bed body bolt calendar check clipboard clock ct diary doctor drop ecg eye female file flag flask folder gear hospital hourglass key list lock lungs mail microscope monitor nose nurse pause pdf pen phone pill scale scope search shield shuffle snow spray star stop syringe truck tube upload user users virus x
- 角色：`role('crc')`。可用键：crc cra mm pi sub pv nurse sys lab read iwrs ec pharm

## 5. 组件（components.py）

| 组件 | 签名 | 用途 |
|---|---|---|
| `Verbatim(*paths)` | `q = Verbatim('src/protocol.md'); q('原文')` | 页面上引用方案原文；原文对不上时构建失败（比较时忽略空白）。参数必须是**不带标记的原文**，标记加在返回值上：`q('…≥16分。').replace('≥16分', '__≥16分__')` |
| `alert` | `(p, x, y, w, h, kind, title, body, s, o, d, fx, cover=True)` | 正例、反例、需判断的提示卡；`kind`：`ok`、`bad`、`warn` |
| `case_card` | `(p, x, y, w, h, head, rows, verdict, kind, s, o, avatar='sub')` | 案例卡：头像、若干行、判定 |
| `kv_card` | `(p, x, y, w, h, title, rows, s, o, d, cls, label_w, ico)` | 标签–值卡 |
| `quote_card` | `(p, x, y, w, h, title, text, s, o, d)` | 方案原文卡（浅橙），文本先经过 `q()` |
| `doc_mock` | `(p, x, y, w, h, title, lines, …, extra, ico, fx, k)` | 纸质文档 |
| `screen_mock` | `(p, x, y, w, h, title, body_html, s, o, d)` | 系统或邮件界面；`body_html` 用 `md()` 生成 |
| `verdict_board` | `(p, x, y, w, rows, title, row_h, s)` | 判定板，`rows=[(标签, {步: (值, kind)})]` |
| `visit_checklist` | `(p, title, sub, groups, skip, x, y, w, h)` | 访视清单，`groups=[(组, [(文本, 步或{步: 'done'/'fail'/'now'})])]` |
| `report_table` | `(p, rows, x=0, y=404, w=540, h=120, title, s)`，默认位置在左下角 | 报告对象与时限，`rows=[(谁→谁, 什么, 时限)]` |
| `day_axis` | `(L, R, d0, d1)` → `X(day)` | 天数换算为 x |
| `piecewise_axis` | `([(w0, w1, x0, x1), …])` → `X(week)` | 分段拉伸的周轴 |
| `time_axis` | `(p, L, R, y, h0, h1, s, step=30)` → `T(h, m)` | 钟点刻度 |
| `StudyDates` | `D = StudyDates(date(...)); D(29)` → `'12/29'`；`D.window(29, 3)` | 虚构日期 |
| `Calendar` | `(p, start, x, y, cw, ch, weeks, s, dim_month)`；`.band(a, b, color, s)`、`.mark(day, text, kind, s)`、`.ring(day, s)`、`.pos(day)` | 月历。`start`、`a`、`b`、`day` 都是 `datetime.date`（不是天数）；`start` 必须是周一。用研究日换算：`DAY.date(-7)` |
| `threshold_bar` | `(p, x, y, w, label, threshold, bad_side, value_pos, value_text, s, o, d, split)` | 阈值条 |
| `gauge` | `(p, x, y, n, total, color, s, o, d, name, note, r)` | 计数环 |
| `tube_html` | `(cap, fill, label, sub)` → HTML | 采血管 |
| `chip` | `(p, x, y, w, h, text, s, o, d, k, cls, ico)` | 可移动的条目 |
| `switch_row` | `(p, x, y, label, k, s, d, label_w)` | 开关行 |
| `Flow` | `.node(key, x, y, w, h, title, sub, ico, cls)`、`.diamond(key, …)`、`.wire(a, b, cls, label, path, sides='rl', curve)`、`.route(pid, *keys)` | 决策流 |
| `Lanes` | `(p, roles, x, y, w, lane_h, gap)`；`.box(lane, x, w, title, sub, ico, cls, s, d, h)` → (x, y, w, h) | 泳道 |
| 常量 | `OK BAD WARN BRAND CRA MM GREY`、`KIND`、`KIND_ICON` | 颜色 |

## 6. 其他模块

- `srctext.Source(path, start=0)`：`.line('行首', after=None)` 返回第一条以该文字开头的行；`.lines('行首', n, after=None)` 返回该行之后的 n 个非空行；`.index('行首')` 返回行号。用于 `orig.py`。
  入选和排除标准都从“1.”编号时，`P.line('1. ')` 会取到入选 1。行首要写 8 个字以上的区分性文字，或者先定位章节：`P.line('1. ', after=P.index('排除标准'))`。
  `docx2md.py` 只会给 Word 标题样式的段落加 `#`；方案没有用标题样式时，锚点直接写标题文字（如 `'3.5.2 排除标准'`），不要写 `'## 3.5.2'`。
- `svgart`：见 `svg-fallback.md`。
- `build.py` 的 `autofit`：自动把旁白卡收紧到内容高度，并把上方元素拉伸，填满让出来的空间。页面里有手绘 SVG、或相邻元素没有余地时跳过，并给出 WARN。
