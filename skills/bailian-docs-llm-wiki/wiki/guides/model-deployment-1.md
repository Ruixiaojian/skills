# model deployment 1

模型部署是百炼平台提供的一种将预置模型或调优后模型转化为独立、资源专享推理服务的能力，适用于对高并发、低延迟、资源确定性有明确要求的生产场景。通过部署，用户可获得专属 endpoint，并根据业务负载选择匹配的计费与性能模式（PTU、模型单元或 [Token](../concepts/token.md) 用量）。部署服务创建即开始计费，且计费方式不可变更，需在创建前审慎选型。

## 支持的模型/功能

- **预置模型**：支持千问（Qwen）、DeepSeek、GLM、千问VL、千问Omni、CosyVoice 等系列的多个版本，具体以控制台实时可选列表为准。详见 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **调优后模型**：
  - LoRA 微调模型：支持从 OSS 导入符合约束的 LoRA 模型（如 rank=8/16/32/64、词汇表与 chat_template 未修改、视觉模型冻结 VIT），导入后可部署为 PTU 或模型单元类型；全参微调模型暂不支持导入 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
  - SFT 后模型：仅部分经 SFT 训练的模型支持按 [Token](../concepts/token.md) 用量计费（如 `qwen3.5-27b`、`qwen3-32b`），且需满足平台白名单要求。
- **核心功能**：
  - PTU 部署支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数和缓存折扣优化额度消耗；
  - 模型单元部署支持 PD 分离计算模式（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文长度、RPM/TPM 限流等；
  - 所有部署类型均支持自动续费（预付费）与 API 全生命周期管理（创建、查询、调用、删除）。

> **注意**：文档 1 中“支持模型”表格列示 `千问3.7-Flash-2026-07-15` 等带未来日期的模型代码，但文档 4 的 API 示例及文档 1 的计费表格中均未体现其实际部署参数（如 `ptu_capacity` 或 `deploy_spec`），且控制台未开放该模型的部署入口。建议以控制台实时可选模型为准，避免依赖文档中未验证的占位符模型。

## 关键参数

| 参数名 | 适用部署类型 | 说明 | 约束 |
|--------|--------------|------|------|
| `plan` | 全部 | 计费模式标识：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 用量） | 必填，不可混用 |
| `ptu_capacity` | PTU | `{ "input_tpm": N, "output_tpm": M }`，单位为 KTPM/小时 | 输入/输出 TPM 需 ≥ 1000；超出购买额度按溢出策略处理 |
| `deploy_spec` / `capacity` | 模型单元 | `deploy_spec`: 如 `"MU1"`；`capacity`: 副本数（如 `4`） | `capacity` 表示部署副本数，非算力规格；`deploy_spec` 决定单副本算力 |
| `enable_thinking` | 模型单元（部分模型） | `true` 启用思考模式，`false` 为非思考模式 | 仅对标注 `Thinking` 或 `Instruct/Thinking` 的模型生效 |
| `max_context_length` | 模型单元（部分模型） | 最长上下文长度（token） | 不得超过模型原生上限（如 `qwen3.8-max` 为 1M） |
| `rpm_limit` / `tpm_limit` | 模型单元（部分模型） | 每分钟请求数 / 每分钟 Token 数上限 | 用于服务级限流，不影响底层资源分配 |

## 使用方式

- **控制台操作**：登录 [百炼控制台 → 模型部署](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费模式、配置参数（如 PTU 容量或模型单元规格），提交创建。
- **API 调用**（推荐自动化集成）：
  - 创建部署：`POST https://dashscope.aliyuncs.com/api/v1/deployments`，按 `plan` 类型传入对应参数（见 [使用 API或命令行进行模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。
  - 查询状态：`GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}`，轮询 `status` 字段直至为 `RUNNING`。
  - 推理调用：使用 DashScope SDK 或直接 HTTP 请求，`model` 参数填写部署服务 ID（非基础模型 ID），例如 `Generation.call(model='my_qwen_flash', ...)`。
  - 删除服务：`DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}`，立即下线并停止计费。
- **前提条件**：已获取 API Key 并配置环境变量；API Key 所属业务空间需被授权部署目标模型；华北2（北京）地域为当前 API 唯一支持地域。

## 限制和注意事项

- **计费刚性**：部署创建成功即开始计费，且计费方式不可更改。如需切换，必须先下线现有服务再重新部署 [模型部署 (raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **PTU 溢出行为**：默认策略为「自动溢出」，超出额度时请求转为按量计费（响应头含 `x-dashscope-ptu-overflow:true`）；若选「仅使用 PTU 容量」，则返回 HTTP 429 错误。单次输入超模型上限（如千问 128K）同样触发自动溢出。
- **模型单元资源独占**：`mu` 模式下资源严格隔离，但 `capacity`（副本数）调整需通过控制台人工审核，API 不支持动态扩缩容（`capacity` 字段在 API 中仅用于初始设置）。
- **LoRA 导入约束**：OSS Bucket 必须添加 `bailian-datahub-access=read` 标签；模型目录不得为 Bucket 根目录；`adapter_model.safetensors` 中不得含 `visual.*` 参数（VIT 必须冻结）；rank 值仅限 8/16/32/64 [模型导入 (raw/model-user-guide/model-deployment-1/model-import.md)](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **地域限制**：API 仅支持华北2（北京）地域，其他地域需切换控制台 Region 或等待后续支持。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


