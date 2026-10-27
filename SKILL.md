---
name: protocol-training-deck
description: 依据临床试验方案（可附日志卡、项目流程材料），为 CRC/CRA/项目组制作“研究方案及操作培训”HTML 幻灯片：浅色康哲品牌风格，每页单独设计的分步动画 scene（按键推进，不自动播放），正反例并列，方案原文在页面旁注或下钻弹层中给出，每一步配逐字稿并在演讲者窗口（S 键）中显示。引擎、品牌资产、组件、兜底 SVG 和 QA 脚本都已内置，不需要 html-ppt 或 kangzhe-design 技能。适用请求：方案培训、启动会培训、研究方案及操作培训、protocol training、SIV 培训、CRC/CRA 培训 PPT、方案执行操作手册。
---

# 研究方案及操作培训 HTML 幻灯片

用这个技能把一份临床试验方案做成一套可放映的培训幻灯片，形式是一个离线可用的 `deck/index.html`。每页的标题区写阶段、访视和时间属性，强调句单独一行。正文是一个按步推进的 scene：先给方案规定，再演示正例、反例或复杂情形，配一句旁白。逐字稿在演讲者窗口里随步骤同步。

`examples/demo-study/` 是一个完整的虚构示例：研究 DEMO-301，26 页（20 个正文页，P1–P20 每种模式一页）。写任何页面之前，先运行 `python3 -I scripts/new_project.py /tmp/demo --example demo-study && cd /tmp/demo && python3 -I engine/build.py`，打开 `deck/index.html` 看效果，再读对应的 `content/pages/p_*.py`。

## 输入与输出

| | 内容 |
|---|---|
| 必需 | 临床试验方案（docx / pdf / md） |
| 可选 | 受试者日志卡、入组审核表、CRO/项目流程截图、实验室手册、ICF。只用于交叉核对和“项目流程”页 |
| 输出 | `<项目>/deck/`（index.html 及运行文件）、`<项目>/dist/*.zip`、`<项目>/plan/` 下的过程记录 |

## 硬规则（每一条都要做到；做不到就停下来问用户）

1. **方案是唯一事实来源。** 页面上的数字、时间窗、阈值、访视项目都要能在 `src/` 里找到原文。页面上直接引用的方案原文一律经 `Verbatim` 校验，下钻原文一律经 `Source` 锚点抽取，不手抄。
2. **只讲方案要求，不指挥运营。** 不写“你需要…”“务必…”“CRC 应当提前一天…”。方案外的做法要么不写，要么标 `[建议]`/`[操作建议]` 并说明理由；来自 CRO/项目的流程标“项目流程（CRO）”。
3. **标题区只写属性，强调句单独成行。** 标题区（META 第 2、3 项）写阶段、访视、第几天、窗口；强调句（META 第 4 项）写这页最该记住的一条规定，要有实质内容。
4. **页面清单按目录来，页数按方案来。** 固定页（F01–F28）按 `reference/page-catalog.md` 逐个判断是做、降级还是删；访视页和入排主题页按其中的生成规则从 SoA 推出来，不预设页数。
5. **每页单独设计。** 先用 catalog 给定的模式，再按本页内容改造构图。同一章内相邻两页不能用同一种主版式；全稿任何一种模式最多占 25%。
6. **规定类、流程类、访视类页面都要有正例和反例，或复杂情形。** 不能只演示成功路径。反例用红色，需要研究者判断的情形用琥珀色，正确做法用绿色。背景和研究信息页（F01–F08）可以不放反例，但至少放一个“容易混淆的点”。
7. **规定先于示例。** 涉及入排、窗口、阈值的页面，第 1 步先给方案原文或阈值，之后再进入示例。原文放在页面旁边，或者放进“方案原文”下钻里，也可以两处都放。
8. **不用工程化词，不用口语。** 禁用词见 `reference/copy-rules.md`，由 `scripts/check_project.py` 自动检查。“预筛”一律写“潜在受试者识别”。
9. **量表要写清内容和分级**，不能只写名称。异常值判“无临床意义（NCS）”时，必须写出判定理由。
10. **重点标记要克制。** 每张卡最多 2 处 `**加粗**`/`__下划线__`/`!!深红!!`/`^^高亮^^`，每页最多 4 处。
11. **逐字稿逐步对齐。** 每页写 1 段开场，再每步 1 段，段数必须等于步数。逐字稿是讲给人听的口语化讲稿，但不能用禁用词。
12. **最小字号 12px；不出现通长装饰色条；只用浅色风格。** 配色和 Logo 只用 `engine/` 里内置的那一套；Logo、页眉、页脚由引擎按康哲规范放置，页面代码不碰。康哲 design 与 html-ppt 的每条硬性要求如何落实、哪些是用户认可的豁免，见 `reference/brand-compliance.md`。
13. **不自动播放。** 用键盘、滑动或触控板逐步推进。翻页进入某页时，不能闪现该页上一次的状态。这一条由引擎保证，不要改 `sop2.js`。
14. **构建无 ERROR，QA 无新问题，并且逐页看过截图。** 自动检查通过不等于完成，截图检查清单见 `reference/visual-qc.md`。
15. **不确定就问。** 方案前后矛盾、口径不清、涉及 SAE 判定或越权风险时，先写进 `plan/conflicts.md`，再问用户，不要自行裁定。

