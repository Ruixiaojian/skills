# model deployment 1

百炼平台的模型部署（model deployment 1）提供三种核心计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 使用量计费。开发者可根据业务对稳定性、延迟、成本敏感度及流量可预测性的要求，选择最适合的部署方式。所有模式均支持预置模型与 LoRA 微调模型，但具体支持范围、参数灵活性和功能边界存在显著差异。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、低延迟、流量可预估的生产场景，如银行智能客服、实时内容审核。支持部分预置模型（如 `qwen3.8-max`、`deepseek-v4-flash`）及部分 LoRA 调优模型。支持长输入（最高 1M token）与前缀缓存，额度消耗按阶梯系数和缓存折扣动态折算 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：适用于需独占资源、自定义性能指标（如 RPM/TPM 限流、最长上下文长度、推理模式）的场景，如医药分子筛选、自动驾驶仿真。支持全部预置模型与所有 LoRA 调优模型，且明确支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **按 [Token](../concepts/token.md) 使用量**：仅支持经 LoRA 高效训练后的自定义模型，用于效果验证或低并发、高性价比场景。不支持全参微调模型，且当前仅限部分基础模型（如 `qwen3-32b`、`qwen3-vl-8b-instruct`）的 LoRA 版本 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

> **注意**：文档 2 明确指出“当前版本仅支持导入 LoRA 模型，全参微调模型不可导入”，而文档 1 在“支持模型”一栏中将“部分经过 LoRA 调优后的模型”列为 Token 计费方式的支持范围，二者一致；但文档 1 表格中“按模型 Token 使用量”计费方式下“支持模型”列写为“部分经过 LoRA 调优后的模型”，与文档 2 的“所有调优后模型”存在表述矛盾。实际以文档 2 的严格限定为准——仅 LoRA 模型可导入并部署，Token 计费亦仅对其生效。

## 关键参数

| 计费方式 | 必填参数 | 可选/自定义参数 | 说明 |
|----------|----------|------------------|------|
| **PTU** | `plan: "ptu"`, `ptu_capacity: {input_tpm, output_tpm}` | `overflow_strategy` (`auto_overflow` 或 `ptu_only`) | 吞吐能力固定，不可调 RPM/TPM；溢出策略决定超限行为（转按量 or 429）[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。 |
| **MU** | `plan: "mu"`, `deploy_spec`, `capacity` | `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit`, `template` | `capacity` 表示副本数；`deploy_spec`（如 `MU1`）决定单副本算力；`enable_thinking` 控制是否启用思考模式 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。 |
| **Token** | `plan: "lora"` | `capacity`（必须填写但无效） | `capacity` 字段无实际作用，扩缩容必须通过控制台申请 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。 |

## 使用方式

- **控制台操作**：登录百炼控制台，在「模型部署」>「创建部署」页面选择模型、计费方式及对应参数，提交即完成部署。PTU 和 MU 方式支持自助扩缩容，Token 方式需提交工单申请。
- **API 调用**：使用 DashScope API 发起 `POST /api/v1/deployments` 请求。需确保 API Key 所属业务空间已获目标模型的部署权限，否则会返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **模型来源**：部署对象必须是已在「我的模型」列表中处于「创建成功」状态的模型。LoRA 模型需先通过 OSS 导入流程完成，该流程强制要求模型文件符合 rank、词汇表、chat_template 等约束，并冻结 VIT（针对 VL 模型） [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **地域限制**：API 文档明确声明“本文档仅适用于华北2（北京）地域”，其他地域（如新加坡）的 API 调用可能失败或返回非预期结果。
- **OSS 授权强依赖**：从 OSS 导入 LoRA 模型前，主账号或已获授权的子账号必须完成服务关联角色创建，并为目标 Bucket 添加 `bailian-datahub-access=read` 标签，否则无法选择 Bucket [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费与生命周期**：
  - PTU 预付费订单无法提前终止，到期后有 2 小时宽限期，之后资源保留 14 小时后释放；
  - MU 后付费资源“先买到先得”，购买失败全额退款；
  - 所有部署服务创建成功即开始计费，无论是否发起调用。
- **模型兼容性**：导入的 LoRA 模型必须与基础模型完全兼容（词汇表、chat_template 不可修改），视觉语言模型必须冻结 VIT；不满足条件的模型在导入校验阶段即失败，错误码为 `AvailableModelFileNotFound` [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)


