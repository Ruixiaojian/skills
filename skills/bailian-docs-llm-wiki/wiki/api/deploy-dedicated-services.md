# deploy dedicated services

阿里云百炼平台提供模型专属部署服务，支持通过 API 将系统模型或自定义模型部署为独占实例，获得稳定的推理性能和吞吐保障。整个流程涵盖模型导入（针对自定义模型）、查询可部署模型、创建部署任务以及部署后的管理操作。

## 整体流程

专属部署服务的典型使用流程如下：

1. **查询可部署模型**：通过 API 获取支持部署的系统模型或微调模型列表
2. **（可选）导入自定义模型**：将 OSS 上的自定义模型导入百炼平台
3. **创建部署任务**：选择部署方案（计费模式）并创建部署
4. **调用与管理**：使用部署后生成的模型名称进行推理调用

所有接口均需在请求头中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 和 `Content-Type: application/json`。

## 模型导入

如需部署自定义微调模型，须先通过导入 API 将模型文件从 OSS 导入百炼平台。详细流程参见 [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)。

### 导入前提

- 已创建 OSS Bucket 并完成百炼平台的 OSS 授权
- 模型文件已上传至 OSS 且符合导入要求

### 创建导入任务

```
POST https://dashscope.aliyuncs.com/api/v1/custom_models/import
```

