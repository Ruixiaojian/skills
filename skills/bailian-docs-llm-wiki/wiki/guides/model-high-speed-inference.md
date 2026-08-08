# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者目标不同——前者解决**确定性容量供给问题**，后者优化**单次响应的 token 生成速率（TPS）**。开发者需根据业务 SLA（是否容忍限流/排队？是否要求确定性吞吐？）选择合适方案，二者可独立使用或组合使用（如为 `glm-5.2-fast-preview` 创建 TPM 预留）。

## 支持的模型与功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期不被公共资源限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表及价格详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档。
  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型，通过底层调度与 kernel 优化将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详细支持模型与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：两篇文档中关于 `glm-5.2` 的缓存折扣描述存在差异。[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确其缓存折扣为 0.25；而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 表格中标注“缓存命中”单价为 4 元（北京），但未说明折扣系数。实际调用时请以控制台实时计费明细或 `usage.prompt_tokens_details.cached_tokens` 字段为准。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|----------|
| **核心指标** | 输入/输出 kTPM（[Token](../concepts/token.md)s Per Minute） | TPS（[Token](../concepts/token.md)s Per Second）提升倍率（1.5~2×） |
| **计费单位** | 预付费（按天，kTPM × 天数） | 按 token（输入/输出分别计费） |
| **溢出策略** | 可选：自动溢出至按量计费（默认）或仅预留容量返回 429 | 请求超出 TPM 额度时进入排队队列，不立即限流 |
| **专属标识** | 自动生成专属 `model` code（如 `qwen38max-tpm-abc123`） | 使用固定 fast model ID（如 `glm-5.2-fast-preview`） |
| **接入域名** | 通用 DashScope 域名（`dashscope.aliyuncs.com`） | 地域专属域名（如 `{workspace_id}.cn-beijing.maas.aliyuncs.com`） |

## 使用方式

- **TPM 预留**：在百炼控制台创建实例后，获取专属 `model` code，并在 API 请求中替换 `model` 参数。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。注意：实例需处于“运行中”状态，且首次调用存在短暂预热期，建议实现重试机制。

- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数，调用地域专属域名。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。完整示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：快速模式当前仅支持 `glm-5.2-fast-preview`，其他模型（包括 `glm-5.2` 标准版）无法通过追加 `-fast-preview` 后缀启用。该能力处于 preview 阶段，接口行为与性能可能随版本迭代调整。

## 限制和注意事项

- **TPM 预留**：
  - “按天”付费周期按自然日结算（当日 00:00 到次日 00:00），非 24 小时滚动，购买时间点影响实际有效时长；
  - 缩容/退订产生违约金（已用部分按 1.5 倍系数结算）；
  - 专属 `model` code 在退订后立即失效，请求回退至公共资源。

- **快速模式**：
  - 仅 preview 阶段，不承诺 SLA，不建议用于生产环境关键链路；
  - 排队机制可能导致端到端延迟升高，需评估业务对 P99 延迟的容忍度；
  - 不支持所有标准 API 参数（如部分采样参数可能被忽略），请以最新控制台文档为准。

- **共性注意事项**：
  - 两者均需在百炼控制台开通对应服务并创建业务空间；
  - TPM 预留与快速模式可叠加使用（例如为 `glm-5.2-fast-preview` 创建 TPM 预留），此时专属 model code 由 TPM 预留生成，调用时仍需使用该 code + 快速模式专属域名；
  - 所有容量计算（含缓存、长输入阶梯系数）均以控制台实时展示为准，[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的换算规则可能随模型升级更新。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


