# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 保障专属容量与确定性 SLA，**快速模式（Fast Mode）** 提升单请求输出速度与 TPS。二者适用不同优化目标——前者解决“容量争抢”问题，后者解决“响应延迟”问题，可独立或组合使用（如在 TPM 预留实例上启用 fast-preview 模型）。

## 支持的模型与功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），提供 1.5~2 倍标准 API 的 TPS（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出流速敏感的场景。该能力处于 preview 阶段，规格可能调整，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两文档对 `glm-5.2` 的缓存折扣描述存在差异——[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中明确其缓存命中部分按 25% 折算容量；而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 仅列出“缓存命中”单价为 4 元（北京），未说明容量折算逻辑。实际容量计算请以控制台实时参数为准，或参考 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的阶梯系数与缓存折扣规则。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入TPM / 输出TPM（kTPM） | TPS（80~100）、输出延迟降低 |
| **计费单位** | 预付费（按天，kTPM） | 按 token（输入/输出分别计费） |
| **容量保障** | 刚性兑付专属容量，不共享 | 无专属容量，依赖公共资源池，超限请求排队而非直接限流 |
| **溢出策略** | 可选：自动溢出至按量（默认）或返回 429 | 请求排队，不返回 429（但排队时延增加） |
| **缓存支持** | 支持（如 glm-5.2 缓存命中按 25% 折算输入容量） | 支持（明确列出缓存命中单价） |

## 使用方式

- **TPM 预留**：创建后获取专属 `model` code，在 API 请求中替换标准模型 ID 即可生效。需确保实例状态为“运行中”，且调用域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/...`）。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的“创建 TPM 预留”与“API 接入”章节。
- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数，并切换至专属接入域名（格式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。无需额外 header 或 query 参数。流式调用时需解析 `delta.reasoning_content` 和 `delta.content` 字段。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **组合使用**：可在已创建的 TPM 预留实例上，将 `model` 参数设为 `glm-5.2-fast-preview`（前提是该模型 code 已开通快速模式支持），从而同时获得容量保障与高速输出。

## 限制和注意事项

- **TPM 预留**：
  - 创建后需等待实例“运行中”状态方可调用；短时间内请求量激增会触发系统预热，预热期可能出现延迟波动，建议实现客户端重试或排队机制。
  - 缩容/退订会产生违约金（已用部分按 1.5 倍系数结算），且退订后专属 model code 失效。
  - 服务到期后 14 小时内资源不可恢复，务必提前续费。
- **快速模式**：
  - 当前仅 `glm-5.2-fast-preview` 可用，不支持其他模型；preview 阶段能力可能变更，不建议用于生产环境长期依赖。
  - 排队机制不保证端到端延迟上限，高并发下排队时延可能显著上升。
  - 返回结构含 `reasoning_content` 字段，需适配解析逻辑（尤其流式场景）。
- **通用限制**：
  - 两种能力均不改变模型本身的能力边界（如上下文长度、token 限制），具体参数以各模型文档为准。
  - TPM 预留与快速模式的计费相互独立：TPM 预留覆盖其专属容量内调用，超出部分按量计费；快速模式所有调用均按 token 计费，不受 TPM 预留额度影响（除非 model code 显式绑定快速模式）。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


