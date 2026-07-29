# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态及智能体等全栈AI能力的生产级用例，支持从模型调用、Prompt工程、RAG构建到实时音视频交互的完整开发链路。所有方案均基于函数计算等云服务开箱即用，兼顾开发效率与生产稳定性。

## 支持的模型/功能

百炼支持阿里云自研模型（如 Qwen 系列、Wan2.7、HappyHorse、qwen3.5-omni-plus-realtime）及第三方直供模型（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu），覆盖文本生成、多模态理解、文生图/文生视频、图生视频、文档转视频、深度研究、AI教学辅学等场景。  
第三方模型接入需注意地域限制：多数仅支持华北2（北京）地域，且需使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 以获得更优性能与稳定性 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。  
> **注意**：多个第三方模型文档（[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均明确标注了模型下架时间（2026年7月或10月），并统一推荐迁移至 `qwen3.7-plus`/`qwen3.7-max`/`qwen3.6-flash`，该迁移路径已在各文档中强提示。

## 关键参数

- **Prompt 相关**：文生文场景推荐使用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出）；文生图/文生视频需区分 `prompt`（正向）、`negative_prompt`（反向），V2 版本支持 `prompt_extend` 自动改写；Vidu 支持 `大动态`/`固定镜头` 等运镜关键词 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **流式与思考模式**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）通过 `extra_body={"enable_thinking": true}` 或 `reasoning_effort` 控制思考过程输出，`reasoning_content` 字段承载推理链，`content` 字段承载最终答案。  
- **缓存与限流**：显式缓存通过 `cache_control` 标记实现确定性命中，适用于 Agent 长上下文管理；限流维度包括 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速），需配合 `X-DashScope-Wait-Timeout` 请求头应对突发流量 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

1. **模型调用**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`base_url` 指向 `compatible-mode/v1`）或 DashScope SDK 调用，需配置 API Key 及业务空间 ID。  
2. **工作流编排**：利用百炼可视化节点（文本/图像/视频生成节点）构建无限画布创作流，或通过函数计算集成 Wan2.7 与 HappyHorse 实现影视全流程自动化 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。  
3. **RAG 构建**：基于 LlamaIndex，使用 `DashScopeParse` 解析 PDF/DOCX，`DashScopeCloudIndex` 创建知识库，`DashScopeCloudRetriever` 检索，支持多源交叉验证与结构化报告生成 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  
4. **实时交互**：WebRTC 方式适用于浏览器端低延迟音视频通话（需处理 SDP 代理），AOQ SDK 适用于 Android/iOS/HarmonyOS 原生应用，多模态交互套件支持 AI 眼镜等硬件场景。

## 限制和注意事项

- **地域与模型绑定**：第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）普遍仅限华北2（北京）地域开通与调用，跨地域请求将失败。  
- **[Token](../concepts/token.md) 与费用**：所有 API 调用按 [Token](../concepts/token.md) 计费，免费额度耗尽后需关注实际成本（如深度研究方案约 6 元/次，AI 教学辅学约 1 元/次）。显式缓存首次写入产生 25% 额外开销，但后续命中可节省 90% 成本。  
- **技术约束**：WebRTC 模式下浏览器无法直连服务端 SDP 交换，需业务 AppServer 代理；Vidu 视频生成对提示词句式敏感，应避免主体物过多/分散及模糊术语；`qwen3.5-omni-plus-realtime` 的 WebRTC 实现仅支持 `server_vad` 模式，不支持手动 VAD。  
- **兼容性风险**：`enable_thinking` 和 `reasoning_effort` 为非 OpenAI 标准参数，需通过 `extra_body`（Python）或顶层参数（Node.js）传入，不同 SDK 实现方式存在差异。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


