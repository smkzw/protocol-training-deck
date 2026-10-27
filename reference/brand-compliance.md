# 康哲 design 与 html-ppt 规范对照

本技能内置了两套上游规范在“常规 HTML-PPT”场景下需要的全部内容。机器上不装 kangzhe-design 或 html-ppt 技能，也能做出合规的 deck。本文逐条列出两套规范的硬性要求，以及本技能的处理方式：

- **执行**：引擎实现，并由检查保证；
- **豁免**：用户认可的有意偏离；
- **降级**：能力受限，需要人工补位；
- **不适用**：本场景用不到。

“谁保证”一列中：
- “引擎”指构建结果天然满足；
- `check` 指 `scripts/check_project.py`；
- `qa` 指 `scripts/qa.py`（`deck-qa.js`）；
- “人工”指 `visual-qc.md` 的截图检查。

## 1. 内置副本与上游的关系

| 文件 | 上游 | 关系 |
|---|---|---|
| `engine/static/assets/logo_bot.svg` | kangzhe-design 官方 Logo | 逐字节相同（`check` 核对 sha256） |
| `engine/brand/header-mark.svg` | kangzhe-design 双菱形 | 逐字节相同（`check` 核对 sha256） |
| `engine/static/kz/kz-drilldown.js`、`kz-audience.js` | kangzhe-design runtime | 逐字节相同 |
| `engine/static/kz/kz-subset.css` | kangzhe-design `kz-glass.css` | 逐行摘录：目录卡、下钻对话框、浮动、孤字、减少动态、打印 |
| `engine/static/kz/kz-tokens.css/js`、`brand/tokens.json` | kangzhe-design tokens | 用到的色值、字号、hero 几何与上游一致 |
| `engine/static/kz/html-ppt-bridge.js` | kangzhe-design adapter | 子集：保留单一比率 `--kz-un`；scene 步进由 `sop2.js` 负责 |
| `engine/static/assets/hero/*.webp`、`body-quiet.webp` | kangzhe-design 参考资产 | 逐字节相同 |
| `engine/static/vendor/html-ppt/assets/base.css` | html-ppt | 逐字节相同（`check` 核对 sha256） |
| `engine/static/vendor/html-ppt/assets/runtime.js` | html-ppt | 一处补丁：演讲者窗口逐步同步、主窗口无响应时自行翻页（`check` 核对 sha256） |

不依赖上游的验证方法：
1. `grep -rn "\.claude/skills\|kangzhe-design\|/Users/" engine scripts qa` 只命中来源注释。
2. 把 `HOME` 指到空目录后，新建项目、构建、检查、QA，结果都应正常。2026-10-27 已验证。

## 2. 康哲 design（常规 HTML-PPT 路线）硬性要求

