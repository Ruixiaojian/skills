# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可版本化的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/多模态/图生视频）和评测集两类核心资源。所有数据集均支持结构化导入、版本迭代、质量处理及下游任务集成，是模型效果优化的关键基础设施。

## 支持的模型与功能

- **训练集类型**：支持文本生成、多模态理解（图/视频→文本）、图生视频（首帧/首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集类型**：仅支持文本生成场景，用于模型泛化能力客观评估，不可用于训练。  
- **数据处理能力**：支持对 SFT-文本生成训练集（ChatML 格式）进行数据清洗（如敏感信息打码、特殊内容移除）和数据增强（通用/分类/抽取/创作等场景），但暂不支持 DPO、CPT 及多模态训练集的数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流能力**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，可用于 SFT/DPO/CPT 训练集或文本生成评测集，覆盖北京与新加坡地域 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京与新加坡**均可用。实际支持地域以文档 3 为准，新加坡 Region 已扩展支持日志回流创建 DPO/CPT 训练集。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/约束 |
|------|------|------|----------------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符；支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；创建后不可修改 |
| 数据集类型 | 决定用途与下游能力 | 是 | `训练集` 或 `评测集`；创建后不可变更 |
| 训练场景 | 限定数据语义与格式要求 | 是（训练集） | `文本生成` / `多模态理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 影响数据格式、最小数据量与草稿支持 | 是（训练集） | `SFT`（全站支持，支持草稿）、`DPO`（北京/新加坡，支持草稿）、`CPT`（北京/新加坡，**不支持草稿**） |
| 存储位置 | 影响计费主体与管理方式 | 是 | `平台 OSS 存储`（免费托管，自动发布）或 `OSS 挂载`（用户自有 Bucket，需标签 `bailian-datahub-access=read`，评测集禁用） |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖）、`OSS 导入`（需 Bucket 标签）、`日志回流`（需 SLS 授权与日志开通） |

> **注意**：文档 1 与文档 3 对“OSS 挂载”的授权要求存在表述差异——文档 1 仅提“Bucket 标签”，文档 3 补充明确需额外授权两个服务角色（`AliyunServiceRoleForAccessCusOss` 和 `AliyunServiceRoleForSFMDataHubOSSImport`）。实际操作中须按文档 3 完成全部角色授权，否则 OSS 挂载失败。

## 使用方式

1. **创建数据集**：在控制台 **数据管理 > 数据集 > 新增数据集**，依次填写名称、类型、场景、方法、存储位置、导入方式及发布配置（草稿/立即发布）。CPT 与图生视频训练集强制“立即发布”。  
2. **导入数据**：  
   - *本地上传*：直接上传符合格式的文件（SFT/DPO/CPT/评测集各需对应模板）；  
   - *OSS 导入*：指定已打标 Bucket 路径，仅限训练集；  
   - *日志回流*：在模型监控页或数据管理页入口配置时间范围、API Key、模型等筛选条件，单次上限 10 万条 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
3. **版本管理**：已发布数据集可通过 **新增版本** 迭代，支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集**不支持继承**，每次必须新建 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
4. **数据处理（仅 SFT 文本生成）**：在 **数据管理 > 数据流** 创建清洗/增强任务，选择目标训练集草稿或已发布版本，任务完成后自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、OSS 挂载、数据处理功能均**仅限华北2（北京）**；日志回流额外支持**新加坡**；多模态/图生视频训练集暂无官方推荐数据量。  
- **格式强约束**：SFT/DPO/CPT/评测集均有严格 JSONL 或 ZIP 格式要求，务必下载对应模板校验；数据处理**仅接受 ChatML 格式 SFT 文本训练集**，其他格式（含 DPO、多模态）不兼容。  
- **不可逆操作**：数据集发布后不可编辑；删除已发布版本或整个数据集**不可恢复**；日志回流任务执行中不可终止。  
- **容量与配额**：  
  - 单次日志回流上限 10 万条（可多次追加至不同版本）；  
  - 数据集数量无上限，但单次 OSS 导入/本地上传建议 ≤10 GB；  
  - CPT 训练建议 ≥5000 万 [Token](../concepts/token.md)，SFT 建议 ≥1000 条，DPO 建议 ≥100 条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗算子需显式开启，不默认执行。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


