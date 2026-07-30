# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力增强、平台功能迭代及关键使用变更。所有信息均基于官方发布内容整理，面向开发者提供可直接落地的版本演进参考。建议结合 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 和 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md) 查阅原始细节与上下文。

## 支持的模型/功能

- **新增模型（2026年7月重点）**：  
  - `qwen3.7-flash`（文本/视觉/深度思考）、`qwen-image-3.0-pro`（图片生成）、`kimi/kimi-k3`（2.8T参数，100万上下文）、`qwen3.7-text-embedding`（多语言向量，支持256–2560维自定义）、`qwen-audio-3.0-tts-plus`/`-flash`（语音合成双版本）、`qwen-audio-3.0-realtime-plus`/`-flash`（实时语音对话双版本）、`pixverse/pixverse-upscale`/`-motioncontrol`/`-lipsync`（视频后处理三件套）、`vidu/viduq3-pro-fast_img2video` 及全系 `viduq3-*`（剧/广告/高性价比视频生成）、`glm-5.2-fast-preview`（GLM-5.2高速版，TPS提升1.5–2倍）。  
  - 全部模型均按华北2（北京）地域首批上线，部分模型（如 `kimi/kimi-k3`、`qwen3.7-flash`）明确标注为“原生视觉语言”或“[多模态](../concepts/multi-modal.md)Agent场景能力显著升级”。

- **平台级功能新增**：  
  - 智能体托管运行时 API（6月29日上线），支持平台托管会话与工具执行；  
  - 知识检索服务与知识问答服务（6月23日上线），支持多知识库联合检索与混合排序；  
  - Responses API 异步调用模式（6月1日），通过 `background=true` 提交长耗时任务；  
  - 模型导入功能国际站上线（6月5日），支持从 OSS 导入 LoRA 微调模型；  
  - [多模态](../concepts/multi-modal.md)交互开发套件 SDK 全栈覆盖（Android/iOS Lite、Linux C++、RTOS C、Java），含音色管理与低延迟接入能力。

> **注意**：文档1中 `kimi/kimi-k3` 标注为“全球首个开源的 3 万亿级别模型”，但文档2未提及其开源状态，且当前百炼平台不提供该模型源码下载入口。实际使用以控制台可选模型为准，非开源模型亦可调用。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`glm-5.2-fast-preview`、`xiaomi/mimo-v2.5-pro`、`deepseek-v4-pro` 均支持 **100万 token**；`qwen3.7-max-2026-06-08` 及后续 `qwen3.7` 系列 Max/Plus/Flash 版本默认启用视觉模态，上下文能力继承同代文本基座。
- **向量维度**：`qwen3.7-text-embedding` 支持 **256–2560 维用户自定义**，需在请求参数中显式指定 `dimension` 字段。
- **语音合成延迟**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`-plus` 版本未承诺具体延迟，侧重音质与表现力。
- **视频生成时长**：`vidu/viduq3-pro-fast_img2video` 支持 **16秒视频生成**（较 `viduq2-pro-fast` 的10秒提升60%）；`pixverse/pixverse-v6-r2v` 支持 **15秒长视频直出**。
- **图像输入能力**：`vidu` 全系 `reference2image`/`reference2video` 模型均支持 **0–14张参考图输入**（`viduq3-mix_reference2video` 限定为1–7张）。

## 使用方式

- **模型调用**：所有新模型均通过标准 `/v1/chat/completions`（文本/[多模态](../concepts/multi-modal.md)）、`/v1/embeddings`（向量）、`/v1/audio/speech`（TTS）、`/v1/video/generation`（视频）等 RESTful API 接入，兼容 OpenAI 兼容层（详见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md) 中“5月15日 文本生成 API 入口聚合四类接口”说明）。
- **智能体托管**：启用 Managed Agent 需调用 `/v1/agents/{agent_id}/runs` 接口，会话状态与工具执行由平台自动管理（6月29日上线）。
- **异步任务**：对长耗时视频/3D生成任务，推荐使用 Responses API 的 `background=true` 模式，再通过轮询 `/v1/async_tasks/{task_id}` 获取结果；也可配置事件总线 HTTP 回调或 RocketMQ 主动推送（4月23日支持）。
- **模型部署**：预置模型（如 `qwen-flash`、`qwen-plus`）支持通过 API 直接部署为专属实例，计费单位为模型单元（MU）时长（1月23日上线）。

## 限制和注意事项

- **模型下线风险**：7月10日、7月9日已发布“部分老旧模型下线通知”及“部分老旧长尾模型下线通知”，涉及 `qwen-turbo` 资源包退市（6月28日）、企业知识库（旧）下线（7月16日）等。请尽快迁移至 `qwen3.7-flash`、`qwen3.7-plus` 等替代模型，并检查依赖项。详情见 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 中“模型下线机制说明”链接。
- **地域限制**：新模型（如 `qwen3.7-flash`、`viduq3-*`）首发仅限华北2（北京），美国、德国、日本地域虽于6月12日新增部署范围，但模型同步存在1–3个工作日延迟，调用前需确认目标地域可用性。
- **功能兼容性**：`qwen-audio-3.0-realtime-plus`/`-flash` 与 `qwen-audio-3.0-tts-plus`/`-flash` 均要求音频采样率 ≥16kHz、位深 ≥16bit；`pixverse` 系列视频后处理模型（`upscale`/`motioncontrol`/`lipsync`）**仅接受 MP4/H.264 编码输入**，AVI/WEBM 等格式需预转换。
- **免费额度变更**：新人免费额度有效期已调整（参见文档2公告），且启用“用完即停”后将返回 `AllocationQuota.FreeTierOnly` 错误码，避免意外计费。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


