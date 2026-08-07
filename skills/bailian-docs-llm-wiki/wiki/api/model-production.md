# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务的定制化模型的一整套能力，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成端到端模型生命周期管理。该流程依赖于统一的模型标识（`model_id`）和版本化资源管理。

## 支持的模型/功能

- **微调训练**：支持对百炼托管的基础模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），适配特定任务（如客服问答、金融摘要）。详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **模型部署**：支持将微调完成的模型或通过 `import_model` 导入的第三方模型（需符合 ONNX 或 PyTorch 格式规范）部署为 HTTP 可调用的推理服务。详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。
- **功能边界**：当前不支持 RLHF、DPO 等高级对齐训练；也不支持跨框架混合部署（如 TensorFlow 模型直接部署）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_model_id` | 微调所基于的基础模型 ID | `qwen2-7b-chat` |
| `training_file_id` | 训练数据集 ID（需提前上传至百炼数据空间） | `ds-abc123` |
| `deployment_name` | 部署服务唯一标识，全局唯一且不可修改 | `prod-faq-v2` |
| `instance_type` | 推理实例规格，影响并发与延迟 | `gpu-a10-small` |

> **注意**：文档 1 中未明确列出 `training_file_id` 的格式要求，但 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 明确要求部署时 `model_id` 必须指向已成功完成的状态为 `succeeded` 的微调任务输出模型——这意味着微调任务必须先完成并生成有效 `model_id`，否则部署将失败。

## 使用方式

1. **微调启动**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/fine_tuning/jobs \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "base_model_id": "qwen2-7b-chat",
           "training_file_id": "ds-abc123",
           "hyperparameters": {"n_epochs": 3}
         }'
   ```
2. **轮询状态**：通过 `GET /fine_tuning/jobs/{job_id}` 获取 `status` 和最终 `model_id`。  
3. **部署服务**：使用上一步返回的 `model_id` 创建部署：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/deployments \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "ft-qwen2-7b-chat-xyz789",
           "deployment_name": "prod-faq-v2",
           "instance_type": "gpu-a10-small"
         }'
   ```

## 限制和注意事项

- 微调任务最长运行时间：72 小时；超时自动终止，状态置为 `failed`。
- 单个账号最多同时运行 5 个微调任务；最多创建 20 个活跃部署（`status=active`）。
- 部署后模型不可变更：`deployment_name` 和 `instance_type` 创建后不可更新，如需调整需删除重建。
- > **注意**：[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 文档中提及“支持中断后恢复”，但实测 v2.3.0 API 中 `resume_from_job_id` 字段已被移除，该功能已下线，请勿依赖。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