| 要求（康哲条款） | 本技能怎么做 | 谁保证 | 状态 |
|---|---|---|---|
| 只用官方 `logo_bot.svg`，不改、不重绘、不变形（CORE-02） | 引擎放置原件，等比显示 | `check` 哈希（换品牌时为 WARN）；`qa` LOGO | 执行 |
| 正文页 Logo 右上右锚；封面、尾页左上；目录、章节页右上；每页一枚（CORE-04、HERO） | `sop2.css` 用 `--kz-chrome-logo-*`；`hero_layout.py` | `qa` LOGO、TITLE_LOGO | 执行 |
| 正文页 chrome：左上双菱形、单行页标题、橙色横线、右上 Logo，打印时也在页内（CORE-04） | `build.py` 给每页写 chrome | 引擎；人工 | 执行 |
| 双菱形用批准资产，整组竖直微浮动 2px / 6.4s（LG-03） | 原件 + `kz-mark-float` | `check` 哈希 | 执行 |
| 页脚恰好两槽：左“产品中心-医学部｜YYYY年M月”，右 `N / 总页数`（含封面）；不写来源等第三段（CORE-04） | `project.py` 的 `footer`；页码构建时写入 | `check` 格式 WARN；`qa` FOOTER | 执行 |
| 页脚字号 18、页标题 32（TYPE-01） | `sop2.css` 用 `--kz-type-footer`、`--kz-type-page-title` | 引擎 | 执行 |
| 正文 20、卡标题 24、下限 16（TYPE-01） | 培训场景采用：正文 14、卡标题 16、下限 12 | `check` 拦 <12；`qa` FONT_FLOOR（12） | **豁免**（见 §3） |
| 字体：微软雅黑优先的康哲字体栈；不分发字体文件、不加载网络字体 | 正文沿用 html-ppt 系统字体栈 `--font-sans`；SVG 文字、导航、封面用 `--kz-font`；不带字体文件 | `package.py` 拦网络引用 | 正文为**豁免**（§3）；其余执行 |
| 色值只取 tokens；部门色只表示部门身份（CORE-01、02） | 品牌色、墨色、页脚色取 tokens；CRA/系统用非部门色 `#4A6D8C` | 人工（`aesthetics.md`） | 执行 |
| 深红只用于真正改变理解的重点；强调克制（COPY） | 强调每卡 ≤2、每页 ≤4；反例统一用红色 | `check` 强调密度 | 执行；反例用红为**豁免**（§3） |
| 视觉预算：浅色 ≥80%、暖饱和色 ≤12%、红 ≤3% | 浅色底 + 克制强调 | 人工看截图 | 降级（无像素统计） |
| 宽屏内容与背景铺满，不做居中 16:9（CORE-03、G5-WIDE） | 背景和 chrome 铺满；正文坐标画布 1168 宽、居中 | `qa --all-viewports` 查版面 | **豁免**（§3） |
| 单一比率 `--kz-un`，不叠第二套缩放 | 所有尺寸 `calc(N * var(--kz-u))` | 引擎 | 执行 |
| Liquid Glass 同族卡：三停渐变、rim、短高光、动态暖影、指针光（LG-01、ELEV-02） | 目录卡用完整 `kz-card`；正文卡 `.pn` 用简化配方，没有指针光 | 人工 | **豁免**（§3） |
| 不用通长装饰色条、侧竖线、标题下划线（LG） | 引擎没有这类元素 | `check` 粗边框 WARN | 执行 |
| 不用省略号、line-clamp、隐藏裁切（TYPE-03） | 强调句超长时构建报 ERROR | `qa` LEAD_OVERFLOW、LAYOUT_OVERFLOW | 执行 |
| 消除孤字行（TYPE-04） | 段落 `text-wrap:pretty`、标题 `balance` | 人工看截图 | 执行（需人工复核） |
| hero 四型固定形态、容量拒绝（HERO） | 封面、目录、章节，加可选尾页 `('ending',)`；容量不足时构建失败；目录最多 6 章，超过时构建报错，需合并章节 | 引擎 | 执行 |
| hero 入场按阅读顺序分层 | hero 页静态呈现；卡片保留微浮动 | — | 降级 |
| hero 与正文背景按本次主题生图，并登记回执（IMG） | 有生图能力就生成并登记；没有就沿用内置参考图，记 WARN | 人工（`image-generation.md`） | 降级 |
| 讲稿写在 `aside.notes`，按 scene 分段，段数等于 scene 数（SPEAK） | `notes.py` → 每步一段 | `check` ERROR；`qa` NOTES_MISMATCH | 执行 |
| 讲稿不用套话（“这一页展示了”“可以看到”“值得关注的是”“接下来我们将”） | 规范写在 `speaker-notes.md`，另加“这一页讲” | `check` WARN | 执行 |
| scene 随翻页键推进，末步后才翻页，后退时落在末步（MOTION-09） | `sop2.js` | `qa` ENTRY_FLASH、PRESENTER_SYNC | 执行 |
| 无人操作入场时走完全部 scene（MOTION-09） | 不自动播放，入场停在第 0 步 | — | **豁免**（用户要求不自动播放，硬规则 13） |
| 无播放、暂停、进度条、时间码控件（G7-NO-PLAYER） | 隐藏上游进度条；页脚不放步骤圆点 | `qa` FOOTER | 执行 |
| 不加载 animations.css、fx-runtime、主题和远程字体 | 只加载 base.css 和康哲层；T（换主题）、A（换动画）已屏蔽 | `package.py` | 执行 |
| 翻页不在 slide 容器上做透明度渐变 | `.slide{transition:none}`；进页时关闭过渡 | `qa` ENTRY_FLASH | 执行 |
| 方法、规则、计算页要有演示舞台（DEMO） | 每页单独设计的关键帧步骤，取代 KZDemo 组件 | 人工（`patterns.md`） | 执行（形式不同） |
| 下钻：宽对话框、层级栈、焦点、按键与滚轮隔离（DRILL） | 原件 `kz-drilldown.js`；“方案原文”单层下钻 | `qa` DRILL | 执行 |
| 离线：随包相对路径，没有远程资源 | 构建只引用 deck 内文件 | `package.py`（HTML、CSS、JS 都扫） | 执行 |
| 验收视口五档 | `qa.py --all-viewports` | `qa` | 执行 |
| 不改上游源码 | runtime.js 有一处补丁（演讲者窗口逐步同步） | `check` 哈希锁定补丁版本 | **豁免**（逐步同步离不开这处补丁） |
| G0–G9 门表与六个状态词 | 本技能用自己的 G0–G8 阶段和 `plan/qa-log.md` | — | 口径不同 |

