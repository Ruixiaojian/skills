# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）与工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器打分、人工标签标注及归因分析，帮助开发者量化效果、定位问题并闭环优化。该能力深度集成于应用观测体系，要求应用已发布且配置[知识库](../concepts/knowledge-base.md)与观测功能。

## 支持的模型/功能

- **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行端到端评分，适用于已发布的智能体应用，依赖[知识库](../concepts/knowledge-base.md)生成评测问题 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式的对话分析评测集或 `.jsonl` 格式的知识问答评测集，通过人工打标产出报告 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，支持从应用观测导入真实数据，并提供字段级表结构编辑能力 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器（Grader）**：提供预置模板（如相关性、格式校验）及自定义 LLM/Code 评估器，支持参数映射与多评估器组合，实现自动化多维评分 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与指标统计，可复用于评测任务与应用观测 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 1（自动评测）明确限定生成评测集和执行评测时仅支持 `qwen-max` 和 `qwen-plus`；而文档 7（评估器）中“创建LLM评估器”步骤提到“评估模型限时免费”，未限定具体型号，且支持用户自主选择模型。二者存在模型范围不一致，实际使用中应以自动评测流程的硬性限制为准，即 `qwen-max`/`qwen-plus` 为唯一可用模型。

## 关键参数

- **评测集类型**：`对话分析`（`.xls`/`.xlsx`，含 `Prompt`/`Completion`/`SessionId` 字段）与 `知识问答`（`.jsonl`，含 `query`/`referenceAnswer`/`fineKeywords`/`coarseKeywords`/`queryType` 字段）必须严格匹配评测方式 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **任务类型**：自动评测默认支持“事实型”“分析型”“比较型”“教程型”，支持自定义；需在生成评测集时指定 2–8 种类型。
- **采样配置**：分类采样数（如事实型采样 5 条）决定最终评测样本量，直接影响 [Token](../concepts/token.md) 消耗与耗时。
- **评估器参数映射**：所有变量（如 `query`, `response`, `referenceAnswer`）必须完成字段映射，否则无法创建评测任务；映射错误将导致评分失败 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型与筛选条件**：分类标签支持“属于/不属于”，数字标签支持“大于/小于等于”等，直接影响指标统计粒度 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据**：  
   - 自动评测：确保智能体已发布、关联[知识库](../concepts/knowledge-base.md)、开通应用观测；  
   - 手动评测：下载模板，按格式填充 `.xls` 或 `.jsonl` 文件，上传后发布为“已发布”状态；  
   - 新版评测集：可手动上传或从应用观测导入，支持增量导入与版本管理。

2. **创建评测任务**：  
   - 自动评测：在控制台选择应用→知识库→生成评测集→配置采样与模型→发起评测；  
   - 手动评测：选择已发布应用与评测集→配置评测维度→开始评测→人工打标；  
   - 新版评测任务：选择评测集与应用类型（智能体/工作流/不关联）→添加评估器（需完成参数映射）→添加标签→完成创建。

3. **执行与分析**：  
   - 自动评测：查看总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效/切片不完整/未获取知识）、调优建议；  
   - 手动评测：在“标注”界面逐条对比并打分（较差/一般/较好），提交后生成报告；  
   - 新版任务：在“数据明细”页切换普通/快速标注模式，在“指标统计”页查看综合得分、各评估器通过率及标签分布。

## 限制和注意事项

- **应用状态限制**：所有评测方式均要求智能体应用处于“已发布”状态；草稿或未发布应用不可选 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **数量上限**：自动评测单次最多支持 8 个应用横向对比；评测集单次上传最多 10 个文件，单个 ≤20MB；每个评测任务最多添加 10 个评估器 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **知识库约束**：多应用横向评测时，所有被选应用必须关联至少一个**相同的知识库**；若选用“选择已有评测集”，其参考答案必须能在当前指定知识库中召回，否则结果失真 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限方可使用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **不可修改性**：评测任务创建后，应用、评测集、评估器映射等核心配置不可修改；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **[Token](../concepts/token.md) 计费**：自动评测、手动评测推理、评估器调用均产生 [Token](../concepts/token.md) 消耗，费用按实际用量结算；预估消耗仅为参考，最大消耗为硬性成本上限 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


