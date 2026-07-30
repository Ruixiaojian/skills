# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它帮助开发者在模型选型、调优验证、质量监控等场景中，基于客观指标（如综合得分、通过率、分数分布）做出技术决策。该功能不提供 API/SDK 接口，当前仅支持控制台操作。

## 支持的模型与功能

- **支持模型类型**：仅限文本生成类模型（包括预置模型与调优后模型），不支持[多模态](../concepts/multi-modal.md)、语音、向量模型等 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型）或已有的推理结果集，配合自定义创建的评测维度执行；支持全地域。
  - **基线评测**：使用平台预置的公开标准数据集（如 C-Eval、GSM8K、BBH 等），系统自动评分；**仅北京地域可用**，且不支持结果下载与人工标注 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分范式**：共五种评测维度类型，覆盖三大评估范式：
  - *大模型评估*（数值型/分类型）：依赖裁判模型（如千问-Max）进行语义级评判；
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine 等）或确定性逻辑自动计算；
  - *人工评估*（分类型）：由人工逐条标注 Pass/Fail 标签 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档1称“当前仅支持文本生成类模型评测”，文档2未明确限定模型类型，但其所有示例与参数说明均围绕文本生成展开，且文档2中“适用场景”列（如 Function Calling、NL2SQL、摘要）均为文本任务。二者无实质矛盾，以文档1的明确声明为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 约束与建议 |
|----------|--------|------|--------|------------|
| **通用** | 维度名称 | 维度模板标识符 | 是 | ≤20 字符；建议采用“评估方面+评估方式”命名（如`回答准确性-LLM评分`） |
| | 描述 | 补充说明 | 否 | ≤100 字符 |
| **大模型评估专用** | 裁判模型 | 执行评分的 LLM | 是（仅大模型评估） | 推荐千问-Max；费用按 [Token](../concepts/token.md) 计费 |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（仅大模型评估） | 必须含至少一个变量：`${prompt}`、`${output}` 或 `${completion}`；≤50000 字符 |
| | 评分范围（数值型） | 整数打分区间 | 是（仅数值型） | 最小值 ≥ 0，最大值 ≥ 1；默认 `0~5`；范围过大（如 >10）会降低评分一致性 |
| | 通过阈值 | Pass 判定下限 | 是（数值型/相似度型） | 数值型步长 0.1（如 `3.0`）；相似度型范围 `0~1`，步长 `0.01` |
| | Pass/Fail 标签（分类型） | 分类输出标签 | 是（仅分类型） | Pass 与 Fail 标签互斥且不可重复；每标签 ≤20 字符 |
| **规则评估专用** | 比较操作符（字符串匹配） | 相等 / 不相等 / 包含 | 是（仅字符串匹配） | 用于 Function Calling、固定答案等确定性场景 |
| | 评估指标（文本相似度） | ROUGE-1/ROUGE-L/BLEU/Cosine 等 | 是（仅文本相似度） | 翻译用 BLEU，摘要用 ROUGE-L，语义相关用 Cosine |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。
2. **创建维度**：在「模型评测 > 评测维度」页面创建至少一个维度模板。类型一经创建不可修改，选错需删除重建 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：
   - 自定义评测：选择目标模型、数据来源（评测数据集或推理结果集）、关联维度；可选开启排行。
   - 基线评测：仅北京地域可见，选择模型与预设数据集（如 MMLU、GSM8K）即可提交。
4. **查看结果**：任务状态变为「评测完成」后，在详情页「指标统计」Tab 查看综合得分、通过率及分布图；「数据明细」Tab 查看逐条评分。人工评估任务需全部标注完成后才进入完成状态。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常设计 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型与数据限制**：
  - 仅支持文本生成类模型；非文本模型无法参与评测。
  - 评测数据集必须为 `EvaluationSet` 类型且已发布版本；训练集、知识库等类型不可用。
  - 数据量建议：小规模验证 50–100 条，正式评测 200–500 条，全面评估 ≥500 条。
- **费用说明**：
  - 使用「评测数据集」作为数据源时，产生被评测模型的推理费用（按 [Token](../concepts/token.md) 计费）。
  - 大模型评估维度（数值型/分类型）额外产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；规则评估与人工评估无此费用。
  - 使用「推理结果集」可规避被评测模型的推理费用。
- **配置约束**：
  - 评测维度类型创建后不可修改；关联该维度的已有任务不受影响，但需删除维度后重建。
  - 任务提交后不可更换被评测模型或修改维度；出错需删除任务后重建。
  - 排行榜绑定维度后，若该维度被删除，将阻止新任务创建。
- **结果解读建议**：
  - 避免仅依赖综合得分做决策；应结合分数分布图识别维度间差异（如某维度持续低分暴露能力短板）。
  - 1–3% 的分数差异通常属评测噪声，不建议据此判断模型优劣。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


