# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优/导入的 LoRA 模型部署为资源独占、性能可预期的专属推理服务。该能力提供三种正交计费与调度模式：预置吞吐（PTU）、模型单元（MU）和按 Token 用量计费，分别适配高并发低延迟、强定制化长时任务、以及低成本效果验证等典型场景。部署后服务通过标准 API 接入，支持 OpenAI、Anthropic 和 DashScope 多协议兼容。

## 支持的模型/功能

- **支持模型类型**：
  - **预置模型**：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek 系列（v3/v4）、GLM 系列（GLM-5/GLM-4.7）、Kimi-K2.5、CosyVoice 等，详见[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)中的价格表。
  - **调优后模型**：所有通过百炼平台完成 LoRA 微调的任务产出模型（含 SFT 后模型），支持全部三种部署方式；全参微调模型仅支持 PTU 和 MU 方式，不支持 `lora` 计费模式。
  - **导入模型**：仅支持从阿里云 OSS 导入符合约束的 LoRA 模型（rank ∈ {8,16,32,64}，未修改 vocab/chat_template，视觉模型需冻结 VIT），不支持全参微调模型导入 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

- **核心功能**：
  - **长输入与前缀缓存**：PTU 部署支持最高 256K token 输入（如 `qwen3.7-plus-2026-05-26`），并提供阶梯容量系数与缓存折扣（如 `glm-5.1` 缓存命中部分按 20% 折算额度）[原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
  - **PD 分离计算模式**：在模型单元（MU）部署中可选，将 Prefill 与 Decode 阶段拆分至不同节点，显著降低首 Token 延迟、提升吞吐 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
  - **多推理模式支持**：部分模型（如 `qwen-plus-2025-12-01`）在 MU 部署时可配置 `enable_thinking: true/false`，分别启用思考模式或非思考模式；Instruct/Thinking 类型模型可在部署时动态选择 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

> **注意**：文档 1 中“支持模型”表格称“部分预置模型与所有调优后模型”支持模型单元方式，但文档 4 明确指出“全参微调模型仅支持 PTU 和 MU 方式”，二者存在隐含矛盾——实际限制是：**全参微调模型不可通过 `lora` 计费方式部署，但可使用 `mu` 或 `ptu` 方式部署**。开发者应以 API 创建时的实际参数校验为准。

## 关键参数

| 参数名 | 适用模式 | 说明 | 示例值 |
|--------|----------|------|--------|
| `plan` | 全部 | 计费模式标识：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 用量） | `"ptu"`, `"mu"`, `"lora"` |
| `ptu_capacity.input_tpm` / `.output_tpm` | `ptu` | 预置吞吐额度（每分钟 Token 数），决定基线服务能力 | `{ "input_tpm": 10000, "output_tpm": 1000 }` |
| `deploy_spec` / `capacity` | `mu` | 模型单元规格（如 `"MU1"`）与副本数（`capacity: 4`），共同决定算力总量 | `"MU1"`, `4` |
| `enable_thinking` | `mu` | 是否启用思考模式（仅部分模型支持） | `true` |
| `max_context_length` | `mu` | 最长上下文长度（token），部分模型支持自定义 | `10000` |
| `rpm_limit` / `tpm_limit` | `mu` | 服务级限流阈值（每分钟请求数 / 每分钟 Token 数） | `500`, `1000` |
| `model_name` | 全部 | 模型唯一标识符（如 `"qwen-flash-2025-07-28"` 或自定义 LoRA 模型 ID） | `"qwen3-8b-ft-202511132025-0260"` |

- **溢出策略**（仅 `ptu`）：创建时指定 `overflow_strategy`（默认 `"auto"`），`"auto"` 表示超额度自动转按量计费（响应头含 `x-dashscope-ptu-overflow:true`），`"reject"` 表示直接返回 HTTP 429。
- **缓存控制**（仅 `ptu`）：无显式参数，由请求内容自动触发前缀缓存；可通过 `cached_tokens` 响应字段验证是否生效 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 使用方式

- **控制台部署**：访问 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，填写服务名称、选择模型、计费方式及对应参数（如 PTU 容量或 MU 规格），点击确认即可。部署状态变为 `RUNNING` 即可用。
- **API 部署**（推荐自动化）：
  - **PTU 模式**：`POST /api/v1/deployments`，传入 `plan: "ptu"` 和 `ptu_capacity` 对象（见[文档 3](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)示例）。
  - **MU 模式**：`POST /api/v1/deployments`，传入 `plan: "mu"`、`deploy_spec`、`capacity` 及可选 `enable_thinking` 等参数。
  - **Token 计费模式**：`POST /api/v1/deployments`，传入 `plan: "lora"`；注意 `capacity` 字段必须填写但无效，扩缩容需走控制台申请。
- **调用方式**：部署成功后，使用 `model_name`（即 `deployed_model` ID）调用 `/api/v1/services/{model_name}/completions`（DashScope 协议）或标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。务必确保 API Key 所属业务空间与部署空间一致 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域，控制台部署需确认当前控制台所在 Region [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限要求**：API 调用需确保业务空间已授权目标模型的部署权限，且 API Key 归属账号在该空间拥有操作权限；常见报错 `Workspace xxx does not have deployment privilege for model xxxx` 需在业务空间管理中手动授权 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **OSS 导入约束**：从 OSS 导入 LoRA 模型时，Bucket 必须添加标签 `bailian-datahub-access=read`，且模型文件须置于子目录（非根目录）；文件必须包含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`，且 rank、vocab、chat_template 等严格符合约束 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **计费与生命周期**：
  - 所有部署方式均**创建即计费**，即使未发起任何推理请求。
  - PTU 预付费订单无法提前终止，到期后延后 2 小时停服；后付费欠费后保留资源 24 小时。
  - MU 模式下，若购买失败（如资源售罄），将全额退款。
  - `lora` 模式仅对实际 Token 用量计费，无闲置成本。
- **性能边界**：单次输入超过模型上限（如千问 128K、DeepSeek 64K）时，无论 PTU/MU 模式，均自动降级为按量计费，且可能受公共流量管控影响性能 [原文标题](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


