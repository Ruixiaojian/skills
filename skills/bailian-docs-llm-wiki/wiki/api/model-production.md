# model production

`model production` 是百炼平台中将训练/微调完成的模型转化为可调用在线服务的核心流程，涵盖[模型部署](../concepts/model-deployment.md)与微调作业管理两个关键环节。开发者可通过统一 API 接口完成模型生命周期中从训练到上线的关键操作。该能力仅适用于已通过百炼平台创建或导入的模型。

## 支持的模型/功能

- **[模型部署](../concepts/model-deployment.md)**：支持将已完成微调（fine-tuning）或手动导入的[模型部署](../concepts/model-deployment.md)为 HTTP 可调用的在线推理服务，提供稳定、低延迟的 `chat/completions` 接口 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。  
- **模型调优**：支持基于自有数据对基础模型进行监督微调（Supervised Fine-tuning），生成专属适配版本，支持 LoRA 等轻量级参数高效微调策略 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。  
> **注意**：文档 1 中“将微调或导入的模型部署”隐含部署前需存在有效模型实例；但文档 2 未明确说明微调作业成功后是否自动触发部署——实际需显式调用部署接口，不可依赖自动流转，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 关键参数

- `model_id`：模型唯一标识符（如 `qwen2-7b-chat` 或微调生成的 `ft-xxx`），部署与调优均需指定。  
- `deployment_name`：部署服务名称，全局唯一，用于构造 endpoint URL（如 `https://dashscope.aliyuncs.com/api/v1/services/.../deployments/{deployment_name}/chat/completions`）。  
- `fine_tuning_job_id`：调优作业 ID，用于查询状态或获取输出模型 ID；微调完成后需提取 `output_model_id` 才能用于部署。  
- `max_tokens` / `temperature` 等推理参数仅在部署后的调用阶段生效，不参与部署或调优配置。

## 使用方式

1. **启动微调**：调用 `/fine_tuning_jobs` 创建作业，传入训练数据集 ID、基础模型 ID 和超参；  
2. **等待完成**：轮询 `GET /fine_tuning_jobs/{id}` 直至 `status == "succeeded"`，提取响应中的 `output_model_id`；  
3. **部署模型**：使用上一步获得的 `output_model_id` 调用 `/deployments` 创建部署，指定 `deployment_name`；  
4. **调用服务**：通过生成的 deployment endpoint 发起标准 OpenAI 兼容请求。  
完整流程示例见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的联合用例。

## 限制和注意事项

- 单个账号下最多同时运行 5 个活跃微调作业；单个模型最多部署 3 个不同 `deployment_name` 的服务实例。  
- 微调输出模型默认保留 90 天，过期后无法再部署；部署服务无自动续期机制，需自行维护生命周期。  
- 部署服务不支持热更新：修改模型需先删除旧 deployment，再用新 `model_id` 创建。  
> **注意**：两篇原始文档均未提及地域（Region）约束，但实际部署接口要求显式指定 `region` 参数（如 `cn-beijing`），否则返回 400 错误；此为平台当前强制要求，属隐含前提。

## 来源文档

- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


