# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、资源调度、性能监控和用量统计的核心粒度。一个 Token 通常对应一个子词（subword）或标点符号，在文本场景中约等于 1.3–1.5 个中文字符或 4–5 个英文字符；在多模态场景中（如图像理解、语音识别），Token 按标准化协议映射为等效的语义处理单元。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费核心单位**：所有按量付费的模型调用（含实时 API、Batch 批量调用）均以输入 Token 和输出 Token 分别计费。例如 `qwen3.7-plus` 在华北2（北京）地域的输入单价为 ¥12/100万 Token（限时折扣），输出单价单独计算；免费额度（默认 100 万 Token/模型）也按此单位核销。
- **订阅服务计量基础**：Token Plan 使用 Credits 统一计价，其消耗量由实际输入/输出 Token 数、缓存命中情况、思考模式（是否启用思维链）、Harness 工具调用次数等动态折算得出，最终以 Token 等效值计入额度。
- **性能与容量度量**：TPM（Tokens Per Minute）是衡量吞吐能力的关键指标——TPM 预留按「输入 TPM」和「输出 TPM」分别配额；快速模式虽不预留容量，但通过提升 TPS（Tokens Per Second）优化单次响应速度。
- **可观测性关键字段**：应用监控与模型监控均将 `prompt_tokens`（输入 Token 数）和 `completion_tokens`（输出 Token 数）作为 Span 和日志的核心字段，支持按 Token 量筛选异常请求、分析成本分布、定位长上下文瓶颈。
- **缓存与优化依据**：上下文缓存（Context Cache）显式区分 `cached_tokens`，其计费单价独立于基础输入单价；缓存命中率直接影响 Token 消耗与首 Token 延时（TTFT），是性能调优的重要观测维度。

## 关键参数和配置

- **计费粒度**：统一按「百万 Token（1M）」为最小结算单位，阶梯计费基于单次请求总输入 Token 数（如 `0 < Token ≤ 32K`、`32K < Token ≤ 128K`），整次请求按所属最高阶梯单价结算。
- **缓存 Token 标识**：API 响应中返回 `usage.prompt_tokens_details.cached_tokens` 字段，明确标示被缓存复用的 Token 数量，该部分按独立单价计费（通常为原价 25%）。
- **输出长度控制**：通过 `max_tokens` 参数显式限制生成长度，直接影响输出 Token 数上限，是控制成本与延迟的最直接手段（建议设合理值，避免无意义截断或过度生成）。
- **Token 统计口径一致性**：  
  - 所有场景（计费、监控、日志）中，Token 数均由百炼后端统一 tokenizer 计算，开发者无需自行分词；  
  - 输入 Token 包含 system [prompt](../guides/prompt.md)、user message、history（含 tool call history）等全部上下文；  
  - 输出 Token 包含模型完整 response 内容（含 `reasoning_content` 与 `content` 分离字段，若启用思考模式）。

## 面向开发者，简洁实用

- ✅ **查用量**：在控制台「模型监控 → 日志」页查看每条请求的精确 `prompt_tokens` 和 `completion_tokens`；「应用监控 → Span 列表」中可直接筛选 `Token 总量 > 10000` 的高消耗请求。
- ✅ **控成本**：优先启用上下文缓存（减少重复 Token 计费）；对长文档摘要等场景，用 `max_tokens` 严格限制输出；批量任务优先选 Batch 调用（单价为实时推理的 50%）。
- ✅ **避陷阱**：  
  - 免费额度仅覆盖实时 API 调用，不适用于 Batch、模型训练、部署、Token Plan 或 Coding Plan；  
  - Token Plan 与按量付费的 API Key / Base URL 完全隔离，混用会导致 401 错误或意外扣费；  
  - TPM 预留不改变 Token 单价，仅保障容量；快速模式仍按标准 Token 价格计费。
- ✅ **调优提示**：监控 `model_first_token_duration_p99`（首 Token 延时）和 `model_generation_duration_per_token`（非首 Token 生成耗时），若前者高而后者低，说明需优化缓存或预热；若后者高，说明模型解码效率或硬件规格不足。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)


