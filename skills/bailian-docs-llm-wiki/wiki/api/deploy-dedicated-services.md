# deploy dedicated services

本主题汇总阿里云百炼平台与「专属服务部署」相关的 HTTP API：将自定义模型从 OSS 导入到百炼，以及把基础模型或导入后的模型部署为可调用的专属推理服务。两类 API 共同构成一条完整链路——**先通过模型导入接口把权重落到平台、再通过模型部署接口拉起推理实例并产出 `deployed_model` 标识**，供后续业务调用。

## 整体流程

典型链路分为两段：

1. **模型导入**（可选）：若要部署自定义微调权重，先调 [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md) 创建导入任务，把 OSS 上的 LoRA / 全参微调权重注册到百炼，得到形如 `qwen3-32b-offline-20240101-abc1` 的系统生成模型名。
2. **模型部署**：根据需要的计费模式，调 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md) 创建部署任务，产出 `deployed_model` 标识；该标识就是后续 SDK / HTTP 调用时传入的 model id。

两类 API 都通过 `DASHSCOPE_API_KEY` 鉴权，公共请求头为：

- `Authorization: Bearer ${DASHSCOPE_API_KEY}`
- `Content-Type: application/json`

## 模型导入 API

模型导入用于把 OSS Bucket 中的自定义模型权重注册到百炼，导入完成后才能作为 `model_name` 进入部署流程。详细字段见 [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)。

### 接口一览

| 操作 | 方法与路径 |
| --- | --- |
| 创建导入任务 | `POST /api/v1/custom_models/import` |
| 查询导入任务详情 | `GET /api/v1/custom_models/import/{job_id}` |
| 查询导入任务列表 | `GET /api/v1/custom_models/import` |
| 删除导入的模型 | `DELETE /api/v1/custom_models/import/{job_id}` |

### 关键参数（创建导入任务）

- `model_name`（必填）：基础模型名称，例如 `qwen3-32b`，需在「支持导入的基础模型」列表中。
- `weight_type`（必填）：`full` 表示全参微调，`lora` 表示 LoRA 微调。
- `source`（必填）：当前仅支持 `oss`；响应中返回大写 `OSS`。
- `storage_info.bucket_name` / `storage_info.object_key`（必填）：OSS Bucket 名称与文件前缀，`object_key` 必须以 `/` 结尾，例如 `models/qwen3-32b-lora/`。
- `display_name`（可选）：控制台展示名称，最长 50 字符，不传则默认沿用基础模型名。

### 任务生命周期

导入任务依次经历 `PENDING → RUNNING → SUCCESSED / FAILED`：

- 只有处于 `SUCCESSED` 或 `FAILED` 的任务可以被 `DELETE` 删除。
- 任务失败时，详情响应会带 `error_code`（例如 `OSS获取文件失败，请检查OSS内文件`）。
- 异常请求统一返回 `code` + `message` 错误体，常见错误码：`InvalidParameter`、`NotFound`、`OperationDenied`、`InvalidApiKey`、`InternalError`。

## 模型部署 API

模型部署 API 用于把已支持的基础模型（或导入完成的自定义模型）以四种计费模式拉起为专属推理服务。完整字段、模型规格价格表见 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)。

### 接口一览

| 操作 | 方法与路径 |
| --- | --- |
| 查询可部署的模型列表 | `GET /api/v1/deployments/models` |
| 创建模型部署任务 | `POST /api/v1/deployments` |

`/deployments/models` 支持 `page_no` / `page_size` 分页（`page_size` 范围 1–200，默认 50），返回每个模型的 `model_name` 与 `base_capacity`（部署所需最小资源单元数）。

### 四种计费 / 部署模式

`POST /api/v1/deployments` 通过 `plan` 字段区分计费模式：

