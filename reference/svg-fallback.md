# 兜底 SVG 画法（无法生图时）

没有生图能力，或者生成的图不能用时，用 `engine/svgart.py` 和 SVG 基本图形画示意图。目标是像教科书插图一样简洁的示意，不追求写实。

## 1. 风格约定

| 项 | 规定 |
|---|---|
| 填充 | 暖中性 `#F3EDE3`（主体）、`#FBF8F3`（背景区）、`#E7DCCB`（结构件） |
| 描边 | `#B9AE9C`，宽 2；次要描边 1.5 |
| 教学对象 | 品牌橙 `#FF9900`，填充用 `rgba(255,153,0,.28)` |
| 禁止 / 阻断 | 红 `#C00000`：× 标记、斜线阴影 |
| 允许 / 正确 | 绿 `#2F8A57` |
| 药物 | CRA 蓝 `#4A6D8C`，与通路的橙色区分 |
| 文字 | `#3D4046`，SVG 内 12–14，粗细 700；次要说明 400 |
| 形体 | 圆角矩形、圆、简单路径；人体无五官、无肤色、无性别特征 |
| 视角 | 正面或剖面；一张图只表达一件事 |

## 2. 现成函数（`from svgart import ...`）

| 函数 | 画什么 | viewBox | 用法 |
|---|---|---|---|
| `person(zones, blocked)` | 正面人形；`zones` 高亮部位，`blocked=('navel',)` 画脐周禁区 | 0 0 200 420 | 注射部位、检查部位；ZONES：abdomen、thigh_l/r、arm_l/r、chest |
| `skin_section(highlight)` | 皮肤剖面（表皮、真皮、皮下组织） | 0 0 400 200 | 皮下注射深度、皮肤病变层次 |
| `lungs()` | 双肺与气管 | 0 0 200 240 | 肺功能、哮喘 |
| `antibody(color, label)` | Y 形抗体 | 0 0 120 180 | 单抗类药物 |
| `moa_layers(ligands, receptor, drug, target_note)` | 机制分层：base、ligand、signal、drug | 0 0 520 300 | 逐步揭示机制 |
| `pen_injector()`、`vial(fill_level)` | 注射笔、药瓶 | 0 0 340 104 / 0 0 120 184 | 给药器械 |

放置：`p.el(x, y, w, h, svg, '')`，框的宽高比要接近 viewBox 的宽高比，否则会留白。

```python
from svgart import moa_layers, person
L = moa_layers(('IL-X', 'IL-Y'), 'IL-X 受体 α 亚基', 'XB-101', '人源化单抗（虚构）')
for key, step in (('base', 1), ('ligand', 1), ('signal', 1), ('drug', 2)):
    p.el(0, 60, 540, 312, L[key], '', s=step, fx='fade')
p.el(640, 60, 150, 315, person(zones=('abdomen', 'thigh_l', 'arm_r'), blocked=('navel',)), '', s=3, fx='fade')
```

## 3. 自己画新图（没有现成函数时）

在页面模块里写一个返回 SVG 字符串的小函数。如果多个页面都要用，就加进 `svgart.py`。

```python
def lesion_section():
    body = ('<path d="M40 20 C 90 40 110 120 100 180 L 40 180 Z" fill="#F3EDE3" stroke="#B9AE9C" stroke-width="2"/>'
            '<ellipse cx="78" cy="110" rx="16" ry="22" fill="rgba(255,153,0,.28)" stroke="#FF9900" stroke-width="2"/>'
            '<text x="104" y="112" font-size="13" font-weight="700" fill="#3D4046">病变部位</text>')
    return f'<svg viewBox="0 0 200 200" style="width:100%;height:100%;overflow:visible">{body}</svg>'
```

步骤：
1. 先在纸上（或在注释里）定 viewBox，例如 0 0 400 240，宽高比与准备放置的框一致。
2. 先画结构（中性色），再画教学对象（橙），最后画标注（文字、引线）。
3. 文字标签放在留白处：左侧标签用 `text-anchor="end"`，右侧用 `start`；离连线、箭头至少 10 个单位。
4. 需要分步出现时，拆成几个同 viewBox 的 SVG，叠在同一个框里，分别设置 `s`。
5. 阻断画红色 ×（两条交叉线，宽 5，圆头）；禁区用斜线图案（参考 `person` 的 `sa-hatch`，图案 id 要唯一）。

## 4. 常用基本图形

| 想表达 | 画法 |
|---|---|
| 细胞膜 / 屏障 | 横向圆角矩形 (h≈22)，下方淡色区表示细胞内 |
| 受体 | 膜上的拱形 + 穿膜小矩形 |
| 配体 | 小圆 + 虚线箭头指向受体 |
| 信号 | 粗箭头（宽 5）穿入细胞内 |
| 时间流程 | 用 `day_axis`/`time_axis`，不要在 SVG 里手画刻度 |
| 器官 | 1–2 条贝塞尔曲线闭合，填暖中性色 |
| 计量 | `gauge()` 圆环、`threshold_bar()` 阈值条 |
| 样本 | `tube_html()` 采血管 |

## 5. 检查

- 截图看：标签不压线、不出框；分步揭示时，层与层对齐。
- SVG 内 `<text>` 的字号 ≥12。
- 页面里有手绘 SVG（`<circle>` 或 `<g>`）时，构建会跳过旁白自动收紧（WARN `autofit skipped (hand-drawn svg)`）。这时要手动核对旁白卡的高度。
