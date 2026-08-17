# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**快速模式（Fast Mode）** 与 **TPM 预留（TPM Reservation）**。前者通过模型侧优化提升单请求输出速度（TPS），适用于对响应流速敏感的实时交互场景；后者通过预分配专属推理容量保障业务高峰期的稳定吞吐（TPM），适用于流量可预估且不可接受限流的关键业务。二者可独立使用，也可组合部署（如在 TPM 预留实例上启用快速模式模型）。

## 支持的模型/功能

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡地域），为 preview 阶段能力，具备更高 TPS（80~100）、[流式输出](../concepts/streaming-output.md)分离 `reasoning_content` 与 `content` 字段等特性。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **TPM 预留**：支持多模型，包括 `Qwen3.8-Max`、`Qwen3.7-Plus-2026-05-26`、`GLM-5.2`、`DeepSeek-v4-Pro-0813`、`Kimi-K2.6` 等（具体以控制台实时列表为准）。不同模型支持的输入/输出 TPM 起步值、阶梯系数及缓存折扣策略各异，需结合业务负载使用 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 估算。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中 `glm-5.2-fast-preview` 的计费单价（北京：输入 56 元/百万 token）与文档 2 中 `GLM-5.2` 的 TPM 预留输入单价（北京：¥36.29 / Per 10,000 TPM）单位与计费逻辑不同，不可直接对比；前者为按 token 计费，后者为按预留容量预付费，二者属于正交能力，实际成本需按各自规则分别核算。

## 关键参数

| 参数 | 快速模式 | TPM 预留 |
|------|----------|-----------|
| **核心标识** | 模型 ID（如 `glm-5.2-fast-preview`） | 专属模型 code（由控制台生成，非公开模型名） |
| **性能指标** | TPS（[Token](../concepts/token.md)s Per Second）：80~100（标准 API 的 1.5~2 倍） | TPM（[Token](../concepts/token.md)s Per Minute）：按 kTPM 预留，输入/输出可独立配置 |
| **计费单位** | 按实际输入/输出 token 计费（同标准 API） | 按预付费购买的 kTPM 容量计费（按天结算，自然日周期） |
| **限流行为** | 超出 TPM 额度时请求入队列，不立即限流 | 预留容量内无限制；溢出策略可选「自动降级至按量」或「严格限流返回 429」 |
| **缓存支持** | 支持缓存命中（北京：4 元/百万 token 缓存单价） | 多数模型支持缓存折扣（如 `glm-5.2` 缓存命中部分按 25% 折算容量） |

## 使用方式

- **快速模式**：无需额外参数，仅需将 `model` 设为 `glm-5.2-fast-preview`，并使用兼容模式域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。流式调用需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。完整示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **TPM 预留**：需先在[百炼控制台](https://bailian.console.aliyun.com/#/efm/tpm_reservation)创建实例，获取专属模型 code 后，将其填入 API 请求的 `model` 字段（其他参数与标准调用一致）。注意：短时间内请求量快速拉升时系统需短暂预热，建议客户端实现排队或重试机制。接入细节见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：TPM 预留实例创建后，`glm-5.2` 的 `thinking_budget` 参数在调用中不生效，该限制仅适用于标准 GLM-5.2 模型，不适用于 `glm-5.2-fast-preview`（其思考长度由服务端动态管理）。

## 限制和注意事项

- **快速模式限制**：当前为 preview 阶段，模型能力、规格及可用地域可能随版本调整；不支持所有标准 API 参数（如 `temperature` 等采样参数效果可能受限）；`reasoning_content` 字段仅在 `glm-5.2-fast-preview` 中存在，其他模型不返回。
- **TPM 预留限制**：「按天」付费周期按**自然日**计算（如 16:00 购买，当日 00:00 到期），非连续 24 小时；缩容/退订按 1.5 倍系数结算违约金；服务到期后 14 小时内资源将被彻底删除且不可恢复。
- **共性注意事项**：两种能力均需确保业务空间已开通对应地域的模型服务；快速模式与 TPM 预留的专属模型 code 互不兼容——不能将 `glm-5.2-fast-preview` 直接用于 TPM 预留实例，反之亦然；实际可用模型列表、价格及参数请始终以[百炼控制台](https://bailian.console.aliyun.com)实时展示为准。

## 来源文档

- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


