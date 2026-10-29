# GitHub 同类项目对照

核查日期：2026-10-29。结论：GitHub 上已有多种相近的传统术数 skill，观象知易不是该类别的首个项目。

本次通过 GitHub 连接器实际读取以下仓库的 README、部分技能或依赖文件及许可证；没有安装或运行这些第三方项目。因此表中功能与宿主支持是**仓库当前声明**，不是本次完成的运行验收，也不代表预测效力已获验证。

| 项目 | 仓库声明的主要能力 | 运行依赖与宿主声明 | 许可证核验 | 与观象知易的关系 |
|---|---|---|---|---|
| [keenone/bazi-skill](https://github.com/keenone/bazi-skill) | 四柱八字、藏干十神、纳音、大运与 HTML 命盘；附传统典籍规则摘要 | Python 3.8+、`lunar_python`；README 以 Claude Code 的全局或项目技能目录安装为主 | [LICENSE](https://github.com/keenone/bazi-skill/blob/main/LICENSE) 实际存在，MIT，版权行署名 jinchenma94 | 同样采用脚本排盘、模型解释；该项目聚焦八字与可视化 |
| [HeiGeAi/HeiGe-SuanMing](https://github.com/HeiGeAi/HeiGe-SuanMing) | 八字、紫微、梅花、六爻纳甲、奇门及独立数字结构分析；支持 JSON 与 HTML 报告 | `requirements.txt` 固定 `lunar_python==1.4.8`；声明可由能读取文件并调用 Python 的 Agent 使用，README 含 Codex、Cursor 等接入方式 | [LICENSE](https://github.com/HeiGeAi/HeiGe-SuanMing/blob/main/LICENSE) 实际为 PolyForm Noncommercial 1.0.0；商业用途需要另行授权 | 方法覆盖更广；非商业许可与本项目的 MIT 发布方式不同。README 顶部作者说明暂不再继续更新 |
| [mingze21/bazi-ziwei-skill](https://github.com/mingze21/bazi-ziwei-skill) | 八字、紫微及两体系对照；Markdown 报告与单文件 HTML 海报 | Node.js 18+；算法目录依赖 `lunar-typescript`，开发构建使用 TypeScript；README 明确列出 Codex、Claude、Cursor、Hermes、OpenClaw 等 | [LICENSE](https://github.com/mingze21/bazi-ziwei-skill/blob/main/LICENSE) 实际存在，MIT；另有 Yiqi 核心来源说明 | 同属带本地算法的跨 Agent 技能，更侧重八字与紫微对照及可视化 |
| [clider0915/divination-skills](https://github.com/clider0915/divination-skills) | README 列八个体系；紫微、奇门与六爻有脚本入口，八字等主要为模型解释框架 | `requirements.txt` 含 `lunar_python>=1.4.8,<2` 与 `tzdata>=2024.1`；主要演示 OpenClaw，亦提及 Claude、GPT 等 Agent | README 声称 MIT，但本次读取根目录 `LICENSE` 返回404，实际根目录清单也未见独立许可文件；**许可条款仍需进一步核实** | 可作为多方法路由的比较对象；不能仅凭 README 标签认定所有脚本和上游素材均已充分获许可 |

## 读资料时要区分的事项

1. 支持 `SKILL.md` 的 Agent，通常还必须具备文件访问、对应运行时和执行权限；普通聊天产品粘贴提示词不会获得这些能力。上述宿主声明均未在本次逐平台实测。
2. 某些仓库 README 写有排盘或解读准确率宣传，本次没有复现其评测，不采用这些百分比作为结论。多体系合参也不自动构成预测效果提升的证据。
3. 三个所查地址的 README 安装示例指向其他 owner 名称：keenone 的示例指向 jinchenma94，mingze21 的示例指向 dzcmemory-web，clider0915 的示例指向 mingkunyuan。这里只报告文件中的链接差异，不据此推断作者身份或代码来源关系；实际安装应先核对欲使用的上游地址与许可。
4. 本比较没有导入或复制这些项目的代码。观象知易的来源与依赖应以自身的第三方许可、文献记录和测试报告为准。

## 本次实际读取的依据

- keenone：[README](https://github.com/keenone/bazi-skill/blob/main/README.md)、[SKILL.md](https://github.com/keenone/bazi-skill/blob/main/SKILL.md)、[LICENSE](https://github.com/keenone/bazi-skill/blob/main/LICENSE)。README blob：`bc2c6e14abcb013b291af421ec83d95e5207d8fc`。
- HeiGeAi：[README](https://github.com/HeiGeAi/HeiGe-SuanMing/blob/main/README.md)、[SKILL.md](https://github.com/HeiGeAi/HeiGe-SuanMing/blob/main/SKILL.md)、[requirements.txt](https://github.com/HeiGeAi/HeiGe-SuanMing/blob/main/requirements.txt)、[LICENSE](https://github.com/HeiGeAi/HeiGe-SuanMing/blob/main/LICENSE)。README blob：`9637c947b99258e5d9d414b4fae317b91ecf9ff0`。
- mingze21：[README](https://github.com/mingze21/bazi-ziwei-skill/blob/main/README.md)、[calculator/package.json](https://github.com/mingze21/bazi-ziwei-skill/blob/main/calculator/package.json)、[LICENSE](https://github.com/mingze21/bazi-ziwei-skill/blob/main/LICENSE)。README blob：`11cd3d1ca8e91c6c0540fd439753b3e844cc876a`。
- clider0915：[README](https://github.com/clider0915/divination-skills/blob/main/README.md)、[requirements.txt](https://github.com/clider0915/divination-skills/blob/main/requirements.txt)、[根目录文件清单](https://api.github.com/repos/clider0915/divination-skills/contents)。README blob：`e0d3504dc4b641c0011e79972cb23a31b0139859`；独立 LICENSE 未核实。

这些项目的存在说明同类工具已经丰富；本项目应以清楚的计算范围、可复现的测试、可追溯的来源和完整许可证说明展示自身定位，不宜宣传“全网唯一”或“算命预测准确率100%”。
