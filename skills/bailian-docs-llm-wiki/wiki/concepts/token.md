# Token

Token 是百炼平台中用于计量模型计算资源消耗的最小单位，代表模型处理文本、图像、音频等输入或生成输出时所消耗的语义单元。在 LLM 场景下，1 个 Token 通常对应一个子词（subword）或标点符号；在[多模态](multi-modal.md)场景中，则按统一标准化规则折算为等效 Token 数（如图像像素块、音频帧等经编码后映射为 Token）。所有计费、配额、限流与监控均以 Token 为基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额管理**：  
  Coding Plan、Token Plan 等订阅服务以「每月可用 Token 总量」为核心额度单位；超出后请求将被限流（HTTP 429），除非配置了溢出降级策略。免费额度、用量包、学生代金券（仅限按量付费）也均以 Token 为计量基础。

- **模型调用与推理监控**：  
  模型监控（Model Monitoring）和应用监控（Application Monitoring）均精确上报每次调用的 `input_tokens` 和 `output_tokens`，支持按分钟级粒度追踪异常消耗（如 Prompt 注入攻击、循环生成）、定位高 Token 开销节点（如长上下文 RAG 检索、思考链展开），并用于配置 TPM（Tokens Per Minute）告警。

- **高性能推理控制**：  
  在 TPM 预留服务中，Token 直接决定预留容量规格（如 50kTPM 输入 + 20kTPM 输出）；在快速模式（Fast Mode）中，Token 吞吐能力以 TPS（Tokens Per Second）衡量，并影响流式响应的 `reasoning_content` / `content` 分离行为。

- **思考模式与高级能力启用**：  
  `thinking.budgetTokens`（如 OpenCode 中配置的 `1024`）显式限制思考链（Chain-of-Thought）生成的最大 Token 数，防止过度推理导致成本失控；类似参数 `enable_thinking`、`reasoning_effort` 也隐式依赖 Token 预算进行服务端调度。

- **缓存与成本优化**：  
  显式缓存（`cache_control`）按 Token 计费（如北京地域缓存命中单价 4 元/百万 Token），其收益直接由重复请求的 Token 节省量决定；缓存折扣策略（如 TPM 预留中缓存部分按 25% 折算容量）亦基于 Token 量动态计算。

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 注意事项 |
|------|------|----------|----------|
| `input_tokens` / `output_tokens` | 单次调用实际消耗的输入/输出 Token 数，含系统提示词、工具描述、思考内容等全部上下文 | 所有监控日志（模型监控、应用监控）、API 响应头（`X-DashScope-Usage`）、账单明细 | 不同模型 Tokenizer 实现不同，相同文本在 `qwen3-plus` 与 `glm-5.2` 中 Token 数可能差异达 ±15%；[多模态](multi-modal.md)输入需查[官方 Token 换算表](https://help.aliyun.com/zh/model-studio/token-calculator) |
| `budgetTokens` | 思考链生成的 Token 上限，硬性截断阈值 | `opencode.json` 的 `thinking.budgetTokens` 字段、部分第三方模型的 `reasoning_effort` | 超出即终止思考，不保证输出完整性；建议设为预期输出长度的 1.2~1.5 倍 |
| `TPM`（Tokens Per Minute） | 每分钟最大 Token 处理能力，用于预分配推理资源 | TPM 预留实例配置、告警规则（`model_tpm_usage` 指标） | 输入/输出 TPM 可独立设置；自然日结算，不跨天累计 |
| `X-DashScope-Usage` 响应头 | 返回 `{"input_tokens":123,"output_tokens":456}`，供客户端实时统计 | 所有标准 API 响应（HTTP 200） | 无需开启高级监控即可获取，是轻量级 Token 追踪首选 |
| `cache_control` | 控制缓存生命周期与作用域，影响 Token 计费逻辑 | 请求体中 `messages` 或 `prompt` 的元数据字段 | 缓存命中时仍计费，但单价显著低于实时计算；需配合 `cache_key` 实现精准复用 |

## 面向开发者，简洁实用

- ✅ **必查**：调用后立即解析 `X-DashScope-Usage` 响应头，建立本地 Token 消耗仪表盘，避免配额突增未察觉。  
- ✅ **必配**：对高频固定 Prompt（如系统角色设定、格式模板），强制添加 `cache_control: {"type": "ephemeral"}`，立省 90%+ Token 成本。  
- ✅ **必控**：启用思考模式时，`budgetTokens` 建议从 512 起步，结合应用监控中的 `LLM` 节点 Token 分布直方图逐步调优。  
- ⚠️ **避坑**：不要假设 Token 数 = 字符数（中文约 1.3~1.8 字符/Token，英文约 0.75 单词/Token）；[多模态](multi-modal.md)输入务必查换算表，避免预算偏差。  
- 📈 **进阶**：用 Prometheus 查询 `model_usage{model="qwen3-plus"}[1h]` 结合 `rate()` 函数计算实时 TPM，驱动自动扩缩容决策。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [use cases](../guides/use-cases.md)


