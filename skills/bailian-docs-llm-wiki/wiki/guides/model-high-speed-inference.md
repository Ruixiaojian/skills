# model high speed inference

百炼平台提供两种面向高吞吐与低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者可独立使用或组合应用——TPM 预留解决资源争抢导致的限流问题，快速模式优化模型解码阶段的 TPS 表现。开发者应根据业务 SLA（是否容忍 429、是否要求首 token 延迟 <200ms、是否需稳定高并发）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期不被公共资源池限流。支持千问（Qwen3.x 系列）、GLM-5.x、DeepSeek-v4、Kimi-K2.6 等主流模型，具体可用模型以控制台实时列表为准。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式（Fast mode）**：Preview 阶段特性，通过优化解码调度与硬件亲和性，将 TPS 提升至标准 API 的 1.5~2 倍（典型值 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。当前仅支持 `glm-5.2-fast-preview` 模型（[原文标题](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。
- > **注意**：文档 1 中列出的 `千问3.7-Flash-2026-07-15` 等带日期后缀的模型，在文档 2 的快速模式支持列表中未出现，且文档 2 明确说明“当前仅支持 `glm-5.2-fast-preview`”。因此，**快速模式暂不支持 Qwen 系列及其他模型**，该信息以 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 为准。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（每分钟 Token 数） | TPS（每秒 Token 数），无显式配额参数 |
| **计费单位** | 预付费：按 kTPM/天；溢出部分按 token 计费 | 按 token 计费（与标准 API 一致） |
| **缓存折扣** | 支持（如 GLM-5.2 为 0.25，Qwen3.8-max 为 0.125） | 支持（`glm-5.2-fast-preview` 缓存命中单价为 ¥4/百万 tokens） |
| **长输入阶梯系数** | 部分模型支持（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数为 1.33） | 文档未提及阶梯系数，按标准 token 计费逻辑执行 |

## 使用方式

- **TPM 预留**：创建成功后获取专属模型 code（如 `qwen3-max-dedicated-abc123`），在 API 请求中直接替换 `model` 字段即可生效。调用域名、鉴权方式、请求体结构与标准 API 完全一致。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的“创建 TPM 预留”与“API 接入”章节。
- **快速模式**：使用专用模型 ID（如 `glm-5.2-fast-preview`）并**切换至专属接入域名**：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（`{workspace_id}` 和 `{region}` 需从控制台业务空间管理页获取）。无需额外 header 或参数，但必须使用该域名。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 的“使用方式”部分。
- > **注意**：TPM 预留的专属模型 code 与快速模式的模型 ID **不可混用**。例如，不能将 `glm-5.2-fast-preview` 作为 TPM 预留的“选择模型”，也不能将 TPM 预留生成的 code 用于快速模式域名。二者是正交的加速路径。

## 限制和注意事项

- **TPM 预留**
  - “按天”付费周期按**自然日**计算（当日 00:00 到次日 00:00），非购买时刻起 24 小时。建议开启自动续费避免服务中断。
  - 缩容/退订产生违约金：退款 = 降量部分预付费 × (1 − 已用时长/购买时长 × 1.5)。
  - 预热期：首次调用或流量陡增时，系统需短暂预热，期间可能出现延迟波动，需客户端实现重试或排队机制。
- **快速模式**
  - 当前为 preview 阶段，能力与规格可能随版本调整，不承诺长期兼容。
  - 超出 TPM 额度时请求进入排队队列（非立即限流），但排队时长受系统负载影响，无确定性 SLA。
  - `glm-5.2-fast-preview` 返回结构包含 `reasoning_content` 字段，流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content`。
- **共性限制**
  - 两种模式均不改变模型本身的能力、上下文长度上限或输出格式语义，仅优化性能与资源保障维度。
  - TPM 预留实例到期 14 小时后自动删除，code 不可恢复；快速模式无独立生命周期管理，依赖底层模型服务状态。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


