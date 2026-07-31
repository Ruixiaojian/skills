# application evaluation

application evaluation 是百炼平台用于系统化评估智能体或工作流应用输出质量的核心能力，支持自动与人工相结合的多维度评测。它通过评测集提供标准化输入数据，结合评估器实现自动化评分，并辅以人工标签进行主观判断，最终生成可归因、可迭代的评测报告。该能力覆盖从数据准备、任务执行到结果分析的完整闭环，适用于模型调优、版本对比和线上质量监控等场景。

## 支持的模型/功能

- **评测类型**：支持**对话分析**（基于 `.xls`/`.xlsx` 的多轮/单轮对话评测）和**知识问答**（基于 `.jsonl` 的结构化问答评测）两类原始评测集格式，详见 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；新版评测集进一步扩展为**智能体**、**工作流**和**自定义**三类，支持按应用出入参自动生成表结构，见 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
  
- **评估方式**：
  - **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）对回答进行语义评分（1–5 分），并自动归因至 RAG 流程环节（如“检索无效”“切片不完整”等）[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；
  - **手动评测**：依赖人工对应用输出与参考答案进行打分或评级（如“较差/一般/较好”），适用于需领域专家判断的场景；
  - **混合评测**：新版评测任务支持同时配置多个**评估器**（LLM 或 Code 类型）进行自动评分，并叠加**人工标签**（分类/布尔/数字/文本）进行补充标注，实现客观规则与主观判断协同 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

- **核心组件**：
  - **评估器**：预置模板覆盖通用质量、智能体能力、文本匹配等场景；支持自定义 LLM 评估器（通过 Prompt 控制评分逻辑）和 Code 评估器（Python 脚本实现精确校验）；
  - **标签管理**：支持四类标签（分类、布尔值、数字、文本），用于构建业务定制化评测维度，并可在评测任务与应用观测中复用。

> **注意**：文档 1 和文档 5 对评测集类型的描述存在差异——文档 1 仅定义“对话分析”与“知识问答”两种逻辑类型，而文档 5 将其重构为“智能体/工作流/自定义”三种技术类型。实际使用中，前者对应评测数据语义范式，后者对应数据结构生成方式，二者正交而非冲突；但需注意文档 1 中“知识问答”要求 `.jsonl` 格式，而文档 5 的“智能体”类型默认生成 Excel 模板，若需 `.jsonl` 结构，须选择“自定义”类型并手动定义字段。

## 关键参数

| 参数 | 说明 | 约束/默认值 |
|------|------|-------------|
| **评测集字段** | 必须与所选评估器参数严格映射。例如，“问答相关性”评估器要求 `query` 和 `response` 字段；若评测集含 `Prompt`/`Completion`，需在参数映射中显式关联 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) | 映射缺失将导致评估器失败 |
| **评估模型** | 自动评测与 LLM 评估器均需指定模型。当前仅支持 `qwen-max` 和 `qwen-plus`，其他模型不可选 | 不支持 `qwen-turbo` 等轻量模型 |
| **评分范围 & 通过阈值** | 决定评估器输出尺度（如 0–1、1–5、0–100）及 Pass/Fail 判定线 | 阈值建议设为范围中位数（如 0–1 时设 0.5） |
| **分类采样数** | 自动评测中，对每类任务（事实型/分析型等）抽取的问题数量 | 各类型独立设置，总样本数 = 各类采样数之和 |
| **标签类型** | 影响标注方式与筛选能力：分类标签支持多选下拉，布尔值仅 True/False，数字标签支持数值运算，文本标签支持模糊搜索 | 创建后不可修改类型 |

## 使用方式

1. **准备评测集**  
   - 手动上传：按 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) 规范准备 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答）文件；新版支持从应用观测导入真实流量数据。
   - 自动生成：仅限知识问答类型，基于已配置的知识库，由 `qwen-max`/`qwen-plus` 生成带 `query`/`referenceAnswer`/`fineKeywords` 的评测样本。

2. **创建评测任务**  
   - 旧版：区分“自动评测”与“手动评测”，前者需绑定已发布且配置知识库的智能体应用，后者仅需发布评测集即可启动人工标注；
   - 新版：统一入口 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)，支持“不关联应用”（纯人工）、“智能体”或“工作流”三种关联模式，并可添加最多 10 个评估器。

3. **配置与执行**  
   - 为每个评估器完成**参数映射**（如将评测集字段 `Prompt` → 评估器变量 `query`）；
   - 为人工标注配置**标签**（通过 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) 创建）；
   - 发起后不可修改配置，但可随时追加新应用（总数 ≤ 8）或新增标签。

4. **分析结果**  
   - 自动评测报告包含总正确率、BadCase 归因（5 类 RAG 环节问题）、RAG 各题型得分；
   - 新版任务详情页提供“数据明细”（逐条查看评估器分+人工标签）和“指标统计”（综合得分仪表盘、各评估器通过率柱状图）。

## 限制和注意事项

- **权限与依赖**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限；且被评测应用必须**已发布**、**配置知识库**、**开通应用观测**并加入观测列表，否则任务无法启动 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
  
- **文件与规模限制**：单次上传评测集文件 ≤ 10 个，单个文件 ≤ 20 MB；自动评测任务最多支持 8 个应用横向对比；评测集版本发布后，历史版本不可编辑，仅可新建版本覆盖。

- **[Token](../concepts/token.md) 消耗**：所有调用大模型的环节（评测集生成、自动评测、LLM 评估器）均产生 [Token](../concepts/token.md) 费用。预估消耗为参考值，实际用量以账单为准；任务失败时，已完成步骤的 [Token](../concepts/token.md) 仍计费 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

- **数据一致性风险**：若选用“选择已有评测集”模式进行自动评测，必须确保评测集中所有 `query` 的 `referenceAnswer` 均能在当前指定知识库中召回，否则评分失真 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

- **新版兼容性**：新版评测任务与旧版（自动/手动评测）功能并存，但二者数据不互通。页面左上角“返回旧版”按钮可切换，但已创建的旧版任务无法迁移至新版框架。

## 来源文档

- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


