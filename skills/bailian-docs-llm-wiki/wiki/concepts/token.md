# Token

Token 是大语言模型处理文本的基本单位，通常对应一个词、子词或标点符号。在百炼平台中，Token 是计量模型计算资源消耗、计费、限流与性能监控的核心原子单位，贯穿模型调用、推理加速、可观测性及服务治理全流程。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额**：Token 是 Token Plan 服务的底层计量单元。实际消耗 = 输入 Token 数 + 输出 Token 数，并受模型类型、思考模式（如 Reasoning）、Harness 工具调用次数等动态影响。Credits 消耗按此精确折算，控制台用量明细可逐次查看。
- **限流控制**：平台以 TPM（Tokens Per Minute）为关键限流维度，区分输入/输出方向。例如 `qwen3.7-plus` 默认享有 5,000,000 TPM 配额，超限返回 `429` 错误；TPM 预留服务则允许用户预购专属 kTPM 容量，保障吞吐确定性。
- **性能监控**：模型监控与应用观测均将 Token 总量（input + output）作为核心指标上报，支持按业务空间、API Key、模型 ID 等多维归因分析；同时支撑首 Token 耗时（TTFT）、非首 Token 延时（ITL）等关键性能诊断。
- **多模态扩展**：图像、视频、语音等非文本模态输入需先经编码器转换为视觉/音频 Token 序列，再送入大模型联合处理。例如 `qwen3.7-plus` 接收图片时，系统自动提取视觉 Token 并计入总输入 Token 数。
- **调试与优化**：通过监控中的 Token 分布（如长上下文输入占比、输出冗余度），开发者可识别 [prompt](../guides/prompt.md) 设计缺陷、截断风险或生成低效问题，针对性优化提示工程或选择更适配的模型（如 `qwen3.7-flash` 适合短响应场景）。

## 关键参数和配置

- **Token 计数规则**：
  - 文本 Token 数由模型专用 tokenizer 统一计算（如 Qwen 使用 tiktoken 兼容分词器），与 OpenAI 标准一致；
  - [多模态输入](multimodal-input.md)（图片/音频）的 Token 消耗由平台自动估算并计入总量，无需手动计算；
  - Harness 工具调用本身不额外计费 Token，但工具返回结果作为新输入参与后续推理，其 Token 会计入总消耗。
- **限流相关参数**：
  - `max_tokens`：控制模型最大输出长度，直接影响输出 Token 上限（默认值因模型而异，如 `qwen3.7-plus` 为 8192）；
  - `input_tpm` / `output_tpm`：TPM 预留服务的必需配置项，单位为千 Token/分钟（kTPM），需在控制台购买并绑定专属模型 code；
  - 流式响应中，`usage.prompt_tokens` 和 `usage.completion_tokens` 字段在 `choices[0].delta` 结束后完整返回，可用于实时成本跟踪。
- **可观测性字段**：
  - 应用监控中 `Token 总量` 字段直接展示该 Span 的双向 Token 消耗；
  - 模型监控日志中 `prompt_tokens` 和 `completion_tokens` 字段提供原始计数，支持与账单对齐。

## 面向开发者，简洁实用

- ✅ **务必校验 Token 消耗**：首次集成时，用 `qwen3.7-plus` 发起含 100 字中文的请求，观察响应中 `usage.total_tokens` 值（通常约 130–150），建立直观感知。
- ✅ **长文本场景必设 `max_tokens`**：避免意外超限触发限流或高额费用，尤其在 RAG 场景中，应结合检索结果长度动态约束。
- ✅ **监控告警建议配置**：在模型监控中为关键业务设置「Token 消耗突增 300%」或「TPM 使用率 > 90%」告警，提前发现异常调用。
- ❌ **不要跨地域混用 API Key 与 Base URL**：北京地域的 Token Plan Key（`sk-sp-`）必须搭配 `cn-beijing.maas.aliyuncs.com` 域名，否则鉴权失败且 Token 计数异常。
- ❌ **避免在生产环境滥用试用域名**：`trial.cn-beijing.maas.aliyuncs.com` 有严格 Token 限流（如 1000 TPM），仅用于快速验证，不可用于压测或上线。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [get started with models](../guides/get-started-with-models.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)


