# model evaluation introduction

模型评测是百炼平台提供的模型能力量化评估功能，支持通过自定义或基线方式对文本生成类模型进行多维度打分与横向对比。它覆盖从数据准备、维度定义、任务执行到结果分析的完整闭环，帮助开发者科学选型、验证调优效果并持续监控模型质量。当前功能仅面向文本生成类模型，不支持[多模态](../concepts/multi-modal.md)或语音等其他模态模型。

## 支持的模型与功能

- **支持模型类型**：仅限文本生成类模型（包括预置模型与调优后的模型），详见[预置模型列表](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)；[多模态](../concepts/multi-modal.md)、语音等模型暂不支持评测 [模型评测产品概览](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评测方式**：  
  - **自定义评测**：用户上传评测数据集（EvaluationSet 类型）或推理结果集，自主创建评测维度并关联执行，支持下载结果、加入排行榜、复用维度模板。  
  - **基线评测**：使用平台预置公开数据集（如 C-Eval、GSM8K、BBH 等），系统自动完成评分，但**仅北京地域可用**，且不支持结果下载、人工标注及排行榜参与 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **评分范式**：共五种评测维度类型，分为三大类：  
  - *大模型评估*（数值型/分类型）：依赖裁判模型（如千问-Max）进行语义级评判，适用于问答质量、内容安全等无确定性标准的场景；  
  - *规则评估*（字符串匹配/文本相似度）：基于算法（ROUGE/BLEU/Cosine/Fuzzy Match 等）或精确匹配逻辑，适用于翻译、摘要、Function Calling 等有明确标准的场景；  
  - *人工评估-分类型*：由人工逐条标注 Pass/Fail，适用于创意写作、合规审核等主观性强的场景 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  

> **注意**：文档1称“当前仅支持文本生成类模型评测”，而文档2未明确限定模型类型，但其所有示例与参数说明均围绕文本生成展开，且文档1为权威概述页，应以该表述为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 约束与建议 |
|----------|--------|------|--------|------------|
| **通用** | 维度名称 | 维度模板标识符 | 是 | ≤20 字符，建议采用“评估方面+评估方式”命名（如`回答准确性-LLM评分`） |
| | 描述 | 补充说明 | 否 | ≤100 字符 |
| **大模型评估专用** | 裁判模型 | 执行评分的 LLM | 是（仅大模型评估） | 推荐千问-Max；费用按 [Token](../concepts/token.md) 计费 |
| | 评分器 Prompt | 指导裁判模型评分的提示词 | 是（仅大模型评估） | 必须含至少一个变量：`${prompt}`、`${output}` 或 `${completion}`；长度 ≤50000 字符 |
| | 评分范围（数值型） | 整数区间，如 `0-5` | 是（仅数值型） | 最小值 ≥0，最大值 ≥1；范围过宽（如 >10）会降低评分一致性 |
| | 通过阈值 | 判定 Pass 的最低分值（数值型）或相似度（规则型） | 是（数值型/相似度型） | 数值型步长 0.1，相似度型范围 0–1、步长 0.01；需结合业务容忍度设定 |
| | Pass/Fail 标签（分类型） | 分类标签定义 | 是（分类型） | Pass 与 Fail 标签互斥且不可重复；简单场景建议二分类 |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。  
2. **创建维度**：在**模型评测 > 评测维度**页创建至少一个维度模板。推荐先用预置模板（如“综合评测”“标准匹配”）快速启动，再根据小样本验证结果迭代优化 Prompt [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建任务**：在**评测任务**页选择“自定义评测”，配置：  
   - 目标模型（预置或调优模型）；  
   - 数据来源（评测数据集 → 触发推理并计费；推理结果集 → 仅评分，零推理费用）；  
   - 关联已创建的维度（可多选）；  
   - System Prompt（可选，作用于被测模型，非裁判模型）。  
4. **执行与查看**：提交后状态流转为“待执行→进行中→评测完成”。完成后可在详情页的**指标统计**Tab 查看综合得分、通过率及分数分布，在**数据明细**Tab 查看每条样本的逐项评分 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
5. **进阶用法**：  
   - 将多个同维度任务加入**排行榜**，实现模型横向对比；  
   - 对人工评估任务，进入标注页面逐条标记；  
   - 下载结果文件用于离线归档或二次分析（基线评测不支持下载）。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常设计 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **不可逆操作**：  
  - 评测维度类型创建后**不可修改**，选错需删除重建（已有任务不受影响）；  
  - 删除被排行榜绑定的维度会导致排行榜无法新建任务；  
  - 终止评测任务后，已评测数据保留但不可恢复继续。  
- **费用相关**：  
  - 使用评测数据集时产生被测模型推理费用；  
  - 大模型评估维度产生裁判模型评分费用（按 [Token](../concepts/token.md)）；  
  - 规则评估与人工评估无裁判模型费用；  
  - 成本优化建议：先用 50–100 条数据小规模验证，再复用推理结果集避免重复推理 [计费说明](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **结果解读**：  
  - 综合得分是各维度平均分，可能掩盖维度间差异，**务必结合分数分布图与逐维度分析**；  
  - 1–3% 的分数差异通常属评测噪声，不宜作为决策依据；  
  - 人工评估任务需全部标注完成后才变为“评测完成”状态。  
- **API 支持**：当前模型评测功能**仅支持控制台操作，不提供公开 API/SDK**；如需自动化，可参考 PAI Judge Model API 替代 [常见问题](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


