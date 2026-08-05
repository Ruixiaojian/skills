# model deployment 1

百炼平台的 `model deployment 1` 是面向生产级推理服务的核心能力，支持将预置模型或用户调优/导入的 LoRA 模型部署为资源独占、性能可预期的专属服务。该能力提供三种计费与资源调度模式：**预置吞吐（PTU）** 保障高并发低延迟稳定性，**模型单元（MU）** 提供细粒度算力控制与 PD 分离等高级特性，**按 [Token](../concepts/token.md) 用量**适用于效果验证与轻量场景。所有部署均通过统一 API 管控，支持自动化扩缩容与精细化监控。

## 支持的模型与功能

- **预置模型**：覆盖千问（Qwen）、DeepSeek、GLM、Kimi、CosyVoice 等主流系列，包括文本生成、多模态（千问VL）、语音合成、Embedding、Rerank 等类型。具体支持列表以控制台实时可选为准，详见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **调优后模型**：支持全部 LoRA 微调模型（含平台调优与 OSS 导入），但**全参微调模型不可部署**；OSS 导入模型需满足 rank（8/16/32/64）、词汇表一致性、chat_template 未修改、VIT 冻结等硬性约束，详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算、自定义推理模式（Instruct/Thinking）、最长上下文、RPM/TPM 限流；
  - 所有部署均支持自动续费、API 状态查询与一键删除。

> **注意**：文档 1 中称“部分预置模型”支持 PTU，但文档 3 的 API 示例及文档 1 的价格表显示千问、DeepSeek、GLM 等主流预置模型均明确支持 PTU；而文档 4 明确指出“当前版本仅支持导入 LoRA 模型”，与文档 1 中“部分经过 LoRA 调优后的模型”支持 [Token](../concepts/token.md) 计费存在表述差异——实际 [Token](../concepts/token.md) 计费**仅限 LoRA 模型**，且必须基于指定基础模型（如 qwen3-8b）完成 SFT 训练，非所有 LoRA 均可用。此为关键约束，应以 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 的技术限制为准。

## 关键参数

| 参数 | 说明 | 适用模式 | 示例值 |
|------|------|----------|--------|
| `plan` | 部署计费模式 | 所有 | `"ptu"`, `"mu"`, `"lora"` |
| `ptu_capacity` | PTU 模式下的输入/输出 TPM 额度 | PTU | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `capacity` | MU 模式下的模型单元规格与副本数 | MU | `"MU1"`, `4` |
| `enable_thinking` | 是否启用思考模式（影响 token 单价与推理行为） | MU & Token | `true` |
| `max_context_length` | 最长上下文长度（仅 MU 模式支持自定义） | MU | `10000` |
| `rpm_limit` / `tpm_limit` | 服务级请求/Token 速率限制 | MU | `500`, `1000` |

- PTU 模式下，`input_tpm`/`output_tpm` 直接对应购买的吞吐能力，超出按溢出策略处理（自动溢出转按量付费，或返回 429）；
- MU 模式下，`deploy_spec`（如 `MU1 x 8`）决定单副本算力，`capacity` 决定副本数，二者共同决定总并发能力；
- Token 计费模式（`plan: "lora"`）中 `capacity` 参数**必须填写但无效**，扩缩容需人工审核，详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

1. **准备前提**：获取 API Key 并配置环境变量；确保业务空间已授权目标模型部署权限；OSS 导入模型需完成 Bucket 授权与标签配置。
2. **创建部署**：调用 `/api/v1/deployments` POST 接口，按 `plan` 选择对应参数结构。例如 PTU 部署千问 Flash：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --data '{
       "name": "my_qwen_flash",
       "model_name": "qwen-flash-2025-07-28",
       "plan": "ptu",
       "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
     }'
   ```
3. **状态查询**：使用 `GET /api/v1/deployments/{deployed_model}` 获取 `status` 字段，`RUNNING` 表示就绪。
4. **推理调用**：使用 DashScope SDK 或直接 HTTP 请求，`model` 参数填部署服务 ID（如 `qwen3-8b-ft-202511132025-0260`），非基础模型名。
5. **销毁服务**：`DELETE /api/v1/deployments/{deployed_model}` 立即停止计费。

## 限制和注意事项

- **地域限制**：API 部署目前**仅支持华北2（北京）地域**，其他地域需通过控制台操作，详见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **计费生效**：部署成功即开始计费，无论是否发起推理请求；PTU 预付费订单无法提前终止，MU 预付费首月退订按日单价 1.2 倍计费。
- **模型约束**：
  - Token 计费仅支持指定基础模型的 LoRA 微调结果，且需在训练时启用 SFT；
  - MU 模式支持 PD 分离，但并非所有模型规格均可用（如 `MU1 x 16` 仅部分模型支持）；
  - 输入超模型上限（如千问 128K、DeepSeek 64K）将自动转为按量计费，不中断服务。
- **监控与调试**：PTU 部署响应头含 `x-dashscope-ptu-overflow:true` 标识溢出；API 响应体含 `provisioned_tokens`（折算后消耗）与 `cached_tokens`（缓存命中数），用于验证长输入与缓存效果，详见 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **安全与权限**：API Key 必须归属拥有模型部署权限的业务空间；子账号需主账号授予 `ram:CreateServiceLinkedRole` 权限方可完成 OSS 授权。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


