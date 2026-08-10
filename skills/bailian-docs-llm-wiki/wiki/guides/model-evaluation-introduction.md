# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它面向模型选型、调优验证、能力归因和持续监控等核心场景，提供 AI 自动评分、规则计算和人工标注三种评估范式，并可生成结构化报告与排行榜。该功能当前仅支持文本生成类模型，不支持[多模态](../concepts/multi-modal.md)或语音类模型。

## 支持的模型与功能

- **支持模型类型**：预置模型（如千问系列）及用户调优后的文本生成模型，详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)；**不支持非文本生成类模型**（如图像生成、语音合成）。  
- **核心功能**：  
  - **自定义评测**：使用用户上传的评测数据集（`EvaluationSet` 类型）或已有推理结果集，关联自定义评测维度执行评分；  
  - **基线评测**：基于平台预置公开数据集（如 C-Eval、GSM8K、BBH）快速获取基准分数，**仅北京地域可用**；  
  - **排行榜**：在统一维度下横向对比多个模型表现，支持自动锁定评分标准；  
  - **人工标注**：针对创意性、专业性等主观场景，支持人工逐条标注 Pass/Fail 标签。  

> **注意**：文档 1 称“当前仅支持文本生成类模型评测”，而文档 2 未明确限定模型类型，但其所有示例（如 Function Calling、NL2SQL、摘要）均属文本生成范畴。因此以文档 1 的表述为准，实际能力边界请参考 [模型评测产品概览](https://help.aliyun.com/zh/model-studio/model-evaluation-introduction/) —— 此处引用原文标题：[模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 约束 |
|----------|--------|------|--------|------|
| **评测维度** | 维度类型 | 5 种：大模型评估-数值型/分类型、规则评估-字符串匹配/文本相似度、人工评估-分类型 | 是 | 创建后不可修改，选错需删除重建 |
| | 裁判模型 | 仅大模型评估类型需指定（如千问-Max），影响评分质量与费用 | 大模型评估类型必填 | — |
| | 评分范围 | 仅数值型维度需设（整数区间，如 `0-5`） | 数值型必填 | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则评估-文本相似度） | 数值型/相似度型必填 | 步长 0.1（数值型）或 0.01（相似度型） |
| | Pass/Fail 标签 | 分类型维度需定义互斥且穷尽的标签集合 | 分类型必填 | 同一标签不可重复出现在 Pass 与 Fail 中 |
| **评测任务** | 数据来源 | “评测数据集”（触发被测模型推理，产生费用）或“推理结果集”（仅评分，无推理费） | 是 | 数据集须为 `EvaluationSet` 类型且已发布版本 |
| | System Prompt | 作用于被测模型，设定角色或行为规范 | 否 | 多数场景可留空；与评分器 Prompt 作用对象不同（后者作用于裁判模型） |

评分器 Prompt 支持 `${prompt}`、`${output}`、`${completion}` 三变量，**至少包含一个变量方可提交**。详细配置逻辑见 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备含 `Output` 的推理结果集文件；  
2. **创建维度**：在「评测维度」Tab 创建至少一个维度模板，根据场景选择类型（推荐先用预置模板如“综合评测”快速验证）；  
3. **创建任务**：在「评测任务」Tab 选择「自定义评测」，关联模型、数据源及维度；若需跨模型对比，开启「参与排行」并绑定已有排行榜；  
4. **查看结果**：任务状态为「评测完成」后，在「指标统计」Tab 查看综合得分、通过率与分数分布，在「数据明细」Tab 审查逐条评分；  
5. **优化迭代**：若分数区分度低，优先检查评分器 Prompt 是否明确（如是否定义各分档判定条件）、裁判模型是否足够强（推荐千问-Max），必要时用小样本（50 条）验证配置——此流程说明详见 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：基线评测仅在北京地域可用，其他地域控制台不显示该选项，属正常行为；  
- **模型限制**：仅支持文本生成类模型，不支持图像、语音等[多模态](../concepts/multi-modal.md)模型；  
- **维度限制**：维度类型创建后不可修改；已被排行榜绑定的维度删除后，将导致该排行榜无法新建任务；  
- **费用说明**：  
  - 使用「评测数据集」时产生被测模型推理费用；  
  - 大模型评估维度（数值型/分类型）额外产生裁判模型评分费用；  
  - 规则评估与人工评估无裁判模型费用；  
- **结果可靠性**：  
  > **注意**：文档 1 提到“LLM 评分器存在位置偏差和自我偏好偏差”，文档 2 未提及此风险。实践中建议定期人工抽查校准评分结果，尤其当综合得分相近（1–3% 差异）时，不应作为决策唯一依据；  
- **API 支持**：当前模型评测功能**仅支持控制台操作，不提供公开 API/SDK**；如需自动化，可参考 PAI Judge Model API 替代（见文档 1 常见问题）；  
- **人工标注**：使用人工评估维度的任务，必须全部数据标注完成后才变为「评测完成」状态，此前始终为「进行中」。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


