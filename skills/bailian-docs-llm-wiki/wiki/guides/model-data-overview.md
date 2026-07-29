# model data overview

百炼平台的模型数据体系为模型调优与评测提供结构化、可管理的数据支撑，涵盖训练集、评测集的构建、处理与回流三大核心能力。所有功能当前仅在华北2（北京）和新加坡地域可用，数据集统一通过[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)控制台进行生命周期管理。本文档面向开发者，聚焦数据格式、参数约束与工程实践要点。

## 支持的模型/功能

- **训练集类型**：支持文本生成（SFT、DPO、CPT）、多模态理解（Qwen-VL 系列）、图生视频（首帧/首尾帧）三类训练场景；其中 SFT 和 DPO 均要求 ChatML 格式，CPT 为纯文本 JSONL；图生视频需 ZIP 压缩包含 `data.jsonl` 及对应图像/视频文件。  
- **评测集类型**：当前仅支持文本生成单轮对话评测集（Excel 或 JSONL 格式），用于模型泛化能力评估。  
- **数据处理能力**：支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、重复去重）与增强（基于千问-Max 的 Few-Shot 生成），详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流能力**：支持将 SLS 推理日志自动转化为结构化训练集（SFT/DPO/CPT）或评测集，适用于文本生成场景，详见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
> **注意**：文档1中称“数据处理暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档3明确日志回流支持 DPO 训练集生成——二者无冲突，因日志回流产出的是原始结构化数据，后续仍需经人工校验或清洗才可用于训练；但文档2未提及对 DPO 数据的清洗/增强支持，该限制依然有效。

## 关键参数

- **`loss_weight`**：SFT（所有 assistant 行）和 DPO（仅 `chosen` 字段）支持该邀测参数，取值范围 `0.0 ~ 1.0`，用于调节单条样本训练权重；需联系商务经理开通权限。  
- **视觉输入字段**：Qwen-VL 训练集中，`system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]`，不可用字符串；图像/视频路径需与 ZIP 包内实际文件名严格一致，且全局唯一。  
- **图生视频坐标规范**：Qwen2.5-VL 使用缩放后图像的绝对像素坐标；Qwen3-VL 使用 `[0, 999]` 归一化相对坐标。  
- **日志回流上限**：单次任务最多回流 10 万条日志，但可通过多次追加版本突破总量限制，详见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

- **创建数据集**：在[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)页面，选择“新建数据集” → 指定类型（训练集/评测集）→ 上传 ZIP（图生视频）、JSONL（SFT/DPO/CPT）、Excel（评测集）或选择“日志回流”导入。  
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式）。需先在数据流画布中编排“数据清洗”与/或“数据增强”节点，发布后创建任务；处理结果自动生成新版本，原数据集不受影响。  
- **日志回流配置**：需先完成 SLS 审计日志与推理日志的开通及角色授权（见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)），再通过模型监控页或数据管理页进入表单，严格按顺序填写时间范围 → API Key → 模型 → 训练方式等参数。  
> **注意**：文档2强调“阿里云百炼目前暂未提供可用的API进行数据处理”，所有数据流操作必须通过控制台完成；而日志回流虽无直接 API，但其底层依赖 SLS OpenAPI，高级用户可通过 SLS 查询后手动构造 JSONL 导入。

## 限制和注意事项

- **地域限制**：全部功能（数据集管理、清洗增强、日志回流）均仅限华北2（北京）和新加坡 Region，其他地域不可用。  
- **格式强约束**：  
  - SFT/DPO 训练集必须为 `.jsonl`（每行一个 JSON 对象），ZIP 包内 `data.jsonl` 必须位于根目录；  
  - 图生视频 ZIP 包内图像/视频文件名不得重复，且 `data.jsonl` 中路径字段（如 `first_frame_path`）仅写文件名，**不可包含子目录路径**；  
  - 多模态训练集中，`system` 消息 content 若含图像/视频，必须用数组格式声明。  
- **存储与版本**：平台存储模式下，数据处理与日志回流均自动发布新版本；OSS 挂载模式不支持“新增版本”操作，追加数据必须通过“导入数据”页完成。  
- **安全与合规**：数据清洗中的“敏感信息打码”等算子仅作用于文本字段，对图像/视频内容无效；含法律、医疗等高敏领域数据，文档2明确建议跳过自动清洗，应人工审核。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


