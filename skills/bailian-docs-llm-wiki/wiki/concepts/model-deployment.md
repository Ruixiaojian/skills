# 模型部署与服务化

模型部署与服务化，是指将训练完成或微调优化后的模型（包括预置模型、LoRA 适配器、全参微调模型等）封装为稳定、可扩展、生产就绪的 HTTP 推理服务的过程。该过程屏蔽底层基础设施复杂性，提供统一 API 接口、弹性资源调度与多维度计费模式，使开发者能专注业务逻辑集成，而非运维细节。

## 在百炼平台的不同场景中，这个概念如何使用

模型部署与服务化是百炼平台模型落地的核心枢纽，贯穿从“模型准备”到“线上调用”的全链路，在不同场景下呈现差异化能力：

- **面向预置模型快速上线**：直接选择千问（Qwen3/Qwen2.5）、GLM、DeepSeek、Kimi、CosyVoice 等预置模型，通过控制台或 API 一键部署为专属 endpoint，支持 PTU（预置吞吐）、MU（模型单元）或 Token 计费三种模式，5 分钟内即可获得高可用服务。

- **面向 LoRA 微调成果交付**：仅支持从 OSS 导入的 LoRA 模型（`adapter_model.safetensors` 格式），部署时必须指定 `"plan": "lora"`（语义等价于 Token 计费），不支持全参微调模型、QLoRA 或 Adapter 直接部署；视觉语言模型需满足 VIT 冻结约束（`visual.` 参数不得存在）。

- **面向全参微调模型生产发布**：通过 `model production` 流程完成 SFT/CPT/DPO 等训练后，获得唯一 `model_id`，再调用 `/v1/deployments` 创建部署，绑定 `instance_type`（如 `ecs.gn7i-c16g1.4xlarge`）和 `max_concurrency`，生成独立 `endpoint_url`，支持灰度发布与版本回滚。

- **面向高性能/低延迟场景增强**：结合 TPM 预留（保障确定性吞吐）或快速模式（`glm-5.2-fast-preview`，提升 TPS），部署时需切换专属 `model` code 或接入特定域名（如 `maas.aliyuncs.com`），二者不可叠加，且不参与彼此容量计算。

- **面向成本优化部署**：对已完成微调的自定义模型，可先执行**模型压缩**（INT8 量化），生成新模型 ID（如 `my-qwen-ft-int8mu8`），再以更小 MU 规格（如 `MU8` 替代 `MU1×2`）部署，显著降低小时成本（典型节省 50%+），但压缩后模型不可再微调或二次压缩。

> ✅ 关键共识：所有部署均通过标准 REST API 统一创建与管理，返回结构一致（含 `endpoint_id`、`endpoint_url`、`status`），调用方只需向 `endpoint_url/v1/chat/completions` 发送带 `Authorization` 的请求即可完成推理，无需感知底层模型格式或资源类型。

## 关键参数和配置

| 参数 | 说明 | 必填 | 典型取值与约束 |
|------|------|------|----------------|
| `plan` | 计费与资源模型标识 | 是 | `"ptu"`（预置吞吐）、`"mu"`（模型单元）、`"lora"`（LoRA 模型专属 Token 计费） |
| `model_name` / `model_id` | 部署目标模型标识 | 是 | 预置模型用 `qwen3-8b`；LoRA 用导入时指定的名称；全参微调模型用 `ft-qwen2-7b-20240510-123456` |
| `ptu_capacity` | PTU 模式专属吞吐额度 | `plan="ptu"` 时必填 | `{"input_tpm": 10000, "output_tpm": 1000}`（单位：token/分钟） |
| `deploy_spec` & `capacity` | MU 模式规格与副本数 | `plan="mu"` 时必填 | `"deploy_spec": "MU1"`, `"capacity": 4`（需查表确认模型支持的规格组合） |
| `instance_type` | 全参模型部署的实例规格 | `model_production` 场景必填 | `"ecs.gn7i-c16g1.4xlarge"`（GPU）、`"ecs.c7.large"`（CPU） |
| `enable_thinking` | 启用思考模式（Instruct/Thinking） | 可选 | `true`（仅部分模型如 `qwen-plus-2025-12-01` 支持） |
| `max_context_length` | 最长上下文长度 | `plan="mu"` 时可选 | 整数，≤ 模型原生上限（如 Qwen3 为 128000） |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | `plan="mu"` 时可选 | `{"rpm_limit": 500, "tpm_limit": 10000}`（硬性拦截） |

> ⚠️ 注意：  
> - `"plan": "lora"` 是历史字段名，实际代表 Token 计费，**仅 LoRA 模型可用**，API 中不可用于全参模型；  
> - TPM 预留与快速模式需使用专属 `model` code 或 `model_id`，**不可混用标准模型名**；  
> - 模型压缩后生成的新模型 ID，需作为 `model_id` 传入部署接口，与其他部署流程完全一致。

## 面向开发者，简洁实用

- ✅ **一句话启动**：`curl -X POST https://dashscope.aliyuncs.com/api/v1/deployments -H "Authorization: Bearer $DASHSCOPE_API_KEY" -d '{"name":"my-app","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":5000,"output_tpm":500}}'`  
- ✅ **部署即生效**：状态变为 `RUNNING` 后，立即可用；首次调用有预热延迟（<2s），建议客户端实现重试（指数退避）。  
- ✅ **统一调用方式**：所有部署服务均使用相同推理接口：`POST {endpoint_url}/v1/chat/completions`，请求体结构与 OpenAI 兼容。  
- ✅ **按需治理**：通过控制台或 `/v1/deployments/{id}` API 可随时启停、扩缩容（MU）、修改限流（MU）、或删除部署（释放资源）。  
- ✅ **安全可靠**：服务默认启用 HTTPS、IP 白名单（可配）、Token 鉴权，无须额外网关层。  

> 💡 提示：生产环境推荐优先使用 MU 模式（强隔离、可限流、支持思考模式）或 PTU 模式（稳态高并发）；验证/POC 场景可选用 LoRA + Token 计费，按量付费、零闲置成本。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)


