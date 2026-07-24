# model deployment 1

`model deployment 1` 是百炼平台面向生产级推理服务的核心能力，提供三种正交的部署范式：预置吞吐（PTU）、模型单元（MU）和 [Token](../concepts/token.md) 用量计费。开发者可根据业务对吞吐稳定性、性能可调性或成本敏感度的要求，选择最适合的部署方式。所有模式均支持平台预置模型与用户调优模型（如 LoRA），并统一通过标准 API 接入。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、低延迟且流量可预估的场景，当前支持 `qwen3.7-plus-2026-05-26`、`deepseek-v4-pro`、`glm-5.1` 等模型，具备长输入（最高 256K token）与前缀缓存能力 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：支持全量微调与 LoRA 模型，提供完全自定义的推理性能（TPS、延迟、上下文长度、思考模式等），适用于需要资源隔离、PD 分离计算或长时任务的场景，如 `qwen3-32b`、`deepseek-v3.2`、`qwen3-vl-32b-instruct` 等 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **[Token](../concepts/token.md) 用量计费**：仅支持经 LoRA 高效微调后的模型（如 `qwen3-8b-ft-*`），按实际输入/输出 token 计费，适合效果验证与低负载场景；该模式不支持自定义性能参数 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **模型导入**：支持从 OSS 导入符合规范的 LoRA 模型（`adapter_model.safetensors` + `adapter_config.json`），要求 rank ∈ {8,16,32,64}、词汇表与 chat_template 与基础模型严格一致，且 VL 模型必须冻结 VIT [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 4 中表格显示 `glm-5.1` 最长输入为 64K，但文档 1 明确其支持 200K token 输入。以 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) 为准，该模型实际上限为 200K。

## 关键参数

| 参数 | 适用模式 | 说明 | 来源依据 |
|------|----------|------|----------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置的每分钟输入/输出 token 容量（单位：KTPM），决定保底吞吐与计费基准 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `deploy_spec`（如 `MU1`, `MU2 x 8`） | MU | 指定模型单元规格，直接绑定算力与性能上限 | [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `enable_thinking` | MU | 控制是否启用思考模式（影响输出单价与首 token 延迟） | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `max_context_length` | MU | 设置最长上下文长度（部分模型支持，如 `qwen-plus-2025-12-01`） | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值，防止突发流量冲击 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `capacity` | [Token](../concepts/token.md) 用量 | 必填但无效字段，扩缩容需人工审核 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

1. **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费方式及对应参数，提交即可。PTU 模式需使用「预置吞吐额度计算器」评估容量需求 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
2. **API 部署**：通过 `POST /api/v1/deployments` 调用，按 `plan` 字段区分模式：
   - `plan: "ptu"` → 提供 `ptu_capacity`
   - `plan: "mu"` → 提供 `deploy_spec`, `enable_thinking` 等
   - `plan: "lora"` → 提供 `capacity`（占位）[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
3. **模型导入后部署**：先通过 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 将 LoRA 模型导入「我的模型」，再在部署界面选择该模型 ID 即可。

## 限制和注意事项

- **计费不可变**：部署创建后无法更改计费方式，切换需先下线再重建 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **溢出策略**：PTU 模式下，超出预置额度时默认自动溢出至按量计费（响应头含 `x-dashscope-ptu-overflow:true`），也可选「仅使用 PTU 容量」返回 429；单次请求超模型 token 上限（如千问 128K）同样触发溢出 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **LoRA 导入硬约束**：仅支持 LoRA，不支持全参微调；`rank` 必须为 8/16/32/64；VL 模型必须冻结 VIT（`adapter_model.safetensors` 中不得含 `visual` 相关权重） [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **地域限制**：API 部署目前仅支持华北2（北京）地域 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限隔离**：API Key 所属业务空间必须已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)


