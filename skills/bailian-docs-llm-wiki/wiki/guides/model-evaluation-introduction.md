# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它帮助开发者在模型选型、调优验证、质量监控等场景中基于客观指标做出技术决策。该功能以数据集、评测维度和评测任务为三大核心要素，覆盖全自动（AI/规则）、半自动（人工标注）及快速基准（基线）三种评测范式。

## 支持的模型/功能

- **支持模型类型**：当前仅支持文本生成类模型（如 Qwen 系列、Llama 等预置及调优后模型），不支持多模态、语音、向量模型等非文本生成模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **核心评测方式**：
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 列）并配置自定义维度，支持大模型评估、规则评估、人工评估三类共五种评分器 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)；
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH 等），仅限北京地域可用，无需准备数据或配置维度 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **复用能力**：评测维度创建为模板后可被多个评测任务引用，实现评分标准统一；排行榜支持跨任务横向对比相同维度下的模型表现。

> **注意**：文档1称“基线评测仅北京地域可用”，文档2未提地域限制，但未否定该约束。应以文档1为准，其他地域控制台不显示基线选项属正常行为。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值示例 |
|----------|--------|------|--------|----------|
| **维度通用** | 维度名称 | 模板标识，≤20 字符 | 是 | `回答准确性-LLM评分` |
| | 描述 | 补充说明，≤100 字符 | 否 | `基于语义完整性与事实正确性综合判定` |
| **大模型评估** | 裁判模型 | 执行评分的 LLM（如 `qwen-max`） | 数值型/分类型必填 | `qwen-max` |
| | 评分器 Prompt | 含 `${prompt}`/`${output}`/`${completion}` 至少一个变量 | 必填 | `请判断${output}是否完整覆盖${prompt}要求且无事实错误…` |
| | 评分范围（数值型） | 整数区间，最小值 ≥ 0，最大值 ≥ 1 | 数值型必填 | `0–5` |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则型），步长 0.1（数值）/0.01（相似度） | 数值型/相似度型必填 | `3.0` / `0.75` |
| | Pass/Fail 标签 | 分类型维度中定义分类标签，互斥且不可重复 | 分类型必填 | `Pass`/`Fail` |
| **规则评估** | 匹配规则 | 相等 / 不相等 / 包含 | 字符串匹配必填 | `包含` |
| | 相似度算法 | ROUGE-1/ROUGE-L/BLEU/Cosine/Fuzzy Match/Accuracy | 文本相似度必填 | `ROUGE-L` |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或复用已有推理结果集（含 `Prompt`/`Output`/`Completion`）以规避重复推理费用 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
2. **创建维度**：在「评测维度」Tab 创建至少一个维度模板，按业务选择类型（如规则评估用于 Function Calling，大模型评估用于问答质量），配置对应参数。  
3. **创建任务**：
   - 自定义评测：选择模型、数据来源（评测数据集 or 推理结果集）、关联维度；可选开启排行榜参与；
   - 基线评测：仅北京地域可见，选择模型 + 公开数据集（如 `MMLU`），提交即执行。  
4. **查看结果**：任务状态为「评测完成」后，进入详情页查看：
   - **数据明细 Tab**：逐条展示 `Prompt`、`Output`、`Completion` 及各维度评分；
   - **指标统计 Tab**：综合得分（各维度平均分）、通过率（≥通过阈值样本占比）、分数分布图。  
5. **结果导出**：支持下载 CSV 结果文件（基线评测不支持下载）。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属预期行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **模型与数据约束**：
  - 仅支持文本生成类模型，不支持图像、音频等多模态模型；
  - 评测数据集必须为 `EvaluationSet` 类型且已发布版本，训练集不可用于评测；
  - 数据格式必须包含 `Prompt` 列，`Completion` 列在规则评估和部分大模型评估中为必需（见[评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)中“需要参考答案”列）。  
- **配置不可变性**：评测维度的类型创建后不可修改，选错需删除重建；任务提交后不可更换被评测模型或修改数据来源。  
- **费用相关**：
  - 使用评测数据集时产生被评测模型推理费用；
  - 大模型评估维度（数值型/分类型）额外产生裁判模型评分费用；
  - 规则评估与人工评估无裁判模型费用，成本更低 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **结果解读建议**：综合得分易掩盖维度间差异，应结合分数分布图与各维度明细分析短板；1–3% 的分差通常属评测噪声，不建议作为决策唯一依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


