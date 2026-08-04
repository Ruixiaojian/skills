# model deployment 1

百炼平台的 model deployment 1 是面向生产环境的模型服务化能力，支持将预置模型或 LoRA 微调后的自定义模型部署为资源独占、性能可预期的推理服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适用于高并发低延迟、高性能可定制及成本敏感型场景。部署后可通过标准 API（OpenAI/DashScope 兼容）调用，所有模式均支持监控、扩缩容与生命周期管理。

## 支持的模型/功能

- **预置模型**：千问（Qwen）、DeepSeek、GLM、Kimi、CosyVoice、千问VL、千问 Omni 等系列的多个版本（如 `qwen3.8-max`、`deepseek-v4-flash`、`glm-5.2`），具体支持列表以控制台实时可选为准 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **自定义模型**：仅支持从 OSS 导入的 LoRA 微调模型，需满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等约束；全参微调模型不支持导入 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **核心功能**：
  - PTU 模式支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗；
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度、RPM/TPM 限流；
  - 所有部署均支持自动续费、服务状态查询（`PENDING`/`RUNNING`/`DELETING`）及标准 API 调用。

> **注意**：文档 1 中“支持模型”表格称 PTU 模式支持“部分预置模型”，而文档 4 的 API 示例中 `qwen-flash-2025-07-28` 可直接用于 PTU 部署，且文档 2 明确列出 `qwen3.7-plus-2026-05-26` 支持长输入与缓存——表明 PTU 实际覆盖范围远超“部分”，应以控制台实时可选模型为准，而非静态表格。

## 关键参数

| 参数 | 模式 | 说明 | 示例值 |
|------|------|------|--------|
| `plan` | 所有模式 | 计费策略标识 | `"ptu"` / `"mu"` / `"lora"` |
| `ptu_capacity` | PTU | 预置吞吐额度（单位：TPM） | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec`, `capacity` | MU | 模型单元规格与副本数 | `"MU1"`, `4` |
| `enable_thinking` | MU | 是否启用思考模式（仅部分模型支持） | `true` |
| `max_context_length` | MU | 最长上下文长度（需模型支持） | `10000` |
| `rpm_limit`, `tpm_limit` | MU | 服务级限流阈值 | `500`, `1000` |
| `model_name` | 所有模式 | 模型唯一标识符（非显示名称） | `"qwen3.5-plus-2026-04-20"` |

- PTU 模式下 `rpm_limit`/`tpm_limit` 等参数不可配置，吞吐由 `ptu_capacity` 固定保障；
- `"lora"` 计费模式实际对应“按 [Token](../concepts/token.md) 用量计费”，`capacity` 字段必须填写但无效，扩缩容需通过控制台人工申请 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

1. **控制台部署**：登录百炼控制台 → 进入[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create) → 选择模型、计费模式、配置参数 → 提交创建。
2. **API 部署**（推荐自动化场景）：
   - 获取模型 ID（自定义模型需先完成 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)）；
   - 设置环境变量 `DASHSCOPE_API_KEY`；
   - 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/deployments`，携带对应 `plan` 和参数（见文档 4 示例）；
   - 调用 GET 接口轮询 `status` 直至 `RUNNING`；
   - 使用 `deployed_model` ID 发起推理请求（SDK 或 HTTP）。
3. **调用验证**：部署成功后，通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，响应中 `service_tier: "ptu-standard"` 表示走 PTU 额度，`x-dashscope-ptu-overflow:true` 响应头表示已溢出至按量计费。

## 限制和注意事项

- **地域限制**：API 部署当前仅支持华北2（北京）地域，新加坡等其他地域需通过控制台操作 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限要求**：API 调用需确保 API Key 所属业务空间已授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`。
- **OSS 导入约束**：LoRA 模型导入必须完成 OSS 服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access=read` 标签；不支持归档/冷归档存储类型，且模型文件须置于子目录（非 Bucket 根目录）。
- **计费生效时机**：服务创建成功即开始计费，无论是否发起调用；PTU 预付费订单无法提前终止，MU 包月订单首月退订按日单价 1.2 倍计费。
- **长输入与缓存**：PTU 模式下输入超过模型上限（如千问 128K）将自动转为按量计费；缓存命中需满足前缀一致、间隔在有效期、token 数足够触发等条件，`cached_tokens=0` 不一定代表缓存失效，需结合监控指标综合判断 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


