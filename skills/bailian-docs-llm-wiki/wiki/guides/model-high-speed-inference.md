# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute reservation）** 和 **快速模式（Fast mode）**。前者通过预购专属容量保障确定性吞吐与稳定性，适用于流量可预估、不可接受限流的核心业务；后者通过底层调度与硬件优化提升单请求输出速度（TPS），适用于对响应实时性敏感的交互式场景（如编程助手、Agent 多步推理）。二者可独立使用，不互斥，但技术原理、计费模型与接入方式完全不同。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期调用不受公共资源池限流影响。支持模型详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中“支持的模型”表格，覆盖千问、GLM、DeepSeek、Kimi 等主流模型在华北2（北京）和新加坡地域的多个版本。  
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（preview 阶段），提供更高 TPS（80~100）和更低输出延迟，但**不提供容量保障**，仍受全局 TPM 限流约束（超出时请求排队而非拒绝）。详细支持列表见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两篇原始文档对“容量保障”定义存在关键差异——TPM 预留文档明确其提供“专属容量刚性兑付”，而快速模式文档强调“超出 TPM 额度不会立即限流，请求进入排队队列”。这意味着快速模式**不等同于容量预留**，其排队机制仍依赖后台共享资源池调度，无法替代 TPM 预留用于 SLA 严苛场景。开发者应依据业务需求（确定性 vs. 实时性）分别选型。

## 关键参数

| 能力 | 核心参数 | 说明 |
|------|----------|------|
| **TPM 预留** | `input_tpm` / `output_tpm`（单位：kTPM） | 必填，按天预付费购买的专属吞吐量。起步值与步长因模型而异，需结合 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 估算。支持缓存折扣（如 GLM-5.2 缓存命中部分按 25% 折算容量）和长输入阶梯系数（如 GLM-5.1 在 \[32K,200K\] 区间输入系数为 1.33）。 |
| **快速模式** | `model` = `glm-5.2-fast-preview` | 唯一启用标识，无需额外参数。调用域名需替换为 workspace 专属地址（格式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。 |

## 使用方式

- **TPM 预留**：创建成功后，系统生成专属模型 code（如 `qwen3.7-max-20260520-tpm-xxxxx`），**必须将 API 请求中的 `model` 参数替换为此 code** 才能生效。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中 Python/curl 调用片段。注意：实例需处于“运行中”状态，且首次大规模调用存在短暂预热期（可能引发延迟波动）。  
- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数调用，域名需指向 workspace 专属 endpoint。流式响应中新增 `reasoning_content` 字段，需按 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档示例解析。  

## 限制和注意事项

- **TPM 预留**：  
  - 专属模型 code 仅在预留实例“运行中”或“待生效”状态下有效；到期后 14 小时自动删除，code 失效。  
  - 缩容/退订触发 1.5 倍违约金结算，归零操作保留 code 但停止计费。  
  - 溢出策略为“仅使用预留容量”时，超限请求返回 HTTP 429，需客户端主动重试或降级。  
- **快速模式**：  
  - 当前为 preview 阶段，模型 ID、性能指标及计费规则可能调整，不建议用于生产环境长期依赖。  
  - 不支持缓存（文档未声明缓存能力，且价格表中“缓存命中”列为 4 元，与标准 GLM-5.2 的 4 元一致，暗示无额外缓存折扣）。  
  - 排队机制不保证端到端延迟上限，高并发下排队时长不可控。  
- **共性限制**：两者均要求业务空间已开通模型服务，且 API Key 具备对应权限。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


