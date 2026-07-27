# model data overview

百炼平台的模型数据体系为大模型调优与评测提供统一的数据管理能力，涵盖训练集、评测集构建、数据清洗增强及日志回流等核心环节。所有功能当前仅支持华北2（北京）和新加坡地域，且需在对应地域开通相关服务后方可使用。数据集以结构化 JSONL 格式为主，支持版本化管理，确保数据可追溯、可复用。

## 支持的模型/功能

百炼支持面向文本生成、多模态理解、图生视频等场景的模型数据构建与处理：

- **训练集类型**：SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）、思考模型（Thinking）、视觉理解（千问VL）、图生视频（首帧/首尾帧）；
- **评测集类型**：仅支持文本生成类单轮对话评测集；
- **数据处理能力**：支持 SFT 文本生成训练集的数据清洗（如敏感信息打码、特殊内容移除）与数据增强（通用/分类/抽取/创作场景），详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
- **日志回流能力**：将 SLS 推理日志自动转化为结构化训练集或评测集，支持 SFT/DPO/CPT 三种训练方式，但当前仅限华北2（北京）和新加坡地域，详见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
- **多模态支持**：Qwen2.5-VL 和 Qwen3-VL 模型支持图像、视频（MP4/MOV）输入，其中视频支持文件路径模式与图片帧列表模式两种格式。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 中 DPO 数据集被列为正式支持类型。该矛盾表明 DPO 数据集**仅支持构建与上传，不支持后续清洗/增强处理**，实际使用中应避免对 DPO 数据集发起数据流任务。

## 关键参数

| 参数 | 适用场景 | 类型 | 必填 | 说明 |
|------|----------|------|------|------|
| `loss_weight` | SFT（所有 assistant 行）、SFT-Thinking（仅最后 assistant 行）、DPO（`chosen` 字段） | float | 否 | 范围 `0.0 ~ 1.0`，数值越大训练权重越高；属邀测参数，需联系商务经理开通 |
| `resized_width` / `resized_height` | VL 训练集中的 image/video 字段 | int | 否 | 图像/视频目标缩放尺寸（像素），影响坐标标注基准（Qwen2.5-VL 用绝对像素，Qwen3-VL 用 `[0, 999]` 相对坐标） |
| `fps` / `sample_fps` | VL 视频训练 | float | 否 | `fps` 用于视频文件路径模式，`sample_fps` 用于图片帧列表模式，控制采样频率 |
| `first_frame_path` / `last_frame_path` / `video_path` | 图生视频训练集 | string | 是（按模式） | 首帧、尾帧、视频文件在 ZIP 包内的相对路径，**必须与压缩包内实际文件名完全一致，且不带目录前缀** |
| `foreignKey` | 数据增强输出 | string | 自动添加 | 系统生成的唯一标识字段，不影响模型训练，无需手动删除 |

## 使用方式

1. **创建数据集**：通过 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 页面上传 ZIP 压缩包（训练集）或 Excel/XLSX 文件（文本评测集），确保 `data.jsonl` 位于 ZIP 根目录，图像/视频文件名全局唯一；
2. **数据清洗与增强**：在数据流画布中编排「开始 → 数据清洗 → 数据增强 → 结束」节点链路，仅支持 ChatML 格式的 SFT 文本训练集，详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
3. **日志回流**：在模型监控页开启审计日志与推理日志后，通过日志回流表单配置时间范围、API Key、模型等参数，生成结构化训练/评测集，支持追加版本；
4. **格式校验**：所有 JSONL 行必须为合法 JSON 对象，多轮对话需严格遵循 ChatML 规范（`system`/`user`/`assistant` 角色嵌套），VL 场景中 `system.content` 必须为数组格式 `[{"text":"..."}]`。

## 限制和注意事项

- **地域限制**：全部功能（含数据清洗、日志回流）仅在华北2（北京）和新加坡可用，其他地域不可见或不可用；
- **文件约束**：
  - ZIP 包最大 2 GB（VL 训练集）或 20 MB（图生视频训练集），仅支持 ASCII 字符命名（a-z/A-Z/0-9/_/-）；
  - 图像单张 ≤ 1024px 宽高、≤ 10MB，支持 BMP/JPEG/PNG/TIFF/WEBP；视频 ≤ 4096×4096 分辨率，仅 MP4/MOV；
  - `data.jsonl` 必须位于 ZIP 根目录，且文件内路径引用仅支持文件名（如 `"image_1.jpg"`），**禁止包含子目录路径**；
- **功能限制**：
  - 数据清洗/增强**不支持 DPO、CPT、VL、图生视频类训练集**，仅限 SFT 文本生成（ChatML 格式）；
  - 日志回流**不支持评测集的 OSS 挂载存储**，且单次回流上限 10 万条（总量无上限，可分批追加）；
- **模型兼容性**：
  - `loss_weight` 参数需模型版本支持，旧版模型可能忽略该字段；
  - 图生视频训练集仅适配 Wan-X 系列模型，非通用文本模型不可用；
- **安全与合规**：敏感信息打码等清洗算子依赖内置规则库，对法律/医疗等专业领域文本效果有限，文档 2 明确建议此类数据**跳过自动清洗**，人工审核优先。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


