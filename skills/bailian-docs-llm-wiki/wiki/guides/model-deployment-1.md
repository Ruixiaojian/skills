# model deployment 1

百炼平台提供三种模型部署方式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 使用量计费，分别面向高并发低延迟、资源独占可定制、以及效果验证与轻量调用等不同场景。部署后获得独立推理服务端点，支持 API 直接调用，适用于生产环境或私有模型上线。所有部署均需在指定地域（如华北2）完成，且计费方式创建后不可变更。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持部分预置模型（如 `qwen3.8-max`、`deepseek-v4-flash`、`glm-5.2`）及所有 LoRA 调优后模型；支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数与缓存折扣优化额度消耗 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **模型单元（MU）**：支持全部预置模型与 LoRA 调优模型（含千问、DeepSeek、GLM、千问VL、CosyVoice 等），并支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟；支持 Instruct/Thinking 推理模式选择及自定义 RPM/TPM 限流、最长上下文长度等参数 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **按 [Token](../concepts/token.md) 使用量**：仅支持经 SFT 高效训练后的 LoRA 模型（非全参微调），且基础模型须在[支持清单](../../raw/model-user-guide/model-deployment-1/model-import.md)中明确列出（如 `qwen3-8b`、`qwen2.5-7b-instruct` 等）；不支持视觉语言模型（千问VL）的 Token 计费 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 4 的 API 示例与文档 1 的计费表格均明确要求“SFT 高效训练”，且文档 2 的[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)强调仅支持 LoRA 导入（不支持全参微调）。因此，“Token 计费仅适用于 LoRA 模型”为准确表述，文档 1 中“部分”一词易引发歧义，应以实际支持清单为准。

## 关键参数

| 部署方式 | 必填参数 | 可选/条件参数 | 说明 |
|----------|----------|----------------|------|
| PTU | `plan: "ptu"`，`ptu_capacity.input_tpm`，`ptu_capacity.output_tpm` | `overflow_strategy`（`auto` 或 `ptu_only`，默认 `auto`） | 输入/输出 TPM 单位为每分钟 token 数；溢出策略决定超限行为（自动转按量 or 返回 429） |
| MU | `plan: "mu"`，`deploy_spec`（如 `"MU1"`），`capacity`（副本数） | `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`、`deployment_template` | `deploy_spec` 决定算力规格；`capacity` 表示部署副本数；PD 分离模式需在控制台或 API 中显式启用 |
| Token 计费 | `plan: "lora"`，`model_name`（LoRA 模型 ID） | `capacity`（必须填写但无效） | `capacity` 字段无实际作用，扩缩容需通过控制台人工申请 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

所有部署均需指定 `name`（服务名称）与 `model_name`（模型标识符）。其中 `model_name` 为模型 ID（非显示名称），LoRA 模型 ID 可在[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)页面查看 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

- **控制台部署**：登录百炼控制台 → 进入「模型部署」→ 选择模型 → 设置计费方式与参数 → 提交。PTU 和 MU 支持自助扩缩容，Token 计费需提交人工审核 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **API 部署**：使用 `POST /api/v1/deployments` 接口，携带 `Authorization` 头（含 API Key）与 JSON 请求体。华北2（北京）地域为当前唯一支持地域 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **模型导入前置**：LoRA 模型需先通过 OSS 导入流程上传至百炼，要求 `adapter_model.safetensors`、`adapter_config.json`、`config.json` 三文件齐全，且 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 冻结 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

部署成功后状态为 `RUNNING`，可通过 `GET /api/v1/deployments/{deployed_model}` 查询；推理调用时，`model` 参数应传入部署服务名（即 `name` 字段值），而非原始模型名。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京），其他地域需使用控制台或等待后续开放 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **计费约束**：
  - PTU 预付费订单无法提前终止，首月退订按日单价 1.2 倍计费；后付费欠费后保留服务 24 小时，超时将释放资源 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
  - MU 模型单元后付费采用“先买到先得”机制，购买失败全额退款；PD 分离模式需额外支付更高单价 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **模型约束**：
  - Token 计费仅支持 LoRA 模型，且基础模型必须在导入时所列清单内；全参微调模型不可导入，亦不支持任何部署方式 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。
  - OSS 导入模型不支持增量训练，源文件变更会导致状态变为“已失效”，需重新导入 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **性能与监控**：
  - PTU 部署中，长输入导致的利用率 >100% 属正常现象（因阶梯系数折算），不代表异常 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
  - 所有部署均可通过[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看 `cached_tokens`、`provisioned_tokens` 等字段，验证缓存与额度消耗 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


