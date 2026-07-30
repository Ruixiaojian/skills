# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化核心能力，提供三种正交部署模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费（LoRA）。三者在资源隔离性、性能确定性、成本结构与配置自由度上形成梯度覆盖，开发者可根据流量稳定性、延迟敏感度与预算约束选择最适方案。所有部署均通过统一 API 接口调用，支持 OpenAI/Anthropic/DashScope 多协议兼容。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持长输入（最高 256K token）与前缀缓存，适用于高并发、可预测负载场景。当前明确支持 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等模型，其长输入阶梯系数与缓存折扣率详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：支持全量微调与 LoRA 模型，提供独占算力、自定义推理模式（Instruct/Thinking）、PD 分离计算、服务限流（RPM/TPM）及最长上下文配置。支持千问3/2.5系列、GLM-5、DeepSeek-v4/v3、千问VL等数十种文本与[多模态](../concepts/multi-modal.md)模型，具体规格与单价见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **按 [Token](../concepts/token.md) 用量计费（LoRA）**：仅支持经百炼平台完成 SFT 高效训练的 LoRA 模型，不支持全参微调模型。该模式下模型必须通过[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)流程上传至平台，且基础模型需在控制台可选清单内（如 `qwen3-8b`、`qwen2.5-14b-instruct` 等）。

> **注意**：文档3中“按模型 [Token](../concepts/token.md) 使用量”表格列出的 `qwen3.5-27B 邀测中` 等条目为历史快照，实际支持列表以控制台实时下拉菜单为准；文档2明确指出“导入来源仅支持从 OSS 导入”，而文档4的 API 示例中 `plan: "lora"` 部署方式要求模型 ID 必须来自已成功导入的 LoRA 模型，二者逻辑一致，无矛盾。

## 关键参数

| 部署模式 | 必填参数 | 说明 |
|----------|----------|------|
| **PTU** | `plan: "ptu"` + `ptu_capacity: {input_tpm, output_tpm}` | `input_tpm`/`output_tpm` 单位为 KTPM（千 token/分钟），决定额度购买量；溢出策略（自动溢出/仅使用 PTU）在创建时选定，不可变更。 |
| **MU** | `plan: "mu"` + `deploy_spec` + `capacity` | `deploy_spec`（如 `"MU1"`）指定算力规格；`capacity` 为副本数；可选 `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit`。 |
| **LoRA（Token 计费）** | `plan: "lora"` + `model_name` + `capacity`（占位，值任意） | `model_name` 必须为已成功导入的 LoRA 模型 ID；`capacity` 字段必须存在但无实际作用，扩缩容需走控制台人工流程。 |

所有部署均需指定 `name`（服务名称）与 `model_name`（模型标识符）。`model_name` 来源分两类：预置模型直接使用文档3中的模型代码（如 `qwen-flash-2025-07-28`）；LoRA 模型则需先完成[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)，再从“我的模型”页面获取其唯一 ID。

## 使用方式

1. **控制台操作**：前往[模型部署控制台](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，按向导完成配置。PTU 模式需使用**预置吞吐额度计算器**估算输入/输出 KTPM；MU 模式可设置副本数、推理模式与限流；LoRA 模式仅需选择已导入模型。
2. **API 调用**：使用 DashScope API 创建部署。示例：
   - PTU：`curl ... --data '{"name":"my_qwen","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":10,"output_tpm":1}}'`
   - MU：`curl ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","capacity":4,"enable_thinking":true}'`
   - LoRA：`curl ... --data '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`
3. **状态查询与管理**：部署后通过 `GET /api/v1/deployments/{deployed_model}` 查询状态（`PENDING` → `RUNNING`），`DELETE /api/v1/deployments/{deployed_model}` 下线服务。详细接口规范见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 限制和注意事项

- **PTU 溢出行为**：选择「自动溢出」时，超出额度的请求将无缝转为按量计费，响应头含 `x-dashscope-ptu-overflow:true`；选择「仅使用 PTU 容量」时，超额请求直接返回 HTTP 429。两种策略均不影响服务可用性，但费用模型不同。
- **长输入与缓存**：单次输入超过模型上限（如千问128K、DeepSeek 64K）会强制转为按量计费；前缀缓存生效需满足严格条件（相同 System Message、token 前缀一致、间隔在有效期以内），`cached_tokens=0` 不一定代表配置错误，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)的 FAQ。
- **模型导入约束**：LoRA 模型导入必须满足 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 未修改、视觉模型 VIT 层冻结等硬性要求；OSS Bucket 必须添加 `bailian-datahub-access=read` 标签，且模型文件须置于子目录而非根目录。
- **计费与生命周期**：所有部署创建即开始计费；PTU 预付费订单不可退订；MU 后付费资源“先买到先得”，购买失败全额退款；LoRA 模式不支持 API 扩缩容，必须通过控制台提交申请。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


