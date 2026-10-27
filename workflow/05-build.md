# G6 编码与构建

目的：把设计卡写成 `content/pages/p_*.py`，然后构建出 `deck/index.html`。

## 项目结构

```
<项目>/
  src/protocol.md            方案文本（Verbatim / Source 的比对对象）
  content/
    project.py               DECK：封面标题、副标题、页脚、下钻来源说明、hero 图
    meta.py                  CHAPTERS / ORDER / META
    notes.py                 HERO_NOTES / NOTES（逐字稿）
    orig.py                  SRC（下钻原文）
    pages/p_<章>.py          页面函数；每个模块末尾 PAGES = [...]
    assets/                  自己的图片（构建时拷到 deck/assets/）
  engine/  qa/  scripts/     由 new_project.py 拷入，不要手改
  deck/                      构建产物，不要手改
  plan/  dist/
```

## 写一个页面

```python
from components import Page, icon, md, Verbatim, quote_card, alert, OK, BAD

q = Verbatim('src/protocol.md')

def screen_window():                    # 函数名 = pid = META 的键
    p = Page('screen_window', '')       # 第一个参数必须等于函数名；标题来自 META，这里留空
    quote_card(p, 0, 0, 540, 150, '筛选期 · 方案 4.1', q('筛选期最长28天。'), s=1)
    ...
    p.narr(0, 414, 1168, 106, ['第 1 步旁白', '第 2 步旁白', '第 3 步旁白'])
    return p

PAGES = [screen_window]                 # 放在模块末尾，放在所有函数定义之后
```

- 组件和参数见 `reference/kit-api.md`，版式坐标见 `reference/patterns.md`，示意图见 `reference/svg-fallback.md`。
- 每个元素都写 `s=`（第几步出现）。需要替换的写 `o=`（第几步消失），需要变化的写 `k={步: {...}}`。
- 一页的步数等于所有元素里出现过的最大步号，由引擎自动计算，所以逐字稿段数要对上。
- 先做一页，构建、截图、看过之后再批量做。照抄示例页的坐标前，先确认本页内容的长短。

## 构建

```bash
python3 -I engine/build.py          # → deck/index.html；有 ERROR 时退出码为 1
python3 -I scripts/check_project.py # 文案与结构静态检查
```

构建输出的含义：

| 输出 | 含义 | 处理 |
|---|---|---|
| `ERROR … in ORDER but has no META` 等 | 结构不一致 | 必须修 |
| `ERROR on-screen quote not found verbatim` | 页面引用与方案原文不一致 | 改成原文，或者换一句原文 |
| `ERROR … anchor not found` | 下钻锚点在方案中找不到 | 改锚点 |
| `ValueError …capacity…` | 封面、目录、章节页的文字超出版式容量 | 缩短标题或描述 |
| `WARN … script has N step paragraphs, page has M steps` | 逐字稿和步数不一致 | 必须修 |
| `WARN … header may overflow` | 标题区可能压到 Logo | 缩短标题或小字 |
| `WARN … lead longer than one line` | 强调句超过一行，会被截断 | 缩短 |
| `WARN … autofit skipped` | 旁白卡没有自动收紧 | 截图看旁白卡是否空，必要时手动调高度 |
| `WARN … no steps` | 页面不会逐步推进 | 补上 `s=` |

`check_project.py` 检查禁用词、“预筛”、指挥性措辞、重点标记密度、逐字稿段数、`[建议]` 标记格式、未替换的模板占位符【…】、旁白和逐字稿长度、页面文件是否引用了 Verbatim，以及最小字号。

## 本地预览

直接双击 `deck/index.html`（file:// 可用），或者在 `deck/` 下运行 `python3 -m http.server 8765`。放映按键见 `reference/runtime.md`。

## 关卡

构建 0 ERROR，**并且** `check_project.py` 0 ERROR（逐字稿段数不匹配在构建里只是 WARN，在 check_project 里是 ERROR，两个都要跑）。其余 WARN 要么修掉，要么在 `plan/TASK.md` 写明为何接受。
