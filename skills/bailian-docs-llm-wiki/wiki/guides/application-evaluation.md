# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体、工作流等应用输出质量的核心能力，涵盖自动评测、手动评测、评测集管理、评估器与标签体系四大模块。它支持从数据准备、任务执行到结果分析的全链路质量保障，既可通过大模型实现端到端自动评分与归因，也支持人工标注与规则化校验，适用于研发迭代、上线验证与持续监控等场景。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比，依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集及执行评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：通过人工构建 Excel 格式评测集（`.xls`/`.xlsx`），结合人工打标完成效果评估，适用于需强业务语义判断的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测任务**：统一支持智能体、工作流与自定义应用类型，可灵活组合 LLM 评估器与 Code 评估器进行多维度自动评分，并同步支持人工标签标注 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评估器体系**：提供预置模板（如相关性、格式校验）及自定义能力，LLM 评估器适用于语义理解类评测，Code 评估器适用于精确规则匹配，二者可共存于同一任务中 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与数据筛选，既可用于评测任务，也可直接应用于应用观测中的 Span 数据标注 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 3 与文档 4 对评测集类型的定义存在差异——文档 3 将评测集分为“对话分析”和“知识问答”两类，而文档 4 引入了“智能体”“工作流”“自定义”三类结构化类型。实际使用中应以新版控制台（文档 4、5、6、7）为准，旧版“知识问答”对应新版“智能体”类型评测集，“对话分析”则需通过“自定义”类型并手动配置字段实现。

## 关键参数

- **评测集字段要求**：不同评估器对字段有硬性依赖。例如，使用“问答相关性”预置评估器时，评测集必须包含 `query` 和 `response` 字段；若映射为 `Prompt`/`Completion`，需在参数映射中显式指定 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **模型选择限制**：
  - 自动评测的评测集生成与最终评分阶段均仅支持 `qwen-max` 和 `qwen-plus` [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；
  - 新版 LLM 评估器支持更广模型范围，但具体可用模型需在创建时下拉选择，且部分模型限时免费。
- **采样与权重**：自动评测中可通过滑块设置各任务类型（事实型、分析型等）的采样数；新版评测任务支持为每个评估器独立配置评分范围（如 0–1 或 1–5）与通过阈值。
- **[Token](../concepts/token.md) 消耗预估**：所有涉及模型调用的操作（生成评测集、执行评测、运行 LLM 评估器）均显示“预估平均消耗”与“预估最大消耗”，前者为参考值，后者为成本硬上限，实际用量以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 使用方式

1. **准备评测数据**：
   - 自动生成：在自动评测流程中，基于已配置的知识库，使用 `qwen-max`/`qwen-plus` 生成 `.jsonl` 格式知识问答评测集；
   - 手动上传：按模板准备 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答）文件，或使用新版“智能体”类型评测集，系统根据所选应用出入参自动生成表结构 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；
   - 从应用观测导入：将线上真实请求-响应数据直接导入评测集，提升评测真实性 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

2. **创建评测任务**：
   - 旧版自动评测：依次完成“创建任务→设置评测集→配置规则→执行评测”四步流程，支持试运行验证；
   - 新版评测任务：在任务创建页选择评测集、关联应用（智能体/工作流/不关联）、添加评估器（最多 10 个）并完成参数映射，再配置人工标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

3. **执行与分析**：
   - 自动评测完成后，报告包含总正确率、BadCase 归因（如“检索无效”“切片不完整”）、RAG 分项得分及调优建议；
   - 新版任务支持在“数据明细”页查看各评估器评分与人工标签，在“指标统计”页查看综合得分、通过率柱状图及数据分布。

## 限制和注意事项

- **应用状态要求**：自动评测仅支持**已发布**且**已配置知识库**的智能体应用；手动评测与新版评测任务虽支持未发布应用，但“智能体”类型评测集仍要求应用处于发布状态方可关联调用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **权限与观测依赖**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测强制依赖 `应用观测` 功能开通并添加目标应用至观测列表，评测期间关闭观测将导致失败或结果不准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评测集版本与引用约束**：评测集发布后生成新版本，创建任务时可指定版本；已发布的评测集若被评测任务引用，则无法删除 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **配置不可变性**：评测任务创建后，其关联的评测集、应用、评估器映射等核心配置不可修改，如需调整须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评估器试运行限制**：基于历史评测任务创建的评估器不支持试运行，需在实际任务中验证效果 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)




