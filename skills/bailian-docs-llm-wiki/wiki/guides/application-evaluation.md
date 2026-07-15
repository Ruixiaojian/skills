# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器协同、人工标签补充的混合机制，实现从数据构建、任务执行到归因分析的完整闭环，适用于模型迭代、知识库更新、Prompt调优等关键场景的质量验证。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，调用大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）完成端到端评分与归因分析，适用于单应用深度诊断或多应用横向对比 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：依赖人工构建的结构化评测集（XLS/XLSX 格式），由人工对模型输出进行打标（如“较差/一般/较好”），适合需强主观判断或高置信度校验的场景 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：支持**智能体**、**工作流**、**自定义**三类评测集，配合可插拔的**评估器**（LLM 或 Code 类型）与**标签管理**，实现灵活的多维度自动+人工混合评测 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
> **注意**：旧版自动评测（文档 1）与新版评测任务（文档 5）在架构上存在显著差异：前者为封闭式流程（知识库→生成评测集→固定模型打分），后者为开放式框架（评测集+评估器+标签自由组合）。两者共存但不兼容，新版不支持旧版的“RAG归因分析”能力，旧版亦无法使用新版的 Code 评估器或布尔值标签等功能。

## 关键参数

- **评测集类型**：  
  - `知识问答`（JSONL）：用于自动评测，含 `query`、`referenceAnswer`、`fineKeywords`、`coarseKeywords`、`queryType` 字段 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；  
  - `对话分析`（XLS/XLSX）：用于手动评测，含 `Prompt`、`Completion`、`SessionId` 字段；  
  - `智能体/工作流/自定义`：新版评测集类型，字段结构由应用出入参或用户自定义决定。  
- **评估器参数**：  
  - LLM 评估器需配置 `模型`、`Prompt`、`评分范围`（如 0–1 或 1–5）、`通过阈值`；  
  - Code 评估器需定义 `入参`（如 `query`, `response`）、`Python 执行函数`（返回数值评分）；  
  - 所有评估器必须完成**字段映射**（如将评测集的 `question` 字段映射至评估器变量 `query`），否则任务无法创建。  
- **标签类型**：支持分类（多选枚举）、布尔值（True/False）、数字（1–5 分）、文本（自由输入）四类，用于人工标注与统计分析 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备评测数据**：  
   - 自动评测：确保目标智能体已**发布**、**配置知识库**、**开通应用观测**；  
   - 手动评测：下载模板，按 `Prompt`/`Completion`/`SessionId` 填写 XLS/XLSX 文件并上传发布；  
   - 新版评测：创建评测集时选择类型（智能体/工作流/自定义），下载模板填写后上传，**必须发布**才可用于任务。  
2. **创建评测任务**：  
   - 旧版自动评测：在控制台依次完成「选择应用→选择知识库→生成评测集→配置采样数与模型→发起评测」；  
   - 新版评测任务：在任务创建页选择「评测集+版本」、「关联应用类型（智能体/工作流/不关联）」、「添加评估器（≤10个）并完成字段映射」、「配置标签」；  
   - 手动评测：在「手动评测」页面选择已发布应用与已发布评测集，进入标注流程。  
3. **执行与分析**：  
   - 自动评测结果直接生成总正确率、BadCase 归因（如“检索无效”“切片不完整”）及调优建议；  
   - 新版任务支持「数据明细」（查看每条评估器评分与人工标签）与「指标统计」（综合得分、各评估器通过率柱状图）；  
   - 手动评测需逐条点击「标注」，选择评价等级后保存。

## 限制和注意事项

- **应用限制**：自动评测仅支持**已发布的智能体应用**，且多应用横向评测时所有应用必须共享至少一个知识库 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；新版评测任务中，已发布的评测集若被任务引用则不可删除。  
- **模型与计费**：自动评测与 LLM 评估器均调用 `qwen-max`/`qwen-plus`，产生 [Token](../concepts/token.md) 费用；Code 评估器无额外调用成本；预估 [Token](../concepts/token.md) 消耗为参考值，实际以账单为准 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **配置不可变性**：评测任务创建后，其关联的评测集、应用、评估器映射关系**不可修改**；如需调整，必须新建任务 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **文件约束**：评测集上传支持 `.xls`/`.xlsx`（≤20MB/个，单次≤10个）或 `.jsonl`（知识问答专用）；新版自定义评测集支持任意表结构，但创建后类型不可更改。  
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限才能使用自动评测功能。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


