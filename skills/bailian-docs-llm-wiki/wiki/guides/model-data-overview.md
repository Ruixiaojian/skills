# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/[多模态](../concepts/multi-modal.md)/图生视频）和评测集的创建、导入、版本管理与质量增强。所有数据集均通过控制台统一管理，支持多种导入方式与存储策略，并与模型调优、评测及日志回流形成闭环工作流。

## 支持的模型/功能

- **训练集类型**：支持文本生成、[多模态](../concepts/multi-modal.md)理解（图/视频→文本）、图生视频（首帧/首尾帧）四类训练场景；其中 SFT 和 DPO 仅限文本生成，CPT 当前仅支持文本生成场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于[多模态](../concepts/multi-modal.md)或图生视频任务 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理能力**：支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（Few-Shot 生成），暂不支持 DPO、CPT 或多模态训练集的数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流能力**：支持将 SLS 推理日志转化为结构化训练集或评测集，覆盖 SFT/DPO/CPT 文本生成及评测场景，但当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档1称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档2明确日志回流在**北京和新加坡**均可用。实际支持地域以控制台入口为准——若新加坡 Region 显示日志回流入口，则该功能在该地域有效；其余功能（如 CPT 训练、OSS 挂载）仍仅限北京。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值约束 |
|------|------|----------|-----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（`.`） |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更 |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧） / 图生视频（首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是（训练集） | 评测集不显示此字段；CPT 不支持草稿与数据继承 |
| 存储位置 | 平台 OSS 存储 / 云存储挂载 | 是 | 评测集不支持云存储挂载 |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | 评测集不支持 OSS 导入；日志回流需提前授权 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| 发布配置 | 草稿 / 立即发布 | 是 | CPT 和图生视频训练集强制“立即发布”，不支持草稿 |

- **数据量建议**：SFT ≥1000 条、DPO ≥100 条、CPT ≥5000 万 [Token](../concepts/token.md)；多模态/图生视频无官方推荐量，需按场景充分准备 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流限制**：单次最多回流 10 万条，时间范围限最近 30 天；预估条数为近似值，实际结果可能略有偏差 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写参数并选择导入方式。
2. **导入数据**：
   - *本地上传*：直接上传符合格式要求的文件（如 SFT 的 JSONL），支持多文件；
   - *OSS 导入*：目标 Bucket 需添加标签 `bailian-datahub-access=read`；
   - *日志回流*：需先完成 SLS 审计日志与推理日志开通及角色授权，再配置时间范围、API Key、模型等筛选条件 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **版本管理**：已发布数据集可通过“新增版本”迭代更新，支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集仅支持新建模式。
4. **数据处理（可选）**：仅对 SFT-文本生成训练集（ChatML 格式）生效，在“数据流”页签创建清洗/增强任务，输出为独立新版本，原数据集不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：CPT 训练、OSS 挂载、数据清洗/增强功能**仅在北京地域可用**；日志回流扩展至新加坡，但其他功能未同步开放 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **不可逆操作**：数据集发布后不可编辑；删除已发布版本或整个数据集均不可恢复；请务必确认后再操作 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式强约束**：各训练场景有严格数据格式要求（如 SFT 必须为 ChatML JSONL），建议下载对应模板校验；评测集导出为 XLSX，SFT 训练集导出为 JSONL [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流依赖链**：必须**先开通审计日志，再开通推理日志**；关闭时顺序相反；关闭后历史日志不可复原 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **OSS 挂载特殊性**：选择 OSS 挂载时需额外授权两个服务角色（`AliyunServiceRoleForAccessCusOss` 和 `AliyunServiceRoleForSFMDataHubOSSImport`），且不支持“新增版本”，只能通过“导入数据”页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


