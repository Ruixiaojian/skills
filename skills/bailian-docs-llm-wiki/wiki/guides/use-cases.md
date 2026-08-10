# use cases

百炼平台的 use cases 覆盖从[多模态](../concepts/multi-modal.md)内容生成、智能体构建到专业领域辅助的完整技术谱系。本文档面向开发者，系统梳理平台支持的核心能力、关键参数配置、标准化使用方式及必须规避的限制项，所有信息均基于官方技术文档提炼，不包含营销性描述。

## 支持的模型/功能

百炼提供两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：覆盖文本（Qwen 系列）、视觉（万相 Wan2.x、HappyHorse）、[多模态](../concepts/multi-modal.md)（Qwen3-VL、qwen3.5-omni-plus-realtime）及深度研究（Qwen-Deep-Research）等全栈能力。例如，`qwen3-vl-plus` 专用于解题与批改场景 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)，而 `HappyHorse` 视频生成能力是影视创作平台的关键组件 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。

- **第三方模型集成**：支持 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等多家厂商模型，但存在地域与协议约束。所有第三方模型当前仅在华北2（北京）地域可用，且需通过专属业务空间域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 接入，以获得更高稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。> **注意**：文档 17（Kimi）、21（MiniMax）和 26（DeepSeek-阿里云）均声明部分旧版模型将于 2026 年下架，推荐迁移至 Qwen3 系列；但文档 16（DeepSeek）、18（Kimi-月之暗面）和 27（DeepSeek-硅基流动）未提及下架计划，实际部署前需以控制台最新公告为准。

## 关键参数

不同模型类型对应差异化参数体系：

- **文生图/视频**：核心为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词）。Wan2.7 支持 `prompt_extend`（默认开启，启用大模型智能改写）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；文生视频则需结构化描述主体、场景、运动及美学控制 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

- **大语言模型**：通用参数包括 `stream`（[流式输出](../concepts/streaming-output.md)）、`extra_body`（非标准扩展参数）。思考模式由 `enable_thinking`（如 GLM、MiMo）或 `reasoning_effort`（如 Kimi、DeepSeek）控制，其值影响推理深度与 [Token](../concepts/token.md) 消耗。

- **实时交互**：WebRTC 场景需配置 `server_vad`（服务端语音活动检测），不支持手动 VAD 模式 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。

## 使用方式

遵循“准备→调用→处理”三阶段流程：

1. **环境准备**：获取 API Key 并配置至环境变量；开通对应模型服务（如在控制台搜索并开通 Kimi 或 HappyHorse）；安装必要 SDK（如 `pip install llama-index-llms-dashscope` 用于 RAG 构建 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）。

2. **API 调用**：
   - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：设置 `base_url` 为地域专属地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），模型名按 `vendor/model-name` 格式指定（如 `kimi/kimi-k3`）。
   - DashScope 原生接口：使用 `dashscope.base_http_api_url` 配置基础 URL，调用 `Generation` 类。

3. **结果处理**：流式响应需按 `delta.reasoning_content` 和 `delta.content` 分离思考过程与最终回复；非流式响应直接解析 `choices[0].message.reasoning_content` 与 `content` 字段。

## 限制和注意事项

- **地域锁定**：所有第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）及部分原生能力（如 AOQ 实时通话）强制要求华北2（北京）地域 API Key 与业务空间，跨地域调用将失败。

- **限流策略**：API 受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS/TPS（瞬时速率）及 Traffic Burst（流量增速）四重限制。突发流量应优先启用 `X-DashScope-Wait-Timeout` 请求头实现服务端排队，而非简单重试 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

- **缓存与成本**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容工具（Claude Code、OpenCode、OpenClaw）原生支持，需确保接入端点为 `/apps/anthropic`；普通 OpenAI 兼容调用不自动启用 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

- **硬件与权限**：WebRTC 实现需浏览器麦克风/摄像头权限；移动端 AOQ SDK 需在 AndroidManifest.xml 或 Info.plist 中声明 `RECORD_AUDIO` 和 `CAMERA` 权限，并在运行时动态申请。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
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
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)


