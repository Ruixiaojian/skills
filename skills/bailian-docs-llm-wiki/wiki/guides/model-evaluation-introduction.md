# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它面向开发者提供 AI 自动评测、规则评估和人工评估三种评分范式，帮助完成模型选型、调优验证、质量监控等核心任务。当前功能仅支持文本生成类模型，不支持多模态或语音模型。

## 支持的模型/功能

- **支持的模型类型**：仅限文本生成类模型（包括预置模型与调优后的模型），详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。多模态、语音等非文本生成模型暂不支持评测 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型）或推理结果集，自主创建评测维度并关联执行，支持全地域。
  - **基线评测**：使用平台预置的公开标准数据集（如 C-Eval、GSM8K、BBH 等），系统自动评分，**仅北京地域可用** [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分器类型**：共五种，分为三大类：
  - *大模型评估*（分类型/数值型）：依赖裁判模型（如千问-Max）进行语义级评判，适用于问答质量、内容安全等场景；
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine/Fuzzy Match 等）或精确匹配逻辑，适用于翻译、摘要、Function Calling 等有确定性标准的场景；
  - *人工评估-分类型*：由人工标注 Pass/Fail，适用于创意写作、合规审核等主观性强的场景 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档1称“当前仅支持文本生成类模型评测”，文档2未明确限定模型类型，但其所有示例与参数说明均围绕文本生成展开，且文档1为更高层级的概览文档，应以文档1为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 备注 |
|----------|--------|------|--------|------|
| **通用** | 维度名称 | 最长20字符，建议采用“评估方面+评估方式”命名（如`回答准确性-LLM评分`） | 是 | 创建后可修改 |
| | 描述 | 最长100字符，用于补充说明评判目标 | 否 | — |
| **大模型评估专用** | 裁判模型 | 如千问-Max，影响评分质量与费用 | 是（仅大模型评估） | 推荐千问-Max以保障判分一致性 |
| | 评分器模板 | 预置（如综合评测、标准匹配）或自定义 | 是（仅大模型评估） | 切换会覆盖已编辑Prompt |
| | 评分范围 | 数值型维度专属，整数区间（默认0–5） | 是（仅数值型） | 范围过宽（>10）易降低LLM评分一致性 |
| | 通过阈值 | 判定Pass的最低分（数值型）或相似度（规则评估），步长0.1（数值型）/0.01（相似度） | 是（数值型/相似度型） | 与评分范围联动，业务容忍度决定阈值高低 |
| | Pass/Fail标签 | 分类型维度专属，标签互斥且穷尽 | 是（分类型） | 同一标签不可在Pass与Fail中重复出现 |
| **规则评估专用** | 比较操作符 | 相等/不相等/包含（字符串匹配） | 是（字符串匹配） | Function Calling常用“包含” |
| | 评估指标 | ROUGE-1/ROUGE-L/BLEU/Cosine/Fuzzy Match/Accuracy（文本相似度） | 是（文本相似度） | 翻译用BLEU，摘要用ROUGE-L，语义相关用Cosine |

所有评分器 Prompt 必须至少包含一个变量：`${prompt}`（用户问题）、`${output}`（模型回答）、`${completion}`（参考答案）。变量缺失将阻止提交 [配置评分器Prompt](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集。
2. **创建评测维度**：在控制台「模型评测 > 评测维度」创建至少一个维度模板。类型一经创建不可修改，选错需删除重建。
3. **创建评测任务**：
   - *自定义评测*：选择被评测模型、数据来源（评测数据集或推理结果集）、关联维度；可选开启排行参与（需绑定已有排行榜）。
   - *基线评测*：仅北京地域可见，选择模型与预置数据集（如MMLU、GSM8K），无需配置维度。
4. **查看结果**：
   - 「数据明细」Tab：逐条查看 `Prompt`、`Output`、`Completion` 及各维度评分；
   - 「指标统计」Tab：查看综合得分（各维度平均分）、通过率（≥通过阈值样本占比）、分数分布图；
   - 支持下载结果（待执行状态及基线评测任务不支持）。

> **注意**：文档1明确指出“模型评测当前仅支持控制台操作，不提供公开 API/SDK”，而文档2未提及接口能力。若需自动化，应参考 PAI Judge Model API 替代方案 [常见问题](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：基线评测仅在北京地域可用，其他地域控制台不显示该选项，属正常行为。
- **模型限制**：仅支持文本生成类模型；非文本生成模型（如多模态、语音）无法参与评测。
- **维度限制**：维度类型创建后不可修改；已被排行榜绑定的维度删除后，将导致排行榜无法创建新任务。
- **费用说明**：
  - 使用评测数据集时产生**被评测模型推理费用**（按[Token](../concepts/token.md)计费）；
  - 大模型评估维度产生**裁判模型评分费用**（按[Token](../concepts/token.md)计费）；
  - 规则评估与人工评估无裁判模型费用；
  - 使用推理结果集可规避被评测模型推理费用 [计费说明](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图逐维度分析短板。1–3%的分差通常属评测噪声，不宜作为决策依据。
- **成本优化建议**：
  - 小规模验证（50–100条）确认配置正确后再扩大规模；
  - 保存并复用推理结果集，避免重复推理；
  - 有确定性标准的场景优先选用规则评估（零裁判模型费用）。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


