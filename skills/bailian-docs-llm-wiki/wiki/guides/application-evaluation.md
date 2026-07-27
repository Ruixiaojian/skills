# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。自动评测基于大模型与知识库自动生成评测集并完成端到端评分与归因分析；手动评测则依赖人工构建评测集并结合人工标注与自动化评估器进行多维度评价。二者均可集成至持续交付流程，支撑 Prompt、检索策略、知识库切片等关键环节的闭环优化。

## 支持的模型/功能

- **自动评测**：仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分，不支持其他模型 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **评估器类型**：支持 LLM 评估器（语义理解类）、Code 评估器（规则校验类）及预置模板（如问答相关性、格式校验、文本相似度等），可组合使用最多 10 个评估器 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
- **评测集类型**：支持三类结构化评测集——**智能体**（按智能体出入参自动生成模板）、**工作流**（适配工作流输入输出）、**自定义**（任意字段定义），取代旧版仅支持“对话分析”与“知识问答”的二分法 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
- **标签体系**：提供分类、布尔值、数字、文本四类标签，支持在评测任务与应用观测中复用，实现人工标注与自动评估协同 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 3 中定义的“知识问答”（`.jsonl`）与“对话分析”（`.xls/xlsx`）两类评测集仍有效，但仅适用于旧版自动/手动评测流程；新版评测集（文档 4）采用应用类型驱动的结构生成机制，二者共存但不兼容——旧版评测集无法直接用于新版评测任务，反之亦然。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集配置** | `queryType`、`coarseKeywords`、`fineKeywords` | 仅知识问答类评测集必需，用于任务分类与细粒度完整性校验；新版智能体/工作流评测集通过应用 Schema 自动推导字段，无需手动维护关键词 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数、评测模型、权重滑块 | 自动评测中需为每类任务（事实型/分析型等）指定采样数量；所有评测模型选择均限于 `qwen-max`/`qwen-plus`；权重滑块用于调整各维度对总分的影响 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md) |
| **评估器配置** | 参数映射、评分范围、通过阈值 | 所有变量必须完成映射（如 `query` → 评测集 `question` 字段）；评分范围（如 `0-1` 或 `1-5`）需与 Prompt 中指令严格一致；通过阈值决定 Pass/Fail 判定基准 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签配置** | 类型（分类/布尔/数字/文本）、筛选项、标注方式 | 分类标签最多支持 20 个选项；布尔值标签固定为 `True`/`False`；数字标签支持 `Double` 类型；文本标签上限 200 字 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备数据**：  
   - 若使用自动评测，需确保目标智能体已**发布**、**配置知识库**且已开通**应用观测**；若使用手动评测或新版评测任务，可上传 `.xls/.xlsx`（对话分析）或 `.jsonl`（知识问答），或通过新版评测集创建流程选择“智能体/工作流”类型自动生成模板。  
2. **创建评测任务**：  
   - 旧版路径：进入[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)或[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)页面，按向导完成任务创建；  
   - 新版路径：访问[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)，选择评测集、关联应用（智能体/工作流/不关联）、添加评估器并完成参数映射、配置标签。  
3. **执行与分析**：  
   - 自动评测任务发起后不可修改，支持试运行预览单条结果；  
   - 新版评测任务支持“快速标注”模式实时保存人工标签，并在“指标统计”页查看综合得分、各评估器通过率及数据分布；  
   - BadCase 归因分析（如“检索无效”“切片不完整”）仅在自动评测报告中提供，新版任务需依赖评估器组合与标签人工归因。

## 限制和注意事项

- **数量限制**：自动评测单次最多支持 8 个应用横向对比；评测集单次上传最多 10 个文件，单个 ≤20MB；每个评测任务最多添加 10 个评估器 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限方可使用全部功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **状态约束**：评测集必须**发布**后才能用于评测任务；已发布的评测集若被评测任务引用，则不可删除；评测任务创建后，应用、评测集等核心配置不可修改，仅可增补标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **计费说明**：LLM 评估器调用、自动评测中的模型推理均产生 [Token](../concepts/token.md) 费用；Code 评估器无额外费用；预估 [Token](../concepts/token.md) 消耗为参考值，实际以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **兼容性警告**：新版评测任务（文档 5）与旧版自动/手动评测（文档 1–3）为并行体系，评测集、评估器、标签均不互通；迁移时需重新创建评测集与任务，不可复用旧数据结构。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


