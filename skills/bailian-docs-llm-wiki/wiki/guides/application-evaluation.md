# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，涵盖自动评测、手动评测、评测集管理、评估器与标签体系四大模块。它支持从知识库自动生成评测数据、多维度自动打分、人工标注协同分析，并提供归因诊断与调优建议，帮助开发者持续优化 RAG 流程与 [Prompt 工程](../concepts/prompt-engineering.md)效果。

## 支持的模型/功能

- **自动评测**：基于 `qwen-max` 和 `qwen-plus` 模型生成评测集并执行端到端评分，仅支持已发布且配置知识库的智能体应用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析类评测集，通过人工打标（如“较差/一般/较好”）产出定性报告 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可复用评估器（LLM/Code/基于任务生成）及多类型标签（分类/布尔/数字/文本），实现自动+人工混合评测闭环 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器能力**：预置通用质量、智能体专项、文本匹配等模板；支持自定义 LLM 评估器（需指定模型与 Prompt）和 Code 评估器（Python 函数校验）[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档 1 明确限定自动评测仅支持 `qwen-max` 和 `qwen-plus`；而文档 7 中“创建LLM评估器”章节提及“评估模型限时免费”，未限定具体型号，且未说明是否与自动评测共享同一模型池。实际使用中应以文档 1 的约束为准，避免因模型不兼容导致评测失败。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **评测集** | `queryType`, `referenceAnswer`, `fineKeywords`, `coarseKeywords` | 知识问答型评测集必需字段，用于大模型比对与归因分析 | `fineKeywords` 必须为嵌套数组格式（如 `[["信息点1"],["信息点2"]]`）[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **采样控制** | 分类采样数（事实型/教程型/比较型/分析型） | 决定各任务类型实际参与评测的问题数量 | 单类型最高支持 8 个样本，总评测数 ≤ 8 × 类型数 |
| **评估器映射** | `query`, `response`, `reference` 等变量映射 | 将评测集字段或应用输出绑定至评估器输入参数 | 所有变量必须完成映射才能保存评测任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签类型** | 分类/布尔/数字/文本 | 定义人工标注维度，影响指标统计粒度 | 布尔标签仅支持 `True`/`False`/`Pass` 三值选项 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备评测数据**：  
   - 自动场景：在[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)中选择已发布智能体及关联知识库，由 `qwen-max`/`qwen-plus` 自动生成知识问答型评测集；  
   - 手动/混合场景：上传 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答）文件，或通过“从应用观测导入”复用线上真实请求 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  

2. **配置评测任务**：  
   - 旧版：按“创建任务→设置评测集→配置规则→执行评测”四步流程操作，支持单/多应用横向对比；  
   - 新版：在[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)中选择评测集、关联智能体/工作流、添加评估器（≤10个）并完成参数映射，支持“不关联应用”纯人工标注模式。  

3. **执行与分析**：  
   - 自动评测：查看总正确率（≥4分占比）、BadCase 归因（如“检索无效”“切片不完整”）及调优建议；  
   - 新版任务：在“数据明细”页切换普通/快速标注模式，在“指标统计”页查看各评估器通过率与标签分布图。  

## 限制和注意事项

- **权限与依赖**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测强制要求开通 `应用观测` 功能且目标应用已加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **知识库强约束**：多应用横向评测时，所有被选应用**必须共享至少一个知识库**；自动评测生成的评测集内容严格依赖所选知识库的完整性与切分策略 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **评测集版本不可逆**：评测集类型（智能体/工作流/自定义）创建后不可修改；已发布的评测集版本无法删除，仅能通过“增量导入”或“全量覆盖”更新 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
- **费用与 [Token](../concepts/token.md) 预估**：自动评测与新版评测任务均产生模型调用费用；文档 1 多次强调“预估平均消耗为参考值，最终用量以实际账单为准”，且“预估最大消耗”是防超支硬上限，非预期消耗值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


