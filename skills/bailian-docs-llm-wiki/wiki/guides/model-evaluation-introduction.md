# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与横向对比。其核心目标是帮助开发者客观衡量模型表现、验证调优效果、支撑选型决策，并实现持续质量监控。该功能不提供 API/SDK 接口，仅支持控制台操作 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 支持的模型与功能

- **支持模型类型**：当前**仅支持文本生成类模型**（如 Qwen 系列、Llama 等），不支持[多模态](../concepts/multi-modal.md)、语音或结构化输出模型。预置模型与调优后模型均可作为被评测对象 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型）或已有推理结果集，搭配自定义创建的评测维度，支持 AI 自动评测、规则评估和人工评估三种评分范式。
  - **基线评测**：基于平台预置的公开标准数据集（如 C-Eval、GSM8K、BBH 等），系统自动执行并评分，**仅在北京地域可用**；不支持维度配置、结果下载及排行榜参与 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **复用能力**：评测维度以模板形式创建，可被多个评测任务引用，确保评估标准统一 [评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 1 称“基线评测仅北京地域可用”，文档 2 未提及地域限制，但未否定该约束。以文档 1 的明确声明为准，其他地域用户无法看到基线评测选项属正常现象。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值示例/约束 |
|----------|--------|------|--------|----------------|
| **维度通用** | 维度名称 | 模板标识符 | 是 | ≤20 字符，建议采用“评估方面+方式”命名，如`回答准确性-LLM评分` |
| | 描述 | 补充说明 | 否 | ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行评分的 LLM | 是（仅大模型评估类型） | 推荐 `qwen-max`；费用按 [Token](../concepts/token.md) 计费 |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（仅大模型评估类型） | 必须含至少一个变量：`${prompt}`、`${output}` 或 `${completion}`；≤50000 字符 |
| | 评分范围（数值型） | 整数打分区间 | 是（仅数值型） | 最小值 ≥0，最大值 ≥1，默认 `0~5` |
| | 通过阈值 | Pass/Fail 判定分界线 | 是（数值型/相似度型） | 数值型步长 0.1（如 `3.0`）；相似度型范围 `0~1`，步长 `0.01` |
| | Pass/Fail 标签（分类型） | 分类输出标签 | 是（仅分类型） | 标签互斥且穷尽；各标签 ≤20 字符 |
| **规则评估** | 比较操作符（字符串匹配） | 匹配逻辑 | 是（仅字符串匹配） | `相等` / `不相等` / `包含` |
| | 评估指标（文本相似度） | 相似度计算算法 | 是（仅文本相似度） | `ROUGE-L`（摘要）、`BLEU`（翻译）、`Cosine`（语义）、`Accuracy`（精确匹配）等 7 种 |

## 使用方式

1. **准备数据**：在数据管理模块上传 **EvaluationSet 类型** 数据集（含 `Prompt` 和 `Completion` 两列），并发布版本；或准备已含 `Output` 的推理结果集文件。
2. **创建维度**：在「评测维度」Tab 创建至少一个维度模板。根据场景选择类型：
   - 有确定性答案 → 优先 `规则评估-字符串匹配`（成本最低）或 `规则评估-文本相似度`；
   - 需语义理解 → `大模型评估-数值型`（精细量化）或 `大模型评估-分类型`（二元判定）；
   - 主观判断 → `人工评估-分类型`（需人力投入）[评测维度 (raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：
   - 选择「自定义评测」或「基线评测」；
   - 指定被评测模型（预置或调优模型）；
   - 数据来源选「评测数据集」（产生推理费用）或「推理结果集」（无推理费用）；
   - 关联已创建的维度；
   - 可选配置 `System Prompt`（作用于被评测模型，非裁判模型）。
4. **查看结果**：任务状态为「评测完成」后，在详情页查看：
   - **数据明细 Tab**：逐条展示 `Prompt`、`Output`、`Completion` 及各维度评分；
   - **指标统计 Tab**：综合得分（各维度平均分）、通过率（≥通过阈值样本占比）、分数分布图。

## 限制和注意事项

- **地域限制**：基线评测功能仅限北京地域可用，其他地域控制台不显示该选项 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **不可逆操作**：
  - 评测维度类型创建后**不可修改**，选错需删除重建（已关联任务不受影响）；
  - 删除维度后，若其已被排行榜绑定，将导致排行榜无法创建新任务；
  - 评测任务提交后**不可更换被评测模型**，需删除重建。
- **费用相关**：
  - 使用 `评测数据集` 作为数据源时，产生被评测模型的推理费用；
  - `大模型评估` 类型产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；`规则评估` 和 `人工评估` 无此费用；
  - 基线评测计费逻辑与自定义评测一致（含推理费用）。
- **结果解读**：
  - 综合得分是各维度平均分，可能掩盖维度间差异，**应结合分数分布图逐维度分析**；
  - 1–3% 的分数差异通常属评测噪声，不宜作为决策依据；
  - 人工评估任务需**全部标注完成后**才变为「评测完成」状态。
- **技术限制**：当前**不提供公开 API/SDK**，自动化集成需借助 PAI Judge Model API 替代 [模型评测 (raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


