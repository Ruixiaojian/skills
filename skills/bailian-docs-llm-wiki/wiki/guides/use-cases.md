# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态的丰富能力，支持从简单 Prompt 调用到复杂工作流编排的全栈 AI 应用构建。开发者可基于预置模型快速落地业务场景，也可通过自定义训练、RAG、Agent 编排与实时交互等能力构建生产级智能体。所有方案均开箱即用，依托函数计算等云服务实现免运维部署。

## 支持的模型与功能

百炼平台支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括 Qwen 系列（如 `qwen3-vl-plus` 用于解题批改 [原文标题](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）、Wan2.7 / HappyHorse（用于文生图/视频与影视创作 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)）、Qwen-Deep-Research（用于深度情报分析 [原文标题](../../raw/model-user-guide/use-cases/deep-research.md)）等，均深度适配百炼平台特性（如显式缓存、WebRTC 实时流）。
  
- **第三方模型**：支持 DeepSeek（`deepseek-v3.2`、`vanchin/deepseek-v4-pro`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、MiMo（`xiaomi/mimo-v2.5-pro`）、Step（`stepfun/step-3.7-flash`）等直供模型。> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)）均明确标注了模型下架时间（2026年7月或10月），且推荐迁移至 Qwen3 系列，开发者需关注生命周期并规划升级路径。

- **多模态交互**：提供 `qwen3.5-omni-plus-realtime` 模型及 `multimodal-dialog` 套件，支持 WebRTC 和 AOQ SDK 两种接入方式，实现低延迟音视频实时通话与视觉理解。

## 关键参数

不同任务类型对应关键参数，需按规范设置：

- **文生文**：核心为 `prompt`，推荐使用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出）提升效果 [原文标题](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/图生图**：`prompt`（正向描述）、`negative_prompt`（反向排除），V2 版本支持 `prompt_extend: true` 启用大模型智能扩写。
- **文生视频/图生视频**：除基础 `prompt` 外，Wan2.7 支持 `shot_type`（单/多镜头）、`sound_description`（人声/音效/BGM）及多镜头时间戳语法；Vidu 模型则依赖“主体/场景+场景描述+环境描述+艺术风格”公式及运镜关键词（如 `镜头推`、`固定镜头`）。
- **实时通话（WebRTC）**：必须配置 `server_vad` 或 `semantic_vad`，不支持手动 VAD 模式；音频通过 UDP 直传，需处理 CORS 限制（Demo 中需 curl 代理）。
- **思考模式**：DeepSeek、Kimi、GLM、MiMo、Step 等模型均通过非标准参数启用（如 `extra_body={"enable_thinking": true}` 或 `{"reasoning_effort": "max"}`），返回结构含 `reasoning_content` 与 `content` 字段。

## 使用方式

- **零代码体验**：通过控制台“立即部署”按钮一键开通方案（如无限画布、AI 客服助手），15–30 分钟完成端到端搭建。
- **API 调用**：
  - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：设置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），直接复用现有 SDK。
  - DashScope 原生接口：需配置 `base_http_api_url`，适用于 Java/Python 等语言。
- **工作流编排**：在百炼控制台使用节点式画布，拖拽组合文本、图像、视频生成节点及 RAG、Agent 工具，支持可视化调试与全局资产中心管理。
- **RAG 构建**：基于 LlamaIndex 集成知识库，通过 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 检索，`as_query_engine` 封装问答逻辑。
- **缓存优化**：对高频重复 Prompt，启用显式缓存（`cache_control` 标记），首次写入成本增加 25%，后续命中节省 90% 成本。

## 限制和注意事项

- **限流策略**：百炼 API 按 RPM（请求数/分钟）、TPM（[Token](../concepts/token.md) 数/分钟）、RPS/TPS（瞬时速率）及 Traffic Burst（增速突增）四维限流。突发流量推荐优先配置 `X-DashScope-Wait-Timeout` 请求头实现服务端排队 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **地域约束**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Step）仅在华北2（北京）地域可用，且需使用该地域的 API Key 及业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得最佳性能。
- **模型兼容性**：`qwen3.5-omni-plus-realtime` 仅支持 WebRTC 的 `server_vad` 模式；AOQ SDK 需按 Android/iOS/HarmonyOS 平台分别导入 `.aar`/`.framework`/`.har` 产物并声明运行时权限。
- **数据安全**：自定义模型训练需对训练数据脱敏；WebRTC 方案中浏览器无法直连 SDP 交换，正式环境必须由业务后端代理。
- **成本控制**：函数计算方案按量付费（如深度研究方案约 6 元/次），建议利用免费试用额度验证流程；显式缓存、Batch API、PTU 等是降低推理成本的关键手段。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


