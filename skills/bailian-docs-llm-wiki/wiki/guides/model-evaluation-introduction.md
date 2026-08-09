# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它面向开发者提供可复用的评测维度、灵活的数据源选择及结构化结果分析能力，适用于模型选型、调优验证和持续质量监控等核心场景。当前功能仅支持文本生成类模型，不支持[多模态](../concepts/multimodal.md)或语音类模型。

## 支持的模型与功能

- **支持的模型类型**：仅限文本生成类模型（包括预置模型与调优后的模型），详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)；[多模态](../concepts/multimodal.md)、语音等非文本生成模型暂不支持 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评测方式**：  
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型）或导入推理结果集，自主创建评测维度并关联执行；支持大模型评估、规则评估、人工评估三类共五种评分器类型 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH 等），仅在北京地域可用，不支持自定义维度与结果下载 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **核心功能模块**：评测维度模板（可复用）、评测任务（含数据源与参数配置）、排行榜（跨任务横向对比）、人工标注界面（仅限人工评估维度）。

> **注意**：文档1称“基线评测仅北京地域可用”，文档2未提及地域限制，但未否定该约束；以文档1为准，其他地域用户将不可见基线评测选项，属正常行为。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值示例 |
|----------|--------|------|--------|----------|
| **维度通用** | 维度名称 | 最长20字符，建议采用“评估方面+评估方式”命名，如`回答准确性-LLM评分` | 是 | `安全性-分类型` |
| | 描述 | 最长100字符，补充评判目标 | 否 | `检测输出是否含违法/歧视性内容` |
| **大模型评估** | 裁判模型 | 执行评分的 LLM，影响评分质量与费用 | 大模型类必填 | `qwen-max` |
| | 评分器 Prompt | 含 `${prompt}`、`${output}`、`${completion}` 至少一个变量，定义评判逻辑 | 大模型类必填 | `请判断${output}是否符合${prompt}要求且无事实错误，仅输出Pass/Fail` |
| | 评分范围（数值型） | 整数区间，最小值≥0，最大值≥1 | 数值型必填 | `0~5` |
| | 通过阈值（数值型/相似度型） | 判定 Pass 的最低分值（步长0.1）或相似度（步长0.01） | 数值型/相似度型必填 | `3.0` / `0.75` |
| | Pass/Fail 标签 | 分类型维度中定义分类标签，互斥且不可重复 | 分类型必填 | `Pass` / `Fail` |
| **规则评估** | 比较操作符（字符串匹配） | `相等`/`不相等`/`包含` | 字符串匹配必填 | `包含` |
| | 评估指标（文本相似度） | 支持 ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy 共7种 | 文本相似度必填 | `ROUGE-L` |
| **任务级** | System Prompt | 作用于被评测模型，设定角色或行为规范，多数场景可留空 | 否 | `你是一名专业法律助理，请严格依据《民法典》回答问题` |
| | 数据来源 | `评测数据集`（触发模型推理，产生费用）或 `推理结果集`（仅评分，零推理费） | 是 | `推理结果集` |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 两列），或准备已含 `Output` 的推理结果集文件。  
2. **创建评测维度**：在控制台 **模型评测 > 评测维度** 页面创建模板。推荐先用预置模板（如“综合评测”“标准匹配”）快速启动，再根据小样本验证结果迭代优化 Prompt [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建评测任务**：  
   - 自定义评测：选择模型 → 指定数据来源（评测数据集或推理结果集）→ 关联已创建维度 → 配置 `System Prompt`（可选）→ 提交。  
   - 基线评测：仅北京地域可见，选择模型 + 公开数据集（如 MMLU）→ 提交 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
4. **查看结果**：任务状态为“评测完成”后，进入详情页：  
   - **数据明细 Tab**：逐条查看 `Prompt`、`Output`、`Completion` 及各维度评分；  
   - **指标统计 Tab**：查看综合得分（各维度平均分）、通过率（≥通过阈值的样本占比）、分数分布图；  
   - **下载结果**：支持 CSV 下载（基线评测不支持）。  

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属设计限制，非故障。  
- **模型限制**：当前仅支持文本生成类模型；图像、语音等非文本模型无法参与评测。  
- **维度不可变**：评测维度的类型（如“大模型评估-数值型”）创建后不可修改，选错需删除重建；已关联的任务不受影响，但排行榜绑定该维度后删除会导致新建任务失败。  
- **费用敏感项**：  
  - 使用 `评测数据集` 作为数据源时，被评测模型推理按 [Token](../concepts/token.md) 计费；  
  - 大模型评估维度（数值型/分类型）额外产生裁判模型评分费用；  
  - 规则评估与人工评估无裁判模型费用，成本最低 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **结果解读建议**：  
  - 综合得分易掩盖维度间差异，须结合分数分布图与各维度明细分析短板；  
  - 1–3% 的分差通常属评测噪声，不建议作为决策唯一依据；  
  - 人工评估任务需全部标注完成后才标记为“评测完成”。  
- **API 支持**：当前模型评测功能**仅支持控制台操作**，不提供公开 API 或 SDK；如需自动化，需自行集成 PAI Judge Model API [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


