# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优后的模型（如 LoRA）部署为资源独占、性能可保障的专属推理服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发低延迟、高性能可定制及低成本验证等典型场景。部署后可通过标准 API（OpenAI/DashScope 兼容）调用，所有模式均支持华北2（北京）地域。

## 支持的模型/功能

- **预置模型**：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek（v3/v3.2/v4）、GLM（5.x/4.7）、Kimi-K2.5、CosyVoice 等，具体支持列表以控制台实时可选为准 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型**：仅支持从 OSS 导入的 LoRA 微调模型，需满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等约束；全参微调模型暂不支持导入 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，通过阶梯系数与缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、推理模式选择（Instruct/Thinking）、最长上下文配置及 RPM/TPM 限流；
  - [Token](../concepts/token.md) 计费模式仅适用于经 SFT 训练的 LoRA 模型，且基础模型需在[支持列表](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)中明确标注。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 4 的 API 示例与说明明确要求“仅对下列基础模型完成 SFT 高效训练并得到自定义模型后”才支持，且文档 3 强调“当前版本仅支持导入 LoRA 模型”。三者一致指向 LoRA 是唯一支持的自定义模型类型，全参微调模型不可部署。文档 1 中“部分预置模型与所有调优后模型”支持 MU 模式，与文档 4 的 MU API 示例（`qwen-plus-2025-12-01`）及文档 3 的 LoRA 导入限制无矛盾。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束/示例 |
|----------|--------|------|-----------|
| **通用** | `name` | 服务名称 | 必填，≤50 字符 |
| **PTU 模式** | `plan: "ptu"`<br>`ptu_capacity.input_tpm`<br>`ptu_capacity.output_tpm` | 预置吞吐容量（每分钟 Token 数） | 输入/输出 TPM 需按模型规格购买，超出触发溢出策略 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| **MU 模式** | `plan: "mu"`<br>`deploy_spec`<br>`capacity`<br>`enable_thinking`<br>`max_context_length`<br>`rpm_limit`/`tpm_limit` | 模型单元规格、副本数、思考模式、上下文长度、限流阈值 | `deploy_spec` 如 `"MU1"`；`capacity` 为副本数；`max_context_length` 因模型而异（如 `qwen3-8b` 最高 10000） |
| **Token 计费** | `plan: "lora"`<br>`capacity` | LoRA 部署标识 | `capacity` 参数必须填写但无效，扩缩容需走控制台申请 |

## 使用方式

1. **控制台部署**：前往 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型与计费方式，配置参数后提交。部署状态变为 `运行中` 即成功 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
2. **API 部署**：使用 DashScope API 发起 HTTP 请求，需提前配置 `DASHSCOPE_API_KEY` 环境变量。示例：
   - PTU：`curl ... --data '{"name":"my_qwen","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":10000,"output_tpm":1000}}'`
   - MU：`curl ... --data '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","capacity":4,"enable_thinking":true}'`
   - Token：`curl ... --data '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","capacity":1,"name":"qwen3-8b-ft"}'`  
   （详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）
3. **调用与监控**：部署成功后，使用 `Generation.call(model='deployed_model_id', ...)` SDK 或直接调用 `/v1/chat/completions` 接口；额度消耗与缓存命中率等指标通过 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域，控制台部署需确认所选地域可用性 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限要求**：API 调用需确保 API Key 所属业务空间已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`；子账号需主账号授予 `ram:CreateServiceLinkedRole` 权限方可完成 OSS 授权 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **OSS 约束**：LoRA 导入要求 Bucket 已添加 `bailian-datahub-access=read` 标签，且模型文件存放于子目录（非根目录）；存储类型不支持归档/冷归档 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费与生命周期**：部署创建即开始计费，下线后停止计费；PTU 预付费订单无法提前终止，MU 预付费退订按日单价 1.2 倍计费；Token 计费模式下，单次调用 Token 用量可从 API 响应 `usage` 字段获取 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **性能差异**：百炼推理引擎默认参数（如 `temperature=1.0`, `top_p=1.0`）可能与本地 vLLM/SGLang 不同，需显式设置参数对齐效果 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


