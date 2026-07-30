# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优后的模型（如 LoRA）部署为资源独占、性能可保障的专属推理服务。该能力提供三种核心计费与资源调度模式：**预置吞吐（PTU）**、**模型单元（MU）** 和 **按 [Token](../concepts/token.md) 使用量计费**，分别适用于高并发低延迟场景、定制化性能需求场景及效果验证与轻量试用场景。部署后服务通过标准 API 接入，支持 OpenAI、Anthropic 等兼容协议。

## 支持的模型与功能

- **支持模型类型**：
  - **预置吞吐（PTU）**：支持部分预置模型（如 `qwen3.7-plus-2026-05-26`、`deepseek-v4-flash`、`glm-5.1`）及所有已完成 LoRA 调优的模型（需满足[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)中关于 rank、词汇表、chat_template 和 VIT 冻结的约束）。
  - **模型单元（MU）**：支持全部预置模型与所有调优后模型（含 LoRA），且明确支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
  - **按 [Token](../concepts/token.md) 计费**：**仅限经 SFT 高效训练完成的 LoRA 模型**，不支持全参微调模型；基础模型范围见文档 1 中“按模型 Token 使用量”表格，且必须已通过[模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console)流程生成 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

- **关键功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
  - MU 模式支持自定义推理模式（`Instruct` / `Thinking`）、最长上下文长度、RPM/TPM 限流及部署副本数配置。
  - 所有部署均支持自动续费（PTU/MU），但按 Token 计费为纯随用随付。

> **注意**：文档 1 中“按 Token 使用量”章节称“仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费”，而文档 4 的 API 示例中却直接使用 `plan: "lora"` 部署了 `qwen3-8b-ft-202511132025-0260`（一个典型 LoRA 模型 ID），且未提及需额外开通或满足特殊条件。此处存在表述模糊——实际限制应以控制台可选模型为准，API 层面若传入不支持 Token 计费的模型 ID 将返回错误，而非静默降级。

## 关键参数

| 参数 | 适用模式 | 说明 | 来源依据 |
|------|----------|------|----------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置输入/输出 TPM（每分钟 Token 数）额度，决定服务吞吐基线 | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `deploy_spec`（如 `"MU1"`） | MU | 模型单元规格，决定算力与性能基线；不同规格对应不同小时单价 | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `enable_thinking` | MU | 布尔值，启用思考模式（影响输出单价与推理行为） | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `max_context_length` | MU | 设置最长上下文长度（部分模型支持），单位 token | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值，防止突发流量冲击 | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) |
| `capacity` | MU & Token | MU 模式下表示部署副本数；Token 模式下为必填但无效字段 | [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

- **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型、指定计费方式及对应参数（如 PTU 容量或 MU 规格），确认后提交。部署状态变为 `运行中` 即成功 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **API 部署**：使用 `POST /api/v1/deployments` 接口，按 `plan` 字段区分模式：
  - PTU：`"plan": "ptu"` + `ptu_capacity` 对象；
  - MU：`"plan": "mu"` + `deploy_spec`, `capacity` 等字段；
  - Token：`"plan": "lora"`（注意：此值易引发误解，实际代表“LoRA 模型按 Token 计费”，非部署类型标识） [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **模型导入前置**：LoRA 模型需先通过 OSS 导入流程完成注册，包括 OSS 授权、Bucket 标签设置、模型文件校验（`adapter_model.safetensors`、`adapter_config.json`、`config.json` 缺一不可），且 rank 必须为 8/16/32/64，VIT 必须冻结 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **计费约束**：
  - PTU 预付费订单无法提前终止，首月退订按日单价 1.2 倍计费；后付费欠费后保留资源 24 小时，超时将释放 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
  - MU 模式下，“模型单元-后付费”资源先买到先得，购买失败全额退款；PD 分离模式需显式选择对应规格（如 `MU1 x 16`）。
  - Token 计费模式不支持扩缩容，如需调整须在控制台重新申请。

- **技术限制**：
  - PTU 模式下，输入超过模型上限（如千问 128K、DeepSeek 64K）或超出预置 TPM 时，按溢出策略处理：`自动溢出` 切换至按量付费（响应头含 `x-dashscope-ptu-overflow:true`），`仅使用 PTU 容量` 返回 429 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
  - MU 模式支持的最长上下文、推理模式等配置项因模型而异，需以控制台下拉选项或 API 文档为准；`Instruct/Thinking` 类型模型可在部署时动态选择模式 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
  - 所有部署服务地域固定为华北2（北京），API 调用必须指向该地域 endpoint [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

- **权限与运维**：
  - API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
  - 导入的 LoRA 模型不支持增量训练，OSS 源文件变更会导致状态变为“已失效”，需重新导入 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


