# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、版本控制与处理能力，支撑模型调优（SFT/DPO/CPT）、评测及数据增强等核心场景。所有数据集均按用途严格划分为训练集与评测集，存储与导入方式灵活，但关键约束（如地域限制、格式要求、草稿支持）需在创建前明确。本文档整合最新实践，聚焦开发者实际使用路径。

## 支持的模型/功能

- **训练集**：支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类训练场景；训练方法覆盖 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）。  
- **评测集**：仅支持文本生成场景，用于模型效果客观评估。  
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），提供敏感信息打码、特殊内容移除等清洗算子，以及基于千问-Max 的 Few-Shot 数据增强能力。  
- **日志回流**：支持将 SLS 推理日志转化为结构化训练集或评测集，适用于文本生成场景下的 SFT/DPO/CPT 训练 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
> **注意**：文档 3 明确指出数据清洗/增强“暂不支持[SFT-图片理解训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)和[DPO-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)”，而文档 1 表格中“支持场景”列未限定 DPO 是否可用，此处以文档 3 的明确限制为准。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/约束 |
|------|------|------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点 |
| 数据集类型 | 创建后不可变更 | 是 | `训练集` / `评测集` |
| 训练场景 | 仅训练集需选 | 是 | `文本生成` / `多模态理解` / `图生视频(首帧)` / `图生视频(首尾帧)` |
| 训练方法 | 仅训练集需选 | 是 | `SFT` / `DPO` / `CPT`（CPT 仅北京地域） |
| 存储位置 | 影响计费与权限 | 是 | `平台 OSS 存储`（免费） / `云存储挂载`（仅训练集，需额外授权） |
| 导入方式 | 决定前置条件 | 是 | `本地上传` / `OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`） / `日志回流`（需 SLS 授权） |
| 发布配置 | CPT 和图生视频强制立即发布 | 是 | `草稿`（SFT/DPO 文本生成支持） / `立即发布` |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写参数并选择导入方式。  
2. **导入数据**：  
   - *本地上传*：直接上传符合格式的 JSONL（SFT/DPO/CPT/评测集）、ZIP（多模态）文件；  
   - *OSS 导入*：需提前为目标 Bucket 添加标签 `bailian-datahub-access=read`，仅训练集可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；  
   - *日志回流*：需先完成审计日志与推理日志开通及角色授权，支持分批次回流（单次 ≤10 万条），可追加至同一数据集的不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
3. **数据处理（可选）**：对 SFT-文本生成训练集（草稿或已发布版本），在数据管理 > 数据流页签创建清洗/增强任务，生成独立新版本，**不覆盖原数据**。  
4. **下游调用**：训练集 ID 通过 `training_file_ids` 参数传入模型调优 API；评测集 ID 用于模型评测任务。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均**仅限华北2（北京）**；日志回流在新加坡 Region 也支持 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **格式与兼容性**：  
  - 多模态/图生视频训练集无官方推荐数据量，需自行验证；  
  - 数据清洗/增强**仅接受 ChatML 格式 SFT-文本生成训练集**，其他类型（如 DPO、多模态）不支持；  
  - 评测集导出格式为 XLSX，训练集导出为 JSONL（SFT）或 ZIP（多模态）。  
- **版本与操作**：  
  - CPT 训练集**不支持数据继承**，每次新增版本必须重新导入全部数据；  
  - 发布与删除操作**不可逆**，已发布版本不可编辑，仅草稿版本可删除；  
  - OSS 挂载数据集**不支持“新增版本”操作**，追加数据须通过“导入数据”页完成。  
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务分别产生对应账单，详见百炼计费页面。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


