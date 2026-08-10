# model deployment 1

百炼平台提供三种模型部署方式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 使用量计费，分别面向高并发低延迟、资源独占可定制、以及效果验证与轻量调用等典型场景。所有部署均生成独立推理服务端点，支持通过 API 或 SDK 调用，且计费方式在创建后不可变更。部署前需确认模型兼容性、权限配置及地域限制（如 API 方式当前仅支持华北2北京）[模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持部分预置模型（如 `qwen3.8-max`、`deepseek-v4-flash`、`glm-5.2`）及所有 LoRA 调优后模型；支持长输入（最高 1M token）与前缀缓存，适用于稳定高负载生产环境 [预置吞吐长输入与缓存 (raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：支持全部预置模型与所有 LoRA 调优模型（含千问、GLM、DeepSeek、Kimi、CosyVoice 等），支持 PD 分离计算模式、思考/非思考模式切换、自定义上下文长度与限流策略；不支持全参微调模型导入 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **按 [Token](../concepts/token.md) 计费**：**仅支持经过 LoRA 高效训练后的自定义模型**（如 `qwen3-8b-ft-*`），不支持原始预置模型直接部署；适用于效果验证与低频调用场景。

> **注意**：文档1称“部分预置模型与所有调优后模型”支持 PTU，但文档4的 API 示例明确使用 `qwen-flash-2025-07-28`（预置模型）进行 PTU 部署，且文档1表格中列出了大量预置模型的 PTU 定价，说明“部分预置模型”实为“绝大多数主流预置模型”。该表述易引发歧义，应以控制台可选列表为准。

## 关键参数

| 部署方式 | 必填参数 | 可选/条件参数 | 说明 |
|----------|----------|----------------|------|
| **PTU** | `plan: "ptu"`，`ptu_capacity.input_tpm`，`ptu_capacity.output_tpm` | `name`（服务名） | 吞吐能力固定，不可调整推理参数（如 `temperature`、`top_p`）；溢出策略（自动溢出/仅使用 PTU）在控制台设置，API 不暴露 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。 |
| **MU** | `plan: "mu"`，`deploy_spec`（如 `"MU1"`），`capacity`（副本数） | `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`、`deploy_template` | 性能指标完全可定制；`deploy_spec` 决定算力规格，`capacity` 控制并发副本；PD 分离模式需在 `deploy_spec` 中显式指定（如 `"MU1 x 16"`）。 |
| **[Token](../concepts/token.md) 计费** | `plan: "lora"`，`model_name`（LoRA 模型 ID），`capacity: 1`（占位必填） | `name` | `capacity` 参数无效，扩缩容必须通过控制台人工申请；仅适用于 LoRA 模型，且 `model_name` 必须是已成功导入并状态为“创建成功”的模型 ID。 |

## 使用方式

- **控制台部署**：登录百炼控制台 → 进入「模型部署」→ 「创建部署」，选择模型、部署方式、地域及对应参数（如 PTU 的 TPM 数值、MU 的规格与副本数），提交即可。部署状态可在列表页实时查看。
- **API 部署**：使用 `POST /api/v1/deployments` 接口，需携带有效 `Authorization` 头（Bearer + API Key）。示例见文档4，**注意该方式仅支持华北2（北京）地域** [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **LoRA 模型导入前提**：必须先完成 OSS 授权（主账号一键授权或子账号需 RAM 权限）、为目标 Bucket 添加 `bailian-datahub-access=read` 标签，并将符合约束的 `adapter_model.safetensors`、`adapter_config.json`、`config.json` 文件置于 OSS 子目录中 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **计费锁定**：部署创建后计费方式不可更改，需下线重部署才能切换。
- **地域限制**：API 部署仅支持华北2（北京），其他地域请使用控制台。
- **模型约束**：
  - MU 和 Token 计费方式**仅支持 LoRA 模型**，全参微调模型不可导入或部署。
  - LoRA 导入有严格校验：`rank` 必须为 8/16/32/64；词汇表与 `chat_template` 必须与基础模型一致；视觉语言模型必须冻结 VIT（`adapter_model.safetensors` 中不得含 `visual.` 开头参数）。
- **PTU 特殊行为**：
  - 输入超过模型上限（如千问 128K、DeepSeek 64K）时，自动转为按量计费，响应头含 `x-dashscope-ptu-overflow:true`。
  - 长输入按阶梯系数折算 TPM 消耗，缓存命中部分按折扣系数（如 glm-5.1 为 0.2）计算，可能导致利用率 >100% 属正常现象。
- **权限要求**：API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


