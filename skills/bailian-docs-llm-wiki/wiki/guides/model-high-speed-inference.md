# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（Token Per Minute Reservation）** 和 **快速模式（Fast Mode）**。前者通过预购专属容量保障确定性吞吐与稳定性，适用于流量可预估、不可接受限流的核心业务；后者通过底层调度与硬件优化提升输出 TPS，适用于对响应速度敏感的实时交互类场景。二者可独立使用，也可组合部署（例如在 TPM 预留实例上启用 fast 模型）。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表及价格详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的“支持的模型”表格。
  
- **快速模式**：当前仅开放 `glm-5.2-fast-preview` 模型（北京及新加坡地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），并引入请求排队机制替代即时限流。详细支持模型与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两文档中对 `glm-5.2` 的缓存折扣描述存在差异——[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确标注其缓存命中部分按 25% 折算容量；而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 仅在价格表中标注“缓存命中”列值为 `4元`（未说明是否参与容量折算）。实际容量消耗以 TPM 预留文档为准，快速模式调用不参与 TPM 容量抵扣。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `model` | 必须替换为专属模型 code（TPM 预留）或 fast 模型 ID（如 `glm-5.2-fast-preview`），**不可混用** | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |
| 输入/输出 TPM | TPM 预留需显式配置输入与输出 kTPM 值，二者独立计量；快速模式无此参数，按 token 计费 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 溢出策略 | TPM 预留创建时可选：`自动溢出至按量`（默认，超限转按 token 计费）或 `仅使用预留容量`（超限返回 429） | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 接入域名 | 快速模式必须使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；TPM 预留仍使用标准 dashscope 域名 | [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，获取专属 `model` code；  
  2. 将 API 请求中的 `model` 字段替换为该 code；  
  3. 调用时无需修改 endpoint 或其他参数，但需注意**首次调用存在短暂预热期**，建议实现重试或排队机制。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的“创建 TPM 预留”与“API 接入”章节。

- **快速模式**：  
  1. 使用 `glm-5.2-fast-preview` 作为 `model` 参数；  
  2. **必须**将请求发送至 `{workspace_id}.cn-beijing.maas.aliyuncs.com` 域名（非 dashscope.aliyuncs.com）；  
  3. 支持流式响应，返回结构含 `reasoning_content` 与 `content` 分离字段，需按示例解析。完整接入流程见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

## 限制和注意事项

- TPM 预留实例状态为“运行中”方可调用；服务到期后 2 小时内仍可调用，之后进入停止/过期状态，code 失效。退订后不可恢复，且 code 立即失效。
- 快速模式为 preview 功能，模型 ID、性能指标及可用地域可能随版本调整，生产环境使用前请确认控制台最新支持状态。
- TPM 预留与快速模式**不可叠加生效**：`glm-5.2-fast-preview` 不支持 TPM 预留，其调用不占用预留容量，也不受预留限流策略约束；反之，TPM 预留专属 code 仅对应标准模型变体，无法启用 fast 模式。
- 缓存折扣仅作用于 TPM 预留的容量计算（如 glm-5.2 输入缓存命中按 25% 折算），不影响快速模式的 token 计费金额。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


