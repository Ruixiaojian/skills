# model high speed inference

百炼平台提供两种面向高吞吐与低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决“容量确定性”问题，快速模式解决“响应实时性”问题。开发者需根据业务 SLA（如是否容忍限流、是否要求毫秒级 token 流出）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期调用不被公共池限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
  
- **快速模式（Fast mode）**：Preview 阶段能力，通过优化推理调度与显存管理，将 TPS 提升至标准 API 的 1.5~2 倍（典型值 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。当前仅支持 `glm-5.2-fast-preview` 模型，且需使用专用接入域名（`{workspace_id}.cn-beijing.maas.aliyuncs.com`）。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：两文档在模型支持范围上存在明显差异——TPM 预留支持十余款模型（含 Qwen3.8-Max、DeepSeek-v4-Pro 等），而快速模式目前仅支持 `glm-5.2-fast-preview`。快速模式暂不支持 TPM 预留所列的其他模型，该限制在 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 中未明确说明，但实际控制台与 API 均不开放。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入TPM / 输出TPM（kTPM） | TPS（tokens per second），非显式配置项，由服务端自动优化 |
| **计费单位** | 预付费（按天，kTPM × 天数） | 按 token 计费（输入/输出单价与标准 API 一致） |
| **缓存折扣** | 支持（如 GLM-5.2 缓存命中部分按 25% 折算容量） | 支持（`glm-5.2-fast-preview` 输入缓存单价为 4 元/百万 token） |
| **长输入阶梯系数** | 支持（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数为 1.33） | 不适用（快速模式未声明阶梯系数，实际按标准 token 数计费） |

## 使用方式

- **TPM 预留**：创建成功后，系统生成专属模型 code（如 `qwen38max-tpm-xxxxx`），需将 API 请求中的 `model` 参数替换为此 code。调用域名与标准 API 相同（`dashscope.aliyuncs.com`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。

- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数值，并切换至专用域名 `{workspace_id}.cn-beijing.maas.aliyuncs.com`（华北2）或对应新加坡域名。无需额外参数，流式响应中 `reasoning_content` 与 `content` 分离推送。完整示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：快速模式文档中未提及地域限制，但其示例域名固定为 `cn-beijing`，且新加坡地域未列出 `glm-5.2-fast-preview` 的价格信息。实际使用时请以控制台可用模型为准，避免跨地域调用失败。

## 限制和注意事项

- **TPM 预留**
  - 「按天」付费周期按自然日结算（00:00–24:00），非购买时刻起 24 小时；例如 16:00 购买 1 天预留，实际有效期仅约 8 小时 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
  - 扩缩容操作会触发 1.5 倍违约金结算，归零输入/输出 TPM 仍保留专属 model code，但已用部分费用不可退 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
  - 部分模型特性受限：如 GLM-5.2 的 `thinking_budget` 参数在 TPM 预留调用中不生效 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **快速模式**
  - 当前为 preview 阶段，能力与规格可能随版本调整，不建议用于生产环境关键链路。
  - 超出 TPM 额度时请求进入排队队列而非立即限流，但排队时延不可控，需业务侧自行实现超时与重试逻辑。
  - 不支持与 TPM 预留叠加使用：`glm-5.2-fast-preview` 无对应 TPM 预留型号，无法通过预留保障其容量。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