## 分阶段工作流（逐阶段做，每阶段产出指定文件后再进入下一阶段）

| 阶段 | 读 | 做 | 产出（关卡） |
|---|---|---|---|
| G0 建项目 | 本文件 | `python3 -I scripts/new_project.py <项目目录>` | 项目目录、`plan/TASK.md` |
| G1 需求确认 | `workflow/00-intake.md` | 问用户 6 个问题，记录答复 | `plan/TASK.md` 的“口径”一节 |
| G2 方案挖掘 | `workflow/01-source-mining.md` | docx→md，按清单逐章摘取事实，与日志卡交叉核对 | `src/protocol.md`、`plan/facts.md`、`plan/conflicts.md`（矛盾已与用户确认） |
| G3 大纲 | `workflow/02-outline.md`、`reference/page-catalog.md` | 固定页逐个判定做/降级/删，从 SoA 和入排标准生成可变页，做差异性检查 | `plan/outline.md`、`content/meta.py` |
| G4 逐页设计 | `workflow/03-page-design.md`、`reference/patterns.md`、`reference/aesthetics.md` | 每页写设计卡：属性、强调句、逐步故事线、正反例、原文出处 | `plan/design.md`（每页一节） |
| G5 文案 | `workflow/04-copy.md`、`reference/copy-rules.md`、`reference/speaker-notes.md` | 页面文字、旁白、逐字稿 | `content/notes.py`、`content/orig.py` |
| G6 编码构建 | `workflow/05-build.md`、`reference/kit-api.md`、`reference/svg-fallback.md` | 编写 `content/pages/p_*.py`，运行构建和静态检查 | 构建 0 ERROR、`check_project.py` 0 ERROR |
| G7 QA | `workflow/06-qa.md`、`reference/visual-qc.md` | 自动 QA、逐页逐步看截图、独立事实核对 | `qa/report.json`、`plan/qa-log.md` |
| G8 交付 | `workflow/07-deliver.md` | 打包、离线复测，写交付说明 | `dist/*.zip`、交付说明 |

每完成一个阶段，在 `plan/TASK.md` 的状态表里打勾，并写一行“做了什么、产出在哪”。上下文被压缩或换会话后，先读 `plan/TASK.md` 再继续。

## 命令速查

第一条在任何目录执行（用技能目录里的脚本），其余都在**项目根目录**执行：

```bash
python3 -I <skill>/scripts/new_project.py <项目目录>                    # 新建（带 --example demo-study 可拷示例）
python3 -I scripts/docx2md.py <方案.docx> src/protocol.md                # 方案转文本（脚本已随项目拷入）
python3 -I engine/build.py                                              # 构建 → deck/index.html
python3 -I scripts/check_project.py                                     # 文案与结构静态检查（每次构建后都跑）
python3 -I scripts/qa.py                                                # 自动视觉 QA（ego lite）+ 截图 → qa/
python3 -I scripts/package.py                                           # 打包 → dist/
```

自动视觉 QA（详见 `qa/README.md`）：
- `python3 -I scripts/qa.py`：通过 ego-browser（ego lite，https://lite.ego.app/ ，macOS / Windows）逐页逐步检查，并给每页存一张最终态截图；`--shots 2` 另外每步各存一张，`--shots 0` 只出报告。退出码 0 = 通过，1 = 有问题（终端列出），2 = 没跑起来（按提示处理）。
- 机器上装不了 ego lite：在浏览器打开 deck，在控制台粘贴 `qa/deck-qa.js` 后运行 `await DeckQA.all()`；截图用 `await DeckQA.show(页, 步)` 后手动截。

## 文件地图

```
SKILL.md                 本文件（规则 + 流程）
README.md                给人看的说明、安装、许可
workflow/00–07           每个阶段的操作步骤、提问清单和模板
reference/
  requirements-retrospective.md  原始需求 → 通用规则 → 实现位置（规则的来历）
  page-catalog.md        固定页 F01–F28（取什么、怎么呈现、scene 分布）+ 访视页/入排页生成规则
  patterns.md            20 种页面模式：用途、构图坐标、逐步故事线、正反例写法、组件
  scene-storyline.md     每页、每章、全稿的故事线；正反例的多步展示模式
  aesthetics.md          配色语义、搭配、每页差异化
  typography.md          字号角色、间距、行高、卡片内边距
  copy-rules.md          标题、强调句、禁用词、重点标记、[建议] 标注
  speaker-notes.md       逐字稿规范、演讲者模式
  visual-qc.md           自动检查代码 + 人工截图清单
  svg-fallback.md        无法生图时的 SVG 画法
  image-generation.md    外部生图：何时生成、提示词、回执；无法生图时的处理
  brand-compliance.md    康哲 design / html-ppt 硬性要求逐条对照：执行、豁免、降级
  kit-api.md             Page / 组件 API
  runtime.md             放映按键、步骤引擎、下钻、目录、打印
  pitfalls.md            踩过的坑与对策
engine/                  构建器、组件、运行时、品牌资产（随项目拷贝，项目自带）
qa/                      页内 QA 库与运行器
scripts/                 new_project / docx2md / check_project / qa / package
templates/project/       新项目起始内容与 plan 模板
examples/demo-study/     完整虚构示例（DEMO-301）
```
