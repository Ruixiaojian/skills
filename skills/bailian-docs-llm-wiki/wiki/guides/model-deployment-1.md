# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优后的模型部署为资源独占、性能可保障的专属推理服务。该能力提供三种计费与调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发低延迟、灵活可控的大规模推理及低成本验证等典型场景。部署后服务具备独立 endpoint，可通过 API 直接调用。

## 支持的模型/功能

- **预置模型**：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek 系列（v3/v4）、GLM 系列（5.x/4.7）、Kimi-K2.5、CosyVoice 等，详见 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 中的计费表格。
- **自定义模型**：仅支持 LoRA 微调后的模型导入与部署；全参微调模型暂不支持导入，详见 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯系数与缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度及 RPM/TPM 限流；
  - 所有模式均支持自动续费（预付费）与扩缩容（PTU/MU 可自助调整，[Token](../concepts/token.md) 模式需人工审核）。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 3 的 API 示例明确要求 `plan: "lora"` 且仅适用于已调优模型；而文档 1 的 Token 计费表格中仅列出基础模型（如 qwen3-8b），未体现 LoRA 模型代码。实际以 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) 的 `plan: "lora"` 为准——该模式专用于 LoRA 模型，且 `capacity` 参数无效，必须通过控制台申请扩缩容。

## 关键参数

| 参数 | 适用模式 | 说明 | 约束 |
|------|----------|------|------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置输入/输出每分钟 Token 数（TPM） | 必填；超出模型上限（如千问 128K）时自动溢出至按量计费 |
| `deploy_spec` / `capacity` | MU | 模型单元规格（如 `MU1`）与副本数 | `deploy_spec` 必填；`capacity` 表示副本数，影响并发能力 |
| `enable_thinking` | MU | 是否启用思考模式 | 仅部分模型支持；思考模式下输出单价更高（见文档 1 表格） |
| `max_context_length` | MU | 最长上下文长度 | 须 ≤ 模型原生上限；部分模型在 MU 模式下可配置 |
| `rpm_limit` / `tpm_limit` | MU | 每分钟请求数/Token 数限流 | 可选；仅 MU 模式支持 |
| `plan` | 全部 | 计费模式标识：`"ptu"` / `"mu"` / `"lora"` | 必填；`"lora"` 专用于 LoRA 模型，非通用 Token 计费 |

## 使用方式

- **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，按向导完成配置。LoRA 模型需先通过 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md) 导入至“我的模型”列表，再从中选择。
- **API 部署**：使用 DashScope API 发起 HTTP 请求，示例如下：
  - PTU 模式：`curl ... --data '{"name":"my_qwen_flash","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":10000,"output_tpm":1000}}'`
  - MU 模式：`curl ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","capacity":4,"enable_thinking":true}'`
  - LoRA 模式：`curl ... --data '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`
- **状态查询与调用**：部署后状态为 `RUNNING` 即可调用；推理时需确保 API Key 所属业务空间已授权该模型（详见 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) 的权限说明）。

## 限制和注意事项

- **模型约束**：
  - LoRA 导入严格校验：`rank` 必须为 8/16/32/64；词汇表与 `chat_template` 不得修改；视觉语言模型必须冻结 VIT（即 `adapter_model.safetensors` 中不可含 `visual.` 开头参数）。
  - PTU 模式不支持自定义性能参数（如 `max_context_length`），仅 MU 模式支持。
- **计费与生命周期**：
  - PTU/MU 预付费订单无法提前终止；欠费后服务保留 24 小时，超时则释放资源。
  - Token 计费模式仅支持 LoRA 模型，且一个月内不使用将自动释放。
- **长输入与缓存**：
  - PTU 长输入按阶梯系数折算 TPM（如 glm-5.1 在 32K–200K 区间输入系数为 1.33），详见 [预置吞吐长输入与缓存 (raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
  - 缓存命中通过响应字段 `cached_tokens` 和 `provisioned_tokens` 验证；利用率 >100% 属正常现象（因阶梯系数导致折算消耗超原始 token 数）。
- **权限与地域**：API 部署仅支持华北2（北京）地域；需确保业务空间对目标模型有部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)


