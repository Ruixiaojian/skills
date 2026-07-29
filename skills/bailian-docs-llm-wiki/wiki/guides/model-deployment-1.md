# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优/导入的 LoRA 模型部署为资源独占、性能可保障的专属推理服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适用于高并发低延迟、定制化性能隔离、以及低成本效果验证等典型场景。部署后可通过标准 API（OpenAI 兼容/DashScope）调用，所有模式均需通过控制台或 API 显式创建。

## 支持的模型与功能

- **预置模型**：覆盖千问（Qwen）全系列（如 `qwen3.7-plus-2026-05-26`、`qwen-flash-2025-07-28`）、DeepSeek（`deepseek-v4-flash`、`deepseek-v4-pro`）、GLM（`glm-5.1`、`glm-5.2`）、千问 VL（`qwen3-vl-plus-2025-09-23`）等，详见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 中的计费表格。
- **调优后模型**：支持全部通过百炼平台完成 SFT/LoRA 调优的模型，部署时需使用其模型 ID（如 `qwen3-8b-ft-202511132025-0260`）。
- **导入模型**：仅支持从阿里云 OSS 导入符合约束的 LoRA 模型，基础模型须在 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 所列清单内（如 `千问3-8B`、`千问3-VL-8B-Instruct`），且必须满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等要求。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯系数与缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算模式（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度及 RPM/TPM 限流；
  - [Token](../concepts/token.md) 计费模式仅支持部分 LoRA 调优模型，用于效果验证。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，而文档 4 明确指出“仅支持导入 LoRA 模型”，且文档 3 的 API 示例中 `plan: "lora"` 实际对应 Token 计费模式。三者一致指向 LoRA 模型是 Token 计费的必要前提，但文档 1 表格中“支持模型”列对 Token 计费的描述（“部分经过 LoRA 调优后的模型”）易引发歧义，应以实际 API 参数 `plan: "lora"` 和文档 4 的约束为准。

## 关键参数

| 参数名 | 适用模式 | 说明 | 示例值 |
|--------|----------|------|--------|
| `plan` | 所有模式 | 部署计费计划类型 | `"ptu"` / `"mu"` / `"lora"` |
| `ptu_capacity` | PTU | 预置吞吐容量，含 `input_tpm` 和 `output_tpm`（单位：token/分钟） | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `model_unit_spec` | MU | 模型单元规格，如 `"MU1 x 8"`、`"MU3 x 16"` | `"MU1 x 8"` |
| `enable_thinking` | MU | 是否启用思考模式（影响计费单价与输出行为） | `true` |
| `max_context_length` | MU | 最长上下文长度（需模型支持） | `10000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值 | `500`, `1000` |
| `capacity` | MU & Token | MU 模式下副本数；Token 模式下为占位参数（必须填，但无效） | `4`, `1` |

## 使用方式

- **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费方式及对应配置（如 PTU 容量、MU 规格、限流值等），提交即可。详细步骤见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **API 部署**：使用 DashScope API 发起 HTTP POST 请求。例如：
  - PTU 模式：`curl -X POST ... --data '{"name":"my_qwen_flash","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":10000,"output_tpm":1000}}'`
  - MU 模式：`curl -X POST ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","enable_thinking":true}'`
  - Token 模式：`curl -X POST ... --data '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`
  具体参数与响应格式详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **调用方式**：部署成功（状态为 `RUNNING`）后，使用 `model_name`（即部署服务名）调用 DashScope Generation API 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，确保 API Key 所属业务空间与部署空间一致。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域，见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) 前提条件。
- **权限要求**：API 调用需确保 API Key 所属业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误；主账号与子账号的 OSS 授权流程不同，子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费约束**：
  - PTU 模式：计费方式创建后不可更改；溢出策略（自动溢出/仅使用 PTU）决定超限行为（转按量计费或返回 429）；长输入超出模型上限（如千问 128K）仍自动转为按量计费。
  - MU 模式：模型单元-后付费资源“先买到先得”，购买失败全额退款；PD 分离模式需显式选择 `deploy_spec`（如 `MU1 x 16`）。
  - Token 模式：仅支持 LoRA 模型，且 `capacity` 参数无效，扩缩容需通过控制台申请。
- **模型约束**：
  - OSS 导入的 LoRA 模型不支持增量训练；
  - 导入模型文件必须包含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`，且 rank、词汇表、chat_template 必须与基础模型一致；
  - 视觉语言模型导入时，VIT 部分必须冻结（`safetensors` 中不能含 `visual.` 开头的权重键）。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