关键请求参数：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model_name` | String | 是 | 基础模型名称，如 `qwen3-32b` |
| `source` | String | 是 | 导入来源，当前仅支持 `oss` |
| `weight_type` | String | 是 | 训练类型：`full`（全参微调）或 `lora`（LoRA 微调） |
| `storage_info` | Object | 是 | 包含 `bucket_name` 和 `object_key`（需以 `/` 结尾） |
| `display_name` | String | 否 | 模型显示名称，最多 50 字符 |

### 任务状态流转

| 状态 | 说明 |
|------|------|
| `PENDING` | 任务已提交，等待处理 |
| `RUNNING` | 正在校验和导入模型文件 |
| `SUCCESSED` | 导入成功，可进行部署 |
| `FAILED` | 导入失败，可通过 `error_code` 了解原因 |

### 其他导入管理接口

- **查询任务详情**：`GET /api/v1/custom_models/import/{job_id}`
- **查询任务列表**：`GET /api/v1/custom_models/import?page_no=1&page_size=10`（支持按 `status` 和 `model_name` 过滤）
- **删除导入模型**：`DELETE /api/v1/custom_models/import/{job_id}`（仅 `SUCCESSED` 或 `FAILED` 状态可删除）

## 查询可部署模型

根据 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md) 的说明，可通过以下接口获取支持部署的模型列表：

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

| 参数 | 说明 |
|------|------|
| `model_source` | `base`（系统模型，默认）或 `custom`（用户微调模型） |
| `version` | 推荐 `v1.0`，可返回完整部署方案和模板信息 |
| `page_no` / `page_size` | 分页参数，page_size 最大 100 |

响应中每个模型包含 `plans` 数组，列出该模型支持的部署方案类型（`mu`、`cu`、`ptu`、`lora`），以及各方案下的部署模板信息。

## 部署方案与计费模式

创建部署任务的接口为：

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

> **注意**：部署成功后即开始计费，即使尚未调用模型。请先确认计费规则再执行部署。

### 四种部署方案

| plan 值 | 计费方式 | 适用场景 |
|---------|---------|---------|
| `mu` | 按模型单元使用时长 | 通用 LLM 部署，支持推理模式、限流等高级配置 |
| `ptu` | 预置吞吐量（按 TPM） | 需要稳定吞吐保障的场景 |
| `cu` | 按算力单元使用时长 | 图片生成、视频生成等模型 |
| `lora` | 按 Token 用量 | LoRA 微调模型共享部署 |

### 核心请求参数

| 参数 | 适用 plan | 必选 | 说明 |
|------|-----------|------|------|
| `model_name` | 所有 | 是 | 待部署模型名称 |
| `plan` | 所有 | 是 | 部署方案：`mu`/`ptu`/`cu`/`lora` |
| `name` | 所有 | 是 | 控制台显示名称 |
| `capacity` | `mu`/`cu` | 是 | 资源单元数量，需为 `base_capacity` 整数倍 |
| `deploy_spec` | `mu` | 是 | 模型单元规格，如 `MU1`、`MU2` |
| `billing_method` | `mu` | 是 | 计费方式，当前仅支持 `POST_PAY` |
| `ptu_capacity` | `ptu` | 否 | 含 `input_tpm` 和 `output_tpm`，默认 10000/1000 |
| `enable_thinking` | `mu` | 否 | 是否启用思考模式 |
| `max_context_length` | `mu` | 否 | 最长上下文长度 |
| `rpm_limit` / `tpm_limit` | `mu` | 否 | 服务限流配置 |
| `suffix` | 所有 | 否 | 模型名称后缀，最长 8 字符，同一模型多次部署时必须设置 |

> **注意**：`lora` 方案中 `capacity` 参数设置无效但必须填写。如需扩缩容，需通过控制台提交申请。

### 请求示例

**PTU 模式：**
```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {
        "input_tpm": 10000,
        "output_tpm": 1000
    }
}'
```

**MU 模式：**
```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "billing_method": "POST_PAY"
}'
```

## 支持的模型

根据 [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md) 中的信息，PTU 方案支持的主要模型包括：

**千问系列：** `qwen3.7-max-2026-05-20`、`qwen3.6-flash-2026-04-16`、`qwen3.6-plus-2026-04-02`、`qwen3-max-2025-09-23`、`qwen-flash-2025-07-28`、`qwen-plus-2025-12-01` 等

**DeepSeek 系列：** `deepseek-v4-pro`、`deepseek-v3.2`、`deepseek-v3`

**千问 VL：** `qwen3-vl-plus-2025-09-23`

**其他：** `glm-5.1`

以上模型最长输入 Token 为 64,000～128,000 不等。完整列表和最新定价请查阅原始文档。

## 模板与 PD 分离部署

使用 `plan=mu` 时，部分模型支持通过模板选择不同的部署拓扑：

- **COUPLED**（非 PD 分离）：使用 `capacity` 参数设置统一节点的资源量
- **SEPERATED**（PD 分离）：分别使用 `prefill_capacity` 和 `decode_capacity` 设置 prefill 和 decode 节点

模板 ID 通过查询可部署模型接口获取，创建部署时作为 `template_id` 参数传入。

## 限制和注意事项

- **部署即计费**：部署成功后立即开始计费，不论是否有推理调用
- **PTU 溢出**：当调用超过购买的 TPM 量或最长输入 Token 时，请求自动降级为按量付费，返回 Header 中包含 `x-dashscope-ptu-overflow:true`
- **欠费保留**：后付费模式下，账户欠费后资源保留并继续计费 24 小时，之后自动释放
- **预付费规则**：预付费订单无法提前终止；到期后延后 2 小时停止服务，资源保留 14 小时后释放
- **MU 资源竞争**：模型单元后付费方式的算力资源先到先得，购买不成功会全额退款
- **CosyVoice 限制**：CosyVoice 系列调优模型仅支持 `plan=mu`，且 `deploy_spec` 必须使用具体规格的真实 ID（形如 `dps-xxx`），不接受 `MU1`/`MU2` 等缩写
- **导入任务删除**：仅 `SUCCESSED` 或 `FAILED` 状态的导入任务可被删除，`RUNNING` 状态的任务不可删除

## 错误处理

导入和部署 API 的常见错误码：

| 错误码 | 说明 |
|--------|------|
| `InvalidParameter` | 参数无效（缺失、格式错误或值不合法） |
| `NotFound` | 资源不存在或无权访问 |
| `OperationDenied` | 操作被拒绝（如删除运行中的任务） |
| `InvalidApiKey` | API-KEY 无效或未提供 |
| `InternalError` | 系统内部错误，请稍后重试 |

## 来源文档

- [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)
- [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)

