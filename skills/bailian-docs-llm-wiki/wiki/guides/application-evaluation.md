# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）与工作流应用输出质量的核心能力，支持自动评测、人工标注、多维度评估器打分及标签化分析。它覆盖从评测集构建、任务执行到归因分析与调优建议的完整闭环，适用于 RAG 应用质量监控、版本对比与持续优化。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比，依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集与执行评分 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：通过人工构建 `.xls`/`.xlsx` 格式评测集（含 Prompt/Completion/SessionId 字段），进行端到端人工打标与效果分析 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：支持「智能体」「工作流」「自定义」三类评测集，并引入可配置的评估器（LLM 或 Code 类型）与多类型标签（分类/布尔/数字/文本），实现自动化+人工协同评测 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- > **注意**：文档 1 和文档 4–5 存在功能演进关系——文档 1 描述的是旧版「自动评测」独立流程；而文档 4–5 定义的新版评测体系（含评估器、标签、任务关联）已逐步替代旧版，控制台页面明确提示“单击**返回旧版**”以切换 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 关键参数

| 参数类别 | 说明 | 约束/默认值 |
|----------|------|-------------|
| **评测集字段** | `query`（用户问题）、`referenceAnswer`（标准答案）、`coarseKeywords`（1–3 个主题词）、`fineKeywords`（嵌套数组格式的关键信息点）为知识问答型评测集必需字段 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) | `fineKeywords` 必须为 `...` 格式；`coarseKeywords` 长度 ≤ 3 |
| **采样配置** | 分类采样数（事实型/教程型/比较型/分析型）决定各类型抽取问题数量；总评测数 = 各类型采样数之和 | 单任务最多支持 8 个应用；采样总数无硬上限，但影响 [Token](../concepts/token.md) 消耗 |
| **评估器参数** | LLM 评估器需配置模型、Prompt、评分范围（如 0–1 或 1–5）与通过阈值；Code 评估器需定义入参（如 `query`, `response`）与 Python 执行函数 | 每个评测任务最多添加 10 个评估器；所有变量必须完成字段映射才能保存任务 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签类型** | 分类（多选枚举）、布尔（True/False）、数字（Double）、文本（String）四类，用于人工标注维度建模 | 分类标签最多支持 20 个筛选项；数字标签支持 ≥ / ≤ 等条件筛选 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备数据基础**  
   - 确保目标智能体应用已发布、配置知识库、并开通「应用观测」功能 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
   - 创建评测集：可自动生成（仅限知识问答型，依赖知识库）或手动上传（支持 `.jsonl`（知识问答）或 `.xls`/`.xlsx`（对话分析））[原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。新版支持从「应用观测」直接导入真实请求数据 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

2. **构建评估逻辑**  
   - 创建评估器：选用预置模板（如「问答相关性」）或自定义 LLM/Code 评估器，严格按要求映射 `query`/`response` 等参数 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
   - 创建标签：按业务需求定义分类、布尔等标签类型，用于人工标注维度 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

3. **执行评测任务**  
   - 在「评测任务」页面创建任务，关联评测集、智能体/工作流应用、评估器与标签。  
   - 发起后不可修改配置，但支持随时追加人工标签；任务状态为「已完成」后，可在「数据明细」页查看每条样本的评估器得分与人工标注结果，在「指标统计」页查看综合得分、通过率与分布图表。

## 限制和注意事项

- **权限与依赖**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测强依赖「应用观测」功能开启，评测期间关闭会导致失败或数据丢失 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **知识库约束**：多应用横向评测要求所有被选应用必须关联至少一个**相同的知识库**；生成评测集时，若知识库内容缺失或切片不完整，将导致参考答案不可达，BadCase 归因中「未获取知识」或「切片不完整」比例升高。  
- **[Token](../concepts/token.md) 消耗**：评测集生成与执行均消耗 [Token](../concepts/token.md)，预估平均消耗仅为参考值，实际以账单为准；预估最大消耗是硬性成本上限，但实际消耗通常显著低于该值 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **版本兼容性**：旧版自动评测（文档 1）与新版评测体系（文档 4–6）并存，但新版支持更灵活的评估器组合与标签管理；若使用新版功能（如自定义评估器），旧版界面无法访问其配置。  
- **评测集发布要求**：手动上传的评测集必须「发布」后才可用于评测任务；草稿状态不可选 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


