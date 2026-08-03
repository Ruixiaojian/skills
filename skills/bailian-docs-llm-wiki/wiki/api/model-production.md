# model production

`model production` 是百炼平台中将训练完成的模型转化为可服务化推理实例的完整流程，涵盖微调任务管理、Checkpoint 产物提取、模型部署与运维等环节。该流程支持文本、图像、视频等多模态模型，开发者需按“调优 → Checkpoint 管理 → 发布 → 部署 → 运维”顺序操作，各阶段均有明确的 API 接口和状态约束。

## 支持的模型/功能

- **微调模型类型**：支持文本生成（如 `qwen3-14b`）、图像生成（如 `wan2.7-image-pro`）、视频生成（如 `wan2.5-i2v-preview`）及语音模型（如 `cosyvoice-v3-flash`）等。不同模型支持的训练方式（如 `sft`、`efficient_sft`）和 Checkpoint 输出策略存在差异，详见 [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md)。
- **Checkpoint 管理**：提供 Checkpoint 列举、发布为可部署模型、验证产物查询与明细查看等功能。其中验证产物仅对成功生成预览内容（如视频/图像）的 Checkpoint 返回，且需在调优任务完成后调用 [列举验证产物](../../raw/model-api-reference/model-production/list-checkpoints-api.md) 接口。
- **部署能力**：支持多种部署方案，包括模型单元（`mu`）、算力单元（`cu`）、预置吞吐量（`ptu`）及 LoRA 共享部署（`lora`）。具体支持情况需通过 [列举可部署模型](../../raw/model-api-reference/model-production/list-deployable-models-api.md) 接口按 `model_source=custom` 查询用户自定义模型的 `plans` 字段确认。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 来源 |
|------|------|------|------|------|
| `job_id` | Path | String | 调优任务唯一标识，格式为 `ft-{yyyyMMddHHmm}-{4位uuid}`，用于所有 Checkpoint 和验证接口 | [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md) |
| `checkpoint_id` / `checkpoint` | Path / Query | String | Checkpoint 唯一标识，格式为 `{job_id}:checkpoint-{LM_epoch}{FM_epoch}` 或 `checkpoint-{LM_epoch}{FM_epoch}`；仅 `status=SUCCEEDED` 时返回 `model_name` | [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md) |
| `model_name` | Body (部署) / Query (发布) | String | 部署时的实际模型 ID（来自 Checkpoint 的 `output[].model_name`）；发布接口中的 `model_name` 仅为控制台显示名，**不作为部署入参** | [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md) |
| `deployed_model` | Path | String | 部署服务唯一标识，由系统生成（如 `emo-35b3f106-sample01`），非用户指定的 `model_name` | [查询和管理部署](../../raw/model-api-reference/model-production/get-deployment-api.md) |
| `capacity` | Body | Integer | 模型单元部署的资源单元数，必须为 `base_capacity` 的整数倍（`base_capacity` 由部署模板 `capacity_unit_per_instance` 决定） | [列举可部署模型](../../raw/model-api-reference/model-production/list-deployable-models-api.md) |

> **注意**：文档 2 中“发布 Checkpoint”接口的 `model_name` 查询参数被明确标注为“仅用于控制台展示”，而实际部署需使用 Checkpoint 返回的 `output[].model_name` 字段值；但文档 4 的部署接口示例中直接使用了 `qwen-plus-202305099980-fac9-sample` 这类已部署 ID，未体现从 Checkpoint 到 `model_name` 的映射过程，易引发混淆。请以 [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md) 中 `status=SUCCEEDED` 时返回的 `model_name` 为准。

## 使用方式

1. **启动调优**：调用创建调优任务 API，获取 `job_id`。
2. **监控与查询**：通过 [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md) 获取 `status` 和 `finetuned_output`（仅 `SUCCEEDED` 时有效）。
3. **提取 Checkpoint**：
   - 列举：`GET /api/v1/fine-tunes/{job_id}/checkpoints`
   - 验证筛选（可选）：`GET /api/v1/fine-tunes/{job_id}/validation-results`
   - 发布为模型：`GET /api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name={display_name}`（返回 `output=true` 表示提交成功，实际模型 ID 在 Checkpoint 列表中 `status=SUCCEEDED` 项的 `model_name` 字段）
4. **部署模型**：
   - 查询可部署模型：`GET /api/v1/deployments/models?model_source=custom&version=v1.0`
   - 创建部署：使用上一步获得的 `model_name`（非 `display_name`）作为 `model_name` 字段，按模板要求传入 `deploy_spec` 和 `capacity`。
5. **运维管理**：通过 [查询和管理部署](../../raw/model-api-reference/model-production/get-deployment-api.md) 实现扩缩容（`/scale`）、限流调整（`/update`）及删除。

## 限制和注意事项

- **Region 限制**：Checkpoint 相关 API 当前仅在北京 Region 开放，其他 Region 用户需通过控制台操作 [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)。
- **Checkpoint 有效期**：每个 Checkpoint 有 `expire_time`（ISO 8601 格式），过期后不可发布或部署；验证产物中的 `video_path` 和 `first_frame_path` 有效期仅 24 小时，需及时下载。
- **部署命名冲突**：创建部署时若 `deployed_model` 已存在，将返回 `Conflict` 错误，需添加唯一后缀。
- **容量约束**：`capacity` 必须是 `base_capacity` 的整数倍，且 `base_capacity` 由所选部署模板（如 `MU1`）的 `capacity_unit_per_instance` 决定，不可任意指定。
- **模型来源区分**：`list-deployable-models-api` 接口需显式指定 `model_source=custom` 才能列出用户调优模型，`base` 为默认系统模型。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [查询和管理部署](../../raw/model-api-reference/model-production/get-deployment-api.md)
- [列举可部署模型](../../raw/model-api-reference/model-production/list-deployable-models-api.md)
- [查询和管理调优任务](../../raw/model-api-reference/model-production/get-fine-tuning-job-api.md)


