# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**快速模式（Fast mode）** 与 **TPM 预留（TPM Reservation）**。前者通过模型侧优化提升单请求输出速度（TPS），适用于对响应流畅性敏感的实时交互场景；后者通过资源预分配保障专属吞吐容量（TPM），适用于流量可预估、不可接受限流的关键业务。二者可独立使用，也可组合（如在 TPM 预留实例上启用快速模式模型）。

## 支持的模型与功能

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡地域），为预览阶段能力，具备更高 TPS（80~100）、支持 `reasoning_content` 分离[流式输出](../concepts/streaming-output.md)等特性。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **TPM 预留**：支持多款主流模型，包括 `Qwen3.8-Max`、`Qwen3.6-Flash-2026-04-16`、`GLM-5.2`、`DeepSeek-v4-Flash`、`Kimi-K2.6` 等（具体以控制台实时列表为准），提供刚性容量保障与专属模型 code。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- > **注意**：文档 1 中 `glm-5.2-fast-preview` 被列为快速模式唯一支持模型；而文档 2 的 TPM 预留支持列表中包含 `GLM-5.2`（非 `-fast-preview` 后缀）。二者模型 ID 不同，**快速模式不可直接应用于 TPM 预留创建时选择的 `GLM-5.2` 基础模型**——若需同时享受高速输出与容量保障，须确认该模型是否已发布对应 `*-fast-preview` 变体并开放 TPM 预留（当前未明确支持，建议以控制台可用模型为准）。

## 关键参数

| 参数类型 | 快速模式 | TPM 预留 |
|----------|-----------|------------|
| **核心指标** | TPS（[Token](../concepts/token.md)s Per Second）提升至 1.5~2× 标准 API | TPM（[Token](../concepts/token.md)s Per Minute）专属配额，单位为 kTPM（1 kTPM = 1,000 tokens/min） |
| **计费单位** | 按输入/输出 token 计费（与标准 API 一致） | 预付费：按天购买，费用 = 输入TPM单价 × 输入kTPM + 输出TPM单价 × 输出kTPM |
| **容量弹性** | 无专属容量，超额度请求进入排队队列（非立即限流） | 可选溢出策略：「自动溢出至按量」（默认，服务不中断）或「仅预留容量」（超限返回 429） |
| **缓存折扣** | `glm-5.2-fast-preview` 在北京/新加坡均支持缓存命中价（4元/百万token） | 多数模型支持缓存折扣（如 `glm-5.2`: 25%，`qwen` 系列: 12.5%~20%），影响实际容量消耗计算 |

## 使用方式

- **快速模式**：无需额外参数，仅需将 `model` 设为 `glm-5.2-fast-preview`，并使用专用域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。完整调用说明见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **TPM 预留**：在百炼控制台创建后，获取系统生成的**专属模型 code**，并在 API 请求中将其设为 `model` 参数值（替换原模型 ID）。接入域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。注意：实例需处于「运行中」状态，且首次大流量请求前存在短暂预热期，建议实现客户端重试逻辑。详情参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **快速模式限制**：当前为 preview 阶段，模型能力、规格及支持地域可能调整；不支持所有标准 API 参数（如 `temperature` 等采样参数行为可能受限，需实测验证）；`glm-5.2-fast-preview` 的输入长度上限为 1 Million token，但未明确说明长输入阶梯系数适用性。
- **TPM 预留限制**：「按天」付费周期按**自然日**结算（例：16:00 购买 1 天预留，有效期至当日 24:00，仅约 8 小时），强烈建议开启「到期自动续费」；缩容/退订将按 1.5 倍系数收取违约金；专属模型 code 在实例退订后立即失效，请求回退至公共资源。
- > **注意**：两文档对计费描述存在隐含差异——文档 1 强调快速模式“按 token 计费，与标准 API 一致”；文档 2 明确 TPM 预留“预留容量内调用不额外收费”，即预付费覆盖额度内 token 调用。**这意味着：使用 TPM 预留 + 快速模式模型（如未来支持）时，费用结构为「预付费保障容量 + 超额按 token 计费」，而非双重计费**。当前因 `glm-5.2-fast-preview` 未列入 TPM 预留支持列表，该组合暂不可用。

## 来源文档

- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


