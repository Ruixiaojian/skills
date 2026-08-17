# model deployment 1

模型部署是百炼平台为预置模型及调优后模型提供的资源专享型推理服务，支持高并发、低延迟等生产级性能需求。通过三种计费模式（预置吞吐/PTU、模型单元/MU、[Token](../concepts/token.md)用量），开发者可按业务场景灵活选择资源保障级别与成本结构。部署后服务具备独立 endpoint、专属算力和完整生命周期管理能力。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于流量稳定、需确定性性能的场景，支持千问3.8-Max、qwen3.7-plus-2026-05-26、glm-5.2、deepseek-v4-pro 等主流大模型；部分模型支持长输入（最高 1M token）与前缀缓存折扣，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：适用于需自定义性能指标、独占资源或长时任务的场景，支持文本生成（如 qwen3.6-35b-a3b）、多模态（qwen3-vl-235b-a22b-thinking）、语音合成（cosyvoice-v3-flash）及 Omni 模型；支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **[Token](../concepts/token.md)用量**：仅支持经 LoRA 调优后的模型（如 qwen3-8b-ft-*），不支持全参微调模型；该模式下模型必须通过 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 流程上传至平台，且基础模型须在导入页可选清单内（如千问3-8B、千问3-VL-8B-Instruct 等）。

> **注意**：文档1中称“Token用量计费支持部分经过 LoRA 调优后的模型”，而文档4的 API 示例中明确使用 `"plan": "lora"` 部署调优模型，但文档3强调“当前版本仅支持导入 LoRA 模型，全参微调模型不可导入”，且未提及全参模型可走 Token 计费。因此，**Token用量计费实际仅限 LoRA 模型，文档1中“部分预置模型与所有调优后模型”在 Token 计费栏属表述不严谨，应以文档3和文档4为准**。

## 关键参数

| 计费模式 | 必填参数 | 可选/条件参数 | 说明 |
|----------|-----------|----------------|------|
| PTU | `plan: "ptu"`, `ptu_capacity: {input_tpm, output_tpm}` | `overflow_strategy: "auto" \| "ptu_only"`（默认 auto） | `input_tpm`/`output_tpm` 单位为 KTPM；溢出策略决定超额度行为（自动转按量 or 返回 429） |
| MU | `plan: "mu"`, `deploy_spec`, `capacity` | `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit`, `template` | `deploy_spec` 如 `"MU1"`；`capacity` 表示副本数；`enable_thinking` 仅对支持思考模式的模型生效（如 qwen-plus-2025-12-01） |
| Token用量 | `plan: "lora"` | `capacity`（必须填写但无效） | `capacity` 字段无实际作用，扩缩容需通过控制台人工申请 |

所有部署均需指定 `model_name`（模型 ID），该 ID 可从控制台「我的模型」或调优任务产出页获取；API 调用地域限定为华北2（北京），详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

- **控制台操作**：登录百炼控制台 →「模型部署」→「创建部署」，选择模型、计费模式及对应配置（如 PTU 容量、MU 规格），提交即完成部署。
- **API 调用**：使用 DashScope SDK 或 HTTP 请求调用 `/api/v1/deployments` 接口。PTU 示例需传 `ptu_capacity` 对象；MU 示例需传 `deploy_spec` 和 `capacity`；Token用量示例需传 `"plan": "lora"` 并确保 `model_name` 为已导入 LoRA 模型 ID。
- **状态管理**：部署后状态为 `PENDING` → `RUNNING`；可通过 `GET /api/v1/deployments/{model_id}` 查询；服务运行中可调用 `DELETE /api/v1/deployments/{model_id}` 下线并停止计费。
- **推理调用**：使用 `Generation.call(model='deployed_model_id', ...)`，其中 `model` 参数必须为部署成功的专属服务 ID（非基础模型 ID）；首次调用前需确认 API Key 所属业务空间已授权该模型部署权限。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域；新加坡地域模型价格与规格见文档1表格，但 API 不支持跨地域部署。
- **模型兼容性**：
  - LoRA 导入严格校验：`rank` 必须为 8/16/32/64；词汇表与 `chat_template` 不得修改；视觉模型必须冻结 VIT（`adapter_model.safetensors` 中不得含 `visual.*` 参数）。
  - PTU 部署的长输入阶梯系数与缓存折扣因模型而异（如 glm-5.1 输入 >32K 时系数为 1.33），超出模型原生上限（如千问128K）将自动转为按量计费 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **计费与生命周期**：
  - 所有部署创建成功即开始计费，无论是否调用；预付费订单无法提前终止，后付费欠费后保留资源 24 小时。
  - MU 模式下 `capacity` 为副本数，扩容需调用 `PATCH /api/v1/deployments/{id}`；PTU 模式扩容仅能增减 `input_tpm`/`output_tpm`；Token用量模式不支持 API 扩容。
- **安全与权限**：API Key 所属业务空间必须显式授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`；子账号需主账号授予 `ram:CreateServiceLinkedRole` 权限方可完成 OSS 导入授权。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


