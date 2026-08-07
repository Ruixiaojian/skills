# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优后的 LoRA [模型部署](../concepts/model-deployment.md)为资源独占、性能可保障的专属推理服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适用于高并发低延迟、高性能定制化及效果验证等不同场景。部署后可通过标准 API（OpenAI/DashScope 兼容）调用，所有模式均支持华北2（北京）和新加坡地域。

## 支持的模型与功能

- **预置模型**：千问（Qwen）全系列（含 Qwen3-Max/Plus/Flash/VL/Omni）、DeepSeek（v3/v4）、GLM（5.x）、Kimi-K2.5、CosyVoice 等，具体支持列表以控制台实时可选为准。  
- **自定义模型**：仅支持从 OSS 导入的 LoRA 微调模型，[必须满足 rank=8/16/32/64、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等约束](../../raw/model-user-guide/model-deployment-1/model-import.md)；全参微调模型暂不支持导入。  
- **核心功能**：
  - PTU 模式支持长输入（最高 200K token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、RPM/TPM 限流及最长上下文配置；
  - 所有部署均支持自动续费（PTU/MU 预付费）、扩缩容（自助增减吞吐或模型单元数量）及监控（[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)）。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持 PTU，但文档 3 明确限定“仅 LoRA 模型可导入”，且文档 4 的 API 示例中 `plan: "ptu"` 仅用于预置模型（如 `qwen-flash-2025-07-28`），而 LoRA [模型部署](../concepts/model-deployment.md)必须使用 `plan: "lora"`（见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。因此，**LoRA 模型不支持 PTU 部署，仅支持 `lora` 计费模式（即按 [Token](../concepts/token.md) 用量计费）**。

## 关键参数

| 参数 | 适用模式 | 说明 | 示例/约束 |
|------|----------|------|-----------|
| `plan` | 全部 | 计费模式标识 | `"ptu"`、`"mu"`、`"lora"` |
| `ptu_capacity` | PTU | 输入/输出 TPM 额度 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `model_unit_spec` | MU | 模型单元规格 | `"MU1"`、`"MU2 x 8"`（见文档 1 表格） |
| `enable_thinking` | MU | 是否启用思考模式（仅部分模型支持） | `true` / `false` |
| `max_context_length` | MU | 最长上下文长度（需模型支持） | `10000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值 | `500`, `1000` |
| `capacity` | LoRA | 必填但无效字段（仅占位） | `1`（文档 4 明确说明） |

## 使用方式

1. **控制台操作**：登录 [百炼控制台 → 模型部署](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费模式及对应参数，提交创建。  
2. **API 调用**（推荐自动化场景）：  
   - 使用 `curl` 或 SDK 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/deployments`；  
   - 必须配置有效的 `DASHSCOPE_API_KEY` 环境变量，并确保 API Key 所属业务空间已授权目标[模型部署](../concepts/model-deployment.md)权限（详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）；  
   - 部署成功后状态为 `"PENDING"`，变为 `"RUNNING"` 即可调用；  
   - 推理时 `model` 参数应填写部署服务 ID（非原始模型名），例如 `Generation.call(model='my_qwen_flash', ...)`。  
3. **模型导入前置**：LoRA 模型需先完成 [OSS 授权与文件校验](../../raw/model-user-guide/model-deployment-1/model-import.md)，再通过“我的模型”页面导入，方可作为 `model_name` 传入部署 API。

## 限制和注意事项

- **地域限制**：API 文档明确声明“仅适用于华北2（北京）地域”，新加坡地域部署需通过控制台操作（文档 1 中价格表分地域列出，但 API 未开放新加坡 endpoint）。  
- **计费生效时机**：所有部署模式在服务创建成功后立即开始计费，**即使尚未发起任何推理请求**（见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。  
- **PTU 溢出策略**：创建时可选「自动溢出」（转为按量付费，返回 `x-dashscope-ptu-overflow:true` 头）或「仅使用 PTU 容量」（超限返回 HTTP 429）；输入超过模型上限（如千问 128K）也自动转为按量计费（见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)）。  
- **LoRA 模型限制**：不支持增量训练、不支持 PD 分离、不支持自定义 `rpm_limit`/`tpm_limit`，且部署后无法修改推理模式（文档 4 中 `lora` 模式无 `enable_thinking` 字段）。  
- **资源释放**：预付费 PTU/MU 订单到期后延后 2 小时停服，资源保留 14 小时后释放；欠费后服务保留 24 小时，超时将删除底层资源（文档 1）。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


