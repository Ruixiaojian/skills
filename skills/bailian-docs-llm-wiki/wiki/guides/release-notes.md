# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及平台能力的最新动态，涵盖新增模型上架、历史模型下线、核心功能迭代与关键限制变更。所有变更均面向开发者设计，直接影响调用逻辑、计费策略与系统集成方式。建议开发者定期查阅本页，并结合 [原文标题](../../raw/model-user-guide/release-notes/model-depreciation.md) 和 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 进行模型生命周期管理。

## 支持的模型/功能

- **新增模型（2026年7–8月重点）**：  
  - 文本/多模态旗舰：`qwen3.8-max`（2.4T MoE）、`kimi/kimi-k3`（2.8T）、`deepseek-v4-pro-0813`（1.6T）、`glm-5.2`（1M上下文）；  
  - 视频生成：`pixverse/pixverse-v6-r2v-omni`（混合参考）、`vidu/viduq3-drama_reference2video`（剧集专用）、`wan3.0-video`（All-in-One）；  
  - 音视频：`qwen-audio-3.0-realtime-plus`（双工低延迟）、`qwen-audio-3.0-tts-plus`（高表现力）；  
  - 向量与工具：`qwen3.7-text-embedding`（256–2560维可调）、`stepfun/step-3.7-flash`（Agent优化）。  
- **功能模块升级**：  
  - 知识库 RAG 新增联合检索与知识问答服务（2026-06-23）；  
  - 智能体托管运行时 API 上线（2026-06-29），支持会话与工具执行全托管；  
  - Responses API 新增异步调用模式（`background=true`，2026-06-01）；  
  - 模型调优新增强化学习（RL）训练（邀约制，2026-05-31）及视频/图像/视觉理解模型类型支持（2026-05–06月）；  
  - 多模态翻译 API 全面上线（2026-05-26），覆盖文本、图片、文档、网页四类接口。  
> **注意**：文档2中 `qwen3.7-flash-2026-07-15` 与文档3中 `qwen3.7-flash`（2026-07-21）存在命名冗余，实际为同一模型快照，推荐以控制台显示的完整 ID（如 `qwen3.7-flash-2026-07-15`）为准调用，避免版本歧义。

## 关键参数

- **上下文长度**：主流旗舰模型（`qwen3.8-max`、`kimi-k3`、`glm-5.2`、`deepseek-v4-pro-0813`）均原生支持 **1,000,000 token**；`qwen-image-3.0` 支持最大 **4.5k token 输入**。  
- **推理性能**：`deepseek-v4-flash-0731` 输出延迟低，`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms，`kimi-k2.7-code-highspeed` 编程场景输出达 260 Token/s。  
- **向量维度**：`qwen3.7-text-embedding` 支持用户自定义 **256–2560 维**，需在请求中显式指定 `dimension` 参数。  
- **异步任务**：Responses API 异步模式需轮询 `/v1/async_tasks/{task_id}` 或配置 EventBridge HTTP 回调（2026-04-23 功能）。

## 使用方式

- **模型调用**：  
  - 所有新模型通过标准 `/v1/services/aigc/text-generation/generation` 或对应模态接口（如 `/v1/services/aigc/image-generation/generation`）调用；  
  - 必须在 `model` 字段传入完整模型ID（如 `qwen3.8-max`），不支持模糊匹配或系列别名；  
  - 视频/3D等多模态模型需按文档要求上传 `input.image_urls`、`input.video_urls` 或 `input.reference_images` 等结构化字段。  
- **功能接入**：  
  - 新增 SDK（如 Linux C++、Android Lite、RTOS C）需引用对应版本依赖并初始化 `BailianClient`；  
  - [Prompt 工程](../concepts/prompt-engineering.md)、Skill 能力包、数据连接模块均通过独立 API 接入，路径见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md) 中各功能点链接；  
  - 临时 API Key 生成用于不可信环境，调用 `/v1/auth/token` 获取（2026-06-03 上线）。

## 限制和注意事项

- **模型下线机制**：  
  - **快照模型**（含日期标识，如 `qwen-max-2025-01-25`）提前 **30天** 通知；**主线模型**（如 `qwen3.7-max`）提前 **3个月** 通知；  
  - 下线通知发布后即开始限流（QPM/TPM 逐步缩减），正式下线后 API 返回 `404` 或 `ModelNotAvailable` 错误；  
  - 已部署/调优的模型不受影响，但**禁止新建调优或部署任务**（详见 [原文标题](../../raw/model-user-guide/release-notes/model-depreciation.md)）。  
- **平台级变更**：  
  - 企业知识库（旧）已于 2026-07-16 下线，存量应用需迁移至新版知识库；  
  - `qwen-turbo` 资源包于 2026-06-28 启动退市，不再续购；  
  - 记忆库自 2026-07-21 起商业化，免费额度仅限个人版基础用量。  
> **注意**：文档3中“2026年7月10日部分老旧模型下线通知”（公告号 118434）与文档1中“2026年10月10日将下线”列表存在时间冲突——文档1明确该公告对应 **2026年10月10日下线批次**，文档3的日期应为公告发布时间而非下线日，开发者请以文档1的下线日期为准。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


