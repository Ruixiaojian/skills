# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它帮助开发者在模型选型、调优验证、质量监控等场景中基于客观指标做出技术决策。该功能以数据集、评测维度和评测任务为三大核心要素，覆盖全自动（AI/规则）与人工评估范式。

## 支持的模型/功能

- **支持模型类型**：当前仅支持文本生成类模型（如 Qwen 系列、Llama 衍生模型等），不支持[多模态](../concepts/multi-modal.md)、语音或结构化输出模型；预置模型与调优后模型均可作为被评测对象 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：用户自主提供评测数据集（EvaluationSet 类型）与自定义维度，支持大模型评估、规则评估、人工评估三种评分范式；
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH），仅限北京地域可用，不支持维度配置与结果下载 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **复用能力**：评测维度创建为模板后可被多个评测任务引用，实现评估标准统一 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束与建议 |
|----------|--------|------|------------|
| **维度通用参数** | 维度名称 | 必填，≤20 字符 | 建议采用“评估方面+评估方式”命名，如`回答准确性-LLM评分` [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 描述 | 选填，≤100 字符 | 补充说明评判目标 |
| **大模型评估专用** | 裁判模型 | 如千问-Max（推荐）、Qwen1.5-72B 等 | 影响评分质量与费用；仅大模型评估类型需配置 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| | 评分器 Prompt | 含 `${prompt}` / `${output}` / `${completion}` 变量 | 至少含一个变量；长度 ≤50000 字符；模糊描述易致评分集中 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| | 评分范围（数值型） | 整数区间，如 `0–5` | 默认 `0–5`；范围过宽（如 `0–100`）会降低 LLM 评分一致性 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 通过阈值 | 数值型/相似度型必填，步长 0.1 或 0.01 | 用于统计通过率；与评分范围解耦（例：0–5 分时设阈值 3.0） [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| **规则评估专用** | 相似度算法 | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 摘要用 ROUGE-L，翻译用 BLEU，语义相关用 Cosine [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 匹配规则 | 相等 / 不相等 / 包含 | Function Calling 场景常用“包含”，NL2SQL 常用“相等” [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |

> **注意**：文档1称“维度类型创建后不可修改”，文档2亦强调“评分器类型创建后不可更改，选错只能删除重建”。二者一致，无矛盾。

## 使用方式

1. **前置准备**  
   - 开通百炼账号并访问[控制台模型评测页](https://bailian.console.aliyun.com/#/efm/model_evaluate/task/creation)；  
   - 在**数据管理模块**上传评测集（EvaluationSet 类型），必须含 `Prompt` 和 `Completion` 两列（基线评测除外） [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

2. **创建评测维度**  
   - 进入**评测维度** Tab → **创建评测维度**；  
   - 选择类型（如`大模型评估-数值型`）→ 配置裁判模型、评分器模板（推荐先用预置模板）→ 设置评分范围与通过阈值；  
   - 自定义 Prompt 时务必引用 `${prompt}`、`${output}` 或 `${completion}` 变量 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

3. **创建评测任务**  
   - 进入**评测任务** Tab → **创建评测任务**；  
   - 选择**自定义评测**（或北京地域的**基线评测**）→ 选定被评测模型 → 数据来源选**评测数据集**（触发推理，产生费用）或**推理结果集**（跳过推理，零推理费）→ 关联已建维度；  
   - System Prompt 为被评测模型设定角色，多数场景可留空 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

4. **查看与分析结果**  
   - 任务状态为“评测完成”后，进入详情页：  
     - **数据明细 Tab**：逐条查看 Prompt / Output / Completion 及各维度评分；  
     - **指标统计 Tab**：关注综合得分（各维度平均分）、通过率（≥通过阈值样本占比）、分数分布图——避免仅依赖综合得分掩盖维度短板 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：基线评测仅在北京地域可用，其他地域控制台不显示该选项，属正常行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **数据格式强约束**：评测数据集必须为 EvaluationSet 类型且已发布版本；训练集、未发布数据集将导致任务失败 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **不可逆操作**：  
  - 维度类型创建后不可修改，需删除重建（已关联任务不受影响）；  
  - 任务提交后不可更换被评测模型或修改数据源；终止任务后已评测数据保留但无法恢复 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **费用敏感点**：  
  - 大模型评估维度产生裁判模型 [Token](../concepts/token.md) 费用；规则评估与人工评估无此费用；  
  - 使用**评测数据集**会触发被评测模型推理并计费，**推理结果集**则无推理费；建议小规模验证（50–100 条）后再全量运行 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **API 缺失**：当前模型评测功能**仅支持控制台操作**，不提供公开 API/SDK；需自动化流程可参考 PAI Judge Model API 替代 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


