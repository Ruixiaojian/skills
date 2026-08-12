# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute reservation）** 和 **快速模式（Fast mode）**。前者通过预购专属容量保障业务稳定性，后者通过优化调度与执行路径提升单请求输出速度（TPS）。二者可独立使用，不互斥，适用于不同维度的性能诉求：TPM 预留解决“能不能稳定扛住流量”，快速模式解决“单次响应够不够快”。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期不受公共资源限流影响。支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。

- **快速模式**：仅对部分模型提供 `*-fast-preview` 变体（如 `glm-5.2-fast-preview`），通过底层调度优化实现 1.5~2 倍 TPS 提升（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出延迟敏感的场景。当前为 preview 阶段，能力可能调整，详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：TPM 预留文档中列出的 `GLM-5.2` 模型需配合专属 model code 使用；而快速模式要求显式调用 `glm-5.2-fast-preview` 这一独立 model ID，二者不可混用。快速模式不支持 TPM 预留的专属容量保障，其调用走独立域名（`{workspace_id}.cn-beijing.maas.aliyuncs.com`），且不参与公共资源池限流，而是采用排队机制。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入TPM / 输出TPM（kTPM） | 无显式容量参数，依赖后台自动调度 |
| **溢出策略** | 可选：自动溢出至按量计费（默认）或仅预留容量（返回429） | 请求超出瞬时承载能力时进入排队队列，不立即限流 |
| **缓存支持** | 支持（如 GLM-5.2 缓存命中按 25% 折算输入容量） | 支持（`cached_tokens` 字段可见，但单价与标准 API 一致） |
| **长输入阶梯系数** | 部分模型支持（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数 1.33） | 不支持阶梯系数，统一按 token 计费 |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，获取专属 `model` code；  
  2. 将 API 请求中的 `model` 参数替换为该 code；  
  3. 调用域名与标准 API 相同（`dashscope.aliyuncs.com`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 示例。

- **快速模式**：  
  1. 使用 `*-fast-preview` 模型 ID（如 `glm-5.2-fast-preview`）；  
  2. 调用域名必须为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（region 如 `cn-beijing`）；  
  3. 无需额外参数，`stream`、`messages` 等行为与标准 API 一致。完整接入说明见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

## 限制和注意事项

- **TPM 预留**：  
  - 「按天」付费周期按**自然日**计算（当日 00:00 到次日 00:00），非购买时刻起 24 小时；建议开启自动续费避免中断；  
  - 专属 model code 退订后立即失效，已发请求回退至公共资源；  
  - 预热期存在：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，需客户端实现重试或排队机制。

- **快速模式**：  
  - 当前为 preview 阶段，模型列表、性能指标及接口行为可能变更；  
  - `reasoning_content` 字段在流式响应中独立推送，需按 `delta.reasoning_content` 和 `delta.content` 分别处理；  
  - 不支持 `thinking_budget` 等部分控制参数（如 GLM-5.2 的该参数在快速模式下无效）。

- **共性限制**：  
  - 两种模式均不支持自定义模型部署，仅限平台已开放的模型变体；  
  - 快速模式暂未开放 TPM 预留能力，无法叠加使用；若需同时保障容量与速度，建议以 TPM 预留为基础，再评估是否启用快速模式变体（需单独测试性能与成本）。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


