# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、清洗、增强与回流能力，支撑大模型训练（SFT/DPO/CPT）、评测及[多模态](../concepts/multi-modal.md)任务。所有数据操作均通过控制台 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 统一入口进行，当前功能**仅适用于华北2（北京）和新加坡地域**。本文档整合训练集、评测集、数据处理与日志回流的核心规范，面向开发者提供可直接落地的结构化参考。

## 支持的模型/功能

百炼支持以下模型类型与对应的数据功能：

- **文本生成类模型**：全面支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三类训练方式，以及文本生成评测集构建；
- **[多模态](../concepts/multi-modal.md)理解模型（如 Qwen-VL 系列）**：支持 SFT 训练，需遵循 ChatML 格式并严格满足图像/视频字段要求（如 `content` 必须为数组格式）；
- **图生视频模型（如 wan-i2v / wan-kf2v）**：支持基于首帧或首尾帧的训练集与验证集构建，需按指定 ZIP 结构组织 `data.jsonl`、图像及视频文件；
- **思考模型（Thinking）**：仅对最后一条 `assistant` 输出进行训练，且必须用 `<think>` 标签包裹思考内容，详见 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

> **注意**：文档 2 明确指出数据清洗与增强**暂不支持 SFT-图片理解训练集和 DPO 训练集**，而文档 1 中未限定该限制。实际使用时请以 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) 的说明为准——即仅支持 SFT-文本生成（ChatML 格式）训练集。

## 关键参数

| 参数 | 适用场景 | 类型 | 取值范围 | 说明 |
|------|----------|------|-----------|------|
| `loss_weight` | SFT（所有 assistant 行）、SFT-Thinking（仅最后 assistant 行）、DPO（`chosen` 字段） | float | `0.0 ~ 1.0` | 控制单条样本/输出在训练中的相对重要性；属邀测功能，需联系商务经理开通 |
| `resized_width` / `resized_height` | [多模态](../concepts/multi-modal.md) SFT（图像/视频） | int | ≥ 1 | 图像/视频帧缩放目标尺寸（像素），影响坐标标注基准（Qwen2.5-VL 用绝对像素，Qwen3-VL 用 `[0,999]` 相对坐标） |
| `fps` / `sample_fps` | 多模态 SFT（视频） | float | > 0 | 视频输入帧率（`fps`）或图片帧序列帧率（`sample_fps`），仅 Qwen3.5+ VL 模型支持 |
| `foreignKey` | 数据增强节点输出 | string | 自动生成 | 增强后自动添加的标识字段，**无需删除，不影响训练** |

## 使用方式

1. **数据集创建**：  
   - 训练集/评测集上传：ZIP 包（≤2 GB）或 Excel 文件（仅评测集），`data.jsonl` 必须位于 ZIP 根目录；  
   - 日志回流：通过 [模型监控](https://bailian.console.aliyun.com/#/model-telemetry) 或 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 入口配置时间范围、API Key、模型等参数，单次上限 10 万条，支持追加版本；详情见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

2. **数据清洗与增强**：  
   - 仅支持 SFT-文本生成训练集（ChatML 格式）；  
   - 在控制台「数据流」中编排节点：先清洗（如敏感信息打码），再增强（如 Few-Shot 生成）；  
   - 处理结果自动生成新版本（如 V1 → V2），原数据集不受影响。

3. **格式校验要点**：  
   - SFT ChatML：`system` 消息中 `content` 必须为 `[{ "text": "..." }]` 数组格式；  
   - DPO：`chosen`/`rejected` 必须为单个 `{"role": "assistant", "content": "..."} ` 对象；  
   - 图生视频：ZIP 内路径名仅支持 ASCII 字符（a-z, A-Z, 0-9, `_`, `-`），图片/视频文件名全局唯一。

## 限制和注意事项

- **地域限制**：所有功能（训练集管理、数据处理、日志回流）均**仅限华北2（北京）和新加坡 Region**，其他地域不可用；
- **格式与容量**：  
  - ZIP 包最大 2 GB（训练集）或 20 MB（图生视频 `data.jsonl`）；  
  - 图片单张 ≤ 1024×1024 px 且 ≤ 10 MB；视频 ≤ 4096×4096 px；  
  - 文本生成评测集仅支持单轮对话 Excel 格式（`.xlsx`），多轮不生效；
- **版本与覆盖**：数据清洗/增强、日志回流均生成**独立新版本**，不会覆盖原始数据集，但需手动切换版本用于训练；
- **模型兼容性**：  
  - 视频参数（`fps`, `video_start` 等）仅 Qwen3.5+ VL 模型支持；  
  - 思考模型训练后，若样本中存在无 `<think>` 标签的 `assistant` 输出，则**不建议开启思考模式调用**；
- **权限与费用**：日志回流需提前开通 SLS 并授权服务角色；推理日志开启后将产生 SLS 存储与读写费用，长期不用应及时关闭。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


