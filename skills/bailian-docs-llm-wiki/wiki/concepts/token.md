# Token

Token 是百炼平台中用于计量模型输入、输出及计算资源消耗的核心单位。在文本生成类模型中，Token 通常对应一个子词（subword）或字符；在多模态场景中，不同模型对 Token 的定义可能扩展至图像 patch、音频帧或视频关键帧等语义单元，其具体计费与统计口径由模型类型和协议决定。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 计费**：所有文本与推理模型调用均以 Credits 抵扣，而 Credits 消耗量由模型类型、实际输入/输出 Token 数、思考模式（如 Reasoning）、Harness 工具调用次数等动态换算得出。例如 `qwen3.6-plus` 单次请求约消耗 3.18 Credits，该值已隐含 Token 数量与模型复杂度的加权计算。多模态模型（图像/视频/语音）虽不直接暴露 Token 数，但其计费仍基于底层 Token 化后的等效计算单元。

- **高吞吐推理（TPM / Fast Mode）**：TPM（Tokens Per Minute）是容量预留的核心指标，表示每分钟可处理的输入 + 输出 Token 总量（单位为 kTPM）；快速模式（Fast Mode）则以 TPS（Tokens Per Second）衡量单请求输出速度提升效果，适用于对首 Token 延时（TTFT）和流式响应速率敏感的场景。

- **应用观测（Application Monitoring）**：在智能体或工作流中，每个 `LLM` 节点会精确上报 `prompt_tokens`（输入 Token）、`completion_tokens`（输出 Token）及 `total_tokens`（二者之和），支持按 Span 粒度分析 Token 分布与成本归因。

- **模型监控（Model Monitoring）**：平台提供实时 TPM、单次调用 Token 消耗、历史 Token 汇总等指标，用于性能诊断与成本优化。注意：图像生成按“张”、视频按“秒”、语音合成按“秒/字符”计费，仅文本类模型严格按 Token 计费。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `prompt_tokens` | 输入内容经 tokenizer 后的 Token 数量 | 可通过 SDK 的 `usage.prompt_tokens` 字段获取；长输入可能触发阶梯系数（如 >32k 时额外加权） |
| `completion_tokens` | 模型实际生成的输出 Token 数量 | 流式响应中需累加各 `delta` 中的 `token_count`；受 `max_tokens`、截断、停止词影响 |
| `total_tokens` | = `prompt_tokens` + `completion_tokens` | 是计费与限额的主要依据；多轮对话中每次 `messages` 都独立计算 |
| `cached_tokens` | 缓存命中带来的 Token 折扣量（如 `usage.prompt_tokens_details.cached_tokens`） | 仅部分模型支持（如 `glm-5.2`），可降低实际计费 Token 数，需在监控中显式查看 |
| TPM / TPS | 分别用于容量规划（TPM）与性能调优（TPS） | TPM 预留需指定 kTPM 值；Fast Mode 仅支持特定 model ID（如 `glm-5.2-fast-preview`），不可泛化启用 |

> ⚠️ 注意：  
> - Token 统计始终以服务端 tokenizer 实际分词结果为准，客户端估算（如 tiktoken）可能存在偏差；  
> - Harness 工具调用（如 `web_search`）仅在 Responses API 下触发并计入 Token/Credits，Chat Completions 协议下不生效；  
> - 多模态模型（如 `wan2.7-image`）不返回 `prompt_tokens`/`completion_tokens` 字段，其用量以“张”为单位单独统计，不在 Token 监控维度内。

## 面向开发者，简洁实用

- ✅ **必查字段**：所有 OpenAI 兼容 API 响应中，`usage` 对象包含 `prompt_tokens`、`completion_tokens`、`total_tokens`，务必解析并记录用于成本审计。  
- ✅ **调试技巧**：启用 `logprobs=true` 可辅助验证分词逻辑；对长文本，优先使用支持 `input_token_limit` 的模型避免截断。  
- ✅ **限额感知**：Token Plan 用户应监听 `x-ratelimit-remaining-tokens` 响应头（若启用），结合控制台用量看板做主动限流。  
- ❌ **避坑提示**：不要复用 Token Plan 的 API Key 调用非 Token Plan 模型（如按量付费模型），否则将导致 401 错误或意外按量扣费；不同地域（如华东1）的模型不参与 Token Plan 计费。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)


