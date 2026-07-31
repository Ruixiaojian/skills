# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优/导入的模型部署为独立、资源隔离的推理服务。该能力提供三种正交计费与资源模式：**预置吞吐（PTU）** 保障确定性性能，**模型单元（MU）** 提供可定制的专属算力，以及 **[Token](../concepts/token.md) 按量计费（LoRA）** 用于低成本效果验证。所有模式均通过统一 API 接口调用，适用于高并发低延迟、长时独占计算或轻量级验证等差异化场景。

## 支持的模型/功能

- **预置模型**：全部千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek-v3/v4、GLM-4.7/5.x、Kimi-K2.5 等主流开源模型，详见[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)中的价格表。
- **调优后模型**：支持 LoRA 微调模型（含本地训练后从 OSS 导入的模型），但**全参微调模型暂不支持导入或部署**；导入流程详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯系数和缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度及 RPM/TPM 限流；
  - LoRA 模式仅支持已通过 SFT 训练并完成模型导入的 LoRA 模型，用于效果验证。

> **注意**：文档 1 中“支持模型”表格称“部分预置模型与所有调优后模型”支持模型单元计费，但文档 4 明确限定“当前版本仅支持导入 LoRA 模型，全参微调模型不可导入”，且文档 3 的 API 示例中 LoRA 部署仅接受 `qwen3-8b-ft-*` 类模型 ID。因此，“所有调优后模型”实际指**所有已完成 LoRA 微调并成功导入的模型**，不包含全参微调模型。

## 关键参数

| 参数 | 适用模式 | 说明 | 来源约束 |
|------|----------|------|-----------|
| `plan` | 全部 | 必填，取值 `ptu` / `mu` / `lora`，决定计费与资源模型 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU | 对象，含 `input_tpm` 和 `output_tpm`（单位：token/分钟），必须按模型支持的阶梯边界配置 | [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| `deploy_spec`, `capacity` | MU | `deploy_spec` 指定规格（如 `MU1 x 8`），`capacity` 指副本数；二者共同决定总算力 | [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` | MU | 可选，控制推理行为与服务限流；仅部分模型支持 `enable_thinking` | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `model_name` | 全部 | 必填，为模型 ID（非显示名称），预置模型 ID 查[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)，LoRA 模型 ID 在[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)页面获取 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

1. **控制台部署**：前往[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费方式及对应参数（如 PTU 容量或 MU 规格），提交即可。部署状态变为 `RUNNING` 后即可调用。
2. **API 部署**（推荐自动化）：
   - PTU 模式：`POST /api/v1/deployments`，传入 `plan: "ptu"` 和 `ptu_capacity` 对象；
   - MU 模式：传入 `plan: "mu"`、`deploy_spec`、`capacity` 及可选参数；
   - LoRA 模式：传入 `plan: "lora"`，`capacity` 字段必须填写但实际无效。
   - 详细请求示例见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
3. **调用方式**：部署成功后，使用 `model_name`（即 `deployed_model` ID）调用 `/v1/chat/completions` 等标准接口，无需额外鉴权变更。SDK 调用示例见文档 3。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域，控制台部署需确认所选地域是否开通服务。
- **权限要求**：API 调用需确保 API Key 所属业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误；权限配置路径见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **OSS 导入约束**：从 OSS 导入 LoRA 模型时，Bucket 必须添加 `bailian-datahub-access=read` 标签，且模型文件须存于子目录（非根目录）；`adapter_model.safetensors` 中不得含 `visual.*` 参数键（即 VIT 必须冻结），rank 必须为 8/16/32/64 之一。
- **计费生效时机**：模型部署创建成功（状态 `PENDING` 或 `RUNNING`）后立即开始计费，**即使未发起任何推理请求**。删除服务后计费立即停止。
- **溢出与降级**：PTU 模式下若启用「自动溢出」，超出额度的请求将无缝转为按量计费，并在响应 Header 中返回 `x-dashscope-ptu-overflow:true`；若选择「仅使用 PTU 容量」，则直接返回 HTTP 429 错误。此行为已在[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)中明确。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


