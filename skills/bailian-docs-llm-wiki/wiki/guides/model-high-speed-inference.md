# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute reservation）** 用于保障稳定、专属的推理容量，适用于流量可预估且不可接受限流的生产服务；**快速模式（Fast mode）** 则聚焦于提升单请求输出速度（TPS），适用于 AI 编程助手、实时对话等对响应流畅性敏感的场景。二者在容量保障机制、计费模型与接入方式上存在本质差异，需按业务目标选型。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表及价格详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），并返回结构化 `reasoning_content` 字段。详细模型列表见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  
- > **注意**：两文档中对 `glm-5.2` 的定价不一致——TPM 预留文档按 kTPM 计费（输入 ¥80.60 / 10,000 TPM），而快速模式文档按百万 token 计费（输入 ¥16 元 / 百万 token）。二者计费模型不同，不可直接换算；实际成本需结合业务 token 分布与并发模式评估。

## 关键参数

| 能力         | 核心参数                     | 说明                                                                 |
|--------------|------------------------------|----------------------------------------------------------------------|
| TPM 预留     | `input_tpm`, `output_tpm`    | 单位为 kTPM（1 kTPM = 1,000 tokens/min），需按模型阶梯系数与缓存折扣估算（参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中“长输入阶梯系数”表） |
|              | `overflow_strategy`          | 可选 `auto_fallback`（默认，超限自动转按量）或 `reject_excess`（超限返回 429） |
| 快速模式     | `model`                      | 必须使用专用 model ID（如 `glm-5.2-fast-preview`），无额外参数       |
|              | 请求域名                     | 使用专属 workspace 域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` |

## 使用方式

- **TPM 预留**：创建后获取专属 `model` code，在 API 请求中替换标准 model 名称即可生效。示例：
  ```python
  response = dashscope.Generation.call(
      model="tpm-qwen38max-abc123",  # 替换为控制台生成的专属 code
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
  > 注意：新预留实例需短暂预热，高峰期请求建议实现排队或重试机制（详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。

- **快速模式**：直接调用专用 model ID，并使用 workspace 域名：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

## 限制和注意事项

- **TPM 预留**
  - 付费周期按**自然日**计算（00:00–24:00），非 24 小时滚动，购买时间影响实际有效时长（例如 16:00 购买 1 天预留，仅剩约 8 小时）；
  - 缩容/退订产生违约金（已用部分按 1.5 倍系数结算），退订后专属 model code 立即失效；
  - 服务到期后 14 小时内资源将被彻底删除，不可恢复。

- **快速模式**
  - 当前为 preview 阶段，模型 ID、性能指标与接口行为可能调整，不建议用于核心生产链路；
  - 不支持所有标准 OpenAI 参数（如 `temperature` 行为可能与标准版不同），请以实测为准；
  - 排队机制仅缓解瞬时超载，长期高负载仍需通过扩容或切换至 TPM 预留保障稳定性。

- > **注意**：快速模式文档未说明是否支持缓存命中折扣，而 TPM 预留文档明确列出 `glm-5.2` 支持 25% 缓存折扣。若业务高度依赖缓存，应优先验证快速模式的实际缓存效果，或选用 TPM 预留方案。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


