# model data overview

百炼平台的模型数据体系围绕训练集与评测集构建，支持从原始日志回流、本地/OSS 导入到清洗增强的全链路数据治理。所有数据集均以结构化 JSONL（或指定格式）存储，服务于模型调优（SFT/DPO/CPT）与评测两大核心场景。数据管理功能本身免费，但底层存储（平台 OSS 或用户 OSS）、SLS 日志服务及模型推理等资源按各自产品计费。

## 支持的模型/功能

- **数据集类型**：明确分为**训练集**（用于模型调优）和**评测集**（用于模型评测），创建后不可变更类型 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **训练场景与方法**：
  - 训练集支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类场景；评测集**仅支持文本生成**。
  - 训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 和 CPT **仅在华北2（北京）地域可用** [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据来源能力**：
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练/评测数据集，形成“推理→数据→微调”闭环 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - **数据处理**：支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），**暂不支持 DPO、CPT 及多模态训练集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 1 明确日志回流仅在**华北2（北京）和新加坡**可用。二者存在地域覆盖矛盾：DPO/CPT 在新加坡 Region 不支持日志回流作为数据源，但文档未说明新加坡是否支持 DPO/CPT 训练本身。开发者应以控制台实际可用选项为准，优先在华北2（北京）开展 DPO/CPT 全流程。

## 关键参数

| 参数 | 说明 | 约束与取值 |
|------|------|------------|
| **数据集名称/描述** | 名称最长 50 字符（中英文/数字/下划线/连字符/点），描述最长 200 字符 | 创建后不可修改 |
| **数据集类型** | 必选：`训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 多模态理解 / 图生视频（首帧/首尾帧） | 评测集仅允许“文本生成” |
| **训练方式** | SFT / DPO / CPT（仅训练集显示） | DPO/CPT 仅北京可用；CPT 不支持草稿 |
| **存储位置** | `平台 OSS 存储`（默认，免费）或 `云存储挂载`（OSS 挂载） | 评测集不支持 OSS 挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传 / OSS 导入 / 日志回流 | 日志回流需授权、仅最近 30 天、单次 ≤10 万条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **时间范围（日志回流）** | 筛选 SLS 日志的时间段 | 最近 30 天（含当天），精确到秒；修改后重置 API Key 与模型选择 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |

## 使用方式

1. **创建数据集**：  
   进入 **[数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)**，点击“新增数据集”，依次填写名称、类型、场景、训练方式、存储位置、导入方式及发布配置（草稿/立即发布）。CPT 和图生视频训练集强制立即发布。

2. **日志回流专用流程**：  
   - 前置授权：在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)页完成审计日志（必须先开启）和推理日志的 SLS 角色授权与开通 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
   - 配置筛选：在日志回流表单中严格按顺序设置时间范围 → API Key 过滤 → 模型选择 → 回流位置等参数。预估条数超 10 万时需缩小范围。  
   - 追加数据：已有数据集可通过“导入数据”页追加日志回流（所有存储类型均支持），或通过“新增版本”弹窗（仅平台存储支持）。

3. **数据清洗与增强**：  
   - 仅适用于**SFT-文本生成训练集（ChatML 格式）**，且必须位于华北2（北京） [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
   - 在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)** 中创建数据流（如：敏感信息打码 → 数据增强），再基于该数据流创建任务，选择目标训练集启动处理。处理完成后自动生成新版本，原版本不受影响。

## 限制和注意事项

- **地域限制**：  
  - 日志回流仅在**华北2（北京）和新加坡**可用；  
  - DPO、CPT 训练方法及数据处理功能**仅在华北2（北京）可用** [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
  > **注意**：文档 1 提到新加坡支持日志回流，但文档 2 未确认新加坡是否支持 DPO/CPT。若需使用 DPO/CPT，务必在华北2（北京）操作，避免因地域不一致导致流程中断。

- **数量与容量**：  
  - 单次日志回流上限 **10 万条**（非数据集总量限制），可多次回流至同一数据集不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；  
  - 数据集总数与单个数据集数据量**无硬性上限**，但 CPT 要求数据量至少达 **5000 万 [Token](../concepts/token.md)** [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；  
  - 数据处理中“数据增强-通用”节点**单次最多生成 2000 条样本** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

- **功能与兼容性限制**：  
  - 评测集**不支持 OSS 导入和 OSS 挂载存储**；  
  - CPT 和图生视频训练集**不支持草稿状态和数据继承**，每次新增版本必须新建数据；  
  - 数据处理**不支持 DPO、CPT、多模态训练集及非 ChatML 格式数据** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；  
  - 日志回流生成的数据集**不可编辑内容**，仅能通过“导入数据”或“新增版本”追加新批次 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

- **安全与费用**：  
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；  
  - 日志回流产生的 SLS 存储与读写费用归属 SLS 账单；OSS 挂载存储费用归属用户自有 OSS 账单；平台 OSS 存储费用按百炼计费规则收取 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


