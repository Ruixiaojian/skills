# model production

`model production` 是百炼平台中模型从训练、验证到部署的全生命周期管理能力，涵盖微调（Fine-tuning）、Checkpoint 管理、模型部署及服务运维等核心环节。开发者可通过统一 API 体系完成定制化模型的构建与上线，无需自行维护训练/推理基础设施。

## 支持的模型与功能

- **支持微调的模型类型**：文本生成（如 `qwen3-14b`）、图像生成（如 `wan2.7-image-pro`）、视频生成（如 `wan2.5-i2v-preview`）及语音模型（如 `cosyvoice-v3-flash`），具体以 [列举可部署模型](../../raw/model-api-reference/model-production/list-deployable-models-api.md) 接口返回的 `model_source=custom` 结果为准。
- **核心功能链路**：
  - 创建并管理微调任务（[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）；
  - 查询任务状态、日志及产出 Checkpoint（[查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md) 和 [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)）；
  - 将 Checkpoint 发布为可部署模型，并创建在线推理服务（[模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）；
  - 对已部署服务进行扩缩容、限流调整与生命周期管理（[查询和管理部署](../../raw/model-api-reference/model-production/get-deployment-api.md)）。

> **注意**：文档 3 中明确说明“当前 Checkpoint API 仅在北京 Region 开放”，而其他文档未限定 Region；若在非北京 Region 调用 Checkpoint 相关接口（如 `/checkpoints` 或 `/export/{checkpoint}`），将返回错误或空响应，需通过控制台操作替代。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model` | Query（列举调优任务） | String | 指定基础模型 ID，用于过滤任务 | `qwen3-14b` |
| `job_id` | Path（所有任务详情/日志/Checkpoint 接口） | String | 微调任务唯一标识，格式为 `ft-{yyyyMMddHHmm}-{4位uuid}` | `ft-202410291653-1c7f` |
| `checkpoint` | Path（发布/验证接口） | String | Checkpoint 名称，格式为 `checkpoint-{LM_epoch}{FM_epoch}`（各4位补零） | `checkpoint-00040004` |
| `deployed_model` | Path（部署管理接口） | String | 部署服务唯一标识，由系统生成或用户指定后缀 | `qwen3-14b-suffix-ft-202410291653-1c7f` |
| `model_source` | Query（列举可部署模型） | String | `base`（系统模型）或 `custom`（用户微调模型） | `custom` |

- `hyper_parameters` 在调优任务详情中返回，包含 `n_epochs`、`batch_size`、`learning_rate` 等实际生效超参，**不支持运行时修改**。
- Checkpoint 的 `step` 字段为整数，计算公式为 `LM_epoch × 10000 + FM_epoch`（见 [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)）。

## 使用方式

1. **启动微调**：调用创建微调任务 API（文档未提供，但可由 [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md) 的输入字段反推需传 `model`、`training_datasets`、`hyper_parameters` 等）；
2. **监控进度**：轮询 `GET /api/v1/fine-tunes/{job_id}`，检查 `output.status`（`SUCCEEDED`/`FAILED`/`CANCELED`）及 `output.finetuned_output`（成功后可用的模型 ID）；
3. **获取中间产物**：
   - 列举 Checkpoint：`GET /api/v1/fine-tunes/{job_id}/checkpoints`，筛选 `status=SUCCEEDED` 的项；
   - 发布 Checkpoint：`GET /api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name={name}`；
4. **部署服务**：
   - 先确认模型可部署：`GET /api/v1/deployments/models?model_source=custom`；
   - 创建部署：`POST /api/v1/deployments`，`model_name` 填入上步发布的 `model_name`（即 `output[].model_name`）；
5. **运维服务**：使用 `GET /api/v1/deployments/{deployed_model}` 查状态，`PUT /api/v1/deployments/{deployed_model}/scale` 调整 `capacity`，`PUT /api/v1/deployments/{deployed_model}/update` 设置 `rpm_limit`/`tpm_limit`。

## 限制和注意事项

- **分页限制**：
  - 列举调优任务：`page_size` 最大 1000，最小 1；
  - 列举部署：`page_size` 最大 200，最小 1；
  - 列举可部署模型：`page_size` 最大 100，最小 1。
- **Checkpoint 生命周期**：每个 Checkpoint 有 `expire_time`（ISO 8601 格式），过期后不可发布或部署；`output_cnt` 和 `max_output_cnt` 仅对 `cosyvoice-v3-flash` 等特定模型返回。
- **部署命名约束**：`deployed_model` 必须全局唯一；若创建失败提示 `Conflict`，需添加后缀重试。
- **Region 限制**：Checkpoint 相关 API（`/checkpoints`、`/export`、`/validation-results`）**仅在北京 Region 可用**，其他 Region 用户需通过百炼控制台操作（见 [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)）。
- **数据集字段兼容性**：`training_file_ids` 和 `validation_file_ids` 已废弃，新任务必须使用 `training_datasets` 和 `validation_datasets`（见 [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md)）。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [查询和管理部署](../../raw/model-api-reference/model-production/get-deployment-api.md)
- [列举可部署模型](../../raw/model-api-reference/model-production/list-deployable-models-api.md)


