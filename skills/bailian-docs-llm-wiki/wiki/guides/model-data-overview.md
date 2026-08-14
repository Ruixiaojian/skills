# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可版本化、可处理的数据基础设施。它支持训练集（SFT/DPO/CPT/多模态/图生视频）和评测集的全生命周期管理，涵盖创建、导入、清洗、增强、版本控制与下游集成。所有操作均通过控制台完成，API 仅支持引用已发布数据集 ID。

## 支持的模型与功能

- **训练集类型**：支持文本生成、多模态理解（图/视频→文本）、图生视频（首帧、首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集类型**：仅支持文本生成场景，不可用于多模态或图生视频 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **数据处理能力**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行数据清洗（如敏感信息打码、特殊内容移除）和数据增强（通用/分类/抽取/创作场景），暂不支持 DPO、CPT、多模态训练集的数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流能力**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，可用于 SFT/DPO/CPT 训练集或文本生成评测集，覆盖北京与新加坡地域 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档2称“数据处理暂不支持 DPO-文本生成训练集”，而文档1明确将 DPO 列为训练方法且支持日志回流生成 DPO 训练集；但文档2未说明 DPO 数据是否可被清洗/增强。实际能力以控制台为准：当前仅 SFT-文本生成训练集支持数据处理，DPO/CPT/多模态训练集均不支持——该限制在三篇文档中一致，无矛盾。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/约束 |
|------|------|------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符；支持中文、英文、数字、下划线、连字符、点（文档1）或斜杠（文档3）；创建后不可修改 |
| 数据集类型 | 决定用途与后续能力 | 是 | `训练集` 或 `评测集`；创建后不可变更 |
| 训练场景 | 限定数据语义与格式要求 | 是（训练集） | `文本生成` / `多模态理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 绑定调优算法与数据规范 | 是（训练集） | `SFT` / `DPO` / `CPT`；CPT 仅限北京地域，且不支持草稿与数据继承 |
| 存储位置 | 影响计费与管理方式 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用）；评测集禁用挂载 |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖）、`OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权与日志开通） |
| 发布配置 | 控制数据就绪状态 | 是 | `草稿`（可编辑）或 `立即发布`；CPT 和图生视频训练集强制 `立即发布` |

## 使用方式

1. **创建数据集**：在 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data) 页面点击「新增数据集」，按向导填写上述参数并选择导入方式。  
2. **导入数据**：  
   - 本地上传：直接拖拽或选择文件（SFT/DPO 文本生成支持多文件）；  
   - OSS 导入：确保目标 Bucket 已添加标签 `bailian-datahub-access=read`；  
   - 日志回流：需先在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)完成审计日志与推理日志的授权及开通，再配置时间范围、API Key、模型等筛选条件 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
3. **数据处理（仅 SFT-文本生成）**：在数据集详情页进入「数据处理」Tab，基于预置模板或自定义数据流（含清洗+增强节点），启动任务生成新版本；处理结果独立保存，不覆盖原版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
4. **版本管理**：已发布数据集可通过「新增版本」迭代，支持「继承模式」（增量修改）或「新建模式」（全量替换）；CPT 训练集强制使用「新建模式」。  
5. **下游调用**：模型调优 API 通过 `training_file_ids` 参数传入已发布训练集 ID；评测集在模型评测任务中直接选择。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均**仅限华北2（北京）**；多模态/图生视频训练集暂无官方推荐数据量 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **格式与兼容性**：数据处理仅接受 ChatML 格式的 SFT-文本生成训练集；日志回流产出 JSONL；评测集导出为 XLSX；OSS 导入不支持评测集 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **容量与频次**：日志回流单次上限 10 万条（可多次追加）；数据集存储无总量上限，但日志回流预估超限时表单按钮禁用；SFT 建议 ≥1000 条，DPO ≥100 条，CPT ≥5000 万 [Token](../concepts/token.md) [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **不可逆操作**：发布、删除（仅草稿可删）、覆盖版本均不可恢复；已发布版本不可编辑，仅草稿版本支持在线修改 Prompt/Completion [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **权限与授权**：OSS 导入需 Bucket 标签；日志回流需 SLS 角色授权（`AliyunServiceRoleForSFMAccessSLS` 等）；OSS 挂载存储需额外两个角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


