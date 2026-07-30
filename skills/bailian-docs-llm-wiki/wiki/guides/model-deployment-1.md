# model deployment 1

model deployment 1 是百炼平台面向生产环境的模型服务化能力，提供三种核心计费与资源隔离模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费。开发者可根据业务对吞吐稳定性、延迟敏感度、成本弹性及模型定制程度的要求，选择最适配的部署方式。所有模式均支持通过控制台或 API 快速创建、扩缩容与监控，且计费方式在创建后不可变更。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、低延迟、流量可预估的生产场景，支持长输入（最高 256K token）与前缀缓存优化额度消耗，当前支持 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等模型，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：适用于需资源独占、性能自定义（如 PD 分离、思考模式、最长上下文、RPM/TPM 限流）的私有化推理场景，支持全部千问系列、GLM、DeepSeek、千问VL 及 CosyVoice 等模型，覆盖 Instruct/Thinking 模式与[多模态](../concepts/multi-modal.md)任务。
- **按 [Token](../concepts/token.md) 用量计费**：仅限 LoRA 微调后的自定义模型（如 `qwen3-8b-ft-*`），适用于效果验证、低频调用或成本优先型实验场景，不支持预置吞吐或模型单元的性能配置能力。

> **注意**：文档 3 中“支持模型”表格将 `qwen3.7-plus-2026-05-26` 归类为 PTU 和 MU 均支持，但文档 1 明确其支持前缀缓存与长输入阶梯系数，而文档 4 的 API 示例中仅将其用于 MU 部署；实际以控制台实时可选列表为准，API 创建时若指定不支持的 `plan` 会返回 400 错误。

## 关键参数

| 参数名 | 适用模式 | 说明 | 来源依据 |
|--------|----------|------|----------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 输入/输出每分钟 [Token](../concepts/token.md) 数（KTPM），决定额度购买量，影响长输入阶梯系数应用范围 | [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| `deploy_spec` / `capacity` / `enable_thinking` / `max_context_length` | MU | 模型单元规格（如 `MU1`）、副本数、是否启用思考模式、最长上下文长度（部分模型支持） | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `plan: "lora"` | [Token](../concepts/token.md) 用量 | 仅用于 LoRA 微调模型，`capacity` 字段必须填写但无效，扩缩容需走控制台人工审核 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `rpm_limit` / `tpm_limit` | MU（可选） | 服务级请求/[Token](../concepts/token.md) 每分钟限流阈值，防止突发流量冲击 | [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |

## 使用方式

- **控制台操作**：前往[模型部署控制台](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，选择模型、计费方式及对应参数（如 PTU 容量、MU 规格、推理模式），提交即完成部署；状态变为 `RUNNING` 后即可调用。
- **API 调用**：使用 DashScope SDK 或 HTTP 请求 `POST /api/v1/deployments`，按 `plan` 字段区分模式：
  - PTU：传 `"plan": "ptu"` + `ptu_capacity` 对象；
  - MU：传 `"plan": "mu"` + `deploy_spec`, `capacity`, `enable_thinking` 等字段；
  - [Token](../concepts/token.md) 用量：传 `"plan": "lora"` + `model_name`（LoRA 模型 ID）。
  详细字段与示例见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **调用地址**：部署成功后，专属服务 ID（`deployed_model`）即为模型名称，直接用于 `Generation.call(model='xxx', ...)` 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。

## 限制和注意事项

- **计费不可变**：部署创建后无法切换计费方式，需下线重部署。
- **PTU 溢出策略**：创建时须明确选择「自动溢出」（转按量计费，响应头含 `x-dashscope-ptu-overflow:true`）或「仅使用 PTU 容量」（超限返回 429），后者可能导致服务中断。
- **长输入上限**：模型物理上限严格（如千问 128K、DeepSeek 64K、GLM-5.2 1M），超出即强制转为按量计费，不受 PTU 阶梯系数约束。
- **LoRA 导入约束**：仅支持从 OSS 导入符合 rank（8/16/32/64）、词汇表一致、chat_template 未修改、VIT 冻结等要求的 SafeTensors 格式模型，详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **地域限制**：API 部署仅支持华北2（北京）地域，其他地域需切换 endpoint 或使用控制台。
- **权限隔离**：API Key 必须归属拥有目标模型部署权限的业务空间，否则报 `Workspace xxx does not have deployment privilege` 错误。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)



