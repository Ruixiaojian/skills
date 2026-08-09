# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障型）与快速模式（性能型）。前者通过预付费锁定专属推理容量，确保业务高峰期不被公共限流影响；后者通过优化调度与执行路径，在 preview 阶段显著提升输出 TPS。二者适用场景不同，可独立使用或组合部署。

## 支持的模型/功能

- **TPM 预留**：为指定模型提供刚性容量保障，支持千问、GLM、DeepSeek、Kimi 等主流大模型系列，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），处于 preview 阶段，TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两套机制无模型交集——TPM 预留支持 Qwen3.8-Max 等多款模型，而快速模式目前仅支持 `glm-5.2-fast-preview`。不可对同一模型同时启用两种加速方式（例如不能为 `glm-5.2-fast-preview` 创建 TPM 预留），因快速模式本身不提供专属容量预留能力。

## 关键参数

| 参数类型 | TPM 预留 | 快速模式 |
|----------|-----------|------------|
| **核心控制参数** | 输入TPM（kTPM）、输出TPM（kTPM）、溢出策略（自动溢出 / 仅预留） | 无显式配置参数；通过模型 ID（如 `glm-5.2-fast-preview`）隐式启用 |
| **计费单位** | 按 kTPM 预付费（按天结算，自然日计费） | 按 token 计费（输入/输出单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 表格） |
| **缓存支持** | 支持缓存折扣（如 GLM-5.2 缓存命中部分按 25% 折算容量） | 支持缓存（`cached_tokens` 字段可见，输入单价含缓存优惠） |
| **长输入处理** | 部分模型支持阶梯系数（如 GLM-5.1 在 \[32K,200K\] 区间输入系数 1.33） | 未说明阶梯系数，按标准 token 计费逻辑处理 |

## 使用方式

- **TPM 预留**：在百炼控制台创建实例后，获取专属模型 code（如 `qwen38max-tpm-abc123`），**将 API 请求中的 `model` 参数替换为该 code** 即可生效。调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。
- **快速模式**：无需额外配置，**直接使用 `glm-5.2-fast-preview` 作为 `model` 参数值**，并切换至专属接入域名：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 的调用示例。

> **注意**：TPM 预留实例需状态为「运行中」才可调用；快速模式 preview 版本能力可能随版本调整，生产环境使用前请确认控制台最新支持状态。

## 限制和注意事项

- **TPM 预留**
  - 「按天」付费周期按**自然日**计算（当日 00:00 到次日 00:00），非连续 24 小时，购买时间点影响实际有效时长（如 16:00 购买仅剩约 8 小时）；
  - 预留到期后 2 小时内仍可调用，但 14 小时后实例删除且不可恢复；
  - 扩缩容操作中服务不中断，但归零（设为 0 kTPM）会触发 1.5 倍违约金结算。

- **快速模式**
  - 当前仅 `glm-5.2-fast-preview` 可用，不支持其他模型；
  - 输出流式响应中新增 `reasoning_content` 字段，需客户端适配解析逻辑；
  - 超出 TPM 额度时请求进入排队队列而非立即限流（429），但排队时延不可控；
  - preview 阶段不承诺 SLA，不建议用于强实时性生产链路。

- **共性限制**
  - 两者均要求业务空间已开通模型服务且地域匹配；
  - TPM 预留专属 code 与快速模式 model ID 不可混用（如 `qwen38max-tpm-xxx` 无法用于快速模式调用）；
  - 缓存命中率依赖请求内容重复性，实际效果以运行监控为准。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


