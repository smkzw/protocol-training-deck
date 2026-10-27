# 外部生图（有能力时用）

康哲规范要求 hero 图（封面、目录、章节、尾页）和正文背景按本次主题生成，并在 `plan/qa-log.md` 登记回执（文件名、提示词、来源、sha256）。所以：
- 用户提供了生图能力（任意服务或技能）时，至少替换封面和章节页的 hero 图（`content/project.py` 的 `hero_images`），并登记回执；
- 没有生图能力时，沿用引擎内置的康哲参考图，在 `plan/qa-log.md` 记一条 WARN“hero 图复用内置参考图，未按主题生成”，交付说明里也写上；
- 正文里的示意图，只有确实需要真实感时才生图（内镜检查场景、喷鼻操作示范、注射部位的人体），默认用 `svg-fallback.md` 的 SVG 画法。

## 1. 什么时候值得生图

| 适合 | 不适合 |
|---|---|
| 操作场景（检查、给药姿势） | 数据、阈值、时间线（用组件画，可以逐步动画） |
| 解剖部位的整体感 | 需要精确标注的机制图（用 SVG，标签可控） |
| 封面、章节页的 hero 图（替换内置图时） | 含文字的图（生图文字不可靠） |

## 2. 提示词规则

- 风格：`clean medical illustration, flat soft shading, warm white background (#FFFFFF), light beige and soft orange accents, no text, no labels, no watermark`。
- 人物：写 `a fully clothed adult patient`、`wearing a hospital gown`。不要写会触发裸体判断的词（如 nothing、mannequin、bare），否则可能被服务端拒绝。
- 不出现真实人脸特写、品牌包装、可辨认的药品外观（研究药物包装以方案为准）。
- 构图留白：主体居中偏左或偏右，给标注留出空间；横图，宽高比与准备放置的框一致。
- 每张图的提示词和输出文件名存进 `plan/prompts/`，方便复现。

## 3. 接入页面

```python
p.el(0, 40, 520, 340, '<img src="assets/gen/endo.jpg" alt="" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply">', '', s=2, fx='fade')
```

- 图片放进 `content/assets/gen/`，构建时会拷到 `deck/assets/gen/`。
- 白底图加 `mix-blend-mode:multiply`，融进浅色背景。
- 标注仍用页面元素（`tag`、`p.wire` 引线）叠加在图上，不要依赖图里的文字。
- 生成的图要逐张看：比例、肢体、器械是否合理；不合理就重生成，或者回到 SVG。

## 4. 凭据安全

- 凭据只放在内存或环境变量里，不写进项目文件，不打印，不写进日志。
- 下载的生图技能包或凭据压缩包，解压到新的空目录；用完删除临时副本。
- 生图脚本放在项目 `scripts/` 之外，或者只读取环境变量。
