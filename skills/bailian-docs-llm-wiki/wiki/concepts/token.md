# Token

Token 是百炼平台中用于计量大模型输入与输出内容的基本单位，也是计费、配额、监控和性能分析的核心粒度。一个 Token 通常对应一个子词（subword）或字符（如中文单字、英文单词/标点），具体切分方式由模型自身的分词器（Tokenizer）决定；不同模型的 Token 化结果可能差异显著，因此 Token 数量需以实际 API 响应中的 `usage` 字段为准。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与资源管理**：所有实时推理调用均以输入 Token 和输出 Token 分别计量，按“百万 Token”为单位计费。免费额度、资源包、节省计划等均以 Token 为抵扣基础，且严格区分模型、地域、快照版本（如 `qwen3.7-plus` 与 `qwen3.7-plus-20241201` 视为两个独立模型，额度不互通）。

- **Token Plan 订阅服务**：Token Plan 不直接暴露原始 Token 数，而是统一折算为 Credits（1 Credit ≈ 1 Token，具体换算系数由模型类型、模式及工具调用动态确定）。个人版采用双窗口限额（5 小时 + 7 天），团队版采用月度总额度制，额度均按 Credits 消耗，本质仍是 Token 级别的资源管控。

- **模型监控（Model Monitoring）**：`model_usage` 指标直接上报原始 Token 总消耗量（单位：Token），支持按分钟级（高级监控）或小时级（普通监控）聚合分析，并可关联 Request ID 追溯单次调用的精确 Token 用量（需开通推理日志）。

- **应用监控（Application Monitoring）**：在智能体/工作流应用的 Span 级别中，每个 `LLM` 节点明确统计「输入 Token 数 + 输出 Token 数」，并展示首 Token 耗时（TTFT）、总延时等关联指标，帮助定位 Token 密集型瓶颈（如长 Prompt 解析或高生成量响应）。

- **模型评测（Model Evaluation）**：当使用「评测数据集」作为数据源时，被评测模型的每次推理将产生真实 Token 消耗并计入账单；裁判模型（如 `qwen-max`）执行大模型评估维度时，其自身调用也按 Token 计费。评测报告中的综合得分虽不直接体现 Token，但 Token 效率（如每分对应的平均 Token 成本）是成本优化的关键参考。

## 关键参数和配置

- **`usage.input_tokens` / `usage.output_tokens`**：API 响应 `usage` 对象中的标准字段（OpenAI 兼容协议），返回本次调用实际消耗的输入与输出 Token 数，开发者必须依赖此值进行成本核算与限流控制，不可自行估算。

- **`max_tokens`（请求参数）**：控制模型最大生成长度，直接影响输出 Token 上限和费用上限。设置过大会增加超时与成本风险；设置过小可能导致截断。建议结合业务预期响应长度保守设定，并配合 `stop` 参数增强可控性。

- **`top_p` / `temperature` 等采样参数**：虽不改变 Token 计量逻辑，但显著影响实际输出 Token 数的方差——低 temperature 倾向稳定短输出，高 temperature 或低 top_p 可能导致更长、更发散的生成，间接推高 Token 消耗。

- **[多模态](multi-modal.md)模型的 Token 等效规则**：图像、视频、语音类模型不按文本 Token 计费，而按“张”“秒”“字符”等专用单位，但在监控与用量统计中统一归一化为等效 Token 量（详见各模型计费文档），便于跨模态成本汇总分析。

## 面向开发者，简洁实用

- ✅ **必查响应字段**：每次调用后务必解析 `response.usage.input_tokens` 和 `response.usage.output_tokens`，这是唯一准确的 Token 消耗依据。
- ✅ **限流与预算控制**：在客户端或网关层基于 `input_tokens` 实施预检（如拒绝 >100K 输入的请求），并按 `output_tokens` 设置 `max_tokens` 安全阈值。
- ✅ **监控告警建议**：在模型监控中配置「Token 消耗超阈值」告警（如单小时 >500 万 Token），结合 `apikey_id` 维度快速定位异常调用方。
- ❌ **避免估算**：不要用字符数 × 1.3 或字数 × 2 等经验公式替代真实 Token 数——Qwen 系列对中文分词更细，实际 Token 数常高于字符数；英文长单词也可能被拆为多个 Token。
- ⚠️ **注意地域与模型绑定**：同一模型在不同地域（如北京 vs 新加坡）的 Token 单价、免费额度、甚至分词器版本都可能不同，跨地域迁移需重新验证 Token 消耗与成本。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


