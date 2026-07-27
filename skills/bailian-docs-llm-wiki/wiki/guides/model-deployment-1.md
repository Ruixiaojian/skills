# model deployment 1

百炼平台的 `model deployment 1` 是面向生产级推理服务的标准化部署能力，支持预置吞吐（PTU）、模型单元（MU）和 [Token](../concepts/token.md) 用量三种计费与资源调度模式。它适用于从长文档分析、多轮对话到专属微调模型上线等不同负载场景，提供确定性性能保障或灵活可调的算力配置。所有部署均基于百炼统一 API 接口，兼容 OpenAI、Anthropic 和 DashScope 协议。

## 支持的模型/功能

- **预置吞吐（PTU）部署**：支持 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等模型，具备长输入（最高 256K token）与前缀缓存能力，适用于高并发、低延迟的稳定生产环境 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）部署**：支持全部千问系列（含 Qwen3/VL/Omni）、DeepSeek、GLM 及 Kimi 等主流模型，允许自定义推理模式（Instruct/Thinking）、最长上下文、服务限流及 PD 分离计算模式，适用于需独占资源、精细调优性能的场景 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **[Token](../concepts/token.md) 用量部署**：仅支持经 LoRA 调优后的部分千问与千问 VL 基础模型（如 `qwen3-8b`、`qwen3-vl-8b-instruct`），按实际输入/输出 token 计费，适合效果验证与低频调用 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型导入**：支持从阿里云 OSS 导入 LoRA 模型，要求 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 与基础模型严格一致，且视觉模型必须冻结 VIT [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 1 中称 `glm-5.1` 输入上限为 200K，而文档 4 的表格明确标注其为 64K；文档 4 同时列出 `GLM-5.2` 支持 1M 输入。此处以文档 4 的官方规格表为准，`glm-5.1` 实际上限为 64K，200K 属于过时描述。

## 关键参数

| 参数 | 说明 | 适用模式 | 示例值 |
|------|------|----------|--------|
| `plan` | 计费模式标识 | 所有 | `"ptu"` / `"mu"` / `"lora"` |
| `ptu_capacity.input_tpm` / `output_tpm` | 预置吞吐额度（KTPM） | PTU | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `capacity` | 模型单元规格与副本数 | MU | `"MU1"`, `4` |
| `enable_thinking` | 是否启用思考模式 | MU | `true` |
| `max_context_length` | 最长上下文长度 | MU（部分模型） | `10000` |
| `rpm_limit` / `tpm_limit` | 服务限流阈值 | MU | `500`, `1000` |

- PTU 模式下，`input_tpm` 和 `output_tpm` 必须显式指定，且受模型阶梯系数影响（如 `glm-5.1` 超 32K 输入部分按 1.33 系数折算）[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- MU 模式下，`deploy_spec` 决定单副本算力，`capacity` 表示副本数，二者共同决定总并发能力；`enable_thinking` 仅对支持思考模式的模型生效（如 `qwen-plus-2025-12-01`）。
- [Token](../concepts/token.md) 用量模式（`plan: "lora"`）中 `capacity` 字段无实际作用，但 API 要求必填（见文档 3 示例）。

## 使用方式

1. **控制台部署**：登录百炼控制台 → 模型部署 → 创建部署 → 选择模型、计费方式及参数 → 提交。PTU 用户可使用「预置吞吐额度计算器」估算输入/输出 KTPM 需求 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
2. **API 部署**：通过 `POST /api/v1/deployments` 发起请求，需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。示例：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --data '{
       "name": "my_qwen_ptu",
       "model_name": "qwen3.7-plus-2026-05-26",
       "plan": "ptu",
       "ptu_capacity": {"input_tpm": 5000, "output_tpm": 500}
     }'
   ```
3. **状态查询与调用**：部署后通过 `GET /api/v1/deployments/{deployed_model}` 查询状态（`status: "RUNNING"` 表示就绪），再使用 `Generation.call(model='deployed_model_id', ...)` 发起推理 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 限制和注意事项

- **地域限制**：API 部署目前仅支持华北2（北京）地域 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限约束**：API Key 所属业务空间必须已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **溢出策略**：PTU 部署创建时需选择「自动溢出」（转按量计费）或「仅使用 PTU 容量」（超限返回 429）。前者在 API 响应头中返回 `x-dashscope-ptu-overflow:true`，后者需自行监控配额避免服务中断 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型导入限制**：LoRA 模型导入不支持全参微调、修改词汇表或 chat_template；视觉模型必须冻结 VIT，否则校验失败 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费不可变**：部署创建后计费方式不可更改，切换需先下线再重建 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)


