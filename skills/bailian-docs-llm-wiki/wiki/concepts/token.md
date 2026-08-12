# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、限流、性能监控和资源调度的核心度量标准。一个 Token 通常对应一个子词（subword）或符号（如标点、空格、中文字符），具体切分方式由模型自身的 tokenizer 决定；开发者无需手动分词，但需理解其对成本、延迟和功能行为的影响。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用与计费**：每次请求的 `input_tokens`（输入 Token 数）和 `output_tokens`（实际生成的输出 Token 数）共同构成计费依据。例如调用 `qwen3.8-max` 模型时，1000 字中文输入约消耗 1300–1500 tokens，每生成 1 token 均计入账单。费用按「输入 + 输出」总 Token 数累加，不同模型单价独立（详见控制台计费页）。

- **请求控制与稳定性保障**：
  - `max_tokens` 参数显式限制单次响应的最大输出长度（如设为 `512`，则模型最多生成 512 tokens），防止意外长输出导致超时或超额扣费；
  - TPM（Tokens Per Minute）预留机制以 kTPM（千 Token/分钟）为单位购买专属吞吐容量，保障高并发下输入/输出 Token 的稳定处理能力；
  - 快速模式（`*-fast-preview`）虽不预留 TPM，但仍按实际 Token 数计费，并通过排队机制平滑瞬时 Token 请求峰。

- **可观测性与调试**：
  - 模型监控中，“Token 消耗”是核心成本指标，支持按 `workspace_id`、`model`、`apikey_id` 维度下钻分析；
  - 应用监控将每个 LLM 节点的 `input_tokens + output_tokens` 作为 Span 级别统计项，用于定位链路瓶颈（如某次 RAG 中检索+重排+生成共消耗 8640 tokens）；
  - 流式响应中，`first_token_latency`（首 Token 延迟）直接反映模型“启动速度”，其值受输入 Token 数显著影响——输入越长，首 Token 延迟通常越高。

- **协议兼容性适配**：
  - [OpenAI 兼容接口](openai-compatible-interface.md)返回字段 `usage.prompt_tokens` / `usage.completion_tokens` 与百炼原生字段 `input_tokens` / `output_tokens` 严格对齐；
  - Anthropic 协议中 `usage.input_tokens` / `usage.output_tokens` 同样映射至百炼 Token 计量体系，确保跨协议计费一致性。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `max_tokens` | 控制模型最大输出长度（不含输入部分） | ✅ 必须显式设置，避免默认值（如 `2048`）导致不可控成本；<br>⚠️ 若设为 `1`，模型可能仅输出单个 token（如句号），无法满足业务逻辑；<br>💡 结合 `stop` 参数可更精准截断（如 `stop=["\n", "。"]`）。 |
| `input_tokens` / `output_tokens` | 响应体中返回的实际消耗量（只读） | ✅ 解析响应 JSON 的 `usage` 字段获取，用于本地成本核算与告警（如单次 > 10k tokens 触发通知）；<br>⚠️ 不可用于请求参数，仅作结果反馈。 |
| TPM 预留额度（kTPM） | 输入/输出方向分别配置的专属吞吐容量 | ✅ 按业务峰值预估：若每秒平均 50 QPS × 平均 200 tokens/req = 10,000 tokens/s ≈ 600k TPM；<br>⚠️ 输入 TPM 和输出 TPM 独立生效，高输出场景（如摘要生成）需重点配置输出 TPM。 |

## 面向开发者，简洁实用

- **不要猜测 Token 数**：使用 [百炼 Token 计算器](https://bailian.console.aliyun.com/tools/token-calculator) 或 SDK 的 `dashscope.Tokenizer.count_tokens()`（Python）精确估算输入文本的 Token 量。
- **警惕隐式 Token 消耗**：系统提示词（system [prompt](../guides/prompt.md)）、工具描述（tool description）、历史对话（messages history）均计入 `input_tokens`；精简提示词、启用 `enable_thinking: false`（如适用）可显著降本。
- **监控必看字段**：在控制台「模型监控 → 性能指标」中重点关注 `input_tpm`、`output_tpm`、`avg_output_tokens_per_request`，三者异常波动往往指向提示词膨胀、循环生成或错误重试。
- **调试技巧**：当遇到 `429 Too Many Requests` 时，检查是否触发 TPM 限流（而非 QPS 限流）；若 `output_tokens` 接近 `max_tokens` 且响应被截断，说明模型已达长度上限，需调整 `max_tokens` 或优化输出逻辑。

## 关联主题页

- [preparations](../api/preparations.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


