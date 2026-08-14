# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它面向模型选型、调优验证、质量监控等核心场景，提供 AI 自动评测、规则评估和人工评估三种评分范式，并可生成结构化报告与排行榜。该功能当前仅支持文本生成类模型，不支持多模态或语音类模型。

## 支持的模型/功能

- **支持的模型类型**：仅限文本生成类模型（包括预置模型与调优后的模型），详见[模型评测产品概览](https://help.aliyun.com/zh/model-studio/model-evaluation-introduction/)；多模态、语音等非文本生成模型暂不支持 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评测方式**：  
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型）或推理结果集，自主配置维度、模型与参数；支持全地域。  
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH 等），系统自动执行，**仅北京地域可用** [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评分器类型**：共五种，分为三大类：  
  - *大模型评估*（分类型/数值型）：依赖裁判模型（如千问-Max）进行语义级评判；  
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine 等）或确定性逻辑计算；  
  - *人工评估-分类型*：由人工标注 Pass/Fail 标签。  
  详细分类与适用场景见 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档1称“当前仅支持文本生成类模型评测”，文档2未明确限定模型类型，但其所有示例与参数说明均围绕文本生成展开，且文档2中“适用场景”列（如翻译、摘要、Function Calling）均为文本任务。二者一致，无矛盾。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 约束 |
|----------|--------|------|--------|------|
| **通用** | 维度名称 | 维度模板标识，用于任务中引用 | 是 | ≤20 字符 |
| | 描述 | 补充说明维度目标 | 否 | ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行评分的 LLM（如千问-Max） | 是（仅大模型评估） | 下拉选择，影响费用与效果 |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（仅大模型评估） | 必须含 `${prompt}` / `${output}` / `${completion}` 至少一个变量 |
| | 评分范围（数值型） | 整数区间，如 `0-5` | 是（仅数值型） | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则评估） | 是（数值型/相似度型） | 数值型步长 0.1；相似度型范围 0–1，步长 0.01 |
| | Pass/Fail 标签 | 分类型维度的输出标签 | 是（分类型） | Pass 与 Fail 标签互斥、不可重复 |
| **规则评估** | 匹配规则（字符串匹配） | 相等 / 不相等 / 包含 | 是（字符串匹配） | — |
| | 评估指标（文本相似度） | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 是（文本相似度） | — |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。  
2. **创建维度**：在控制台 **模型评测 > 评测维度** 页面创建至少一个维度模板。类型一经创建不可修改，选错需删除重建 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建任务**：  
   - 选择 **自定义评测** 或 **基线评测**；  
   - 自定义评测：指定被评测模型、数据来源（评测数据集 or 推理结果集）、关联维度；  
   - 基线评测：仅需选择模型与预置数据集（如 MMLU）；  
   - System Prompt 可为空，用于约束被测模型行为；Temperature/TopP 等参数按所选模型动态加载。  
4. **查看结果**：任务状态为“评测完成”后，在详情页的 **指标统计** Tab 查看综合得分、通过率及分布图；**数据明细** Tab 查看逐条评分。支持下载 CSV 结果（基线评测不支持下载）。

## 限制和注意事项

- **地域限制**：基线评测仅在北京地域可用，其他地域控制台不显示该选项，属正常行为 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **维度不可变**：评测维度类型创建后不可修改；删除维度前需确保无排行榜绑定，否则将阻止新任务创建 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **费用说明**：  
  - 使用评测数据集 → 产生被评测模型推理费用；  
  - 大模型评估维度 → 产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；  
  - 规则评估与人工评估 → 无裁判模型费用；  
  - 推理结果集方式 → 无被评测模型推理费用。  
- **数据要求**：  
  - 评测数据集必须为 `EvaluationSet` 类型且已发布版本；  
  - 小规模验证建议 50–100 条，正式评测建议 200–500 条；  
  - 人工评估任务需全部标注完成后才标记为“评测完成”。  
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图与逐维度分析定位短板。1–3% 的分差通常属评测噪声，不宜作为决策依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


