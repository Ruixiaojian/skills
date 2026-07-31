# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、处理与版本控制能力，支撑模型调优（SFT/DPO/CPT）、评测及数据增强等核心场景。数据集分为训练集与评测集两类，支持多种导入方式、格式校验与质量治理能力，所有操作均通过控制台完成，暂不开放 API 接口。本文档整合关键能力与约束，面向开发者提供可直接落地的实践指南。

## 支持的模型/功能

- **训练集**：支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类训练场景；训练方法覆盖 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估，不可用于训练 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），提供数据清洗（如敏感信息打码、特殊内容移除）和数据增强（基于千问-Max 的 Few-Shot 生成）能力；SFT-图片理解、DPO 训练集暂不支持 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：将 SLS 推理日志转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）与评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京和新加坡**均可用。此处以文档 3 为准，新加坡 Region 同样支持 DPO/CPT 日志回流。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/限制 |
|------|------|------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） |
| 数据集类型 | 创建后不可变更 | 是 | `训练集` 或 `评测集` |
| 训练场景 | 仅训练集需选 | 是 | `文本生成` / `多模态理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集固定为文本生成 |
| 训练方法 | 仅训练集需选 | 是 | `SFT`（全站点）、`DPO`（北京/新加坡）、`CPT`（北京/新加坡） |
| 存储位置 | 创建后不可更改 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，评测集禁用） |
| 导入方式 | — | 是 | `本地上传`（小批量）、`OSS 导入`（大批量，需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权，仅最近 30 天日志） |
| 发布配置 | CPT/图生视频强制立即发布 | 是 | `草稿`（仅 SFT/DPO 文本生成支持）或 `立即发布` |

## 使用方式

- **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写参数并选择导入方式。SFT/DPO 文本生成支持多文件本地上传；OSS 导入需提前为目标 Bucket 添加标签 `bailian-datahub-access=read`；日志回流需先完成 SLS 审计日志与推理日志授权 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅对草稿状态的 SFT-文本生成训练集生效。在 [数据管理 > 数据流](https://bailian.console.aliyun.com/?tab=model#/efm/model_data) 中创建数据流（含清洗/增强节点），再通过“任务列表 > 从数据流列表创建任务”绑定目标训练集。处理完成后自动生成新版本（如 V1 → V2），原版本保留 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：入口包括模型监控页顶部按钮、模型监控详情页时间选择器旁按钮、或数据管理新建数据集时选择“日志回流”导入方式。配置时间范围（≤30 天）、API Key、模型等参数后提交；平台存储模式下导入完成即自动发布 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **版本管理**：同一数据集可创建多个版本。新增版本时可选“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集不支持继承，必须新建 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、云存储挂载、数据清洗/增强功能均仅限华北2（北京）；日志回流扩展支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **格式与兼容性**：SFT 训练集必须为 ChatML 格式 JSONL；DPO/CPT/多模态/评测集格式要求详见 [调优数据上传规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-support-matrix)；非 ChatML 格式的 SFT 数据无法用于数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **不可逆操作**：数据集发布后不可编辑；已发布版本删除不可恢复；仅草稿版本可删除 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与性能**：
  - 日志回流单次上限 10 万条，但可通过多次回流累积数据（非总量限制）[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - 数据增强-通用节点单次最多生成 2000 条样本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - CPT 训练建议数据量 ≥5000 万 [Token](../concepts/token.md)，SFT 建议 ≥1000 条，DPO 建议 ≥100 条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS，AES256）；敏感信息打码等清洗算子需显式开启 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


