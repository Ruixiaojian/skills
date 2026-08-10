# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 保障专属容量与确定性 SLA，**快速模式（Fast Mode）** 提升单请求输出吞吐率（TPS）。二者定位不同，可独立使用或组合应用——TPM 预留解决“能不能稳定跑”，快速模式解决“能不能更快出结果”。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出 TPM 容量，确保高峰期不受公共资源限流影响。支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表以控制台实时展示为准，详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），通过底层调度与计算优化，将 TPS 提升至标准 API 的 1.5~2 倍（典型值 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。该能力处于 preview 阶段，模型 ID 和能力边界可能调整，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：两套机制不互通。TPM 预留需使用专属 model code（如 `qwen3.8-max-tpm-xxxxx`），而快速模式使用固定 fast model ID（如 `glm-5.2-fast-preview`）。二者不可混用——即不能对 `glm-5.2-fast-preview` 创建 TPM 预留，也不能在快速模式调用中传入 TPM 预留的 model code。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | TPS（[Token](../concepts/token.md)s Per Second），无显式配额参数 |
| **计费单位** | 预付费（按天，kTPM × 天数） | 按 token 计费（输入/输出 token 数 × 单价） |
| **超额行为** | 可选：自动溢出至按量计费（默认）或返回 429 | 请求排队，不立即限流；排队超时返回 429 |
| **缓存支持** | 支持（不同模型缓存折扣率不同，如 GLM-5.2 为 25%） | 支持（`cached_tokens` 字段可见，单价含缓存优惠） |
| **长输入处理** | 支持阶梯系数（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数 1.33） | 不支持阶梯系数，统一按基础单价计费 |

## 使用方式

- **TPM 预留**：  
  1. 在[百炼控制台](https://bailian.console.aliyun.com/#/efm/tpm_reservation)创建预留实例，获取专属 model code；  
  2. 将 API 请求中的 `model` 字段替换为该 code（例如 `"model": "qwen3.8-max-tpm-abc123"`）；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。详细步骤见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **快速模式**：  
  1. 使用 `glm-5.2-fast-preview` 作为 model 参数；  
  2. **必须使用专属接入域名**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名；  
  3. 支持流式响应，返回结构含 `reasoning_content` 与 `content` 分离字段。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

## 限制和注意事项

- **TPM 预留**：  
  - “按天”付费周期按**自然日**结算（当日 00:00 到次日 00:00），非连续 24 小时，建议开启自动续费避免中断；  
  - 扩缩容操作会触发 1.5 倍违约金结算已用部分；  
  - 退订后专属 model code 立即失效，请求回退至公共资源。

- **快速模式**：  
  - 当前仅 `glm-5.2-fast-preview` 可用，不支持其他模型；  
  - preview 阶段不承诺长期兼容性，model ID 或接口行为可能变更；  
  - 排队机制不保证端到端延迟，高并发下仍可能出现排队延迟。

- **共性限制**：  
  - 两种模式均不改变模型本身的能力边界（如上下文长度、推理逻辑）；  
  - TPM 预留的专属容量**不覆盖**快速模式的 TPS 加速能力——若需同时保障容量+提速，须分别配置 TPM 预留（针对 `glm-5.2` 标准版）与快速模式（独立调用 `glm-5.2-fast-preview`）。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


