# model high speed inference

百炼平台提供两种面向高吞吐与低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决“能不能稳定扛住流量”，快速模式解决“单次响应够不够快”。开发者需根据业务 SLA（如峰值 RPM、P99 延迟要求、容错容忍度）选择合适方案。

## 支持的模型与功能

- **TPM 预留**：为指定模型锁定专属 [Token](../concepts/token.md)s Per Minute（TPM）吞吐量，确保高峰期不被公共资源限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型（详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的模型列表），覆盖华北2（北京）与新加坡地域。  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型，通过优化调度与计算流水线，将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。> **注意**：快速模式不提供容量保障，其请求仍受全局 TPM 限流约束，超出时进入排队而非直接拒绝（见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）；而 TPM 预留明确承诺专属容量刚性兑付，二者能力边界不可混淆。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `model` | 必须替换为专属模型 code（TPM 预留）或 fast-preview 模型 ID（如 `glm-5.2-fast-preview`），否则无法启用对应能力 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |
| 输入/输出 TPM（kTPM） | TPM 预留需显式配置输入与输出吞吐量，单位为 1,000 tokens/分钟；起步值与步长因模型而异，以控制台实时展示为准 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 溢出策略 | TPM 预留创建时可选：`自动溢出至按量计费`（默认，服务不中断）或 `仅使用预留容量`（超出返回 HTTP 429） | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 接入域名 | 快速模式必须使用专属域名 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{workspace_id}` 和 `{region}` 需从控制台获取；TPM 预留仍使用标准 DashScope 域名 | [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |

## 使用方式

- **TPM 预留**：在百炼控制台创建实例后，复制生成的专属模型 code，将其填入 API 请求的 `model` 字段即可生效。无需修改 endpoint 或认证方式。示例：
  ```python
  response = dashscope.Generation.call(
      model="tpm-reserved-qwen38max-abc123",  # 替换为实际专属 code
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数，并确保请求发往 `maas.aliyuncs.com` 域名（非 `dashscope.aliyuncs.com`）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段（见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 示例）。  
- **组合使用**：可先为 `glm-5.2` 创建 TPM 预留，再基于其专属 model code 构造 `glm-5.2-fast-preview`（若该模型支持 fast 变体），从而同时获得容量保障与速度提升。

## 限制和注意事项

- TPM 预留实例创建后需短暂预热（数秒），期间请求可能出现延迟波动；建议客户端实现重试或排队机制。  
- 快速模式为 preview 功能，其模型 ID、性能指标、支持地域可能随版本调整，不承诺长期兼容性。  
- TPM 预留到期后 2 小时内仍可调用，但 14 小时后实例删除且不可恢复；退订将立即失效专属 model code。  
- 缓存折扣、长输入阶梯系数等容量优化规则仅作用于 TPM 预留（见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中详细表格），快速模式按标准 token 计费，不适用缓存折扣。  
- 快速模式请求超限时进入队列，无明确超时保证；TPM 预留在「仅使用预留容量」策略下严格返回 429，适合强一致性要求场景。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


