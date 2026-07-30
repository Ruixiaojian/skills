# model evaluation introduction

模型评测是百炼平台提供的模型能力评估功能，支持通过自定义或基线方式对文本生成类模型进行量化打分与横向对比。它帮助开发者在模型选型、调优验证、质量监控等场景中，基于客观指标（如综合得分、通过率、分数分布）做出技术决策。该功能不提供 API/SDK 接口，仅支持控制台操作 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 支持的模型与功能

- **支持模型类型**：当前仅支持文本生成类模型（包括预置模型与调优后的模型），不支持[多模态](../concepts/multi-modal.md)、语音、图像等非文本生成模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 列）或已有的推理结果集，搭配自定义创建的评测维度，支持 AI 自动评测、规则评估、人工评估三种评分范式。
  - **基线评测**：仅限北京地域可用，使用平台预设的公开标准数据集（如 C-Eval、GSM8K、BBH 等），系统自动执行、不可配置维度、不支持结果下载 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **核心能力**：生成评测报告（含综合得分、通过率、分数分布）、支持排行榜横向对比、提供人工标注入口（仅限人工评估维度）、支持结果下载（待执行及基线任务除外）。

> **注意**：文档1称“基线评测仅北京地域可用”，文档2未提及地域限制，但未否定该约束；以文档1为准，此为平台实际部署限制，非过时信息。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值示例 |
|----------|--------|------|--------|----------|
| **评测维度** | 维度类型 | 决定评分逻辑，创建后不可修改 | 是 | `大模型评估-数值型`、`规则评估-字符串匹配` |
| | 裁判模型 | 仅大模型评估类型需指定，影响评分质量与费用 | 大模型评估类型必填 | `qwen-max`（推荐） |
| | 评分器 Prompt | 指导裁判模型评判，须至少含 `${prompt}` / `${output}` / `${completion}` 之一 | 大模型评估类型必填 | 见[评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)中自定义 Prompt 示例 |
| | 评分范围 | 数值型维度专属，整数区间 | 数值型必填 | `0~5`（默认） |
| | 通过阈值 | 判定 Pass/Fail 的分界值，支持小数（步长 0.1） | 数值型/相似度型必填 | `3.0`（数值型）、`0.75`（相似度型） |
| | Pass/Fail 标签 | 分类型维度专属，标签互斥且不可重复 | 分类型必填 | `Pass`/`Fail` 或 `合规`/`违规` |
| **评测任务** | 数据来源 | 决定是否触发被评测模型推理 | 是 | `评测数据集`（产生推理费）或 `推理结果集`（无推理费） |
| | System Prompt | 作用于被评测模型，设定角色或行为规范，多数场景可留空 | 否 | 空值或 `"你是一个严谨的法律助手"` |
| | 排行榜参与 | 开启后需绑定已创建的排行榜（维度必须一致） | 开启时必填 | — |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），并发布版本；或准备已含 `Output` 的推理结果集文件。
2. **创建评测维度**：在「模型评测 > 评测维度」中创建，按业务选择类型（如问答质量用 `大模型评估-数值型`，Function Calling 用 `规则评估-字符串匹配`），配置对应参数 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建评测任务**：
   - 选择「自定义评测」或「基线评测」；
   - 指定被评测模型（预置或调优模型）；
   - 配置数据来源（评测数据集或推理结果集）；
   - 关联已创建的评测维度（可多选）；
   - 设置 `System Prompt`（可选）、是否参与排行（可选）；
   - 单击「开始评测」。
4. **查看结果**：任务状态变为「评测完成」后，进入详情页：
   - 「数据明细」Tab 查看每条样本的 `Prompt`、`Output`、`Completion` 及各维度评分；
   - 「指标统计」Tab 查看综合得分（各维度平均分）、通过率、分数分布图；
   - 支持下载 CSV 结果文件（基线评测不支持）。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：仅支持文本生成类模型；非文本生成模型（如[多模态](../concepts/multi-modal.md)、ASR）暂不支持评测。
- **维度限制**：评测维度类型创建后不可修改，选错需删除重建；已被排行榜绑定的维度删除后，将导致排行榜无法新建任务。
- **费用说明**：
  - 使用 `评测数据集` 作为数据源时，产生被评测模型的推理费用；
  - `大模型评估` 类型（数值型/分类型）产生裁判模型评分费用；
  - `规则评估` 与 `人工评估` 无裁判模型费用；
  - `推理结果集` 数据源不产生被评测模型推理费用。
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图逐维度分析短板；1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **API 限制**：当前模型评测功能**仅支持控制台操作，不开放 API/SDK**；如需自动化，需参考 PAI Judge Model API 替代方案 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


