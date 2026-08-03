# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型的推理结果进行多维度打分与对比。它服务于模型选型、调优验证、能力量化及持续质量监控等核心场景，提供 AI 自动评测、规则评估和人工评估三种评分范式，并可生成结构化评测报告与排行榜。当前功能仅面向文本生成类模型，不支持多模态或语音模型。

## 支持的模型与功能

- **支持模型类型**：仅支持文本生成类模型（包括预置模型与调优后的模型），详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)；多模态、语音等非文本生成模型暂不支持 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评测方式**：  
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型）或导入推理结果集，自主创建评测维度并关联执行，支持全地域；  
  - **基线评测**：使用平台预置的公开标准数据集（如 C-Eval、GSM8K、BBH 等），系统自动完成评分，**仅北京地域可用** [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评分器类型**：共五种，分为三大类：  
  - *大模型评估*（分类型/数值型）：依赖裁判模型（如千问-Max）进行语义级评判；  
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine 等）或确定性逻辑自动计算；  
  - *人工评估-分类型*：由人工逐条标注 Pass/Fail 标签 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  

> **注意**：文档1称“当前仅支持文本生成类模型评测”，文档2未明确限定模型类型，但其所有示例与参数说明（如 `${prompt}`/`${output}`/`${completion}` 变量、Function Calling/NL2SQL 场景）均隐含文本生成前提。二者一致，无矛盾。

## 关键参数

| 参数 | 适用维度类型 | 说明 | 约束 |
|------|--------------|------|------|
| **裁判模型** | 大模型评估（分类型/数值型） | 执行评分的 LLM，推荐千问-Max | 必填；影响评分质量与费用 |
| **评分器 Prompt** | 大模型评估（分类型/数值型） | 指导裁判模型打分的提示词，须含 `${prompt}`/`${output}`/`${completion}` 至少一个变量 | 长度 ≤ 50000 字符；无变量则提交失败 |
| **评分范围** | 大模型评估-数值型、规则评估-文本相似度 | 数值型：整数区间（默认 `0–5`）；相似度型：`0.00–1.00` | 数值型最小值 ≥ 0，最大值 ≥ 1；相似度步长 0.01 |
| **通过阈值** | 所有需 Pass/Fail 判定的类型 | 数值型/相似度型：≥ 该值为 Pass；分类型/人工型：由标签定义 | 步长：数值型 0.1，相似度型 0.01 |
| **匹配规则** | 规则评估-字符串匹配 | `相等`/`不相等`/`包含` | 至少一侧输入含变量（如 `${output}`） |

- **System Prompt**：配置于评测任务层级，作用于被评测模型（非裁判模型），用于设定角色或行为约束，多数场景可留空。  
- **维度名称与描述**：名称 ≤ 20 字符，描述 ≤ 100 字符，建议采用“评估方面+评估方式”命名（如 `回答准确性-LLM评分`）[评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。  
2. **创建评测维度**：在控制台 **模型评测 → 评测维度** 创建至少一个维度模板。类型选定后不可修改，选错需删除重建。  
3. **创建评测任务**：  
   - *自定义评测*：选择模型、指定数据来源（评测数据集或推理结果集）、关联维度、设置 `System Prompt`（可选）、开启排行（可选）；  
   - *基线评测*：仅北京地域可见，选择模型与预置数据集（如 MMLU、HellaSwag），无需配置维度 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
4. **查看结果**：任务状态为“评测完成”后，进入详情页：  
   - **数据明细 Tab**：逐条展示 `Prompt`、`Output`、`Completion` 及各维度评分；  
   - **指标统计 Tab**：显示综合得分（各维度平均分）、通过率（≥通过阈值样本占比）、分数分布图。  

> **注意**：基线评测任务不支持结果下载、不显示综合得分与维度详情列（显示短横线）、不可进入人工标注页面 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常设计 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **模型与数据约束**：  
  - 仅支持文本生成类模型；  
  - 评测数据集必须为 `EvaluationSet` 类型且已发布版本；训练集不可用于评测；  
  - 推理结果集需严格按模板格式上传（含 `Prompt`、`Output` 等列）。  
- **维度与任务不可变项**：  
  - 评测维度类型创建后不可修改；  
  - 评测任务提交后不可更换被评测模型；  
  - 已绑定维度的排行榜，删除该维度将导致排行榜无法新建任务。  
- **费用相关**：  
  - 使用评测数据集会触发被评测模型推理费用（按 [Token](../concepts/token.md) 计费）；  
  - 大模型评估维度产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；规则评估与人工评估无裁判模型费用；  
  - 成本优化建议：小规模验证（50–100 条）→ 保存推理结果集复用 → 优先选用规则评估 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **结果解读**：综合得分是各维度平均值，可能掩盖维度间差异；建议结合分数分布图与逐维度分析识别短板；1–3% 分差通常属评测噪声，不宜作为决策依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


