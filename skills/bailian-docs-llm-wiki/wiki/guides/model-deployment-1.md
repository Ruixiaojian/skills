# model deployment 1

百炼平台提供三种模型部署模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别面向高并发低延迟、资源隔离可定制、以及低成本验证等不同业务场景。所有部署均基于平台预置模型或用户通过 LoRA 微调后导入的自定义模型，支持 API 直接调用与控制台可视化管理。部署即计费，服务状态变更（如扩容、下线）需通过明确操作触发。

## 支持的模型与功能

- **预置模型**：千问（Qwen）、DeepSeek、GLM、千问VL、千问Omni、CosyVoice 等系列模型均支持 PTU 和 MU 部署；部分模型（如 `qwen3.5-27b`）仅支持 [Token](../concepts/token.md) 计费，且限于 LoRA 调优后模型 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型**：仅支持 LoRA 微调模型导入与部署，全参微调模型暂不支持 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。导入前需满足 rank（8/16/32/64）、词汇表一致性、chat_template 未修改、视觉模型 VIT 冻结等硬性约束。
- **核心能力**：
  - PTU 模式支持长输入（最高 1M token，如 `qwen3.8-max`）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗 [预置吞吐长输入与缓存 (raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、推理模式选择（Instruct/Thinking）、RPM/TPM 限流及最长上下文配置；
  - Token 计费模式仅适用于 LoRA 微调模型，且当前仅限北京地域部分基础模型（如 `qwen3-32b`、`qwen3-vl-8b-instruct`）。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持 MU 部署，但文档 4 的 API 示例与文档 3 的导入约束共同表明——**MU 部署实际要求模型必须为 LoRA 类型且已成功导入**；文档 1 中“所有调优后模型”的表述易引发歧义，应以实际支持的 LoRA 导入模型为准。

## 关键参数

| 部署模式 | 必填参数 | 可选/条件参数 | 说明 |
|----------|-----------|----------------|------|
| **PTU** | `plan: "ptu"`<br>`ptu_capacity.input_tpm`<br>`ptu_capacity.output_tpm` | `overflow_strategy`（`auto` 或 `ptu_only`，默认 `auto`） | `input_tpm`/`output_tpm` 单位为 KTPM；溢出策略决定超限行为（自动转按量计费 or 返回 429） |
| **MU** | `plan: "mu"`<br>`deploy_spec`（如 `"MU1"`）<br>`capacity`（副本数） | `enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` | `deploy_spec` 必须从控制台或文档 1 表格中选取（如 `MU1 x 8`）；`capacity` 为整数，表示部署副本数量 |
| **Token** | `plan: "lora"`<br>`model_name`（LoRA 模型 ID） | `capacity`（必须填写但无效） | `capacity` 字段无实际作用，扩缩容需通过控制台人工申请 |

## 使用方式

- **控制台部署**：登录百炼控制台 →「模型部署」→「创建部署」，选择模型、计费模式及对应参数（如 PTU 容量、MU 规格），提交后服务进入 `PENDING` 状态，约数分钟至数十分钟变为 `RUNNING`。
- **API 部署**：使用 DashScope SDK 或 HTTP `POST /api/v1/deployments`，需提前配置 `DASHSCOPE_API_KEY` 并确保其归属业务空间已授权目标模型 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。示例：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "my_qwen_flash",
      "model_name": "qwen-flash-2025-07-28",
      "plan": "ptu",
      "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
    }'
  ```
- **调用与监控**：部署成功后，使用 `model_name`（非 `deployed_model` ID）调用 `/v1/chat/completions` 等接口；额度消耗、缓存命中率等指标可通过「模型监控」页面查看，API 响应中 `usage.prompt_tokens_details.cached_tokens` 和 `usage.prompt_tokens_details.provisioned_tokens` 字段用于实时验证 [预置吞吐长输入与缓存 (raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 限制和注意事项

- **地域限制**：API 部署目前仅支持华北2（北京）地域；新加坡地域模型价格与规格详见文档 1 的分区域表格，但 API 调用暂不支持。
- **计费与生命周期**：
  - 所有部署创建成功即开始计费，无论是否发起调用；
  - PTU 预付费订单不可提前终止，到期后延后 2 小时停服，资源保留 14 小时后释放；
  - MU 后付费资源“先买到先得”，购买失败全额退款；预付费包月订单首月退订按日单价 1.2 倍计费；
  - Token 计费模式下，单次调用最小计费单位为 1 token。
- **模型约束**：
  - LoRA 导入模型不支持增量训练，源文件变更将导致状态变为“已失效”，需重新导入；
  - PTU 模式下，输入超过模型上限（如千问 128K、DeepSeek 64K）或超出购买 TPM 时，按溢出策略处理（`auto` 则转按量计费并返回 `x-dashscope-ptu-overflow:true` 头；`ptu_only` 则返回 429）；
  - MU 模式下，`enable_thinking` 仅对支持思考模式的模型生效（如 `qwen-plus-2025-12-01`），调用时需显式传参。
- **权限与调试**：
  - API 部署失败常见原因为业务空间未授权模型（报错 `Workspace xxx does not have deployment privilege for model xxxx`）或账号无空间操作权限；
  - 本地 vLLM 推理效果与百炼不一致时，需显式设置 `temperature=1.0`、`top_p=1.0`、`presence_penalty=0` 等参数对齐默认值 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


