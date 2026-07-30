# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 与基础设施层面的重要更新，涵盖新模型上架、能力升级、接口变更、计费调整及下线通知。开发者应重点关注与自身调用链路强相关的模型支持范围、参数兼容性、API 行为变更及已知限制。所有变更均以实际生效日期为准，部分功能需配合 SDK 或服务端版本升级方可使用。

## 支持的模型/功能

- **新增模型（2026年7月起）**：  
  - 多模态大模型：`qwen3.7-flash`（原生VL Flash）、`qwen3.7-max-2026-06-08`（增强视觉理解）、`kimi/kimi-k3`（100万上下文，2.8T参数）、`glm-5.2-fast-preview`（1M上下文，TPS提升1.5–2倍）；  
  - 音视频模型：`qwen-audio-3.0-asr-flash-*`（方言/古诗词/多语种优化）、`qwen-audio-3.0-tts-plus/flash`（细粒度控制）、`qwen-audio-3.0-realtime-plus/flash`（双工低延迟）；  
  - 视频生成：`vidu/viduq3-*` 系列（Ad/Drama/Fast/Pro）、`pixverse/pixverse-motioncontrol/lipsync`、`wan2.7-t2v/r2v-2026-06-12`；  
  - 图像生成：`qwen-image-3.0-pro`（4.5k token输入、10px小字渲染）、`vidu/vidu-image_reference2image`（UI/图表像素级还原）；  
  - 向量模型：`qwen3.7-text-embedding`（支持256–2560维自定义维度，MTEB评测提升20%）。  
- **新增功能模块**：  
  - [知识库](../concepts/knowledge-base.md)RAG：上线[知识检索服务](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval)与[知识问答服务](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa)，支持多[知识库](../concepts/knowledge-base.md)联合检索与混合排序；  
  - 智能体托管：发布[Managed Agent商业化通知](https://www.aliyun.com/notice/118456)及配套[智能体托管运行时 API](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview)；  
  - 模型调优：新增强化学习（RL）训练（邀约制）、0代码安全合规强化、视频/图像/视觉理解模型类型支持；  
  - 数据连接：上线[数据连接模块](https://help.aliyun.com/zh/model-studio/data-connection)，支持 MySQL/语雀/OSS 等数据源接入；  
  - 多模态交互开发套件：提供 Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK 及服务端 Java SDK。  
- **平台能力升级**：  
  - PTU 部署支持[长输入与前缀缓存](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache)；  
  - Responses API 新增 `background=true` [异步调用模式](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference#7226dca8fe4ld)；  
  - 异步任务支持通过 EventBridge 主动推送完成事件，替代轮询；  
  - 新增[模型评测排行榜](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)与多种评估器（字符串匹配、模型打分、人工分类等）。

> **注意**：文档1中“6月15日 PTU 长输入与缓存”与文档2未提及该能力对新上架模型（如 `qwen3.7-flash`）的默认支持状态。实际使用时请以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)中 PTU 部署文档为准，并验证目标模型是否启用缓存特性。

## 关键参数

- **上下文长度**：`qwen3.7-max`、`glm-5.2`、`kimi-k3`、`deepseek-v4-pro` 等主流模型均支持 **100万 token** 上下文；`qwen3.5-ocr`、`qwen-audio-3.0-asr-flash-filetrans` 等专用模型按场景设定合理上限（详见各模型文档）。  
- **输出控制**：  
  - TTS 模型（如 `qwen-audio-3.0-tts-plus`）支持 `style`、`emotion`、`speed`、`volume` 等细粒度标签；  
  - 视频生成模型（如 `vidu/viduq3-ad_reference2video`）支持 `duration=16s`、`audio_sync=true` 等业务参数；  
  - RAG 检索接口支持 `sort_model` 与 `instruction_intervention` 参数（见[知识库检索 API](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-51)）。  
- **计费单元**：模型部署支持按 **模型单元（MU）时长计费**（见[模型部署快速入门](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)），部分模型（如 `qwen-turbo`）资源包已启动退市（见[文档1](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 使用方式

- **模型调用**：  
  - 文本生成类模型统一通过 DashScope API 调用，支持 OpenAI Responses / Anthropic Messages 兼容接口；  
  - 新版[智能体应用 DashScope API](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference) 支持单轮/多轮、流式、文件问答、视觉理解；  
  - 多模态模型（如 `qwen3.7-flash`）需在请求 payload 中显式传入 `messages` 包含 `image_url` 或 `base64_image` 字段。  
- **SDK 集成**：  
  - Spring AI Alibaba 框架调用文档已上线，支持百炼智能体与工作流集成（见[Spring AI Alibaba 文档](https://help.aliyun.com/zh/model-studio/spring-ai-alibaba-integrate-llm-application#26239bc5e4is9)）；  
  - 多模态交互开发套件提供 Android/iOS/Lite/Linux C++/Java SDK，各 SDK 均含完整初始化、配置与调用示例。  
- **临时凭证**：敏感环境推荐使用[生成临时 API Key](https://help.aliyun.com/zh/model-studio/application-obtain-temporary-authentication-token)机制，避免永久密钥泄露。

## 限制和注意事项

- **模型下线**：  
  - `qwen-turbo` 资源包已启动退市（2026年6月28日），存量用户需迁移至 `qwen3.7-flash` 或 `qwen3.7-plus`；  
  - 企业[知识库](../concepts/knowledge-base.md)（旧）已于2026年7月16日下线，新应用必须使用新版知识库服务；  
  - 部分老旧模型（含长尾型号）于2026年7月9日–10日分批下线，具体清单见[模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)。  
- **地域与权限**：  
  - 新增美国、德国、日本地域支持（2026年6月12日），但部分模型（如 `qwen-audio-3.0-asr-flash`）当前仅限华北2（北京）可用；  
  - API Key 加密存储与业务空间专属推理域名已升级（2026年6月29日），旧域名将于后续灰度停用，请及时更新 endpoint。  
- **行为变更**：  
  - 免费额度启用“用完即停”后，将返回错误码 `AllocationQuota.FreeTierOnly`（见[免费额度文档](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)）；  
  - 记忆库商业化后，[长期记忆](../concepts/memory.md)能力（Memory 2.0）需订阅对应服务，免费额度内仅限基础会话记忆；  
  > **注意**：文档1中“7月6日部分老旧模型延期下线通知”与“7月10日部分老旧模型下线通知”存在时间冲突。实际执行以[模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)最新公告为准，建议通过控制台「模型管理」页查看实时状态。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


