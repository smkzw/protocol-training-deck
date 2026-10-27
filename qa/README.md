# 自动视觉 QA

`deck-qa.js` 是注入到页面里运行的检查库，任何浏览器自动化工具都能用。它会把每一页的每一步都检查一遍：
- 画布越界、文字溢出、文字重叠；
- 旁白溢出、标题压 Logo；
- 坏图；
- 逐字稿段数；
- 进页闪现。

检查代码的含义见 `reference/visual-qc.md`。

## 运行方式（在项目根目录执行）

| 环境 | 命令 | 说明 |
|---|---|---|
| ego lite（推荐，已验证） | `python3 -I scripts/qa.py` | 自动检查每页每步，并给每页存一张最终态截图 |
| ego lite，逐步截图 | `python3 -I scripts/qa.py --shots 2` | 另外每一步各存一张 `qa/shots/NN-k.png`，用来检查动画 |
| 装不了 ego lite | 打开 `deck/index.html` → 开发者工具 Console → 粘贴 `deck-qa.js` 全文并回车 → `await DeckQA.all()` | 手动；截图用 `await DeckQA.show(页, 步)` 后手动截 |

安装 ego lite：从 https://lite.ego.app/ 下载（macOS、Windows），打开后完成首次引导，引导会把 `ego-browser` 命令加到 PATH。装好后 `ego-browser --version` 能输出版本号即可。

`scripts/qa.py` 的退出码：0 = `summary` 为空（通过）；1 = 有问题，终端列出前 40 条；2 = 没跑起来（没装 ego lite、项目没构建，或者另一个 QA 正在驱动同一页面），按提示处理。`qa.py` 只是把项目路径拼到 `run-ego.mjs` 前面再交给 `ego-browser nodejs`，因为 ego-browser 不传递当前目录和环境变量。

输出：`qa/report.json`，即 `{slides, steps, summary, problems[]}`。终端只打印汇总。

## 判读

- `summary` 为空（`{}`）才算通过。菱形节点按内切正方形测量，不会误报。
- 自动检查通过之后，仍要按 `reference/visual-qc.md` §2 逐页看截图。
- 截图前 runner 已关闭缓存。如果改了 CSS 截图却没有变化，检查是否先重新构建了。
