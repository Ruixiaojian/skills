# model deployment 1

百炼平台的 Model Deployment 1 是面向生产环境的模型服务化能力，支持将预置模型或调优后的 LoRA 模型部署为资源独占、性能可保障的专属推理服务。该能力提供三种计费模式：预置吞吐（PTU）、模型单元（MU）和按 Token 用量计费，分别适配高并发低延迟、高性能定制化及成本敏感型场景。所有部署均通过统一 API 接口管理，支持自动化扩缩容与细粒度监控。

## 支持的模型/功能

- **预置模型**：覆盖千问（Qwen）、DeepSeek、GLM、Kimi、CosyVoice 等主流系列，包括文本生成、多模态（VL）、语音合成、Embedding 和 Rerank 等任务类型。具体支持列表详见 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型**：仅支持 LoRA 微调模型导入与部署，不支持全参微调（Full Fine-tuning）。基础模型需严格匹配平台支持列表，且必须满足 rank 值为 8/16/32/64、词汇表与 chat_template 未修改、VL 模型 VIT 部分冻结等约束 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯系数与缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算、推理模式（Instruct/Thinking）切换、最长上下文配置及 RPM/TPM 限流；
  - Token 计费模式仅适用于经 SFT 训练的特定基础模型（如 qwen3-8b、qwen2.5-7b-instruct 等），详见文档 1 的“按模型 Token 使用量”章节。

> **注意**：文档 1 中“支持模型”表格称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 4 的 API 示例中 `plan: "lora"` 实际对应 Token 计费模式，且文档 1 明确列出支持该模式的基础模型（如 `qwen3-8b`），而文档 4 示例中使用的 `qwen3-8b-ft-202511132025-0260` 是 LoRA 模型 ID。这表明 Token 计费实际要求模型基于指定基础模型训练，而非任意 LoRA 模型——此为关键约束，文档 1 表述易引发歧义，应以文档 4 的 API 要求和文档 1 的基础模型列表为准。

## 关键参数

| 参数 | 适用模式 | 说明 | 示例值 |
|------|----------|------|--------|
| `plan` | 所有 | 计费模式标识：`ptu`、`mu`、`lora`（Token 计费） | `"ptu"` |
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置吞吐容量（每分钟 Token 数） | `{ "input_tpm": 10000, "output_tpm": 1000 }` |
| `deploy_spec` / `capacity` | MU | 模型单元规格与数量（如 `MU1 x 8`） | `"MU1"`, `4` |
| `enable_thinking` | MU | 是否启用思考模式（影响计费单价与输出 Token 单价） | `true` |
| `max_context_length` | MU | 最长上下文长度（部分模型支持） | `10000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级请求/Token 速率限制 | `500`, `1000` |

## 使用方式

- **控制台部署**：访问 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，配置参数后提交。详细步骤见 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **API 部署**：使用 DashScope REST API，需提前配置 `DASHSCOPE_API_KEY` 环境变量。示例命令如下：
  - PTU 模式：`curl -X POST ... --data '{"name":"my_qwen_flash","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{...}}'`
  - MU 模式：`curl -X POST ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","enable_thinking":true,...}'`
  - Token 计费：`curl -X POST ... --data '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`
  完整 API 参考见 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **状态管理**：部署后通过 `GET /api/v1/deployments/{deployed_model}` 查询状态（`RUNNING` 表示就绪），通过 `DELETE /api/v1/deployments/{deployed_model}` 删除服务。

## 限制和注意事项

- **权限与授权**：API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限；首次从 OSS 导入模型需主账号或具备 `ram:CreateServiceLinkedRole` 权限的子账号完成 OSS 服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access` 标签 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费约束**：
  - PTU 模式：计费方式创建后不可更改；溢出策略（自动溢出/仅使用 PTU）决定超限行为（转按量计费或返回 429）；预付费订单无法提前终止，首月退订按日单价 1.2 倍计费。
  - MU 模式：模型单元规格购买后资源独占，后付费按小时计费，算力“先买到先得”；PD 分离模式需显式指定（如 `MU1 x 16`）。
  - Token 计费：仅对文档 1 明确列出的基础模型有效，且 `capacity` 参数在 API 中必须填写但实际无效。
- **技术限制**：
  - 输入长度上限因模型而异（千问 128K/256K，DeepSeek 64K/256K，GLM 1M），超限请求自动转为按量计费；
  - PTU 模式下利用率可能 >100%（因长输入阶梯系数），属正常现象；
  - 所有部署服务创建成功即开始计费，无论是否发起调用。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


