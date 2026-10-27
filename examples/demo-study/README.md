# 示例：DEMO-301（虚构）

一个虚构的Ⅲ期研究：XB-101 治疗中重度特应性皮炎，240 例，按 2:1 随机。示例用来演示技能的写法，研究、药物和申办者都不是真实的。

```bash
python3 -I <skill>/scripts/new_project.py /tmp/demo --example demo-study
cd /tmp/demo && python3 -I engine/build.py && open deck/index.html
```

示例共 26 页：封面、目录、4 个章节页和 20 个正文页，每个正文页演示一种模式，P1–P20 各一页。真实项目要按 `reference/page-catalog.md` 做全套，页数由方案决定。哪些固定页做了、哪些合并或省略，见 `plan/outline.md`。

`src/protocol.md` 是虚构方案；`src/review_guide.md` 是虚构的 CRO 入组审核资料要求，用来演示“非方案材料”怎么引用和标注来源。

| 页 | pid | 目录编号 | 模式 | 看点 |
|---|---|---|---|---|
| 4 | bg_disease | F01 | P1 | 四栏因果链，末栏绕回首栏的循环线；最后一步给出治疗需求和“中重度”的方案定义 |
| 5 | bg_drug | F02 | P17 | svgart 分层机制图、人形注射部位、器械 |
| 6 | study_info | F03 | P2 | 编号条、事实网格、按比例画的分组条 |
| 7 | scales | F06 | P3 | 2×2 量表卡逐张聚焦（on / is-dim）、分级条擦出 |
| 8 | overview | F07 | P4 | 分段拉伸的周轴，分期、访视、给药、采样逐层出现 |
| 9 | matrix | F08 | P5 | 访视 × 项目矩阵从同一份 SoA 数据生成，按行、按列聚焦并配问答卡 |
| 11 | v1_flow | F12 | P20 | 12 项蛇形排列，序号属于槽位；顺序陷阱用两项互换位置表示 |
| 12 | incl_easi | V1 入排主题页 | P6 | Verbatim 原文、阈值条、同人两时点、判定板 |
| 13 | excl_prior | F10 | P7 | 原文与解析逐句对齐，误读提示盖在被误读的那一句上 |
| 14 | washout_calc | F11 | P8 | 真实日期轴倒推；三种药物取最晚日期，D1 竖线随之移动 |
| 15 | screen_cal | F13/F16 | P9 | 日历、区间带、计数环、越界复查 |
| 16 | diary_form | F15 | P16 | 按原表格画日志卡，逐格填写；补填（错）→ 留空（对）→ 划线更正 |
| 17 | nrs_calc | F16 | P10 | 计算器：数字滚动、分母用错的算法反例、恰好等于阈值的边界值 |
| 19 | v4 | F20 | P11 | 清单先错后对、窗口落到日期、采血管 |
| 20 | dose_day | F18 | P12 | 关键帧位移和最后一步复原 |
| 22 | conmed | F24 | P18 | 三色分类栏，药物 chip 用 data-k 槽位逐个落入；反例 chip 先落错再纠正 |
| 23 | ae_judge | F25 | P19 | 四层漏斗，三个案例 token 停在各自的层；NCS 只写结论（错）→ 写明理由（对） |
| 24 | ae_flow | F26 | P13 | 决策流、三个 token 分路、案例卡同位轮换 |
| 25 | docs_pack | F14 | P15 | 散落资料归入 5 个文件夹、文件名、脱敏黑条；文件名含姓名的反例 |
| 26 | review_lanes | F14 | P14 | 泳道、信封 token、邮件界面、来源标注 |

第 12–17 页的数据互相衔接：日志卡那一周（diary_form）就是 screen_cal 的 5/7 天和 nrs_calc 的第一组数；washout_calc 用的条款就是 excl_prior 解析的那几句。真实项目也应该这样，让同一位示例受试者贯穿相关页面。
