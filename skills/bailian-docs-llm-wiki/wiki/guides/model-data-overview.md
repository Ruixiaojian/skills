# model data overview

百炼平台的模型数据体系为大模型调优与评测提供端到端的数据支撑能力，涵盖训练集、评测集的构建、清洗、增强及自动化回流。所有功能当前仅在华北2（北京）和新加坡地域可用，且依赖统一的数据管理控制台进行生命周期操作。数据格式以 JSONL 为主，强调结构化、可版本化与任务场景强对齐。

## 支持的模型/功能

平台支持三类核心数据用途：**训练集**（用于 SFT、DPO、CPT、图生视频等调优任务）、**评测集**（用于文本生成类模型效果评估）以及**日志回流生成的数据集**（将 SLS 推理日志自动转化为结构化训练/评测数据）。  
- **训练集类型**包括：SFT（含 ChatML 格式、思考模型、千问VL 多模态）、DPO、CPT、图生视频（首帧/首尾帧）；详见 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集类型**目前仅支持单轮文本生成 Excel 或 JSONL 格式；同上文文档。  
- **日志回流**支持将 SLS 推理日志转化为 SFT/DPO/CPT 训练集或文本生成评测集，是闭环数据飞轮的关键环节；详见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
> **注意**：文档2明确指出数据清洗与增强**暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集**，而文档1中 VL 和 DPO 格式均被列为“支持”，此处存在功能覆盖范围矛盾，实际使用时请以控制台可用算子为准。

## 关键参数

| 参数 | 适用场景 | 说明 | 约束 |
|------|----------|------|------|
| `loss_weight` | SFT（所有 assistant 行）、SFT-thinking（仅最后一行）、DPO（`chosen` 字段） | 控制单条样本或单个 assistant 输出在训练中的相对重要性 | 取值范围 `0.0 ~ 1.0`；属邀测参数，需联系商务经理开通 |
| `resized_width` / `resized_height` | 千问VL 视觉理解训练集 | 图像/视频帧缩放目标尺寸（像素） | 非必填；图像单边 ≤ 1024px，视频分辨率 ≤ 4096×4096 |
| `fps` / `sample_fps` | 千问VL 视频训练（qwen3.5+） | 视频帧率采样控制 | `fps` 用于视频文件路径模式，`sample_fps` 用于图片帧列表模式 |
| `video_start` / `video_end` | 千问VL 视频训练（qwen3.5+） | 视频截取时间范围（秒） | 仅视频文件路径模式支持 |
| `foreignKey` | 数据增强节点输出 | 系统自动生成的唯一标识字段 | 不影响模型调优，无需手动删除；详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |

## 使用方式

1. **创建数据集**：通过 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 控制台上传 ZIP 包（SFT/VL/图生视频）或 Excel/JSONL 文件（评测集），或使用日志回流功能自动拉取 SLS 日志。  
2. **数据处理**：对 SFT-文本生成训练集（ChatML 格式），可在控制台配置数据流任务，组合「数据清洗」（如敏感信息打码、去重）与「数据增强」（基于千问-Max 的 Few-Shot 生成）节点；该能力**不支持 API 调用**，详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
3. **日志回流**：在模型监控页开启审计日志与推理日志后，按时间范围、API Key、模型等条件筛选，选择平台存储或 OSS 挂载方式生成结构化数据集；单次上限 10 万条，支持多版本追加。

## 限制和注意事项

- **地域限制**：所有功能（训练集管理、数据清洗、日志回流）均仅在华北2（北京）和新加坡 Region 可用；文档1与文档3均强调此约束，文档2虽未重复说明，但上下文一致。  
- **格式与结构硬约束**：  
  - SFT/VL 训练集 ZIP 包内 `data.jsonl` 必须位于根目录，图片/视频文件名全局唯一，仅支持 ASCII 字符命名；  
  - 图生视频 ZIP 包中 `first_frame_path`/`last_frame_path`/`video_path` 字段值**必须为纯文件名**（不含路径），否则解析失败；  
  - CPT 训练集仅接受 `{"text":"..."}` 单字段 JSONL，不支持 `messages` 结构。  
- **功能兼容性限制**：  
  - 数据清洗与增强**仅支持 SFT-文本生成（ChatML）训练集**，明确不支持 VL、DPO、CPT 及图生视频类数据集；  
  - 日志回流生成的评测集**不支持 OSS 挂载**，仅限平台存储；  
  - OSS 挂载数据集**不支持「新增版本」操作**，追加数据必须通过「导入数据」页完成。  
- **版本管理**：所有数据处理（清洗、增强、日志回流）均生成独立新版本，原数据集不受影响，需在下游任务中显式选择目标版本。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


