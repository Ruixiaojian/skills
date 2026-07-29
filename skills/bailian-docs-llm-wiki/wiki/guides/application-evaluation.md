# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）与工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器打分、人工标签标注及归因分析，帮助开发者量化效果、定位问题并闭环优化。该能力深度集成于应用观测体系，要求应用已发布且配置知识库（自动评测）或已接入观测（部分场景），是 RAG 应用调优的关键基础设施。

## 支持的模型/功能

- **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行端到端评分，适用于已发布的智能体应用，依赖知识库与应用观测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集（XLS/XLSX 格式），通过人工打标完成效果评估，适用于对话分析类场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，并支持从应用观测真实数据导入评测集，突破旧版仅限知识问答的限制 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器（Grader）**：提供预置模板（如相关性、格式校验、文本相似度）及自定义 LLM/Code 评估器，支持多维度自动评分；LLM 评估器需指定模型（评估模型限时免费），Code 评估器通过 Python 脚本实现确定性规则判断 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与多维统计分析，可复用于评测任务与应用观测模块 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 1（自动评测）明确限定生成评测集与执行评测均仅支持 `qwen-max` 和 `qwen-plus`；而文档 7（评估器）指出 LLM 评估器“选择模型下拉框”中可选模型未限定具体型号，且强调“评估模型限时免费”。二者存在模型范围不一致风险——实际使用中应以自动评测流程的硬性约束为准，即 `qwen-max`/`qwen-plus` 是当前唯一受支持的自动评测底座模型。

## 关键参数

- **评测集字段**：知识问答型评测集必需 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType` 字段（JSONL 格式）；对话分析型必需 `Prompt`、`Completion`、`SessionId`（XLS/XLSX 格式）[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **采样与权重**：自动评测中可通过滑块设置各任务类型（事实型、分析型等）的分类采样数；新版评测任务支持为每个评估器配置独立的评分范围（如 0–1 或 1–5）和通过阈值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **评估器映射**：在评测任务中添加评估器后，必须完成所有变量（如 `query`、`response`、`reference`）到评测集字段或应用输出的精确映射，否则任务无法创建 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型参数**：分类标签最多支持 20 个筛选项；数字标签支持 Double 类型；文本标签输入上限 200 字 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据**：  
   - 自动评测：确保智能体已发布、关联知识库、开通应用观测；  
   - 手动评测：下载模板，按 `Prompt`/`Completion`/`SessionId` 填写 XLS/XLSX 文件；  
   - 新版评测集：可手动上传（支持智能体/工作流/自定义类型），或从应用观测导入真实 Span 数据 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)、[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

2. **创建评测任务**：  
   - 自动评测：控制台 → 创建评测任务 → 选应用/知识库 → 生成或选评测集 → 配置采样与模型 → 发起；  
   - 新版评测任务：控制台 → 创建评测任务 → 选评测集版本 + 关联应用（智能体/工作流/不关联）→ 添加评估器（必配参数映射）+ 标签 → 完成 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

3. **执行与分析**：  
   - 自动评测：查看总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效/切片不完整/未获取知识）、RAG 分项得分；  
   - 手动/新版评测：进入任务详情页，使用“普通模式”或“快速标注”进行人工打标，结合评估器自动评分结果，在“指标统计”页查看综合得分、通过率、数据分布 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 限制和注意事项

- **应用状态限制**：自动评测仅支持**已发布**的智能体应用；手动评测与新版评测任务虽支持“不关联应用”，但若需调用应用推理，则仍要求应用处于发布状态 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **数量上限**：单次自动评测最多支持 8 个应用横向对比；单个评测任务最多添加 10 个评估器；单次上传评测集文件最多 10 个，单文件 ≤20MB [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评测集兼容性**：自动评测仅支持知识问答型（JSONL）评测集；手动评测仅支持对话分析型（XLS/XLSX）；新版评测集三类类型互不兼容，创建后不可修改类型 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)、[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **权限与观测依赖**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测强依赖应用观测功能开启，评测期间关闭观测将导致任务失败或报告不准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **[Token](../concepts/token.md) 消耗说明**：所有涉及大模型调用的操作（评测集生成、自动评测、LLM 评估器运行）均产生 [Token](../concepts/token.md) 费用；预估消耗为参考值，实际以账单为准；失败步骤的已消耗 [Token](../concepts/token.md) 仍计费 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)、[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


