# model deployment 1

百炼平台的 `model deployment 1` 是面向生产级推理服务的模型部署能力，支持将预置模型或 LoRA 调优后的自定义模型，以资源隔离、性能可预期的方式部署为专属 API 服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发稳态、高性能定制化及低成本验证等典型场景。部署后服务具备独立 endpoint、完整监控与 API 级扩缩容能力。

## 支持的模型与功能

- **预置模型**：千问（Qwen）、DeepSeek、GLM、千问VL、千问 Omni、CosyVoice 等系列的多个版本均支持 PTU 和 MU 部署；[Token](../concepts/token.md) 用量计费仅限部分经 LoRA 调优后的千问与千问VL基础模型（如 `qwen3-8b`、`qwen3-vl-8b-instruct`），详见[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型**：仅支持从 OSS 导入的 LoRA 模型，需严格满足 rank（8/16/32/64）、词汇表一致性、chat_template 未修改、视觉模型 VIT 冻结等约束；全参微调模型暂不支持导入 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算模式（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度及 RPM/TPM 限流；
  - 所有部署均支持自动续费、API 级状态查询与删除，并可通过[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看实时利用率、`cached_tokens` 和 `provisioned_tokens` 等关键指标。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持模型单元部署，但文档 3 明确限定“仅支持导入 LoRA 模型”，且文档 4 的 API 示例中 `plan: "mu"` 仅用于预置模型（如 `qwen-plus-2025-12-01`）或已成功导入的 LoRA 模型。实际部署时，**未导入的调优模型无法直接以 MU 方式部署**——必须先完成[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)流程。

## 关键参数

| 参数 | 适用模式 | 说明 | 来源依据 |
|------|----------|------|----------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置输入/输出每分钟 Token 数（TPM），决定基础吞吐保障能力；长输入场景下按阶梯系数折算实际消耗 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) | |
| `deploy_spec` + `capacity` | MU | `deploy_spec` 指定模型单元规格（如 `MU1`），`capacity` 指定副本数；二者共同决定总算力与并发能力 | 文档 4 |
| `enable_thinking` | MU（部分模型） | 控制是否启用思考模式；影响输出单价与生成行为，需与模型类型匹配（如 `qwen-plus-2025-12-01` 支持） | 文档 4 |
| `max_context_length` | MU（部分模型） | 设置最长上下文长度，覆盖模型原生限制（如千问3.5-Plus 默认 128K，可设为 10000） | 文档 4 |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值，防止突发流量冲击底层资源 | 文档 4 |
| `plan: "lora"` | Token 用量 | 此值标识按 Token 计费模式；`capacity` 字段虽必填但无效，扩缩容须通过控制台人工申请 | 文档 4 |

## 使用方式

1. **控制台操作**：登录[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费模式、地域（当前仅华北2北京与新加坡可用），填写对应参数（如 PTU 的 TPM 值、MU 的规格与副本数），提交创建。
2. **API 调用**（推荐自动化集成）：
   - 使用 `curl` 或 DashScope SDK 发起 `POST /api/v1/deployments` 请求；
   - 必须配置有效的 `DASHSCOPE_API_KEY` 且归属业务空间已授权目标模型部署权限；
   - PTU 示例需传 `plan: "ptu"` 与 `ptu_capacity` 对象；MU 示例需传 `plan: "mu"`、`deploy_spec`、`capacity` 及可选 `enable_thinking` 等字段；Token 用量模式传 `plan: "lora"`；
   - 创建后通过 `GET /api/v1/deployments/{deployed_model}` 查询 `status`，待变为 `RUNNING` 后即可调用；
   - 推理时使用 `model` 参数指定部署服务 ID（即 `deployed_model`），而非基础模型名。
3. **模型导入前置**：若部署自定义 LoRA 模型，须先完成 OSS 授权、准备合规文件（`adapter_model.safetensors`、`adapter_config.json`、`config.json`）、在[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)页导入，再于部署页选择该模型 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **地域限制**：API 文档明确标注“仅适用于华北2（北京）地域”，新加坡地域部署需通过控制台操作，API 调用暂未开放跨地域支持 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **计费刚性**：PTU/MU 部署创建后立即开始计费，即使未发起任何请求；计费方式创建后不可更改，切换需先下线再重建。
- **溢出策略风险**：PTU 模式下，若选择「自动溢出」，超出额度的请求将无缝转为按量付费，可能产生意外费用；建议结合[预置吞吐额度计算器](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)合理规划 TPM。
- **LoRA 模型约束**：导入的 LoRA 模型不支持增量训练；OSS 源文件变更会导致模型状态变为「已失效」，需重新导入；删除模型仅移除百炼记录，不影响 OSS 源文件 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **权限依赖**：API 部署失败常见原因为业务空间未授权模型部署权限或账号无空间操作权，需在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中显式开启 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


