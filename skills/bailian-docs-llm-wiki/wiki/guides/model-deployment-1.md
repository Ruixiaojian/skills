# model deployment 1

百炼平台的 `model deployment 1` 是面向开发者的一站式模型部署能力，支持将自定义 LoRA 模型（仅限）导入后，通过 API 或控制台以多种计费模式（PTU、MU、LoRA）快速部署为专属推理服务。该能力与百炼模型中心深度集成，覆盖从 OSS 导入、参数配置、状态管理到监控调优的完整生命周期。

## 支持的模型与功能

- **支持的模型类型**：当前**仅支持 LoRA 微调模型**，不支持全参微调模型 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **基础模型范围**：覆盖千问3系列（如 `qwen3-8B`、`qwen3-VL-8B-Instruct`）、千问2.5系列（如 `qwen2.5-7B-Instruct`、`qwen2.5-VL-72B-Instruct`）等，详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)中“支持导入的基础模型”表格。  
- **核心功能**：
  - 长输入支持（部分模型最高 256K token），配合阶梯容量系数与前缀缓存折扣降低额度消耗；
  - 前缀缓存（Prefix Caching），命中时按模型特定折扣率（如 glm-5.1 为 0.2）折算输入 token 消耗；
  - 溢出策略可选：自动溢出至按量计费（默认）或严格限于 PTU 容量（超限返回 429）；
  - 多协议兼容响应字段（OpenAI Chat、Anthropic、DashScope），含 `cached_tokens` 和 `provisioned_tokens` 等关键监控指标 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

> **注意**：文档 2 中示例命令使用 `"plan": "lora"` 部署 LoRA 模型，但该 `plan` 值实际为历史遗留标识，**当前 API 已统一归入 `mu`（模型单元）计费模式下部署 LoRA 模型**；`"plan": "lora"` 不再是独立计费类型，且 `capacity` 参数在该场景下无效但必须填写。真实部署应使用 `plan: "mu"` 并指定 `deploy_spec`，具体请以 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) 中 MU 模式为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `model_name` | string | 是 | 自定义模型 ID（非显示名称），需从[我的模型](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_center)页面获取 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `plan` | string | 是 | 计费模式：`ptu`（预置吞吐）、`mu`（模型单元）。`lora` 为已弃用别名，实际等效于 `mu` | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | object | `plan=ptu` 时必填 | `{ "input_tpm": N, "output_tpm": M }`，单位 KTPM，决定预置吞吐能力 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `deploy_spec` | string | `plan=mu` 时必填 | 如 `"MU1"`，定义算力规格；不同规格支持不同 `max_context_length` 和 `enable_thinking` | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `max_context_length` | integer | 可选 | 最长上下文长度（token），仅部分模型在 MU 模式下支持，如 `qwen3-8b` 默认 32768，可设为 128000 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `enable_thinking` | boolean | 可选 | 是否启用思考模式（如 ReAct），仅部分模型支持 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

1. **准备模型**：将 LoRA 模型文件（`adapter_model.safetensors` + `adapter_config.json`）上传至已打标 `bailian-datahub-access:read` 的 OSS Bucket 子目录，并确保 rank 为 8/16/32/64、未修改 vocab/chat_template、VL 模型 VIT 部分已冻结 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
2. **导入模型**：在控制台「我的模型」→「导入模型」填写 Bucket、模型目录等信息，提交后状态变为 `创建成功` 即可部署。  
3. **部署服务**：调用 `/api/v1/deployments` 接口，根据计费模式选择参数组合：
   - PTU 模式：传 `plan: "ptu"` + `ptu_capacity`；
   - MU 模式：传 `plan: "mu"` + `deploy_spec` + `capacity`（副本数）等；
   - LoRA 模型必须使用 MU 模式，`plan: "lora"` 已废弃但向后兼容 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
4. **验证与调用**：轮询 `/api/v1/deployments/{deployed_model}` 直至 `status: "RUNNING"`，然后使用 `model` 参数为部署服务 ID（非原始 `model_name`）发起推理请求。  
5. **监控与扩缩容**：通过控制台「模型监控」查看 `cached_tokens`、`provisioned_tokens` 及利用率曲线；MU 模式支持动态调整 `capacity`，PTU 模式需通过扩容操作变更额度 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 限制和注意事项

- **OSS 访问限制**：百炼**不支持访问 Bucket 根目录下的文件**，模型必须置于子目录中；Bucket 存储类型不可为归档/冷归档/深度冷归档 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **LoRA 强制约束**：`rank` 必须为 {8,16,32,64} 之一且全层一致；禁止修改基础模型 vocab 或 chat_template；VL 模型必须冻结 VIT，`adapter_model.safetensors` 中不得含 `visual.*` 参数键 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **地域限制**：API 部署目前**仅支持华北2（北京）地域** [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
- **权限要求**：API Key 所属业务空间必须显式授权目标模型的「模型部署」权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
- **计费启动时机**：无论是否发起推理请求，**部署成功即开始计费**；删除服务后立即停止计费 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
- **长输入与缓存生效条件**：前缀缓存仅对重复输入前缀有效，若 system message 动态变化或请求间隔超缓存有效期（通常数分钟），`cached_tokens` 将为 0 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)


