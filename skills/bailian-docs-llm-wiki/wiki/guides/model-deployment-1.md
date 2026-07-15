# model deployment 1

百炼平台提供三种模型部署方式：预置吞吐（PTU）、模型单元（MU）和按 Token 用量计费，分别面向高并发低延迟、资源隔离可定制、以及低成本验证等不同业务场景。所有部署均通过统一 API 接口或控制台完成，支持预置模型与 LoRA 微调模型，但全参微调模型暂不支持导入与部署。部署即计费，服务状态变更（如扩容、下线）需注意计费规则与权限约束。

## 支持的模型/功能

- **预置模型**：千问系列（Qwen3/2.5/Flash/Plus/Max/VL/Omni）、DeepSeek（v3/v3.2/v4-Pro/v4-Flash）、GLM（5.2/5.1/4.7）、MiniMax-M2.5、Kimi-K2.5、CosyVoice 等，详见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md) 中的计费表格。
- **自定义模型**：仅支持 LoRA 微调模型导入与部署，需满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、VL 模型 VIT 部分冻结等严格要求；全参微调模型明确不支持 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 256K token）与前缀缓存，自动应用阶梯系数与缓存折扣 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)；
  - MU 模式支持 PD 分离计算（降低首 Token 延迟）、推理模式选择（Instruct/Thinking）、最长上下文与服务限流配置；
  - Token 计费模式仅适用于经 SFT 训练后的 LoRA 模型，且仅限部分基础模型（如 qwen3-32b/qwen3-8b/qwen2.5-vl-7b 等）。

> **注意**：文档 1 中“支持模型”表格称“部分预置模型与所有调优后模型”支持模型单元计费，但文档 3 明确限定“仅支持导入 LoRA 模型”，且文档 4 的 API 示例中 `plan: "lora"` 实际对应 Token 计费（非 MU），三者存在术语混淆。实际支持情况以 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 的 LoRA 限制为准：**只有符合规范的 LoRA 模型才能部署，且 MU/PTU/TOKEN 三种计费方式均仅对 LoRA 模型开放**。

## 关键参数

| 参数 | 适用模式 | 说明 | 示例值 |
|------|----------|------|--------|
| `plan` | 全部 | 计费策略标识：`ptu` / `mu` / `lora`（注意：`lora` 此处指 Token 计费，非模型类型） | `"ptu"` |
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置吞吐额度（每分钟 Token 数），决定服务容量上限 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `capacity` | MU | 模型单元规格（如 `"MU1"`）与副本数，直接关联算力与并发能力 | `"MU1"`, `4` |
| `enable_thinking` | MU | 是否启用思考模式（影响输出单价与性能） | `true` |
| `max_context_length` | MU | 最长上下文长度（部分模型支持，单位 token） | `10000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值（每分钟请求数 / 每分钟 Token 数） | `500`, `1000` |

- PTU 模式不支持自定义 `max_context_length` 或限流，其吞吐与延迟由平台预置；
- Token 计费模式（`plan: "lora"`）的 `capacity` 参数无效，仅需填写占位值（如 `1`），扩缩容必须通过控制台申请 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

1. **控制台部署**：访问 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费方式及对应参数（如 PTU 容量或 MU 规格），提交创建。
2. **API 部署**（推荐自动化）：
   - PTU：`POST /api/v1/deployments`，携带 `plan: "ptu"` 与 `ptu_capacity` 对象；
   - MU：`POST /api/v1/deployments`，携带 `plan: "mu"`、`deploy_spec`、`capacity` 及可选 `enable_thinking` 等；
   - Token 计费：`POST /api/v1/deployments`，携带 `plan: "lora"` 与占位 `capacity`。
3. **状态查询与管理**：通过 `GET /api/v1/deployments/{deployed_model}` 获取状态（`RUNNING` 表示就绪），`DELETE /api/v1/deployments/{deployed_model}` 下线服务。
4. **推理调用**：使用 `model` 参数指定部署服务 ID（即 `deployed_model` 字段值），而非基础模型名，例如 `model='qwen3-8b-ft-202511132025-0260'`。

## 限制和注意事项

- **权限约束**：API 部署需确保 API Key 所属业务空间已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **计费刚性**：部署成功即开始计费，PTU/MU 无法中途切换计费方式，必须先下线再重建；PTU 预付费订单不可提前终止，首月退订按日单价 1.2 倍计费。
- **额度溢出**：PTU 模式下，超出购买 TPM 或输入超模型上限（如 Qwen 128K）时，请求自动降级为按量计费，响应头含 `x-dashscope-ptu-overflow:true`，`service_tier` 字段不返回或为 `default` [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **LoRA 导入限制**：OSS Bucket 必须添加 `bailian-datahub-access` 标签，且模型文件不得位于根目录；`adapter_model.safetensors` 中禁止出现 `visual` 相关权重参数 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **地域限制**：API 部署当前仅支持华北2（北京）地域 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


