# model deployment 1

百炼平台的 `model deployment 1` 是面向生产级推理服务的模型部署能力，支持将预置模型或用户调优后的模型（如 LoRA）部署为资源独占、性能可预期的专属服务。该能力提供三种核心计费与调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发低延迟、高性能可定制及低成本验证等典型场景。部署后服务通过统一 API 接入，支持 OpenAI、Anthropic 等兼容协议。

## 支持的模型/功能

- **预置模型**：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek（v3/v4）、GLM（5.x/4.7）、Kimi-K2.5、CosyVoice 等主流模型均支持 PTU 和 MU 部署；部分模型（如 `qwen3.7-plus-2026-05-26`、`glm-5.1`）额外支持长输入（最高 256K token）与前缀缓存 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **自定义模型**：仅支持从 OSS 导入的 LoRA 微调模型，需满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等约束 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。全参微调模型暂不支持导入。
- **关键功能**：
  - PTU 模式支持阶梯容量系数（如 glm-5.1 超 32K 输入按 1.33 系数折算）和缓存折扣（命中部分按 20% 折算）；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、推理模式选择（Instruct/Thinking）及最长上下文配置；
  - 所有部署均支持自动续费、扩缩容（PTU/MU 可自助调整，[Token](../concepts/token.md) 计费需人工审核）。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持模型单元部署，但文档 3 明确限定“仅支持导入 LoRA 模型”，且文档 4 的 API 示例中 `plan: "lora"` 实际对应 Token 计费模式（非 MU）。此处以文档 3 和文档 4 为准：**模型单元（MU）仅支持预置模型及符合约束的 LoRA 模型；Token 计费（`plan: "lora"`）专用于已调优 LoRA 模型，与 MU 无关**。

## 关键参数

| 参数 | 说明 | 适用模式 | 示例值 |
|------|------|----------|--------|
| `plan` | 部署计费模式 | 全部 | `"ptu"`, `"mu"`, `"lora"` |
| `ptu_capacity` | PTU 额度（输入/输出 TPM） | PTU | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `capacity` | MU 规格与副本数 | MU | `"MU1"`, `4` |
| `enable_thinking` | 是否启用思考模式 | MU（部分模型） | `true` |
| `max_context_length` | 最长上下文长度 | MU（部分模型） | `10000` |
| `rpm_limit` / `tpm_limit` | 服务限流阈值 | MU | `500`, `1000` |

- PTU 模式下 `rpm_limit`/`tpm_limit` 等参数不可配置，吞吐由预置额度决定；
- Token 计费模式（`plan: "lora"`）中 `capacity` 参数必须填写但实际无效，扩缩容需通过控制台申请 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

1. **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，确认后提交。状态变为 `RUNNING` 即部署成功。
2. **API 部署**：使用 DashScope API 发起 HTTP 请求，需配置 `DASHSCOPE_API_KEY` 环境变量。示例：
   - PTU：`curl -X POST ... --data '{"name":"my_qwen","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{...}}'`
   - MU：`curl -X POST ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","enable_thinking":true}'`
   - Token 计费：`curl -X POST ... --data '{"model_name":"qwen3-8b-ft-xxx","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`
3. **调用与监控**：部署成功后，使用 `model_name`（即 `deployed_model` ID）调用推理 API；额度消耗、缓存命中率等指标可通过 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看。

## 限制和注意事项

- **权限要求**：API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **OSS 导入约束**：LoRA 模型导入前须完成 OSS 服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access=read` 标签；模型文件须包含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`，且 rank、词汇表、chat_template 必须与基础模型一致 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费与生命周期**：
  - PTU 预付费订单无法提前终止，到期后延后 2 小时停服，资源保留 14 小时后释放；
  - MU 后付费资源“先买到先得”，购买失败全额退款；
  - 所有部署服务创建成功即开始计费，即使未发起调用。
- **溢出行为**：PTU 模式下若超出额度，「自动溢出」策略将切换为按量付费（响应头含 `x-dashscope-ptu-overflow:true`），「仅使用 PTU 容量」则返回 429；单次输入超模型上限（如千问 128K）亦自动转为按量计费 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


