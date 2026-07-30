# use cases

百炼平台提供覆盖文本、图像、视频、语音及[多模态](../concepts/multi-modal.md)的全栈AI能力，支持从简单Prompt调用到复杂工作流编排的多样化应用场景。开发者可基于预置模型快速构建应用，也可通过自定义训练、RAG、Agent编排等技术深度适配业务需求。所有能力均通过统一API接口和控制台提供，兼顾开箱即用性与工程可控性。

## 支持的模型/功能

百炼平台支持多种模型类型与生成能力，涵盖通用大语言模型、[多模态](../concepts/multi-modal.md)模型、视觉生成模型及第三方直供模型：

- **文本模型**：Qwen系列（如 `qwen3.7-plus`、`qwen3.7-max`）、DeepSeek（`siliconflow/deepseek-v3.2`、`vanchin/deepseek-v4-pro`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、MiMo（`xiaomi/mimo-v2.5-pro`）、Step（`stepfun/step-3.7-flash`）等。[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 和 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 文档详细说明了各供应商模型的接入方式与思考模式控制参数（如 `enable_thinking` 或 `reasoning_effort`）。

- **视觉模型**：万相系列（`wan2.7` 图像/视频生成）、Qwen-VL系列（`qwen3-vl-plus` 用于解题与批改）、HappyHorse 视频生成模型。其中，[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 展示了如何融合 Wan2.7 与 HappyHorse 构建节点式无限画布创作流。

- **[多模态](../concepts/multi-modal.md)与实时交互**：`qwen3.5-omni-plus-realtime` 支持 WebRTC 实时音视频通话；[多模态](../concepts/multi-modal.md)交互套件（multimodal-dialog）面向硬件终端提供低延迟交互能力。

- **增强与编排能力**：RAG（基于 LlamaIndex 集成知识库）、Agent（自主决策与 Function Call）、工作流（可视化节点编排）、深度研究（Qwen-Deep-Research 自动化情报分析）。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型将于 2026 年下架，并统一推荐迁移至 Qwen3 系列。该迁移建议具有一致性，非矛盾信息。

## 关键参数

不同模型与任务类型对应关键参数，需按规范设置：

- **文本生成**：`model`（模型标识符）、`messages`（对话历史）、`stream`（流式开关）、`extra_body`（非标准参数，如 `enable_thinking: true` 或 `reasoning_effort: "max"`）。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中，`extra_body` 是传递厂商特有参数的标准方式。

- **文生图/图生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用智能扩写，默认 `true`）。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

- **文生视频/图生视频**：除基础 `prompt` 外，支持 `motion`（运动描述）、`camera`（运镜控制）、`sound`（声音描述）等维度。[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 提供了多镜头公式与参考视频公式。

- **显式缓存**：在请求头中添加 `X-DashScope-Wait-Timeout`（服务端排队等待）或在消息体中使用 `cache_control` 字段（如 Anthropic 协议兼容工具），实现确定性缓存命中。

- **限流应对**：`X-DashScope-Wait-Timeout`（突发流量排队）、客户端需同步调整超时时间；[Token](../concepts/token.md) Plan/Coding Plan 等套餐对应不同 Base URL，影响限流额度。

## 使用方式

开发者可通过多种方式集成百炼能力：

- **API 直接调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（推荐）或 DashScope 原生 SDK。所有第三方模型（如 Kimi、GLM、MiniMax）均提供 OpenAI 兼容调用示例，要求配置地域专属 `base_url`（如华北2为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）并传入 `DASHSCOPE_API_KEY`。

- **低代码编排**：通过百炼控制台的“无限画布”可视化拖拽节点（文本、图像、视频、特效），构建影视创作、电商设计等端到端工作流。[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 是典型范例。

- **RAG 应用开发**：基于 LlamaIndex 集成百炼知识库服务，使用 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 检索，`DashScopeCloudQueryEngine` 查询。[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 提供完整代码示例。

- **实时交互集成**：WebRTC 方式适用于浏览器端（需处理 SDP 代理），AOQ SDK 适用于移动端（Android/iOS/HarmonyOS）。两者均需业务侧 AppServer 签发 [Token](../concepts/token.md) 并管理会话生命周期。

- **深度研究与文档转换**：Qwen-Deep-Research 模型自动规划检索路径并生成结构化报告；文档转视频方案则分步执行切片、图文生成、语音合成、视频剪辑。[深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md) 与 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md) 分别详述其流程。

## 限制和注意事项

- **地域与域名约束**：绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且强烈推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用域名以获得更高稳定性与性能。

- **限流策略**：百炼 API 按 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS/TPS（每秒峰值）、Traffic Burst（增速突增）四维限流。单纯重试无效，需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的服务端排队、客户端令牌桶或架构层 MQ 削峰。

- **缓存与成本**：显式缓存对高频复用 Prompt 场景收益显著（首次写入成本为标准价25%，后续命中节省90%），但需确保输入内容稳定；`cache_control` 仅在 Anthropic 协议兼容工具（Claude Code、OpenCode、OpenClaw）中默认启用。

- **模型生命周期**：第三方模型存在明确下架计划（如 DeepSeek 系列于 2026年10月、Kimi/GLM/MiniMax 于 2026年7月），生产环境应提前规划迁移到 Qwen3 系列。

- **安全与合规**：训练数据需脱敏处理，避免含 PII 或敏感信息；WebRTC 实现中浏览器受 CORS 限制，SDP 交换必须由业务后端代理，不可前端直连。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)




