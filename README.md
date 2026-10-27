# protocol-training-deck：研究方案及操作培训 HTML 幻灯片技能

给 Agent 一份临床试验方案（可附日志卡和项目流程材料），它会按本技能的流程做出一套离线可用的培训幻灯片：
- 浅色康哲品牌风格；
- 每页是单独设计的分步 scene，按键推进；
- 正反例并列；
- 方案原文在页面旁注或下钻弹层中给出；
- 逐字稿在演讲者窗口中逐步同步。

技能的通用需求和设计规则见 `reference/requirements-retrospective.md`。

## 安装

把整个目录放进 Agent 的技能目录，例如 `~/.claude/skills/protocol-training-deck/`，或者其他 Agent 约定的位置。也可以只把 `SKILL.md` 的路径告诉 Agent，让它照着做。

运行要求：
- Python 3.9 及以上（只用标准库）；
- 一个现代浏览器（Chrome / Edge / Safari）用于放映。

自动视觉 QA 用 ego lite（https://lite.ego.app/ ，macOS / Windows，免费）：`python3 -I scripts/qa.py`。装不了时可以在浏览器开发者工具里手动运行，见 `qa/README.md`。

不需要 html-ppt 或 kangzhe-design 技能：运行时、品牌资产和封面版式都已内置在 `engine/`。两套规范的每条硬性要求如何落实，见 `reference/brand-compliance.md`。

## 快速开始

```bash
S=~/.claude/skills/protocol-training-deck
python3 -I $S/scripts/new_project.py ~/work/demo --example demo-study   # 先看示例
cd ~/work/demo && python3 -I engine/build.py && open deck/index.html

python3 -I $S/scripts/new_project.py ~/work/my-study                    # 新研究
cd ~/work/my-study
python3 -I scripts/docx2md.py ~/Downloads/方案.docx src/protocol.md
# 然后让 Agent 按 SKILL.md 的 G1–G8 逐阶段推进
```

放映：
- → / ← 逐步推进；
- S 打开演讲者窗口；
- O 打开总览；
- F 全屏；
- 左缘悬停打开目录。

## 目录

| 路径 | 内容 |
|---|---|
| `SKILL.md` | Agent 的入口：硬规则、分阶段流程、命令 |
| `workflow/` | 每个阶段的操作步骤 |
| `reference/` | 页面目录、模式手册、故事线、配色、字号、文案、逐字稿、视觉 QC、SVG 兜底、生图、API、运行时、坑 |
| `engine/` | 构建器（Python）、组件、运行时（JS/CSS）、品牌资产 |
| `qa/` | 页内 QA 库与运行器 |
| `scripts/` | 新建项目、docx 转文本、静态检查、打包 |
| `templates/project/` | 新项目的起始内容和 plan 模板 |
| `examples/demo-study/` | 完整虚构示例 DEMO-301（26 页，20 个正文页覆盖全部 20 种模式） |

## 设计要点

- **固定页 + 可变页**：约 28 个固定页规定了取什么、怎么呈现、每步演什么；访视页和入排页从方案的流程表与入排标准推导，不预设页数。
- **代码生成页面**：每页是一个 Python 函数，坐标、步骤、关键帧都可以检查。构建器会检查结构、逐字稿段数、标题长度和原文一致性。
- **原文校验**：页面上的方案原文经 `Verbatim` 比对，下钻原文经 `Source` 按锚点抽取。对不上时构建失败。
- **项目自带引擎**：每个项目都拷一份 `engine/`，技能以后升级不会影响已交付的稿子。需要更新时运行 `new_project.py <项目> --update-engine`。

## 许可与品牌

- `engine/static/vendor/html-ppt/` 来自 html-ppt-skill，MIT 许可（见 `licenses/html-ppt-MIT.txt`）。`runtime.js` 含一处补丁：演讲者窗口逐步同步，主窗口无响应时自行翻页。
- `engine/static/kz/`、`engine/brand/`、`engine/static/assets/`（Logo、背景与 hero 图、双菱形标记）是**康哲药业内部品牌资产**，仅限康哲内部使用。外部使用前必须替换：
  - Logo：替换 `engine/static/assets/logo_bot.svg`；
  - 背景与 hero：替换 `engine/static/assets/body-quiet.webp` 和 `assets/hero/*.webp`，或在 `content/project.py` 的 `hero_images` 中指向自己的图；
  - 品牌色：修改 `engine/static/sop2.css` 开头的 `--c-brand` 等变量和 `kz/kz-tokens.css` 中的品牌色，以及 `components.py`、`svgart.py` 中的常量；
  - 双菱形标记：替换 `engine/brand/header-mark.svg`。
- 示例研究 DEMO-301、药物 XB-101 和申办者都是虚构的。
