# Token

Token 是百炼平台中用于计量大模型输入与输出文本、图像、语音等多模态内容处理规模的基本单位，也是计费、限流、监控与性能优化的核心度量基准。1 个 Token 通常对应一个子词（subword）或字符片段（如中文单字、英文单词切分后的单元），其具体切分逻辑由底层模型 tokenizer 决定，开发者无需手动计算，但需理解其在调用链路中的统计口径与影响。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与用量管理**：Token 是 Token Plan 订阅服务的统一计量单位，实际消耗 = 输入 Token 数 + 输出 Token 数。多模态模型（如图像生成、语音合成）同样按输入提示词、输出元数据及媒体描述文本折算 Token，不直接按像素或时长计费。
- **应用观测（Application Monitoring）**：在 Span 级别可观测性中，“Token 总量”字段精确记录单次 LLM 节点调用的 `input_tokens + output_tokens`，用于分析智能体/工作流的成本热点与响应效率；Embedding 节点仅统计输入 Token。
- **模型监控（Model Monitoring）**：基础用量统计（总 Token 数）、高级指标（如 TPS = Tokens Per Second）均以 Token 为分子。开通推理日志后，可回溯单次请求的精确 Token 拆分（含 [prompt](../guides/prompt.md)、completion 各部分）。
- **高并发与加速能力**：TPM（Tokens Per Minute）预留直接以 Token 为吞吐量单位，配置时需分别指定输入 TPM 和输出 TPM；快速模式（Fast Mode）的性能提升也以 TPS（Tokens Per Second）衡量。
- **API 调用控制**：`max_tokens` 参数硬性限制模型输出长度，直接影响 Token 消耗上限与响应成本；[异步任务](asynchronous-task.md)中，Token 用量在任务完成时统一结算。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `max_tokens` | 控制模型最大输出 Token 数 | 设置过小可能导致截断；设置过大可能增加延迟与费用；默认值因模型而异（如 `qwen3.8-max` 默认 8192） |
| `input_tokens` / `output_tokens` | 监控与日志中返回的细分计数 | 仅在开通推理日志后可见；流式响应中 `output_tokens` 在结束前为估算值，最终以 `usage` 字段为准 |
| TPM（Tokens Per Minute） | TPM 预留配置项，单位为 kTPM（1,000 tokens/分钟） | 输入/输出 TPM 分开配置；溢出策略影响是否降级至按量计费 |
| `model`（专属模型 Code） | 启用 TPM 预留或 Fast Mode 时必须使用的模型标识 | 如 `tpm-reserved-qwen38max-abc123` 或 `glm-5.2-fast-preview`；普通模型名（如 `qwen3.8-max`）不触发加速能力 |

## 面向开发者，简洁实用

- ✅ **必看**：Token 消耗 = 输入（[prompt](../guides/prompt.md) + system message + history）+ 输出（completion），图片/视频 URL 不计入 Token，但其文本描述（如 `input.prompt`）会计入。
- ✅ **调试建议**：启用模型监控的推理日志，查看每次调用的 `usage.input_tokens` 和 `usage.output_tokens`，快速定位高消耗环节。
- ✅ **成本优化**：对长上下文场景，优先使用支持长上下文的模型（如 `qwen3.8-max` 支持 32K），避免因截断重试导致重复 Token 消耗。
- ⚠️ **避坑提醒**：  
  - Token Plan 的 API Key 必须以 `sk-sp-` 开头，且仅限华北2（北京）地域调用；  
  - Harness 工具（如 `web_search`）的调用本身不额外计 Token，但工具返回结果作为新 [prompt](../guides/prompt.md) 输入 LLM 后，会参与后续 Token 计算；  
  - 多模态生成（图像/视频）必须通过专用 API 接口，不可复用文本模型 Base URL，否则 Token 统计失效且调用失败。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