## 3. 用户认可的豁免（2026-10-27）

以下几处是有意偏离，不要“修正”。理由是：这套培训稿面向 CRC/CRA 逐页讲解，信息密度高，版式针对培训场景设计。

1. **字号**：正文 14、卡标题 16、下限 12（康哲为 20 / 24 / 16）。`check` 和 `qa` 都按 12 把关。
2. **正文画布居中**：宽屏时正文坐标画布（1168 × 564）居中，背景和 chrome 仍然铺满。
3. **正文卡配方**：`.pn` 用简化的玻璃卡（没有短高光、动态暖影和指针光）；目录卡仍是完整的康哲 `kz-card`。
4. **反例统一用红色**：硬规则 6（用户要求）。
5. **不自动播放**：入场停在第 0 步，硬规则 13（用户要求）。
6. **runtime.js 补丁**：演讲者窗口逐步同步（用户要求逐字稿随步骤高亮）。
7. **正文字体**：沿用 html-ppt 的 `--font-sans`。两套字体栈中文都落在系统黑体（mac 苹方 / Windows 微软雅黑），差别主要在英文和数字的字形；demo 两种字体 QA 都通过。改回康哲字体栈只需在 `sop2.css` 加 `.kz{font-family:var(--kz-font)}`，改后重跑 QA。

对外交付说明里写一句：“版式按康哲 design 常规 HTML-PPT 路线制作，字号、正文卡配方和正文字体按培训场景豁免。”

## 4. html-ppt 运行时约定

| 约定 | 本技能怎么做 | 谁保证 | 状态 |
|---|---|---|---|
| ← → 空格 PageUp PageDown Home End Enter Backspace | 上游保留；`sop2.js` 先消耗步骤，步骤用完再交给上游翻页；另加 ↑ ↓ | `qa` ENTRY_FLASH | 执行 |
| 触屏滑动 | 同上 | 引擎 | 执行 |
| S 演讲者窗口：当前页 / 下一页预览（`?preview`）、逐字稿、计时器、页码、Prev/Next、拖拽布局 | 上游实现，加补丁：逐字稿随步骤高亮、显示“第 k/n 步”、按键逐步推进、主窗口无响应时自行翻页 | `qa` PRESENTER_SYNC；2026-10-27 实测 | 执行 |
| BroadcastChannel 同步（频道 `html-ppt-presenter-<路径>`） | `sop2.js` 用同名频道收发 `hello` / `step` / `stepstate` | `qa` PRESENTER_SYNC | 执行 |
| 预览 iframe 只加载一次，之后用 postMessage 切页 | 上游原样 | 实测 | 执行 |
| N 备注抽屉、O 总览、F 全屏、Esc 关闭浮层 | 上游原样；总览缩略图改为显示每页最终状态 | 实测 | 执行 |
| `#/n` 路由 | 上游原样；目录标签也用 `#/n` | `qa` 依赖它 | 执行 |
| 逐字稿写在 `<aside class="notes">`，观众端不可见、打印不输出 | `build.py` 生成 | `check`、`qa` NOTES_MISMATCH | 执行 |
| 页面结构：一个 `.deck`，每页一个 `.slide`，`is-active` 由 runtime 写 | `build.py` 生成 | 引擎 | 执行 |
| 缩放 | `data-fit="fluid"`，改用康哲 `--kz-un` | 引擎 | 执行 |
| 打印：每页一张，隐藏 chrome 以外的界面元素 | `@page 16in 9in`；打印前显示末步 | 2026-10-27 实测 PDF 18 页 | 执行 |
| fonts.css（Google Fonts） | 不带；用系统字体栈 | `package.py` | 执行 |
| 主题 T、动画 A、`data-anim` | 不用，按键已屏蔽 | 引擎 | 不适用 |
| `data-logo`、进度条 | 用康哲 chrome；进度条隐藏 | 引擎 | 不适用 |
| 每页逐字稿 150–300 字 | 改为开场 20–50 字、每步 60–150 字 | `check` WARN | 本技能口径 |

## 5. 不适用

- PPTX 路线：logo PNG、PowerPoint 回读、`bind_header_mark_pptx`。
- 站点式、流式 HTML：折叠区、Bento、responsive 正文。
- 旗舰路线：`kz-flagship.*`。
- 甘特、电影、ECharts 数据图：本技能没有这些页型；以后要加数值图，先读康哲 05 CHART。
- 外部文献参考行：方案培训一般不用。
