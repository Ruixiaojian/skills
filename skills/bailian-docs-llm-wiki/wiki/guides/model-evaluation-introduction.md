# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它帮助开发者在模型选型、调优验证、质量监控等场景中，基于客观指标（如综合得分、通过率、分数分布）做出技术决策。该功能不提供 API/SDK 接口，仅支持控制台操作 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 支持的模型与功能

- **支持模型类型**：仅限文本生成类模型（包括预置模型与调优后模型），不支持多模态、语音、图像等非文本生成模型。具体可用模型列表见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。
- **评测方式**：
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 列）或推理结果集，自主配置维度、评分方式及 System Prompt，支持全地域使用。
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH 等），系统自动执行并评分，**仅北京地域可用**；不支持下载结果、不显示综合得分列、不可关联人工标注 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分器类型**：共五种，分为三大类：
  - *大模型评估*（需裁判模型）：分类型（Pass/Fail）、数值型（0–5 整数分）；
  - *规则评估*（无裁判模型费用）：字符串匹配（相等/不相等/包含）、文本相似度（ROUGE/BLEU/Cosine 等 7 种算法）；
  - *人工评估*（无裁判模型费用）：分类型（人工逐条标注 Pass/Fail） [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 1 称“当前仅支持文本生成类模型评测”，而文档 2 未明确限定模型类型，但其所有示例与参数（如 `${prompt}`/`${output}`/`${completion}`）均基于文本生成任务设计。实践中，非文本生成模型无法适配评测数据格式与评分逻辑，应以文档 1 的限定为准。

## 关键参数

| 参数 | 说明 | 必填性 | 约束与建议 |
|------|------|--------|------------|
| **维度类型** | 决定评分范式（如大模型评估-数值型），创建后不可修改 | 是 | 选错需删除重建；已关联任务不受影响 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **裁判模型** | 用于大模型评估的 LLM（如千问-Max），影响评分质量与费用 | 大模型评估类型必填 | 推荐千问-Max；费用按 Token 计费 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| **评分器 Prompt** | 指导裁判模型打分的提示词，须含至少一个变量（`${prompt}`/`${output}`/`${completion}`） | 大模型评估类型必填 | 变量引用错误或缺失将导致提交失败；模糊标准易致评分区分度低 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **评分范围** | 数值型维度的整数区间（如 `0–5`） | 数值型必填 | 建议 ≤10；过大范围降低 LLM 评分一致性 |
| **通过阈值** | 判定 Pass 的最低分（数值型）或相似度（规则评估） | 数值型/相似度型必填 | 步长 0.1（数值型）或 0.01（相似度型）；业务容忍度决定阈值高低 |
| **匹配规则 / 相似度算法** | 字符串匹配（相等/包含等）、文本相似度（ROUGE-L 适合摘要，BLEU 适合翻译） | 规则评估类型必填 | 算法选择直接影响评估合理性 |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 两列），或准备已含 `Output` 的推理结果集文件。
2. **创建维度**：在「评测维度」Tab 创建至少一个维度模板，选择类型并配置参数（如裁判模型、Prompt、标签、评分范围等） [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：
   - 自定义评测：选择模型、数据来源（评测数据集 or 推理结果集）、关联维度、设置 System Prompt（可选）；
   - 基线评测：仅北京地域可见，选择模型与预置数据集即可。
4. **查看结果**：任务状态为「评测完成」后，在详情页「指标统计」Tab 查看综合得分、通过率、分数分布；「数据明细」Tab 查看逐条评分。支持结果下载（基线评测不支持） [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

> **注意**：使用「评测数据集」会触发被评测模型推理，产生推理费用；使用「推理结果集」则跳过推理，仅产生评分费用（大模型评估类型）或零费用（规则/人工评估）。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **不可逆操作**：维度类型、评测任务的目标模型、已提交任务均不可修改；错误配置需删除后重建，已消耗 Token 费用不可追回。
- **数据要求**：评测数据集必须为 `EvaluationSet` 类型且已发布版本；推理结果集需严格按模板格式上传（含 `Prompt`、`Output`、`Completion` 列）。
- **费用说明**：
  - 被评测模型推理费：仅「评测数据集」方式产生，按输入/输出 Token 计费；
  - 裁判模型评分费：仅大模型评估维度产生，按 Token 计费；
  - 规则评估与人工评估无裁判模型费用 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **成本优化建议**：优先用规则评估（低成本）、小规模验证（50–100 条）再扩量、复用推理结果集避免重复推理。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


