# 模型部署

模型部署是百炼平台将预置模型或 LoRA 微调后的自定义模型，转化为稳定、可扩展、生产就绪的在线推理服务的核心能力。它为业务提供确定性资源、可控延迟与灵活计费，是模型从训练/调优走向实际应用的关键环节。

## 在百炼平台的不同场景中，这个概念如何使用

- **面向标准业务上线**：直接部署百炼预置模型（如 `qwen3-vl-plus`、`deepseek-v4`、`glm-5.2`），无需训练，开箱即用，适用于快速验证、A/B 测试或通用能力集成。  
- **面向定制化场景**：部署通过百炼完成 LoRA 微调的模型（如 `ft-abc123`），继承领域知识与风格特征，支撑客服、金融问答、代码助手等垂直任务。  
- **面向高性能需求**：结合模型压缩（INT4 量化）后部署，显著降低 MU 成本；或叠加 TPM 预留（PTU 模式），保障高并发下的吞吐稳定性与首 token 延迟。  
- **面向多模态交互**：部署 `qwen3-vl-*` 等 VL 模型时，需选择支持图像输入的 MU 规格（如 `MU2 x 8`），并确保请求中携带 base64 编码图片及正确 content-type。  
- **不支持的场景**：全参微调模型、OSS 导入模型、第三方 ONNX/HF 模型（除非已通过百炼模型导入流程注册且状态为“可用”）、未完成训练的微调任务产出模型——均不可部署。

> ⚠️ 注意：所有部署操作均绑定 Region（如华北2），跨地域调用需重新部署；部署成功即开始计费，无论是否发起请求。

## 关键参数和配置

| 参数 | 所属模式 | 是否必填 | 说明 | 示例 |
|------|----------|-----------|------|------|
| `name` | 全部 | 是 | 服务唯一标识，用于 API 调用路径和控制台管理，3–32 字符，仅含小写字母、数字、短横线 | `"qa-bot-prod"` |
| `plan` | 全部 | 是 | 计费与资源模式：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（[Token](token.md) 按量） | `"mu"` |
| `model_name` | 全部 | 是 | 模型 ID：预置模型名（如 `"qwen-flash-2025-07-28"`）或微调模型 ID（如 `"ft-xyz789"`） | `"qwen3-8b-ft-20251113"` |
| `ptu_capacity.input_tpm` / `output_tpm` | `ptu` | 是 | 预置吞吐量（单位：token per minute），决定服务容量上限 | `{"input_tpm": 20000, "output_tpm": 2000}` |
| `deploy_spec` | `mu` | 是 | 模型单元规格，格式为 `MU{N}` 或 `MU{N} x {K}`（K=副本数），支持 PD 分离 | `"MU2 x 4"` |
| `enable_thinking` | `mu` | 否 | 是否启用思考模式（部分模型支持），默认 `false` | `true` |
| `capacity` | `mu` / `lora` | `mu`: 否（默认1）<br>`lora`: 是（占位，实际无效） | `mu` 模式下为部署副本数；`lora` 模式下必须填但不生效，扩缩容需人工操作 | `2` |
| `max_context_length` | `mu` / `ptu` | 否 | 自定义上下文长度（token），需模型本身支持 | `131072` |
| `rpm_limit` / `tpm_limit` | 全部 | 否 | 服务级限流阈值（RPM/TPM），防止突发流量冲击 | `{"rpm_limit": 100, "tpm_limit": 5000}` |

> ✅ 提示：`lora` 模式仅适用于 LoRA 微调模型，按实际 [Token](token.md) 使用量计费，无资源独占，适合低频、成本敏感型场景；`ptu` 和 `mu` 模式支持长上下文（最高 256K）、前缀缓存与 PD 分离，是生产环境首选。

## 面向开发者，简洁实用

- **一句话启动**：用 curl 或 SDK 调用 `/api/v1/deployments`，传入 `name`、`model_name`、`plan` 及对应模式参数，5 秒内返回部署 ID。  
- **调试建议**：首次部署后，先用 `curl -X POST https://<name>.api.bailian.aliyun.com/v1/chat/completions` 发起简单请求，验证 endpoint 可达性与鉴权。  
- **错误排查优先级**：  
  1. 检查 `model_name` 是否在 [支持列表](https://help.aliyun.com/zh/model-studio/model-deployment) 中且状态为“可用”；  
  2. 核对 `plan` 与参数组合是否合法（如 `ptu` 模式误填 `deploy_spec` 会返回 `422`）；  
  3. 查看控制台部署详情页的 `status` 与 `error_message` 字段，常见错误包括 `MODEL_NOT_FOUND`、`QUOTA_EXCEEDED`、`INVALID_PARAMETER`。  
- **最佳实践**：  
  - 高并发核心服务 → 选 `ptu` 模式 + 合理预估 TPM 并开启前缀缓存；  
  - 低延迟交互场景（如编程助手）→ 选 `mu` 模式 + `MU2 x N` + `enable_thinking: true`；  
  - 快速验证或 PoC → 选 `lora` 模式，零资源预留，按需付费；  
  - 成本敏感且已微调 → 先做模型压缩（INT4），再以 `mu` 模式部署，节省 40%~60% MU 成本。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)


