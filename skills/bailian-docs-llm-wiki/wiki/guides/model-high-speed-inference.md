# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 用于保障稳定专属容量，避免公共池限流；**快速模式（Fast mode）** 用于提升单请求输出速度（TPS），适用于对响应实时性敏感的交互场景。二者可独立使用，不互斥，但适用目标与技术机制不同。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保业务高峰期容量刚性兑付。支持模型包括千问系列（Qwen3.6/3.7/3.8）、GLM-5.1/5.2、DeepSeek-v4 系列及 Kimi-K2.6 等，具体以控制台实时列表为准。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡地域），通过优化调度与计算路径实现 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等场景。该能力处于 preview 阶段，规格可能调整，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：文档 1 中列出的 `千问3.7-Flash-2026-07-15` 等带日期后缀的模型，在文档 2 的快速模式支持列表中未出现；而文档 2 明确限定快速模式**仅支持 `glm-5.2-fast-preview`**，未提及其他模型。因此，快速模式当前不具备模型泛化能力，不可将 TPM 预留的任意模型 code 直接用于快速模式调用。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（每分钟 token 数） | TPS（每秒 token 数），非显式配置项，由服务端自动优化 |
| **溢出策略** | 可选：`自动溢出至按量`（默认）或 `仅预留容量（返回 429）` | 请求超出当前队列处理能力时进入排队，**不立即限流**，无 429 返回（但排队延迟可能升高） |
| **缓存折扣** | 支持（如 GLM-5.2 输入缓存命中按 25% 折算容量） | 支持（`glm-5.2-fast-preview` 输入缓存单价为 4 元/百万 token） |
| **长输入阶梯系数** | 部分模型支持（如 GLM-5.1 在 \[32K,200K\] 区间输入系数 1.33） | 文档未提及阶梯系数，实际行为以运行结果为准 |

## 使用方式

- **TPM 预留**：创建成功后获取专属模型 code（如 `qwen3-max-dedicated-xxxxx`），在 API 请求中**替换 `model` 字段**即可生效。需使用标准 DashScope 兼容域名（`https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。
- **快速模式**：直接使用预置模型 ID `glm-5.2-fast-preview` 发起请求，**无需修改其他参数**，但必须使用专属接入域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（`workspace_id` 和 `region` 需从控制台业务空间页面获取）。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：TPM 预留的专属 model code 与快速模式的 `glm-5.2-fast-preview` 是两类完全独立的模型标识，**不可混用**。例如，不能将 `glm-5.2-fast-preview` 作为 TPM 预留的“选择模型”，也不能将 TPM 预留生成的 code 用于快速模式域名调用。

## 限制和注意事项

- **计费周期差异**：TPM 预留「按天」计费按**自然日**结算（当日 00:00 到期），非 24 小时滚动，易导致首日有效时长不足；建议开启自动续费或在每日 00:00 后购买。快速模式按 token 实时计费，无周期性约束。
- **预热与稳定性**：TPM 预留实例在流量快速拉升时需短暂预热，期间可能出现延迟波动，需在客户端实现请求排队或重试机制（见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。
- **preview 限制**：快速模式为预览能力，接口行为、模型可用性及性能指标可能随版本迭代调整，生产环境使用前需充分验证。
- **模型兼容性**：TPM 预留支持的模型范围远大于快速模式；若需同时满足容量保障与高速输出，目前仅能对 `glm-5.2` 系列分别配置 TPM 预留（保障吞吐）与启用快速模式（提升 TPS），但二者需独立管理。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


