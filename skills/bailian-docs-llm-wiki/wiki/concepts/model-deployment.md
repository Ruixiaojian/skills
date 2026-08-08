# 模型部署

模型部署是百炼平台将训练完成或预置的大模型转化为可稳定、可计量、可调用的在线推理服务的核心能力。它通过资源隔离、容量保障与标准化接口，使模型具备生产级可用性，支持高并发、低延迟或低成本验证等多样化业务场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **面向预置模型的即开即用服务**：直接选择千问（Qwen3/Qwen2.5）、GLM-4.7/5.2、DeepSeek-v3/v4、Kimi-K2.5、CosyVoice 等官方预置模型，无需训练，一键部署为专属 API 服务，适用于快速接入、A/B 测试或基准验证。

- **面向 LoRA 微调模型的轻量交付**：仅支持已成功导入的 LoRA 微调模型（不支持全参微调），通过 `model_name` 引用其唯一 ID（如 `qwen3-8b-ft-202511132025-0260`），实现定制能力的快速上线。这是当前唯一支持 [Token](token.md) 计费模式的部署类型。

- **面向全参微调/第三方模型的灵活托管**：通过 `model production` 能力链路，将 SFT/CPT/DPO/RL 等训练产出的模型（含 `model_id`）或符合 ONNX/Triton 格式的自定义模型，以 `instance_type`（如 `gpu-a10-2`）指定硬件规格进行部署，适用于需强算力控制或异构模型集成的场景。

- **面向性能敏感型业务的加速增强**：可叠加使用「TPM 预留」（保障确定性吞吐）或「快速模式」（提升单请求 TPS），二者均生成专属 `model` 标识，与部署实例解耦——即：先部署模型，再为其配置容量或加速策略，实现“能力交付”与“性能保障”的分层治理。

> ⚠️ 注意：  
> - 所有部署均需指定地域（华北2 北京为 API 必选；控制台额外支持新加坡）；  
> - PTU/MU/Lora 三种计费模式互斥且创建后不可变更；  
> - 部署状态为 `RUNNING` 后方可调用，首次调用存在短暂预热期，建议客户端实现指数退避重试。

## 关键参数和配置

| 参数 | 适用模式 | 说明 | 实用提示 |
|------|----------|------|----------|
| `model_name` | 全模式 | 必填。预置模型代码（如 `qwen3.8-max`）或 LoRA 模型 ID；全参模型需传 `model_id`（格式 `org-id/model-name`） | 控制台实时列表为准；API 调用前请确认模型已在目标业务空间授权 |
| `plan` | 全模式 | 必填。取值 `ptu` / `mu` / `lora`，决定计费与调度逻辑 | `lora` 模式下 `capacity` 字段必须传但实际无效，勿误配 |
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置吞吐量（单位：TPM），决定保底服务能力 | 输入/输出 TPM 可独立设置；超出时默认自动溢出至按量计费，可在控制台关闭该策略 |
| `deploy_spec` / `capacity` | MU | `deploy_spec` 如 `"MU1 x 8"`；`capacity` 为副本数（如 `2`） | MU 支持 PD 分离（降低首 token 延迟），需显式指定并确认基础模型兼容性 |
| `enable_thinking` | MU | 布尔值，启用思考模式（返回 `reasoning_content` 字段） | 仅部分模型支持，调用前请查阅模型文档或试用 `model_info` 接口 |
| `max_context_length` / `rpm_limit` / `tpm_limit` | MU | 最长上下文长度、每分钟请求数、每分钟 token 数限制 | 运行时不可修改，需在创建时合理预估并设置 |
| `instance_type` | [model production](../api/model-production.md) 部署 | GPU 规格（如 `gpu-a10-2`），决定推理实例硬件 | 当前仅支持 GPU 实例；CPU 部署暂未开放 |
| `cached_tokens`（响应字段） | PTU/TPM 预留 | API 返回中 `usage.prompt_tokens_details.cached_tokens` 表示缓存命中 token 数 | 用于监控缓存效率，结合 `provisioned_tokens` 计算实际 PTU 消耗折扣 |

## 面向开发者，简洁实用

- ✅ **首选 API 自动化**：使用 `POST /api/v1/deployments` 创建部署，比控制台更易集成 CI/CD；状态轮询 `GET /api/v1/deployments/{id}` 直至 `status: "RUNNING"`。
- ✅ **调用即标准 [OpenAI 兼容接口](openai-compatible-interface.md)**：所有部署实例均支持 `POST /v1/chat/completions`，只需替换 `model` 参数为部署生成的 `model_name` 或专属 code（如 `qwen38max-tpm-abc123`）。
- ✅ **监控看板直达**：部署后立即生效 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)，重点关注 `PTU Utilization`、`Cached Tokens Trend` 和 `429 Rate`。
- ❌ **避免常见错误**：  
  - 不要对 LoRA 模型使用 `plan: "ptu"` 或 `plan: "mu"`；  
  - 不要在 MU 模式下传 `ptu_capacity`；  
  - 不要尝试修改运行中部署的 `max_batch_size` 或 `rpm_limit`（不支持）；  
  - 不要复用已失效的 OSS LoRA 模型 ID（文件变更后需重新导入）。

部署不是终点，而是模型价值落地的第一步。请始终以业务 SLA 为锚点：高确定性选 PTU，高性能定制选 MU，低成本验证选 LoRA，再按需叠加 TPM 预留或 Fast Mode 加速。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)


