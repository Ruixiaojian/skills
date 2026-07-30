# model data overview

百炼平台的模型数据体系围绕训练集与评测集构建，支持文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频等主流任务类型，并提供日志回流、数据清洗与增强等配套能力，帮助开发者高效构建高质量模型训练与评估数据。所有功能当前仅在华北2（北京）地域可用，部分能力（如日志回流）额外支持新加坡地域。

## 支持的模型/功能

- **训练集类型**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三类训练方式，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解（Qwen-VL 系列）、图生视频（首帧/首尾帧）等场景。其中 SFT 训练集细分为 ChatML 格式（含思考模型支持）、视觉理解专用格式；DPO 与 CPT 各有独立数据结构要求 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：当前仅支持文本生成类单轮对话评测集（Excel 或 JSONL 格式），用于模型效果量化评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据衍生能力**：
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练集或评测集，支持 SFT/DPO/CPT 三种训练方式及文本生成评测 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - **数据清洗与增强**：仅支持 SFT-文本生成训练集（ChatML 格式），提供敏感信息打码、去重、毒性消除等清洗算子，以及基于千问-Max 的 Few-Shot 数据增强能力 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 3 明确指出数据处理“暂不支持[SFT-图片理解训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)和[DPO-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)”，而文档 1 中 DPO 数据集明确列为支持类型。该矛盾表明 DPO 数据集虽可创建，但**不可通过数据清洗/增强功能进行后处理**——此为功能边界限制，非文档错误。

## 关键参数

- `loss_weight`：SFT 和 DPO 数据中用于调节样本相对重要性的浮点参数（范围 `0.0 ~ 1.0`），仅对 SFT 的最后一条 assistant 输出（思考模型）或全部 assistant 输出（标准 SFT），以及 DPO 的 `"chosen"` 字段生效。该参数属邀测功能，需联系商务经理开通 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- `resized_width` / `resized_height`：[多模态](../concepts/multi-modal.md)训练中图像/视频帧的缩放尺寸，单位像素，影响坐标标注基准（Qwen2.5-VL 使用绝对像素坐标，Qwen3-VL 使用 `[0, 999]` 归一化坐标） [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- `fps` / `sample_fps`：视频训练中控制帧率采样的关键参数，分别用于视频文件路径模式与图片帧列表模式 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- 日志回流 `预估日志回流数据`：系统估算值，用于提示是否超出单次 10 万条上限；实际回流条数可能略有偏差，属正常现象 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

- **数据集创建**：统一入口为 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data)，支持手动上传（ZIP 压缩包，含 `data.jsonl` 及媒体文件）或日志回流导入。
- **日志回流流程**：需先在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)页完成审计日志与推理日志的授权与开启（顺序不可逆），再配置时间范围、API Key、目标模型等参数创建任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据清洗/增强**：在数据管理 > 数据流页签创建自定义数据流，串联“数据清洗”与“数据增强”节点，再基于该数据流创建任务，指定待处理的 SFT-文本生成训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据处理（含日志回流追加、清洗增强）均生成新版本，原数据集不受影响，支持版本间对比与回滚。

## 限制和注意事项

- **地域限制**：所有文档均强调“本文档仅适用于华北2（北京）地域”；日志回流额外支持新加坡地域，其他 Region 不显示入口 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)、[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **格式与规模硬性要求**：
  - ZIP 包内 `data.jsonl` 必须位于根目录，文件名严格为 `data.jsonl`；
  - 图像单张 ≤ 1024px 宽高、≤ 10MB；图生视频图像/视频 ≤ 4096×4096；
  - CPT 训练集建议 ≥ 1000 万 [Token](../concepts/token.md)，SFT ≥ 数千条优质样本，DPO ≥ 百条偏好样本 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **存储与权限**：
  - 日志回流选择 OSS 挂载时，需额外授权 `AliyunServiceRoleForAccessCusOss` 和 `AliyunServiceRoleForSFMDataHubOSSImport` 角色，且评测集不支持 OSS 挂载 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - OSS 挂载数据集不支持“新增版本”操作，仅能通过“导入数据”页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **功能兼容性**：数据清洗与增强**仅支持 SFT-文本生成训练集（ChatML 格式）**，明确不支持多模态、DPO、CPT 类型 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


