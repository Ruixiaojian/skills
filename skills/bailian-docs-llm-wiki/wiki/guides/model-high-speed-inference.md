# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（Token Per Minute Reservation）** 用于保障确定性容量与稳定性，适用于流量可预估、不可接受限流的关键业务；**快速模式（Fast Mode）** 则聚焦输出速度优化，通过底层调度与计算优化提升 TPS，适用于 AI 编程助手、Agent 多步推理等对响应速度敏感的场景。二者可独立使用，不互斥，但接入方式、计费模型与适用边界存在本质差异。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属推理吞吐量（单位：kTPM），支持输入/输出维度独立配置，保障高峰期服务可用性。当前支持千问、GLM、DeepSeek、Kimi 等主流模型的多个版本，具体以控制台实时列表为准。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅开放 `glm-5.2-fast-preview` 模型（北京/新加坡地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），并引入排队机制替代硬限流。该能力不改变模型逻辑，但返回结构新增 `reasoning_content` 字段。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两篇原始文档对“缓存命中”定义不一致——TPM 预留文档中 `glm-5.2` 的缓存折扣为 0.25（即命中部分按 25% 折算容量），而快速模式文档中 `glm-5.2-fast-preview` 的“缓存命中”列值为 `4元`（实为缓存命中单价，非折扣率）。二者属不同计费上下文，不可直接对比；实际调用时请以对应模式的计费说明为准。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（刚性容量） | TPS（吞吐性能目标，非硬配额） |
| **溢出行为** | 可选：自动溢出至按量计费（默认）或返回 429 | 请求排队，不立即限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） |
| **专属标识** | 自动生成专属 `model` code（如 `qwen37max-20260520-tpm-xxxx`） | 固定 model ID（如 `glm-5.2-fast-preview`） |
| **接入域名** | 通用 DashScope 域名（`dashscope.aliyuncs.com`） | 地域专属 MaaS 域名（如 `{workspace_id}.cn-beijing.maas.aliyuncs.com`） |
| **缓存策略** | 支持缓存折扣（如 glm-5.2：0.25）、长输入阶梯系数（如 glm-5.1 分段计费） | 仅标注缓存命中单价，未提及阶梯或折扣逻辑 |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，填写模型、输入/输出 kTPM、购买时长及溢出策略；  
  2. 复制生成的专属 `model` code；  
  3. 将 API 请求中的 `model` 参数替换为该 code，其余参数与标准调用完全一致（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。  
  > 注意：首次调用后存在短暂预热期，期间可能出现延迟波动，建议客户端实现重试或排队机制。

- **快速模式**：  
  1. 确认业务空间已开通对应地域（如华北2）；  
  2. 使用专属 MaaS 域名（格式：`{workspace_id}.cn-beijing.maas.aliyuncs.com`）；  
  3. 在请求中指定 `model="glm-5.2-fast-preview"`，无需额外参数；  
  4. 流式响应需分别处理 `delta.reasoning_content` 和 `delta.content` 字段（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。

## 限制和注意事项

- **TPM 预留**：  
  - 预留实例到期后 2 小时内仍可调用，但 14 小时后自动删除且不可恢复；  
  - 缩容/退订产生违约金（已用部分按 1.5 倍系数结算）；  
  - 专属 `model` code 在退订后立即失效，请求回退至公共资源。

- **快速模式**：  
  - 当前仅 `glm-5.2-fast-preview` 单一模型可用，其他模型暂不支持；  
  - preview 阶段能力可能调整，不承诺 SLA；  
  - 不支持与 TPM 预留叠加使用（即不能将 `glm-5.2-fast-preview` 作为 TPM 预留的目标模型）。

- **共性限制**：  
  - 两种模式均要求业务空间已开通模型服务权限；  
  - 快速模式的排队机制不保证端到端延迟上限，高并发下队列等待时间可能显著增加；  
  - TPM 预留的容量计算器会自动应用缓存折扣与长输入阶梯系数，但快速模式无对应换算逻辑，需按实际 token 数计费。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


