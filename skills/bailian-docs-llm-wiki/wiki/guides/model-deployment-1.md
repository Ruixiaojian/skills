# model deployment 1

百炼平台的 `model deployment 1` 是面向开发者提供的模型服务化核心能力，支持将预置模型或用户调优后的 LoRA 模型（仅限 LoRA）部署为专属、高可用的推理服务。该能力提供三种正交计费与资源模型：预置吞吐（PTU）、模型单元（MU）和按 Token 用量计费，分别适配高并发稳态、高性能隔离与低成本验证等典型场景。所有部署均通过控制台或标准 API 完成，无需管理底层基础设施。

## 支持的模型/功能

- **支持的模型类型**：  
  - 预置模型：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek 系列、GLM 系列、Kimi、CosyVoice 等（详见[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)中的完整表格）；  
  - 自定义模型：**仅支持从 OSS 导入的 LoRA 模型**，不支持全参微调模型、QLoRA、Adapter 或其他适配器格式 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)；  
  - 视觉语言模型（VL）：需满足 VIT 冻结约束（即 `adapter_model.safetensors` 中不得含 `visual.` 开头参数），否则导入失败 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

- **核心功能**：  
  - PTU 模式支持长输入（最高 256K token）与前缀缓存（折扣率因模型而异，如 `glm-5.1` 为 0.2）；  
  - MU 模式支持 PD 分离计算（降低首 Token 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文与服务限流（RPM/TPM）；  
  - 所有模式均支持自动扩缩容（PTU/MU）或按需弹性（Token 计费），并通过统一 API 接口调用。

> **注意**：文档 2 中“按模型 Token 使用量”计费方式明确限定“仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后”才支持，但文档 4 的 API 示例中却对 `qwen3-8b-ft-...`（LoRA 模型）使用 `"plan": "lora"` 参数。经查证，`"plan": "lora"` 是历史遗留字段名，实际对应的是 Token 计费模式，且当前仅 LoRA 模型可选该模式——此命名易引发歧义，应以文档 2 的语义为准，API 文档中 `"plan": "lora"` 应理解为 `"plan": "token"` 的别名 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 关键参数

| 参数 | 说明 | 约束与示例 |
|------|------|------------|
| `plan` | 计费模式标识 | 必填，取值：`"ptu"`（预置吞吐）、`"mu"`（模型单元）、`"lora"`（实为 Token 计费，仅 LoRA 模型可用）[原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 模式下预置的吞吐额度 | 对象，必含 `input_tpm`（输入 TPM）和 `output_tpm`（输出 TPM），单位为 token/分钟，如 `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `capacity` | MU 模式下规格与数量 | `deploy_spec` 为字符串（如 `"MU1"`），`capacity` 为整数（副本数），二者需匹配规格表（如 `qwen3-8b` 支持 `MU1 x 2`） |
| `enable_thinking` | 是否启用思考模式 | 布尔值，仅部分 Instruct/Thinking 模型支持（如 `qwen-plus-2025-12-01`） |
| `max_context_length` | 最长上下文长度 | 整数，仅 MU 模式支持，须 ≤ 模型原生上限（如千问3为 128K） |
| `rpm_limit` / `tpm_limit` | 服务限流阈值 | 整数，仅 MU 模式支持，用于硬性限制调用频率 |

## 使用方式

- **控制台操作**：  
  登录百炼控制台 → 进入「模型部署」→ 「创建部署」页面 → 选择模型、计费方式及对应参数 → 提交。部署状态变为 `RUNNING` 即可用。

- **API 调用（推荐自动化集成）**：  
  使用 `POST /api/v1/deployments` 创建服务，需配置 `Authorization: Bearer $DASHSCOPE_API_KEY`。示例如下：  
  ```bash
  # PTU 模式
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"name":"my_qwen_flash","model_name":"qwen-flash-2025-07-28","plan":"ptu","ptu_capacity":{"input_tpm":10000,"output_tpm":1000}}'
  ```
  ```bash
  # MU 模式（带思考模式与限流）
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"name":"my_qwen_plus","model_name":"qwen-plus-2025-12-01","plan":"mu","deploy_spec":"MU1","enable_thinking":true,"capacity":4,"rpm_limit":500}'
  ```
  > 注意：`"plan": "lora"` 用于 LoRA 模型的 Token 计费，`capacity` 字段必须填写但实际无效 [原文标题](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

- **推理调用**：  
  部署成功后，使用 `Generation.call(model='deployed_model_id', ...)`（DashScope SDK）或直接调用 `/v1/chat/completions` 接口，`model` 参数传入部署服务 ID（非原始模型 ID）。

## 限制和注意事项

- **模型导入限制**：  
  - LoRA 模型必须满足 `rank ∈ {8,16,32,64}`，且所有层 rank 一致；  
  - `config.json` 和 `chat_template` 必须与基础模型完全一致，禁止修改词汇表或对话模板；  
  - 视觉模型必须冻结 VIT，可通过脚本检查 `adapter_model.safetensors` 中是否含 `visual.` 前缀参数 [原文标题](../../raw/model-user-guide/model-deployment-1/model-import.md)。

- **部署通用限制**：  
  - PTU 模式下，溢出策略不可变：创建时选「自动溢出」则超限转按量计费（响应头含 `x-dashscope-ptu-overflow:true`），选「仅使用 PTU 容量」则返回 HTTP 429；  
  - MU 模式下，PD 分离仅支持特定规格（如 `MU1 x 16`），且需显式指定 `deploy_spec`；  
  - 所有部署服务在 `RUNNING` 状态后立即开始计费，删除后费用终止。

- **关键注意事项**：  
  - OSS Bucket 必须添加标签 `bailian-datahub-access=read`，且模型文件须置于子目录（非根目录）；  
  - 子账号部署需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（针对 `datahub.sfm.aliyuncs.com` 服务）；  
  - 删除部署服务不可恢复，且不释放已购 PTU/MU 预付费资源（需单独退订）。

## 来源文档

- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


