# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 和 **快速模式（Fast Mode）**。前者通过预付费锁定专属推理容量，保障业务高峰期的确定性吞吐与稳定性；后者通过优化调度与计算路径，在标准计费模型基础上提升输出 TPS，适用于对响应速度敏感的实时交互场景。二者可独立使用，不互斥，但接入方式、计费逻辑与适用边界存在本质差异。

## 支持的模型/功能

- **TPM 预留**：为指定模型提供刚性容量保障，支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流模型的多个版本，覆盖华北2（北京）和新加坡地域。创建后生成专属 `model` code，调用时替换即可启用预留容量 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），处于 preview 阶段，具备更高 TPS（80~100）与排队式限流机制，无需修改请求参数，仅需指定对应 model ID 即可启用 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  
- > **注意**：文档 1 中列出的 `千问3.6-Flash-2026-04-16` 等模型虽支持 TPM 预留，但**未在文档 2 中列为快速模式支持模型**；反之，`glm-5.2-fast-preview` 仅支持快速模式，**不支持 TPM 预留**（控制台无该模型的预留选项）。二者模型集合无交集，不可混用。

## 关键参数

| 能力         | 核心参数                     | 说明                                                                 |
|--------------|------------------------------|----------------------------------------------------------------------|
| TPM 预留     | `input_tpm` / `output_tpm`   | 单位为 kTPM（1,000 tokens/分钟），需按模型阶梯系数与缓存折扣估算 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
|              | `overflow_strategy`          | 可选 `auto_fallback`（默认，超量转按量）或 `reject_excess`（超量返回 429） |
| 快速模式     | `model`                      | 固定为 `glm-5.2-fast-preview`，不可更改                              |
|              | 请求域名                     | 必须使用专属 workspace 域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` |

## 使用方式

- **TPM 预留**：  
  1. 在[百炼控制台](https://bailian.console.aliyun.com/#/efm/tpm_reservation)创建预留实例，获取专属 `model` code；  
  2. 将 API 请求中的 `model` 字段替换为该 code（如 `"qwen37max-20260520-tpm-abc123"`）；  
  3. 注意：首次调用存在短暂预热期，建议实现请求排队或重试机制 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  

- **快速模式**：  
  1. 确保已开通对应地域的业务空间，并获取 `workspace_id`；  
  2. 使用专属域名发起请求，`model` 设为 `glm-5.2-fast-preview`；  
  3. 流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content` 字段 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  

## 限制和注意事项

- **TPM 预留**：  
  - 预留容量按天计费，缩容/退订产生违约金（已用部分按 1.5 倍系数结算）；  
  - 服务到期后 2 小时内仍可调用，14 小时后实例彻底删除且 `model` code 失效；  
  - 不支持跨地域复用，北京预留的 code 无法在新加坡调用。  

- **快速模式**：  
  - 当前为 preview 阶段，模型 ID、性能指标与接口行为可能调整，不承诺向后兼容；  
  - 不支持缓存命中率折扣（文档 2 表格中“缓存命中”列值为固定单价，非折扣系数）；  
  - 排队机制不保证端到端延迟上限，高并发下队列等待时间可能显著增加。  

- > **注意**：文档 1 提到“TPM 预留支持缓存折扣”，而文档 2 中 `glm-5.2-fast-preview` 的计费表格明确列出“缓存命中”为固定金额（4元/百万 token），**二者计费逻辑不一致**。快速模式不参与缓存容量折算，其输入/输出 token 均按表中单价直接计费。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


