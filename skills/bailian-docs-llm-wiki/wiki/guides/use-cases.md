# use cases

百炼平台提供覆盖文本、多模态、音视频、智能体与工作流的全栈式 AI 应用构建能力。开发者可基于预置模型快速落地业务场景，也可通过自定义模型调优、RAG 构建、Prompt 工程等手段深度适配需求。所有用例均依托统一 API 接口与计费体系，支持从原型验证到生产部署的一站式交付。

## 支持的模型/功能

百炼支持两类模型接入方式：  
- **原生模型**：包括 Qwen 系列（如 `qwen3-vl-plus`、`qwen3.5-omni-plus-realtime`）、`Qwen-Deep-Research` 等阿里云自研模型，具备开箱即用的多模态理解、深度推理与[实时交互](../concepts/realtime-interaction.md)能力；  
- **第三方模型直供服务**：通过百炼统一入口调用 DeepSeek（`deepseek-v3.2`、`vanchin/deepseek-v4-pro`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、Stepfun（`stepfun/step-3.7-flash`）、MiMo（`xiaomi/mimo-v2.5-pro`）等，各模型均支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。  

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)）均声明部分旧版本将于 2026 年下架，并推荐迁移至 `qwen3.7-plus` 等 Qwen 新模型，但未明确说明迁移路径或兼容性保障，实际升级前需验证接口行为一致性。

核心功能覆盖：  
- **智能体与工作流**：支持自主决策 Agent（Function Call）、多步骤对话流编排，典型应用于电商客服助手 [原文标题](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)；  
- **RAG 增强检索**：提供[知识库](../concepts/knowledge-base.md)服务与 LlamaIndex 集成方案，支持 PDF/DOCX 等格式解析与向量检索 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
- **多模态生成**：文生图（万相 V1/V2）、文生视频/图生视频（万相 2.6/2.7）、Vidu 视频生成，均提供结构化 Prompt 公式与词典指导；  
- **教育与研究场景**：AI 解题批改（`qwen3-vl-plus`）、深度研究报告生成（`Qwen-Deep-Research`），强调解题思路拆解与多源交叉验证能力。

## 关键参数

不同任务类型对应关键参数如下：  
- **文生图（万相）**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）；  
- **文生视频/图生视频**：除基础 `prompt` 外，支持 `motion`（运动描述）、`aesthetic_control`（美学控制，含镜头/运镜）、`style`（风格化）及 `sound_description`（声音描述）；  
- **第三方模型推理**：通用非标准参数 `enable_thinking`（开启思考模式）、`reasoning_effort`（控制推理深度，值为 `"max"`/`"high"`/`"none"`），需通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入；  
- **限流控制**：`X-DashScope-Wait-Timeout` 请求头用于服务端排队等待，仅对 `Throttling.BurstRate` 类型限流生效 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **显式缓存**：`cache_control` 标记（Anthropic 协议兼容），支持在 system [prompt](prompt.md) 或 user message 中注入，实现确定性缓存命中。

## 使用方式

1. **模型调用**：  
   - OpenAI 兼容模式：配置 `base_url` 为地域专属地址（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），使用标准 `chat.completions.create` 接口；  
   - DashScope SDK 模式：设置 `dashscope.base_http_api_url`，调用 `Generation` 等原生服务；  
2. **RAG 构建**：通过 `DashScopeParse` 解析文档，`DashScopeCloudIndex` 创建[知识库](../concepts/knowledge-base.md)，再结合 `DashScopeCloudRetriever` 或 `as_query_engine` 实现检索增强；  
3. **Prompt 工程**：  
   - 文生文：采用结构化框架（背景/目的/风格/语气/受众/输出），或使用平台 Prompt 一键优化工具；  
   - 多模态生成：按“主体+场景+运动/风格”公式组织提示词，参考官方词典细化景别、运镜、氛围等维度；  
4. **[实时交互](../concepts/realtime-interaction.md)**：WebRTC 方式需创建 `RTCPeerConnection`，处理 SDP 交换（需后端代理绕过 CORS），AOQ SDK 则面向移动端封装音视频通道与 [Token](../concepts/token.md) 鉴权流程。

## 限制和注意事项

- **地域与模型绑定**：所有第三方模型直供服务（DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo）均明确限定仅支持华北2（北京）地域，且必须使用该地域 API Key 及业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，跨地域调用将失败；  
- **限流策略**：API 按主账号、模型独立计算 RPM/TPM、RPS/TPS 及 Traffic Burst 三类限流，突发流量建议优先配置 `X-DashScope-Wait-Timeout` 头而非简单重试；  
- **文件处理限制**：`DashScopeParse` 解析器要求单个文档 ≤100MB 且 ≤1000 页，超限文件需预处理分片；  
- **缓存适用性**：显式缓存仅对 Anthropic 协议兼容的 Agent 工具（Claude Code、OpenCode、OpenClaw）原生支持，其他调用方式需手动构造 `cache_control`；  
- **模型下架风险**：`deepseek-v3.*`、`kimi-k2-*`、`glm-4.*`、`MiniMax-M2.1` 等模型已标注明确下架日期（2026年7–10月），迁移至 Qwen 系列需同步验证 Prompt 行为、[Token](../concepts/token.md) 计费及功能覆盖度。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
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
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)


