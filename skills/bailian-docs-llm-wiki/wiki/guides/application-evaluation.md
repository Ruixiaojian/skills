# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体、工作流等应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器协同、人工标签补充的混合机制，实现从数据构建、任务执行到归因分析的全链路质量闭环。该能力既可用于上线前的效果验证，也适用于迭代过程中的回归测试与持续监控。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，利用大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）完成问答类任务的端到端评分与归因分析，详见 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集并进行人工打标，适用于需主观判断或缺乏标准答案的场景，如多轮对话分析 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，并支持评估器（LLM/Code）、标签（分类/布尔/数字/文本）与评测任务的灵活组合，构成可扩展的质量评估框架 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器能力**：提供预置模板（通用质量、智能体、文本匹配等）及自定义 LLM/Code 评估器，支持参数映射与试运行验证 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

> **注意**：文档 1 和文档 4–7 描述的评测体系存在版本差异。文档 1（自动评测）属于旧版统一入口，而文档 4–7 构成新版模块化评测体系（评测集 → 评估器/标签 → 评测任务）。新版不强制依赖知识库，也不限定仅支持智能体应用；旧版则明确要求“已发布且配置知识库”的智能体应用。实际使用中，应根据控制台当前界面选择对应路径——若页面含“返回旧版”按钮，则新版为主流；否则以旧版为准。

## 关键参数

| 参数类别 | 名称 | 说明 | 来源约束 |
|----------|------|------|----------|
| **评测集字段** | `query` / `referenceAnswer` / `fineKeywords` / `coarseKeywords` | 知识问答型评测集必需字段，用于自动评分与归因分析 | [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评估器参数** | `query`, `response`, `context`, `reference_response` | LLM/Code 评估器的输入变量，需在评测任务中显式映射至评测集字段或应用输出 | [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签类型** | 分类、布尔值、数字、文本 | 定义人工标注维度，影响指标统计与筛选逻辑 | [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |
| **采样与规模** | 分类采样数（事实型/教程型等）、评测总数 | 控制自动评测的样本量，直接影响 [Token](../concepts/token.md) 消耗与结果代表性 | [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md) |

## 使用方式

1. **准备评测数据**  
   - 自动路径：选择已发布且配置知识库的智能体应用 → 基于知识库生成知识问答型 `.jsonl` 评测集（仅限旧版自动评测）；  
   - 手动路径：下载 `.xls`/`.xlsx` 模板填写 Prompt/Completion/SessionId（对话分析）或构造 `.jsonl` 文件（知识问答）→ 上传并发布评测集；  
   - 新版路径：在[评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)页面选择“智能体/工作流/自定义”类型，按应用出入参生成结构后导入数据。

2. **配置评估能力**  
   - 创建评估器：选用预置模板或自定义 LLM（指定模型、Prompt、评分范围）或 Code（编写 Python 函数）评估器；  
   - 创建标签：定义分类（如“回答质量：较差/一般/较好”）、布尔值（如“是否存在幻觉”）等标注维度。

3. **发起评测任务**  
   - 旧版：在自动评测界面依次完成“创建任务→设置评测集→配置规则→执行”，或在手动评测界面选择应用+评测集+维度后启动；  
   - 新版：在[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)页面关联评测集、应用（智能体/工作流/不关联）、评估器（≤10个）与标签，确认后启动。

4. **分析与迭代**  
   - 查看报告：旧版提供总正确率、BadCase 归因（模型理解/重排/检索/切片/未获取知识）及调优建议；新版通过“数据明细”和“指标统计”页查看评估器得分、标签分布与综合仪表盘；  
   - 持续优化：依据归因或标签结果调整 Prompt、知识库切分策略、检索配置或模型选型，并复用同一评测集验证改进效果。

## 限制和注意事项

- **权限与状态要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；旧版自动评测要求应用已发布、已配置知识库、且已开通并加入[应用观测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；新版无此强依赖。
- **文件与规模限制**：评测集上传支持 `.xls`/`.xlsx`（≤20MB/个，单次≤10个）与 `.jsonl`；旧版自动评测最多支持 8 个应用横向对比；新版评测任务最多添加 10 个评估器。
- **[Token](../concepts/token.md) 消耗说明**：旧版预估消耗为参考值，实际以账单为准；`预估最大消耗` 是成本硬上限，实际极少达到；评测失败步骤仍计费 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **评测集兼容性**：旧版自动评测仅接受知识问答型 `.jsonl`；手动评测仅接受对话分析型 `.xls`/`.xlsx`；新版支持三类评测集，但类型创建后不可修改。
- **版本共存风险**：旧版（文档 1–3）与新版（文档 4–7）功能并存，但评测集结构、任务配置逻辑与归因能力不互通。混用可能导致评测集无法被新版任务识别，或旧版无法加载新版创建的评估器。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


