# LiZhou BaZi · 观象知易

可复核的中文传统术数 Agent Skill：本地计算排盘，模型结合来源解释。

支持Codex插件安装，并提供豆包、DeepSeek、Grok、腾讯元宝等可读取的通用提示词。用于传统文化学习、娱乐与自我反思，不宣称具有经科学验证的命运预测能力。

## 功能

| 模块 | 已实现范围 |
|---|---|
| 八字 | 公历1901–2099、UTC+08:00标准时的四柱、藏干、十神、纳音及可选大运 |
| 六爻卦象 | 六次6/7/8/9记录生成本卦、动爻、之卦；不含完整纳甲装卦 |
| 梅花易数 | 固定三数报数、本卦、结构互卦、之卦及体用 |
| 紫微、奇门、六壬等 | 可靠已有盘面的文化解读与文献讨论；不含自动排盘引擎 |
| 文献 | 26项古今代表书目及实际查阅层级、官方历法资料，非著作全集 |
| 跨模型 | 自包含提示词和输入协议；不会为普通聊天产品增加代码执行权限 |

## Codex安装

```powershell
git clone https://github.com/pursuer1130-max/lizhoubazi.git
cd lizhoubazi
codex plugin marketplace add . --json
codex plugin add guanxiang-divination@guanxiang-local --json
```

也可完整下载仓库后运行`安装到Codex.ps1`。需要已安装的Codex CLI。保留来源文件夹以供刷新；同名来源已存在时先核对位置。

安装后输入：

> 使用 $guanxiang-divination，帮我看八字，先收集必要信息。

或：

> 使用观象知易，用梅花报数法分析“本月如何安排学习”，三个数是12、25、9。

技能清单未刷新时重新打开Codex。仓库名为`lizhoubazi`，技能调用标识为`guanxiang-divination`。

## 豆包、DeepSeek、Grok、腾讯元宝等

复制[通用系统提示词](portable/通用系统提示词.md)完整正文作为新对话的第一条消息，再发送问题和资料。API可将规则放入`system`、输入放入`user`，以服务商当前文档为准。

规则自包含。不能运行代码时，可复核简单起卦算术；复杂历法需先由可靠工具生成命盘。外部平台未在本项目逐一登录实测，文本适配不等于原生插件导入。见[多模型说明](docs/多模型使用说明.md)。

## 输入

- 八字：公历/农历、出生年月日、时间及精度、城市、当时时区和夏令时；农历另需闰月。本地脚本直接接受核验后的公历东八区标准时；未知时辰不补猜。
- 六爻：明确问题、期限、由初爻到上爻六次6/7/8/9，不需生日。
- 梅花：问题、期限、三个正整数，不需生日。
- 其他体系：可靠完整盘面、来源/流派和必要口径。

不需要真名、身份证、详细住址或照片。见[输入规范](codex-plugin/skills/guanxiang-divination/references/input-contract.md)。

## 离线运行与测试

Python3.10+；MIT许可的lunar-python 1.4.8源码随包提供，运行无需pip、网络或API密钥。

```powershell
python -X utf8 codex-plugin/skills/guanxiang-divination/scripts/divination.py --input examples/八字输入示例.json
python -X utf8 codex-plugin/skills/guanxiang-divination/scripts/divination.py --input examples/六爻输入示例.json
python -X utf8 codex-plugin/skills/guanxiang-divination/scripts/divination.py --input examples/梅花输入示例.json
python -X utf8 tests/test_calculations.py
```

示例均为虚构测试资料。计算输出是历法与传统符号数据，解读和现实判断应分别说明依据。

## 12,000例公开排盘样本测试

已运行12,000个不同出生时刻的公开计算样本：全部完成；来源标签一致11,794例（98.2833%）。206例差异均符合交节当天整日/精确时刻的口径不同。统一口径后，另一套sxtwl实现复核12,000例四柱均一致。

它只验证选定条件下的计算实现，不是12,000名真人的命运预测验证，也不是12,000次模型解读评测。见[测试摘要](docs/benchmark.md)及[机器可读结果](docs/benchmark-summary.json)。本仓库只发布摘要，不重新分发原始案例集。

## 目录

- `codex-plugin/skills/guanxiang-divination/`：技能、方法资料和离线工具。
- `codex-plugin/.codex-plugin/plugin.json`：兼容插件清单。
- `.agents/plugins/marketplace.json`：本地市场入口。
- `portable/`：其他模型可读取的自包含提示。
- `examples/`、`tests/`：输入示例、计算回归测试。
- `docs/`：来源、测试摘要与同类项目对照。

## 来源和许可

原写指令、脚本和文档采用[MIT](LICENSE)。随包历法来自[6tail/lunar-python](https://github.com/6tail/lunar-python)，保留[MIT许可证](codex-plugin/skills/guanxiang-divination/scripts/vendor/LICENSE)及[固定版本来源记录](codex-plugin/skills/guanxiang-divination/scripts/vendor/PROVENANCE.json)。其他书籍、网页、平台与参考数据保留各自权利。

[文献记录](docs/文献查阅与来源.md)区分原文选段、提要和目录，未将目录核查写成通读。GitHub已有类似工具，见[同类项目对照](docs/related-projects.md)；本次发布未复制这些项目的代码。

## 使用边界

不预测死期或诊断疾病，不用命理替代投资、治疗、法律、录用等现实判断，不以恐吓推销改运。离线脚本不联网、不上传、不主动保存用户资料；向外部模型发送信息时适用该平台的数据条款。
