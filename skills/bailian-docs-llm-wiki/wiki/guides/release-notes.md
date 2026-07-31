# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、能力升级、平台功能迭代及关键变更。所有信息均基于官方发布内容整理，面向开发者提供可直接用于集成与调用的实用参考。模型能力、参数与限制以最新稳定版本为准，历史快照类模型（如 `*-2026-05-20`）仅在明确标注时可用。

## 支持的模型/功能

百炼平台持续扩展[多模态](../concepts/multi-modal.md)模型矩阵与平台级能力，覆盖文本、语音、图像、视频、3D 及[多模态](../concepts/multi-modal.md)交互场景：

- **文本生成与智能体**：`qwen3.7-max-2026-06-08`（支持视觉模态）、`kimi/kimi-k3`（100万上下文，2.8万亿参数）、`glm-5.2-fast-preview`（TPS 提升 1.5–2 倍）、`deepseek-v4-pro`（1.6T MoE，百万上下文）；详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **语音处理**：`qwen-audio-3.0-asr-flash-streaming`（实时方言识别）、`qwen-audio-3.0-tts-plus`（高表现力合成）、`qwen-audio-3.0-realtime-plus`（低延迟双工对话）；同上文档亦明确区分 `Plus`（质量优先）与 `Flash`（延迟优先）两类变体。
- **图像与视频生成**：`qwen-image-3.0-pro`（4.5k token 输入，10px 小字渲染）、`vidu/viduq3-drama_reference2video`（剧集专用一致性增强）、`pixverse/pixverse-motioncontrol`（动作迁移）、`wan2.7-r2v-2026-06-12`（5图混合参考）。
- **平台功能**：新增 `Responses API` 异步调用（`background=true`）、`Managed Agent` 托管运行时 API、`Skill 能力包`、`知识检索服务`（多知识库联合检索）、`模型压缩模块`（量化部署）；详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

> **注意**：文档 1 中 `kimi/kimi-k2.7-code` 与 `kimi/kimi-k2.7-code-highspeed` 均标注为“同一模型”，但后者宣称输出速度为前者的 5–6 倍；而文档 2 未提及该高速变体。实际调用时请以控制台或 API 文档中列出的可用模型 ID 为准，避免依赖未公开的别名。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`xiaomi/mimo-v2.5-pro` 等主流旗舰模型均支持 **1,000,000 token**；`qwen3.7-text-embedding` 支持 **256–2560 维自定义向量维度**。
- **输入能力**：`qwen-image-3.0-pro` 支持最大 **4.5k token 输入**；`vidu/viduq3-fast_reference2image` 支持 **0–14 张参考图片**；`pixverse/pixverse-v6-r2v` 支持 **2–7 张图像输入**。
- **性能指标**：`kimi-k2.7-code-highspeed` 在短上下文场景下可达 **260 [Token](../concepts/token.md)/s**；`qwen-audio-3.0-realtime-flash` 通过并行推理与全向流式优化，端到端响应时延控制在低水平。
- **多语种支持**：`fun-asr-flash-2026-06-15` 和 `qwen-audio-3.0-asr-flash` 均明确支持 **30 个语种**，含中、英、日、韩及东南亚、欧洲主要语言；但 `qwen3.5-livetranslate-flash-realtime` 宣称“能听懂60种语言，会说29种语言”，存在覆盖范围差异。

## 使用方式

- **模型调用**：所有模型通过统一 DashScope API 接入，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（如 `/v1/chat/completions`）与百炼专属接口（如 `/v1/services/aigc/text-generation/generation`）。新版智能体应用 API 已支持单轮/多轮、流式、文件问答与视觉理解 [详见文档](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **平台能力集成**：
  - 异步任务：使用 `background=true` 参数提交，通过轮询或事件总线（EventBridge/RocketMQ）接收完成通知；
  - 知识库 RAG：调用 `/v1/rag/knowledge-retrieval`（联合检索）与 `/v1/rag/knowledge-qa`（生成式问答）；
  - [模型部署](../concepts/model-deployment.md)：支持预置模型（如 `qwen-flash`）API 部署，计费模式含按模型单元（MU）时长与资源包两种；
  - 技能扩展：通过 `Skill 能力包` 添加官方或自定义技能，提升智能体执行能力。
- **开发工具链**：已提供多端 SDK，包括 Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK 及 Codex 客户端接入支持；Spring AI Alibaba 框架调用文档亦已上线。

## 限制和注意事项

- **模型下线**：平台定期清理老旧模型，7月已发布“部分老旧模型下线通知”与“部分老旧长尾模型下线通知”；历史快照模型（如 `qwen3.7-max-2026-05-20`）可能随时停用，生产环境请优先选用无时间戳的稳定版 ID（如 `qwen3.7-max`）。
- **地域与部署**：6月新增美国、德国、日本地域部署，但部分模型（如 `qwen-audio-3.0-*` 系列）当前仅限华北2（北京）可用，调用前需确认 endpoint 区域匹配。
- **参数兼容性**：`qwen3.7-text-embedding` 支持用户自定义维度，但 `text-embedding-v4` 等旧版模型不支持此特性，迁移时需检查 embedding 接口参数。
- **安全与合规**：模型调优新增“0 代码安全合规强化”流程，适用于文本生成模型；但图像/视频生成模型暂未开放同等能力，敏感内容生成仍需业务层过滤。
- **计费变更**：`qwen-turbo` 资源包已启动退市，`GLM-5.2 Fast mode` 模式降价，`通义千问VL系列模型` 与 `千问系列模型` 均有独立降价通知，具体以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中公告链接为准。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


