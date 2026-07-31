# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者可独立使用或组合使用——TPM 预留解决资源争抢导致的限流问题，快速模式优化模型解码阶段的 TPS。开发者需根据业务 SLA（如是否容忍 429、是否要求首 token 延迟 <100ms）选择合适方案。

## 支持的模型与功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期调用不被公共资源池限流。支持千问、GLM、DeepSeek、Kimi 等主流模型，详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
- **快速模式（Fast mode）**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡地域），通过优化解码调度与硬件利用率，将 TPS 提升至标准 API 的 1.5~2 倍（典型值 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感场景。该能力处于 preview 阶段，规格可能调整，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：TPM 预留文档中列出的 `glm-5.2` 是标准版模型，而快速模式文档明确指出仅 `glm-5.2-fast-preview` 支持快速模式。二者模型 code 不同，不可混用；标准 `glm-5.2` 即使配置了 TPM 预留，也不会获得快速模式的 TPS 提升。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `model` | 必须替换为专属模型 code（TPM 预留）或 `-fast-preview` 后缀模型 ID（快速模式） | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |
| 输入/输出 TPM | TPM 预留需显式设置输入与输出吞吐量（kTPM），二者独立计费与限流 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 溢出策略 | TPM 预留创建时可选：`自动溢出至按量计费`（默认，服务不中断）或 `仅使用预留容量`（超限返回 429） | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 接入域名 | 快速模式必须使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，标准 API 域名不生效 | [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，获取专属模型 code；  
  2. 将 API 请求中的 `model` 参数替换为该 code；  
  3. 调用时无需修改 endpoint 或其他参数，但需注意预热期（首次突增流量时可能有短暂延迟波动，建议实现重试机制）。

- **快速模式**：  
  1. 确保业务空间已开通对应地域（北京/新加坡）；  
  2. 使用专属域名，并将 `model` 设为 `glm-5.2-fast-preview`；  
  3. 流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段（见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 示例）。

> **注意**：快速模式不支持 TPM 预留的专属模型 code 组合使用。若需同时保障容量+提速，需先为 `glm-5.2-fast-preview` 创建 TPM 预留（当前控制台暂未开放该模型的 TPM 预留入口，属能力缺口，建议关注后续更新）。

## 限制和注意事项

- TPM 预留实例到期后 2 小时内仍可调用，但 14 小时后彻底删除且不可恢复；退订后专属 model code 失效，请求自动回退至公共资源 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- 快速模式为 preview 功能，其模型 ID、性能指标、支持地域可能变更，生产环境使用前请确认控制台最新状态 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- 缓存折扣仅影响输入 TPM 消耗（如 GLM-5.1 支持 20% 缓存命中折扣），不影响输出 TPM 或快速模式计费；长输入阶梯系数（如 GLM-5.1 在 32K–200K 区间输入系数为 1.33）仅作用于 TPM 预留容量计算，与快速模式无关。
- TPM 预留缩容/退订会产生违约金（已用部分按 1.5 倍系数结算），公式见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 计费说明。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


