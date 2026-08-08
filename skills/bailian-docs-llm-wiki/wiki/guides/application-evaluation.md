# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持从自动打分到人工标注的全链路质量验证。它既可通过大模型基于知识库自动生成评测集并完成端到端评分（自动评测），也支持开发者上传结构化评测集、配置多维评估器与人工标签进行精细化分析（新版评测任务）。评测结果直接驱动 RAG 流程优化与版本迭代决策。

## 支持的模型/功能

- **自动评测**：面向已发布的智能体应用，依赖知识库自动生成评测集，支持单应用深度诊断与最多 8 个应用的横向对比。仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测（旧版）**：基于人工构建的 Excel 格式评测集（`.xls`/`.xlsx`），通过人工打标产出报告，适用于对话分析类场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测任务**：统一评测入口，支持智能体、工作流、自定义三类应用；可组合使用预置/自定义 LLM 或 Code 评估器（最多 10 个），并叠加人工标签实现多维评价 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **评测集类型**：明确区分「对话分析」（Excel，含 `Prompt`/`Completion`/`SessionId`）与「知识问答」（JSONL，含 `query`/`referenceAnswer`/`fineKeywords`/`coarseKeywords`）两类数据格式，分别适配人工与自动评测路径 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **评估器体系**：提供通用质量、智能体专项、文本匹配等预置模板；支持自定义 LLM 评估器（需指定模型与 Prompt）和 Code 评估器（Python 脚本），并支持基于历史人工标注任务反向生成 LLM 评估器 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

> **注意**：文档 4（新版评测集）与文档 3（评测集）对评测集类型的定义存在不一致——前者将评测集分为「智能体」「工作流」「自定义」三类（按应用形态划分），后者则按数据语义划分为「对话分析」与「知识问答」两类。实际使用中，**评测集类型应以数据格式和用途为准**：JSONL 知识问答集专用于自动评测流程；Excel 对话分析集用于人工打标或新版任务中的非 RAG 场景。创建时需确保格式与后续评测方式匹配，否则会导致字段映射失败或评分逻辑异常。

## 关键参数

- **评测集字段**：自动评测要求 JSONL 中必须包含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords` 和 `queryType`；手动评测及新版任务中 Excel 需含 `Prompt` 和 `Completion` 字段；新版评测集若选「智能体」类型，系统会根据应用出入参自动生成模板字段。
- **采样与规模**：自动评测中「分类采样数」控制各任务类型（事实型/分析型等）抽取问题数量，直接影响 [Token](../concepts/token.md) 消耗与评测时长；新版评测任务无全局采样控制，但可通过评测集版本选择限定数据范围。
- **评估器参数映射**：所有变量（如 `query`, `response`, `reference`）必须在评测任务中完成字段映射，否则无法保存任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型**：支持分类、布尔值、数字、文本四类，影响标注方式与筛选能力；数字标签常用于 1–5 分制评分，布尔值标签适用于「是否正确」等二元判断 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据**：  
   - 自动评测 → 确保智能体已发布、配置知识库、开通应用观测 → 进入[自动评测](https://bailian.console.aliyun.com/?&tab=app#/efm/app_evaluate/tabs)界面创建任务，系统基于知识库生成 JSONL 评测集。  
   - 新版评测任务 → 先创建评测集（支持手动上传 Excel/JSONL 或从应用观测导入）→ 再创建评测任务，关联评测集、应用及评估器/标签 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
   - 手动评测（旧版）→ 下载 Excel 模板填写 `Prompt`/`Completion` → 上传并发布为「对话分析」评测集 → 在手动评测页面选择该集并启动人工打标 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

2. **配置评测逻辑**：  
   - 自动评测：设置任务类型（事实型/教程型等）、生成模型（`qwen-max`/`qwen-plus`）、采样数、评测模型。  
   - 新版评测任务：添加评估器后，严格完成参数到评测集字段的映射；添加标签后，在任务详情页启用「快速标注」模式提升效率 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

3. **执行与分析**：  
   - 自动评测完成后，报告包含总正确率、BadCase 归因（如「检索无效」「切片不完整」）及调优建议。  
   - 新版评测任务在「指标统计」页查看综合得分、各评估器通过率及标签分布；「数据明细」页支持逐条标注与筛选。

## 限制和注意事项

- **权限与状态**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限；所有评测任务均要求应用处于「已发布」状态，草稿评测集不可用于评测 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **资源约束**：自动评测单次最多支持 8 个应用横向对比；评测集文件大小上限为 20MB，格式仅限 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答） [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **[Token](../concepts/token.md) 消耗**：自动评测与新版评测任务调用大模型均产生 [Token](../concepts/token.md) 费用，预估消耗仅为参考，实际以账单为准；Code 评估器无额外费用 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **不可逆操作**：评测任务创建后配置不可修改（应用、评测集、评估器映射）；评测集发布后类型不可更改；删除被引用的评估器或评测集将失败 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **归因局限性**：自动评测的 BadCase 归因（如「模型理解有误」）是启发式推断，需结合原始输入与输出人工复核，不可完全替代领域专家判断 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


