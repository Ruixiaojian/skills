# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与对比。它覆盖从数据准备、维度定义、任务执行到结果分析的完整链路，帮助开发者科学选型、验证调优效果并持续监控模型质量。当前功能仅面向文本生成类模型，不支持[多模态](../concepts/multimodal.md)或语音等其他模态模型。

## 支持的模型与功能

- **支持模型类型**：仅支持文本生成类模型（包括预置模型与调优后模型），详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)；[多模态](../concepts/multimodal.md)、语音等模型暂不支持 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评测方式**：提供**自定义评测**（用户上传数据集 + 自定义维度）和**基线评测**（平台预置公开数据集，仅北京地域可用）两种模式 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评分器类型**：共 5 种，分为三类范式：  
  - *大模型评估*（分类型/数值型）：依赖裁判模型（如千问-Max）进行语义级评判，适用于问答质量、内容安全等场景；  
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine 等）自动计算，适用于翻译、摘要、Function Calling 等有确定性标准的场景；  
  - *人工评估-分类型*：由人工标注 Pass/Fail，适用于创意写作、合规审核等主观性强的场景 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  

> **注意**：文档 1 称“基线评测仅北京地域可用”，而文档 2 未提及地域限制，但明确其使用“平台预设的公开数据集”且“不支持推理结果集”。二者一致，故以文档 1 的地域约束为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 取值示例 |
|----------|--------|------|--------|----------|
| **通用** | 维度名称 | 最长 20 字符，建议采用“评估方面+评估方式”命名（如`回答准确性-LLM评分`） | 是 | `安全性-分类型` |
| | 描述 | 最长 100 字符，补充维度目标 | 否 | `检测输出是否含违法不良信息` |
| **大模型评估** | 裁判模型 | 执行评分的 LLM，影响费用与准确性 | 分类型/数值型必填 | `qwen-max` |
| | 评分器 Prompt | 含 `${prompt}`、`${output}`、`${completion}` 至少一个变量，定义评判逻辑 | 是 | `请判断${output}是否符合${prompt}要求且无事实错误，仅输出Pass或Fail` |
| | 评分范围（数值型） | 整数区间，最小值 ≥ 0，最大值 ≥ 1 | 数值型必填 | `0~5` |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则型），步长 0.1（数值）/0.01（相似度） | 数值型/相似度型必填 | `3.0`（数值）、`0.75`（相似度） |
| **规则评估** | 比较操作符（字符串匹配） | `相等`/`不相等`/`包含` | 是 | `包含`（用于 Function Calling 验证） |
| | 评估指标（文本相似度） | 支持 ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 是 | `ROUGE-L`（摘要任务） |
| **人工评估** | Pass/Fail 标签 | 标签互斥且穷尽，各标签 ≤ 20 字符 | 是 | `合规`/`不合规` |

## 使用方式

1. **准备数据**：在数据管理模块上传 **评测集（EvaluationSet）类型** 数据，至少包含 `Prompt`（问题）和 `Completion`（参考答案）两列；若复用已有输出，可上传含 `Output` 的推理结果集 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
2. **创建维度**：在控制台 **模型评测 > 评测维度** 创建模板，选择类型并配置参数（如裁判模型、Prompt、阈值等）；维度创建后类型不可修改，需删除重建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建任务**：在 **评测任务** Tab 选择评测方式（自定义/基线），指定被评测模型、数据来源（评测集/推理结果集）、关联维度；若参与排行，需绑定已创建的排行榜 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
4. **查看结果**：任务状态为“评测完成”后，在详情页的 **指标统计** Tab 查看综合得分、通过率及分布图；**数据明细** Tab 查看每条样本的逐项评分。支持下载 CSV 结果文件（基线评测不支持下载）。

## 限制和注意事项

- **模型限制**：仅支持文本生成类模型，图像、语音等模态暂不支持；基线评测仅限北京地域可用，其他地域控制台不显示该选项 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **维度限制**：维度类型创建后不可修改；已被排行榜绑定的维度删除后，将导致排行榜无法新建任务 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **费用说明**：费用由两部分构成——被评测模型的推理费（使用评测数据集时产生）和裁判模型的评分费（仅大模型评估维度产生）；规则评估与人工评估无裁判模型费用 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图逐维度分析短板；1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **API 支持**：当前模型评测功能**仅支持控制台操作，不提供公开 API 或 SDK**；如需自动化，可参考 PAI Judge Model API 替代 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