| 计费模式 | `plan` 取值 | 适用场景 | 关键参数 |
| --- | --- | --- | --- |
| 按预置吞吐（PTU）| `ptu` | 稳定高并发、低延迟、流量可预估 | `ptu_capacity.input_tpm` / `ptu_capacity.output_tpm` |
| 按模型单元使用时长 | `mu` | 大规模推理、性能与成本灵活可调 | `deploy_spec`（如 `MU1`，**必填**）、`capacity`、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` |
| 按 Token 用量 | `lora` | 高性价比、对并发/延迟不敏感（如 LoRA 微调模型） | `capacity`（必填但实际无效，扩缩容走控制台表单） |
| 按算力单元使用时长（图片/视频生成专用）| 不设置 `plan` | 多模态生成类调优后的大规模推理 | `capacity` |

> **注意**：执行 `POST /api/v1/deployments` 后，即使尚未调用模型，部署成功后即开始计费——务必先确认计费规则再下发部署命令。

### 常用请求参数

- `model_name`（必填）：待部署的模型 ID，对应控制台「我的模型」。
- `capacity`（必填）：分配给模型的资源单元数量，**必须是 `base_capacity` 的整数倍**；`plan=lora` 时该字段无效但仍需填写。
- `name` / `display_name`：部署任务名称与控制台显示名。
- `suffix`：部署后生成的新模型名后缀，最长 8 字符且全局唯一；同一模型多次部署时必须设置以便区分。
- `enable_thinking`：部分模型支持，区分 Instruct（非思考）与 Thinking（思考）推理模式；部分模型支持「Instruct/Thinking」，部署时再选。
- `max_context_length`、`rpm_limit`、`tpm_limit`：仅 `plan=mu` 的部分模型支持，用于自定义最长上下文与 RPM/TPM 限流。

### 模型单元（MU）部署支持

`plan=mu` 模式支持的模型覆盖文本生成、多模态、语音合成等场景，包括但不限于：

- **千问系列**：qwen3.6 / qwen3.5 / qwen3 / qwen2.5 各尺寸（含 MoE、Embedding、Rerank），以及 qwen-flash / qwen-plus 的定版模型。
- **多模态**：qwen3-vl 系列、qwen-vl-max / qwen-vl-ocr、qwen3.5-omni-flash / plus。
- **第三方**：GLM-5 / GLM-4.7、DeepSeek-v4-Flash / DeepSeek-v3.2、MiniMax-M2.5、Kimi-K2.5。
- **语音**：cosyvoice-v3-flash。

> **注意**：部分大模型仅在 **PD 分离模式**（Prefill 与 Decode 拆到不同计算节点）下提供，目的是「降低首 Token 延迟、提高吞吐」；PD 分离规格的小时单价显著高于普通规格，下单前需对照 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md) 的价格表。

### 响应与部署生命周期

创建成功后响应包含 `deployed_model`（新模型唯一标识，调用时使用）、`base_model`、`base_capacity` / `capacity` / `ready_capacity`、`workspace_id`、`charge_type`（如 `post_paid`）等字段。部署状态字段 `status` 可能为：

- `PENDING`：正在创建部署任务。
- `UPDATING`：正在更新部署任务。
- `RUNNING`：可正常处理推理请求。
- `STOPPED`：已停止，不再计费。
- `DELETING`：正在删除。
- `FAILED`：创建或更新失败。

## 使用建议与限制

- **先导入、后部署**：自定义权重必须先通过模型导入 API 完成 `SUCCESSED`，其响应中的 `model_name` 才能作为部署 API 的 `model_name`。
- **OSS 前置条件**：调用导入 API 前需创建 OSS Bucket 并完成百炼平台的 OSS 授权，模型文件需满足导入要求（详见 OSS 授权与文件格式约束的官方说明）。
- **capacity 约束**：除 `plan=lora` 外，`capacity` 必须为 `base_capacity` 的整数倍；可先调 `GET /api/v1/deployments/models` 取得 `base_capacity` 后再换算。
- **多次部署同一模型**：必须显式设置 `suffix`，否则会因生成的 `deployed_model` 冲突而失败。
- **扩缩容**：`plan=lora`（按 Token 计费）部署后无法通过 API 修改 `capacity`，需前往百炼模型部署控制台填写表单申请。
- **计费起点**：部署成功立刻开始计费，与是否发起模型调用无关；不再使用时记得通过控制台或对应 API 停止/删除部署任务。
- **错误处理**：导入 API 的失败原因通过 `error_code` 暴露；部署 API 的常见失败包括资源不足、`deploy_spec` 与模型不匹配、`capacity` 非整数倍等，可先在控制台验证后再回到 API 自动化流程。

## 来源文档

- [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)
- [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)


