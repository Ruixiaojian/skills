# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它面向开发者提供可复用的评测维度、灵活的数据来源配置及结构化结果分析能力，适用于模型选型、调优验证和持续质量监控等核心场景。评测过程解耦了被评测模型与评分逻辑，支持 AI 自动评分、规则计算和人工标注三种范式。

## 支持的模型/功能

- **支持模型类型**：当前仅支持文本生成类模型（如 Qwen 系列、Llama 等），不支持多模态、语音或结构化输出模型。预置模型与调优后模型均可作为被评测对象，详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。  
- **评测方式**：  
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 列）或推理结果集，自主创建评测维度并关联执行；支持全地域。  
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH），系统自动完成评测；**仅北京地域可用**，且不支持结果下载与人工标注 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评分器类型**：共五种，分为三大类：  
  - *大模型评估*（分类型/数值型）：依赖裁判模型（如千问-Max）进行语义理解评分，产生裁判模型 [Token](../concepts/token.md) 费用；  
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine/Fuzzy Match 等）全自动计算，无裁判模型费用；  
  - *人工评估-分类型*：由人工逐条标注 Pass/Fail，无模型费用但需人力投入 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  

> **注意**：文档1称“当前仅支持文本生成类模型评测”，而文档2未明确限定模型类型，但所有示例与参数说明均围绕文本生成展开，且两处均未提及非文本模型支持。此处以文档1的明确声明为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值约束 |
|----------|--------|------|--------|-----------|
| **维度通用** | 维度名称 | 模板标识符 | 是 | ≤20 字符 |
| | 描述 | 补充说明 | 否 | ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行评分的 LLM | 是（仅该类） | 如 `qwen-max`，影响费用与效果 |
| | 评分器 Prompt | 指导裁判模型评分的提示词 | 是（仅该类） | 必须含 `${prompt}` / `${output}` / `${completion}` 至少一个变量，≤50000 字符 |
| | 评分范围（数值型） | 整数区间，如 `0-5` | 是（仅数值型） | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则型） | 是（数值型/相似度型） | 数值型步长 0.1；相似度型范围 0–1，步长 0.01 |
| | Pass/Fail 标签 | 分类型维度的输出标签 | 是（分类型） | 互斥、无重复，每标签 ≤20 字符 |
| **规则评估** | 比较操作符（字符串匹配） | 相等 / 不相等 / 包含 | 是（仅该子类） | — |
| | 评估指标（文本相似度） | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 是（仅该子类） | 根据任务类型选择，如翻译用 BLEU，摘要用 ROUGE-L |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。  
2. **创建评测维度**：在控制台 **模型评测 > 评测维度** 页面创建模板。推荐从预置模板（如“综合评测”“标准匹配”）起步，再按需自定义 Prompt [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建评测任务**：  
   - 选择 **自定义评测** 或 **基线评测**；  
   - 自定义方式下：选择被评测模型、指定数据来源（评测数据集或推理结果集）、关联至少一个已创建维度；  
   - 基线方式下：仅需选择模型与公开数据集（如 MMLU）；  
   - 配置 `System Prompt`（作用于被评测模型，通常留空）与推理参数（Temperature/TopP）。  
4. **执行与查看**：提交后状态流转为 `待执行 → 进行中 → 评测完成`。完成后可在详情页的 **数据明细** Tab 查看逐条评分，**指标统计** Tab 查看综合得分、通过率及分数分布图 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
5. **结果复用**：首次评测后下载结果文件，后续任务可选用“推理结果集”模式避免重复调用被评测模型，降低成本。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **不可逆操作**：  
  - 评测维度类型创建后不可修改，选错需删除重建（已有任务不受影响）；  
  - 评测任务提交后无法更换被评测模型或修改维度，失败/终止任务不可恢复；  
  - 删除被排行榜绑定的维度将导致该排行榜无法新建任务。  
- **费用说明**：  
  - 使用“评测数据集”时产生被评测模型推理费用；  
  - 大模型评估维度产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；  
  - 规则评估与人工评估无裁判模型费用；  
  - 推理结果集模式不产生被评测模型推理费用。  
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图与逐维度分析定位短板。1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **API 支持**：当前模型评测功能**仅支持控制台操作，不提供公开 API/SDK**。如需自动化，可参考 PAI Judge Model API 替代 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


