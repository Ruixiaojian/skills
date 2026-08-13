# model deployment 1

`model deployment 1` 是百炼平台面向生产环境的模型服务化核心能力，提供三种主流部署模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费。其中 PTU 模式专为高并发、低延迟、流量可预估的场景设计，支持长输入处理与前缀缓存优化；MU 模式提供资源独占与性能自定义能力；[Token](../concepts/token.md) 用量模式适用于效果验证与轻量级调用。所有模式均通过统一 API 接口调用，支持 OpenAI/Anthropic/DashScope 多协议兼容。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持 `qwen3.7-plus-2026-05-26`、`deepseek-v4-pro`、`glm-5.1` 等主流模型，具备长输入（最高 256K token）与前缀缓存能力，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **模型单元（MU）**：支持全部调优后 LoRA 模型及部分预置大模型（如 `qwen3.6-35b-a3b`、`glm-5.1`、`deepseek-v4-flash`），支持 PD 分离计算、思考/非思考模式切换、RPM/TPM 限流等高级配置。  
- **[Token](../concepts/token.md) 用量计费**：仅支持经 LoRA 调优后的模型（如 `qwen3-8b-ft-*`），不支持全参微调模型；该模式下模型必须已通过[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)流程成功导入并状态为“创建成功”。  
- **[多模态](../concepts/multimodal.md)与语音模型**：千问 VL 系列（如 `qwen3-vl-plus-2025-09-23`）、CosyVoice 等专用模型仅支持 MU 部署模式。

> **注意**：文档 2 中 `glm-5.1` 的输入长度上限标注为 64K，但文档 1 明确其支持 200K token；文档 2 表格数据存在滞后，应以文档 1 的[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)为准。

## 关键参数

| 部署模式 | 必填参数 | 说明 | 示例值 |
|----------|----------|------|--------|
| PTU | `"plan": "ptu"`, `"ptu_capacity": { "input_tpm": N, "output_tpm": M }` | `input_tpm`/`output_tpm` 单位为 **每分钟 token 数（TPM）**，需结合阶梯系数与缓存折扣预估，推荐使用控制台内置计算器 | `"input_tpm": 10000`, `"output_tpm": 1000` |
| MU | `"plan": "mu"`, `"deploy_spec": "MUx"`, `"capacity": N` | `deploy_spec` 指定算力规格（如 `MU1`, `MU3`），`capacity` 为副本数；支持 `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` 等扩展字段 | `"deploy_spec": "MU1"`, `"capacity": 4` |
| Token 用量 | `"plan": "lora"`, `"capacity": 1` | `capacity` 参数无效但**必须填写**（固定填 `1`），扩缩容须通过控制台操作 | `"capacity": 1` |

- 所有模式均需指定 `model_name`（模型 ID，非显示名称），LoRA 模型 ID 可在[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)页面获取；预置模型 ID 见文档 2 的计费表格。
- PTU 模式不支持 `enable_thinking`、`rpm_limit` 等运行时参数，吞吐与延迟由平台预置。

## 使用方式

1. **控制台操作**：登录[百炼控制台 → 模型部署 → 创建部署](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，选择模型、计费模式及对应参数，提交即完成部署。PTU 用户应优先使用「预置吞吐额度计算器」评估输入/输出 KTPM 需求。  
2. **API 部署**：使用 `POST /api/v1/deployments` 接口，按上述关键参数构造 JSON 请求体，详见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
3. **调用推理**：部署成功（`status: RUNNING`）后，使用 `Generation.call(model='deployed_model_id', ...)` 或直接调用 `/v1/chat/completions` 等兼容接口。PTU 部署响应中必含 `service_tier: "ptu-standard"` 字段，用于确认计费路径。  
4. **监控验证**：通过[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看 `cached_tokens`、`provisioned_tokens` 及利用率曲线，验证缓存与阶梯系数生效情况。

## 限制和注意事项

- **PTU 溢出策略**：创建时必须选择「自动溢出至按量计费」（默认）或「仅使用 PTU 容量」。前者超限请求自动转为按量计费（响应头含 `x-dashscope-ptu-overflow:true`），后者直接返回 HTTP 429；两种策略均不影响服务可用性。  
- **长输入与缓存约束**：  
  - 输入超过模型硬上限（如千问 128K、DeepSeek 64K）时，无论 PTU 策略如何，均强制转为按量计费；  
  - 前缀缓存仅对重复且连续的输入前缀生效，`system` message 变更、请求间隔超时（默认 5 分钟）、token 数不足阈值均导致 `cached_tokens=0`。  
- **模型导入限制**：LoRA 模型导入仅支持 OSS 来源，且要求 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 与基础模型严格一致、视觉模型必须冻结 VIT；全参微调模型不可导入，详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **地域与权限**：API 部署当前仅支持华北2（北京）地域；调用方 API Key 所属业务空间必须已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


