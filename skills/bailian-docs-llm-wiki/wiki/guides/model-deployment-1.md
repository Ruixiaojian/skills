# model deployment 1

百炼平台的 Model Deployment 1 是面向生产环境的模型服务化能力，支持将预置模型或调优后[模型部署](../concepts/model-deployment.md)为资源独占、性能可保障的专属推理服务。该能力提供三种计费与调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发低延迟、灵活可控的大规模推理及低成本效果验证等典型场景。部署后服务通过统一 API 接入，支持监控、扩缩容与生命周期管理。

## 支持的模型/功能

- **预置模型**：覆盖千问（Qwen）、DeepSeek、GLM、千问VL、千问Omni、CosyVoice 等系列，详见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 中的计费表格。
- **自定义模型**：仅支持 LoRA 微调后的模型导入与部署；全参微调模型暂不支持导入，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，按阶梯系数与缓存折扣折算额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度及服务限流（RPM/TPM）；
  - 所有模式均支持自动续费，PTU 和 MU 支持自助扩缩容，[Token](../concepts/token.md) 计费模式需人工审核扩容。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 3 明确指出 `plan: "lora"` 仅适用于已调优模型，且文档 2 强调“仅支持导入 LoRA 模型”，三者一致指向 LoRA 是 Token 计费的必要前提；而文档 1 表格中 Token 计费栏下“基础模型”列实际列出的是千问3.5-27B等基座模型——此为表述矛盾。**正确逻辑是：仅对完成 LoRA 微调并成功导入的模型，才可选择 Token 计费方式**，基座模型本身不可直接按 Token 部署。

## 关键参数

| 参数 | 适用模式 | 说明 | 约束 |
|------|----------|------|------|
| `plan` | 全部 | 计费模式标识：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 用量） | 必填 |
| `ptu_capacity` | PTU | `{ "input_tpm": N, "output_tpm": M }`，单位为 TPM（每分钟 Token 数） | `input_tpm` ≥ 1000，`output_tpm` ≥ 100 |
| `deploy_spec` / `capacity` | MU | `deploy_spec` 指定规格（如 `"MU1"`），`capacity` 指定副本数 | `capacity` ≥ 1，`deploy_spec` 必须与模型兼容（见文档 1 表格） |
| `enable_thinking` | MU | `true` 启用思考模式，`false` 为非思考模式 | 仅部分模型支持（如 `qwen-plus-2025-12-01`） |
| `max_context_length` | MU | 最长上下文长度（token 数） | 不得超过模型原生上限（如千问3.7-Max 为 256K） |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值 | 必须 ≥ 1 |
| `name` | 全部 | 部署服务唯一名称 | ≤ 50 字符，全局唯一 |

## 使用方式

- **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，配置参数后提交。首次部署前需完成 [OSS 授权](../../raw/model-user-guide/model-deployment-1/model-import.md)（若导入 LoRA 模型）。
- **API 部署**：使用 DashScope API 发起 HTTP 请求，示例见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。关键步骤包括设置 `Authorization` 头、指定 `model_name`（模型 ID）、`plan` 及对应参数结构体。
- **状态查询与调用**：部署后状态为 `RUNNING` 即可调用；使用 `Generation.call(model='deployed_model_id', ...)`（SDK）或直接请求 `/v1/chat/completions`（兼容 OpenAI 格式）发起推理。
- **扩缩容**：PTU 和 MU 模式支持控制台或 API 自助调整（如修改 `ptu_capacity` 或 `capacity`）；Token 计费模式扩容需提交工单审核。

## 限制和注意事项

- **权限约束**：API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误，详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **模型兼容性**：LoRA 导入严格校验 `rank`（仅支持 8/16/32/64）、词汇表一致性、`chat_template` 未修改、视觉模型 VIT 冻结等，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费与生命周期**：
  - 所有模式部署成功即开始计费，即使未调用；
  - PTU 预付费订单无法提前终止，到期后延后 2 小时停服，保留资源 14 小时后释放；
  - MU 后付费资源“先买到先得”，购买失败全额退款；
  - Token 计费模式下，单次调用 Token 数不足 1 也按 1 计费。
- **长输入与缓存**：PTU 模式下，输入超 32K token 触发阶梯系数（如 glm-5.1 在 [32K,200K] 区间输入系数为 1.33），缓存命中部分按折扣率（如 0.2）折算；可通过响应头 `x-dashscope-ptu-overflow:true` 或 `service_tier: "ptu-standard"` 字段判断计费路径，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)


