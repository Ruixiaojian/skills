# Token

Token 是百炼平台中用于计量模型计算资源消耗的核心计费与调度单元，代表模型处理文本、图像、音频等多模态内容时的最小语义或结构化处理单位。在百炼体系中，Token 不仅是计费基础（以 Credits 抵扣），更是模型输入/输出长度、推理复杂度、[工具调用](tool-use.md)开销的统一量化标尺。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用计量**：每次 API 请求的 `input_tokens`（输入内容经 tokenizer 编码后的 token 数）与 `output_tokens`（模型生成内容的 token 数）之和构成单次调用的总 Token 消耗。例如调用 `qwen3.7-plus` 处理一段含图片的对话，其 `messages` 中的文本和 `image_url` 对应的视觉特征编码均计入 input tokens；生成的文本响应长度决定 output tokens。

- **Token Plan 订阅服务**：Token Plan 以 Credits 为统一货币，1 Credit ≈ 1 Token（具体换算由模型类型与能力动态加权）。多模态生成（如 `wan2.7-image`）、Harness [工具调用](tool-use.md)（如 `web_search`）、思考模式（`enable_thinking=true`）均产生额外 Token 开销，实际消耗以控制台「我的订阅」用量明细为准，非静态定价表可覆盖。

- **可观测性监控**：  
  - **应用观测（Application Monitoring）**：在 Span 级别上报 `LLM` 或 `EMBEDDING` 节点的 `Token总量`（input + output），用于分析智能体/工作流中各环节资源占比；  
  - **模型监控（Model Monitoring）**：提供按业务空间、API Key、时间维度聚合的 Token 消耗统计，并支持分钟级粒度（需启用高级监控），是成本优化与限流策略的核心依据。

- **流式与增量输出控制**：`stream=True` 下，每个 SSE chunk 的 `content` 字段长度对应本次返回的 token 数；启用 `incremental_output=True` 时，客户端收到的是新增 token（非累计），便于精准统计实时输出量。

- **RAG 与插件场景**：知识库检索返回的文档切片、插件调用的输入/输出内容（如代码解释器的 `stdin/stdout`）均经 tokenizer 处理并计入 Token，影响整体用量。

## 关键参数和配置

- `max_tokens`：显式限制模型最大输出 token 数，**强烈建议生产环境必设**。超限将触发 `400-InvalidParameter` 错误，且不计费；合理设置可防意外长输出导致 Token 浪费。

- `enable_thinking`：启用思考模式时，模型内部多步推理过程会产生额外中间 token，显著增加总消耗（通常为输出 token 的 2–5 倍），需在成本敏感场景谨慎开启。

- `messages` / `prompt` 内容结构：纯文本模型仅接受字符串型 `content`；多模态模型（如 `qwen3-vl-plus`）要求 `content` 为对象数组（`type: "text"` / `"image_url"` / `"video_url"`），其编码方式直接影响 input token 数——例如一张高分辨率图可能生成数百 tokens。

- API Key 类型影响计费归属：  
  - 通用 Key（`sk-xxx` 或 `sk-ws-xxx`）：用量计入对应业务空间，受该空间配额与告警规则约束；  
  - Token Plan 专属 Key（`sk-sp-xxxxx`）：用量严格绑定订阅套餐，独立于业务空间配额，但仅限华北2（北京）地域使用。

## 面向开发者，简洁实用

- ✅ **查用量**：实时用量看控制台「模型监控 → 日志页签」或「Token Plan → 我的订阅」；历史用量导出用「费用与成本」账单。  
- ✅ **省 Token**：  
  - 输入端：精简 [prompt](../guides/prompt.md)、压缩图片 URL（避免原始大图）、禁用冗余 system message；  
  - 输出端：设合理 `max_tokens`、优先用 `json_object` 格式约束输出结构、避免开放-ended 生成。  
- ✅ **避坑**：  
  - Token Plan 不支持 `qwen3.8-max-preview` 等预览模型的稳定计费承诺，生产环境请选用正式版；  
  - 多模态生成模型（图像/视频/语音）必须通过独立 HTTP API 调用，不可走 [OpenAI 兼容接口](openai-compatible-interface.md)，否则 token 计量失效；  
  - Harness 工具（如 `web_search`）**必须通过 Responses API**，用 Chat Completions 接口调用将失败且不计费。  
- ✅ **调试技巧**：启用模型监控的「推理日志」后，可在日志详情中直接查看 `input_tokens` 和 `output_tokens` 字段，快速验证 tokenizer 行为。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)
- [application monitoring](../guides/application-monitoring.md)
- [application support](../guides/application-support.md)
- [model monitoring](../guides/model-monitoring.md)


