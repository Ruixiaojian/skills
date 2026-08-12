# model deployment 1

百炼平台提供三种模型部署方式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 使用量计费，分别面向高并发低延迟、性能可定制及成本敏感型场景。所有部署均生成独立、资源专享的推理服务端点，支持通过 API 或控制台完成创建、扩缩容与生命周期管理。部署前需确认模型兼容性、计费策略与权限配置。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持部分预置模型（如 `qwen3.7-flash-2026-07-15`、`glm-5.1`、`deepseek-v4-flash`）及所有 LoRA 调优后模型；支持长输入（最高 1M token，依模型而异）与前缀缓存，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：支持全部预置模型与所有调优后模型（含 LoRA 和全参微调），覆盖文本生成、多模态（千问VL）、语音合成（CosyVoice）及嵌入/重排序模型；支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟，并允许自定义推理模式（Instruct/Thinking）、最[长上下文](../concepts/long-context.md)长度、RPM/TPM 限流等参数。
- **按 [Token](../concepts/token.md) 使用量**：**仅支持经 LoRA 高效训练后的自定义模型**（非基础模型），且当前仅限部分基础模型（如 `qwen3-32b`、`qwen3-14b`）的 LoRA 微调版本；不支持全参微调模型或未调优的基础模型 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 4 明确要求“仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费”，且文档 3 强调“当前版本仅支持导入 LoRA 模型，全参微调模型不可导入”。因此，Token 计费实际**仅适用于 LoRA 微调模型**，文档 1 的表述存在歧义，应以文档 4 和文档 3 为准。

## 关键参数

| 部署方式 | 必填参数 | 可选/条件参数 | 说明 |
|----------|----------|----------------|------|
| PTU | `plan: "ptu"`、`ptu_capacity.input_tpm`、`ptu_capacity.output_tpm` | `overflow_strategy`（`auto` 或 `ptu_only`） | `input_tpm`/`output_tpm` 单位为 KTPM；溢出策略决定超限行为（自动转按量计费或返回 429） |
| MU | `plan: "mu"`、`deploy_spec`（如 `"MU1"`）、`capacity`（副本数） | `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`、`deployment_template` | `deploy_spec` 与 `capacity` 共同决定算力总量；`enable_thinking` 仅对支持思考模式的模型生效 |
| Token 计费 | `plan: "lora"`、`model_name`（必须为 LoRA 模型 ID） | `capacity`（必须填写但无效） | `capacity` 字段为占位符，扩缩容需通过控制台申请，API 不支持动态调整 |

所有部署均需指定 `name`（服务名称）和 `model_name`（模型 ID）。模型 ID 获取路径：控制台 → [模型调优](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_manager) → 任务产出 → 进入“我的模型”页面查看 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

- **控制台操作**：登录百炼控制台 → 模型部署 → 创建部署 → 选择地域、模型、计费方式及对应参数 → 提交。PTU 和 MU 支持自助扩缩容；Token 计费扩容需提交人工审核。
- **API 调用**：使用 DashScope API 发起 HTTP 请求，需配置有效的 `DASHSCOPE_API_KEY` 环境变量。示例见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。注意：API 调用前须确保业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误。
- **模型导入前提**：LoRA 模型需先通过 OSS 导入流程上传至百炼（需完成 OSS 服务关联角色授权、Bucket 标签配置及文件校验），导入成功后方可部署 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **地域限制**：API 部署文档明确限定仅支持华北2（北京）地域，其他地域需使用控制台或确认 API Endpoint 适配性。
- **计费约束**：
  - PTU 预付费订单无法提前终止，首月退订按日单价 1.2 倍计费；后付费欠费后保留服务 24 小时，超时将释放资源。
  - MU 后付费资源“先买到先得”，购买失败全额退款；预付费包月订单同样适用首月退订加价规则。
  - Token 计费无额度保障，性能受公共流量管控，不适用于高 SLA 场景。
- **模型约束**：
  - LoRA 导入严格校验：`rank` 必须为 8/16/32/64；词汇表与 `chat_template` 必须与基座模型一致；视觉语言模型必须冻结 VIT（禁止 `visual.*` 参数）。
  - PTU 部署中，单次输入超过模型上限（如千问 128K、DeepSeek 64K）将自动转为按量计费，响应头含 `x-dashscope-ptu-overflow:true`。
- **运维限制**：从 OSS 导入的模型不支持增量训练；删除部署服务仅移除百炼侧记录，不影响 OSS 源文件；状态为 `PENDING` 时即开始计费，务必确认后再提交。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


