# 模型部署

模型部署是百炼平台将训练或微调完成的模型（包括预置模型、LoRA 微调模型、量化压缩模型等）转化为稳定、可调用、可监控的在线推理服务的核心能力。它为模型提供统一的 `chat/completions` 兼容接口，并支持按需配置资源、计费模式与服务质量保障。

## 在百炼平台的不同场景中，这个概念如何使用

- **从微调到上线**：微调作业成功后，需显式调用部署接口（不可自动触发），使用输出的 `output_model_id` 创建部署服务；部署前必须确保模型状态为“成功”，且已通过地域（如 `cn-beijing`）和权限校验。
- **从导入到服务**：支持手动导入 LoRA 微调模型（需满足 rank、词表、chat_template 等兼容性要求），再部署为专属服务；全参微调模型暂不支持直接导入部署。
- **从压缩到推理**：模型压缩（PTQ 量化）生成的新模型 ID（如 `qwen35-int4`）可作为独立模型参与部署，但压缩后模型不可再微调或二次压缩。
- **多模态统一接入**：文本、视觉（千问VL）、语音（CosyVoice）、图像/视频（万相）等微调产出的模型，均可通过同一套部署 API 和控制台流程发布为标准推理服务。
- **生产级运维支撑**：部署服务天然集成模型监控（用量、延迟、错误率）、扩缩容（PTU/MU 模式自助调整）、生命周期管理（删除重建、限流配置）等能力，无需额外对接。

## 关键参数和配置

| 参数 | 必填 | 说明 | 注意事项 |
|------|------|------|----------|
| `model_id` | 是 | 模型唯一标识，如 `qwen2-7b-chat`、`ft-xxx` 或压缩后 `my-qwen35-int4` | 必须已在当前工作空间存在且状态有效 |
| `deployment_name`（或 `name`） | 是 | 部署服务全局唯一名称，用于构造 endpoint URL | ≤ 50 字符，不可重复；建议含业务含义（如 `customer-service-qwen35`） |
| `plan` | 是 | 计费与调度模式：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（[Token](token.md) 用量） | `lora` 模式仅适用于 LoRA 微调/导入模型，基座模型不可选 |
| `region` | 是 | 部署地域，如 `cn-beijing` | 所有部署请求必须显式指定，否则返回 400 错误 |
| `ptu_capacity` | 条件必填（`plan=ptu`） | `{ "input_tpm": N, "output_tpm": M }`，单位 TPM | `input_tpm ≥ 1000`，`output_tpm ≥ 100`；长输入触发阶梯系数 |
| `deploy_spec` + `capacity` | 条件必填（`plan=mu`） | `deploy_spec`（如 `"MU1"`）定义单副本规格，`capacity` 定义副本数 | `capacity ≥ 1`；规格需与模型兼容（见控制台实时列表） |
| `enable_thinking` / `max_context_length` / `rpm_limit` / `tpm_limit` | 可选（`plan=mu`） | 启用思考模式、最大上下文长度、服务级限流阈值 | `max_context_length` 不得超过模型原生上限（如 256K） |
| `workspace_id` | 隐式 | 由 API Key 自动关联，用于权限与数据隔离 | 无需手动传入，但需确保该 workspace 已授权目标模型部署权限 |

> ⚠️ 注意：`max_tokens`、`temperature` 等推理参数**不属于部署配置项**，仅在调用 `/chat/completions` 接口时生效；部署本身不绑定任何推理超参。

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台一键部署（[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)）或调用 `POST /v1/deployments` API，5 分钟内获得可用 endpoint。
- ✅ **一次部署，多端调用**：部署后服务完全兼容 OpenAI SDK（`Generation.call(model='deployment_name', ...)`）和标准 REST 请求，无需适配。
- ✅ **按需弹性**：PTU/MU 模式支持控制台或 API 实时扩缩容；[Token](token.md) 计费模式扩容需提交工单审核。
- ✅ **可观测即开即用**：部署成功即自动接入基础监控；开通高级监控后，可查看分钟级延迟、完整推理日志及 Prometheus 指标。
- ❌ **避免踩坑**：
  - 不要省略 `region` 参数；
  - 不要复用 `deployment_name`（全局唯一）；
  - 不要尝试对 LoRA 导入模型使用 `ptu` 或 `mu` 以外的 `plan`；
  - 修改模型必须先删除旧 deployment，再用新 `model_id` 重建——不支持热更新。

部署不是终点，而是模型进入生产闭环的第一步。请结合 [模型监控](model-monitoring.md) 观察效果，用 [模型压缩](model-compression.md) 优化成本，持续迭代你的 AI 服务。

## 关联主题页

- [model production](../api/model-production.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [model monitoring](../guides/model-monitoring.md)


