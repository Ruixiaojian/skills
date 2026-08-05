# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）和工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器协同、人工标签补充的闭环机制，帮助开发者量化应用表现、定位 RAG 流程瓶颈，并指导 Prompt、检索、知识库等关键环节的持续优化。该能力深度依赖应用观测（Application Observation）数据采集与知识库配置，适用于上线前验证、版本迭代对比及日常质量监控。

## 支持的模型/功能

- **自动评测**：基于大模型与知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比，内置归因分析（如“检索无效”“切片不完整”）并提供调优建议 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集（XLS/XLSX 格式），通过人工打标（如“较差/一般/较好”）产出定性报告，适用于需专家判断的业务场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可复用评估器（LLM/Code）、多维标签体系（分类/布尔/数字/文本），支持混合评估（自动评分 + 人工标注）[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评估器**：提供预置模板（如“问答相关性”“格式校验”）与自定义能力，LLM 评估器适用于语义理解类指标，Code 评估器适用于规则确定性判断，二者可组合使用以覆盖复杂质量维度 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

> **注意**：文档 4（新版评测集）与文档 3（评测集）存在类型定义冲突——文档 3 仅定义“对话分析”与“知识问答”两类，而文档 4 扩展为“智能体/工作流/自定义”三类，且字段结构由应用出入参动态生成。实际使用应以新版控制台为准，旧版文档中“知识问答”对应新版“智能体”类型，“对话分析”对应部分“自定义”场景。

## 关键参数

- **评测集类型**：决定数据结构与适用场景。`智能体`类型自动适配应用输入输出字段；`知识问答`（JSONL）要求 `query`/`referenceAnswer`/`fineKeywords` 等字段；`对话分析`（XLS/XLSX）需 `Prompt`/`Completion`/`SessionId` [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **评估器参数映射**：所有变量必须完成映射（如将评估器 `query` 参数映射至评测集 `question` 字段），否则无法创建评测任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **采样与权重**：自动评测中可设置各任务类型（事实型/分析型等）的采样数；新版评测任务支持为每个评估器配置权重，影响综合得分计算。
- **标签类型**：分类标签（枚举选项）、布尔值标签（True/False）、数字标签（1-5 分）、文本标签（自由描述），直接影响人工标注方式与统计维度 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据基础**：
   - 开通并启用 `应用观测` 功能，确保目标应用已加入观测列表；
   - 为智能体应用配置知识库（自动评测必需）；
   - 创建并发布评测集：可上传 XLS/XLSX（手动评测）、JSONL（自动评测）或通过新版控制台选择“智能体”类型自动生成模板。

2. **创建评测任务**：
   - **自动评测**：在控制台选择应用→指定知识库→生成评测集（仅 `qwen-max`/`qwen-plus`）→配置采样规则→发起评测 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；
   - **手动评测**：上传评测集→选择已发布评测集→人工逐条打标→提交生成报告；
   - **新版评测任务**：选择评测集与应用→添加评估器（配置参数映射）→添加标签→启动评测。

3. **分析与迭代**：
   - 查看自动评测报告中的 `BadCase 分析` 与 `归因分析`，定位 RAG 各环节问题；
   - 在新版评测任务详情页切换 `数据明细` 与 `指标统计`，结合评估器评分与人工标签交叉验证；
   - 基于结论调整 Prompt、知识库切分策略或检索配置，发布新版本后复用同一评测集进行回归验证。

## 限制和注意事项

- **应用状态限制**：自动评测与手动评测均**仅支持已发布的智能体应用**，草稿或未发布应用不可选 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **知识库约束**：多应用横向评测时，所有被选应用**必须关联至少一个相同的知识库**；自动评测依赖知识库生成评测集，无知识库则无法使用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限，否则无法访问评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **[Token](../concepts/token.md) 消耗**：自动评测与 LLM 评估器调用均产生 [Token](../concepts/token.md) 费用，预估消耗为参考值，实际以账单为准；`qwen-max`/`qwen-plus` 是当前唯一支持的评测模型 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评测集发布要求**：手动上传的评测集必须 `发布` 后才能用于评测任务，草稿状态不可用 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **配置不可变性**：评测任务创建后，其关联的评测集、应用、评估器配置均不可修改，如需调整须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


