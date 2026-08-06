# use cases

百炼平台提供覆盖文本、图像、视频、语音及[多模态](../concepts/multimodal.md)的全栈AI能力，支持从简单Prompt调用到复杂工作流编排的多样化应用场景。开发者可基于预置模型快速构建生产级应用，也可通过自定义训练、RAG增强、实时交互等能力深度适配业务需求。所有方案均以函数计算、知识库、WebRTC等云原生组件为底座，兼顾开箱即用性与工程可控性。

## 支持的模型/功能

百炼平台支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括Qwen系列（如`qwen3-vl-plus`用于解题批改 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）、Wan2.7（文生视频）、HappyHorse（图生视频）、Qwen-Deep-Research（深度研究）等，均深度集成于无限画布、RAG、实时通话等场景。
- **第三方模型**：通过OpenAI兼容接口或DashScope SDK接入DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun等厂商模型。需注意地域限制——多数第三方模型（如[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）仅在华北2（北京）可用，且部分模型已标注下架时间（如GLM-4.6/4.7将于2026年7月9日下架）。
- **[多模态](../concepts/multimodal.md)交互套件**：面向硬件终端（AI眼镜、学习机），提供WebRTC低延迟音视频通道与AOQ移动端SDK双路径接入，支持qwen3.5-omni-plus-realtime等实时模型。

> **注意**：文档16（DeepSeek-阿里云）与文档17（DeepSeek）均描述DeepSeek模型接入，但前者强调“阿里云百炼供应商”，后者明确为“快手万擎直供”，二者服务端点、限流策略与功能特性（如联网搜索支持）存在差异，实际使用需按控制台开通的模型来源选择对应文档。

## 关键参数

不同任务类型依赖特定参数组合，直接影响生成质量与成本：

- **Prompt相关**：
  - 文生文：推荐使用[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)中的框架化结构（背景/目的/风格/语气/受众/输出），避免模糊指令。
  - 文生图/视频：`prompt`（正向描述）与`negative_prompt`（反向排除）为必需；文生视频V2支持`prompt_extend: true`启用智能扩写；图生视频需聚焦`运动+运镜`公式。
- **推理控制**：
  - 思考模式：DeepSeek、Kimi、GLM、MiMo、Stepfun等模型均支持`enable_thinking`或`reasoning_effort`参数控制推理过程输出，需通过`extra_body`传入OpenAI SDK。
  - 实时通话：WebRTC模式强制使用`server_vad`（服务端语音活动检测），不支持手动VAD；AOQ SDK需通过AppServer鉴权获取[Token](../concepts/token.md)。
- **缓存与限流**：
  - 显式缓存：通过请求头`cache_control`标记关键上下文片段，适用于Agent长链路场景，首次写入成本为标准价25%，命中后节省90%成本。
  - 限流应对：突发流量优先配置`X-DashScope-Wait-Timeout`请求头实现服务端排队；高频请求需结合客户端令牌桶或并发信号量控制。

## 使用方式

根据复杂度分层，从零代码到全栈开发均可覆盖：

- **零代码/低代码**：
  - 无限画布：拖拽节点（文本/图像/视频生成器）可视化编排影视创作流程，支持AI导演对话式建模 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
  - RAG应用：通过百炼控制台上传文档→自动解析→创建知识库→配置Query Engine，无需编码即可对接LlamaIndex [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **代码集成**：
  - 模型调用：统一使用OpenAI兼容接口（`base_url`指向`{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）或DashScope SDK，传入`model`名称（如`kimi/kimi-k3`）与`messages`。
  - 工作流编排：基于百炼API构建电商客服助手，组合智能问答、RAG、Agent决策、对话流四类能力 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。
  - [多模态](../concepts/multimodal.md)转换：将文档切片→生成PPT图片→合成语音字幕→剪辑成视频，全程调用百炼多模态模型 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 限制和注意事项

- **地域与模型绑定**：第三方模型（DeepSeek、Kimi、GLM等）普遍仅支持华北2（北京），跨地域调用将失败；部分模型（如Vidu）未在文档中明确地域限制，需以控制台实际开通为准。
- **资源约束**：
  - 函数计算部署方案有明确成本预估（如深度研究方案约6元/次），但实际费用受资源规格与使用时长影响，需以控制台计费明细为准。
  - 文档解析服务（DashScopeParse）限制单文件≤100MB且≤1000页，超限需预处理分割。
- **技术边界**：
  - WebRTC浏览器端受限于CORS，SDP交换需业务后端代理，Demo中依赖curl命令绕过限制。
  - 显式缓存仅对Anthropic协议接入的工具（Claude Code、OpenCode、OpenClaw）原生支持，自定义HTTP客户端需手动注入`cache_control`。
- **演进风险**：
  - 多个第三方模型已标注下架日期（如DeepSeek系列2026年10月10日、GLM系列2026年7月9日），迁移至Qwen系列为官方推荐路径。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)


