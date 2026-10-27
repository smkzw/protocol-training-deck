# G8 交付

## 1. 打包

```bash
python3 -I engine/build.py && python3 -I scripts/check_project.py && python3 -I scripts/package.py
```

`package.py` 先检查 index.html 中所有引用都是包内的相对路径（离线可用），再写 `deck/MANIFEST.sha256`，最后输出 `dist/<名称>_<日期>.zip`。

## 2. 离线复测

1. 把 zip 解压到一个新的空目录。
2. 双击 `index.html`（file://），翻完全部页面，确认没有坏图。再在项目根目录对解压目录跑一次自动 QA：`python3 -I scripts/qa.py --shots 0 --deck <解压出的文件夹>`，退出码应为 0（其中 `IMG_BROKEN` 为 0 说明图片都打包进去了）。这一步会覆盖 `qa/report.json`。
3. 按 S 确认演讲者窗口能打开，逐字稿同步。

## 3. 交付说明（给用户）

写清以下几点，不写过程：
- 产出位置：zip 路径、页数、章节结构；
- 放映方法：双击 index.html；→/← 逐步推进；S 演讲者窗口；O 总览；左侧悬停目录；“方案原文”下钻；
- 已验证：自动 QA 结果、截图复核范围、交互清单、内容核对的结论；
- 方案中需要用户知悉的问题：`conflicts.md` 中的条目及其裁定；
- 未验证、已知限制：例如 4:3 投影会裁切，某些浏览器未测试；
- 方案外内容：列出标了 `[建议]`的页面，便于用户复核。

## 4. 版本

- 用户要求的版本号写进 `content/project.py` 的 `html_title`，或写进打包名称。没有要求时，用日期区分版本。
- 每次交付在 `plan/TASK.md` 记一行：版本、日期、包路径、变更摘要。
