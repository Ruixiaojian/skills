# model deployment 1

阿里云百炼平台提供模型部署功能，支持将预置模型或调优后的模型部署为独立的、资源专享的推理服务，以满足高并发、低延迟等不同业务需求。部署方式涵盖控制台操作和 API/命令行调用，同时支持从 OSS 导入本地训练的 LoRA 模型进行部署。

> **注意**：本文档所述功能仅适用于"中国内地（北京）"地域。

## 支持的模型与功能

### 预置模型部署

平台支持多种预置模型的部署，涵盖以下类别（详见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)）：

- **文本生成**：千问系列（Qwen3.x、Qwen2.5）、DeepSeek 系列、GLM 系列、MiniMax、Kimi 等
- **多模态**：千问 VL 系列（视觉语言）、千问 Omni 系列
- **语音合成**：CosyVoice
- **图片/视频生成**：万相文本生成图像、悦动人像 EMO、舞动人像 AnimateAnyone

### 模型导入

支持将本地训练的 LoRA 模型从 OSS 导入到百炼平台（详见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)）。当前支持的基础模型包括：

| 模型系列 | 支持的模型 |
|---------|-----------|
| 千问3 | qwen3-32b、qwen3-14b、qwen3-8b、qwen3-4b-instruct-2507 |
| 千问3-VL | qwen3-vl-8b-instruct |
| 千问2.5 | qwen2.5-72b/32b/14b/7b-instruct |
| 千问2.5-VL | qwen2.5-vl-72b/7b-instruct |

导入限制：
- **仅支持 LoRA 模型**，不支持全参微调模型
- 必需文件：`adapter_model.safetensors` 和 `adapter_config.json`
- rank 值限定为 8、16、32 或 64
- 不支持修改过词汇表或 `chat_template` 的模型
- VL 模型必须冻结 VIT 部分

## 计费方式

平台提供三种主要计费方式，创建后**无法更改**，需下线后重新部署：

| 维度 | 预置吞吐（PTU） | 模型单元（MU） | Token 用量 |
|------|----------------|---------------|-----------|
| 定义 | 预留资源保障 TPM 吞吐 | 按时长与模型单元数量配置算力 | 按输入/输出 Token 计量 |
| 付费方式 | 随用随付/包天 | 随用随付/包月 | 随用随付 |
| 适用模型 | 部分预置模型 | 部分预置模型与所有调优后模型 | 部分 LoRA 调优后模型 |
| 扩缩容 | 自助增减吞吐量 | 自助增减模型单元数量 | 控制台提交申请，人工审核 |

此外，图片/视频生成模型采用**按实例时长计费**（后付费按小时 / 预付费包月）。

### 关键计费公式

- **预置吞吐**：`费用 = 使用时长 × (输入TPM单价 × 输入TPM + 输出TPM单价 × 输出TPM)`
- **模型单元**：`费用 = 使用时长(小时) × 模型单元数量 × 模型单元单价`
- **Token 用量**：`费用 = 输入Token数 × 输入单价 + 输出Token数 × 输出单价`

> **注意**：预置吞吐模式下，超出购买的 TPM 量时，调用将自动降级为按量付费模式，API 返回 Header 将包含 `x-dashscope-ptu-overflow:true`。

## 使用方式

### 控制台部署

1. 前往 [模型部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)
2. 选择模型、计费方式，设置模型名称
3. 等待部署状态变为**运行中**

### API/命令行部署

通过 HTTP API 进行部署，完整流程参见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

**前提条件**：已获取 API Key 并配置到环境变量。

#### 部署请求示例

**预置吞吐（PTU）**：

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

**模型单元（MU）**：

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
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

**Token 用量（LoRA）**：

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

> **注意**：LoRA 部署中 `capacity` 参数设置无效但必须填写；扩缩容需通过控制台提交申请。

#### 查询与管理

- **查询状态**：`GET /api/v1/deployments/{deployed_model}`，状态为 `RUNNING` 时部署完成
- **删除服务**：`DELETE /api/v1/deployments/{deployed_model}`，删除后立即停止计费且不可恢复

### 部署后调用

模型部署成功后，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope 接口及 Assistant SDK 调用。调用时 `model` 参数应使用部署后的模型 `code`（可在控制台获取）。

## 关键参数

### 模型单元部署配置

| 配置项 | 说明 |
|-------|------|
| 推理模式 | Instruct（非思考模式）/ Thinking（思考模式） |
| 最长上下文 | 部分模型支持，长度基于模型类型 |
| 服务限流 | 可限制 RPM、TPM |
| PD 分离模式 | 将 Prefill 和 Decode 拆分到不同计算节点，降低首 Token 延迟、提高吞吐 |

### 导入模型推理参数

导入模型与本地推理效果不一致时，建议调整以下参数以对齐 vLLM 默认值：

| 参数 | 推荐值 |
|------|-------|
| `temperature` | 1.0 |
| `top_p` | 1.0 |
| `top_k` | None 或 >100 |
| `presence_penalty` | 0 |
| `repetition_penalty` | 1.0 |

## 限制和注意事项

- **地域限制**：仅支持"中国内地（北京）"地域
- **计费不可切换**：服务创建后无法更改计费方式，需下线后重新部署
- **部署即计费**：执行部署命令后，即使未调用模型也会开始计费
- **预置吞吐**：预付费按天计费、无法提前退费；超出购买量自动降级为按量付费
- **模型单元**：后付费算力先到先得，购买不成功全额退款；预付费首月内提前退订日单价按 1.2 倍计费
- **Token 用量**：仅支持部分 LoRA 调优后模型；一个月内不使用将自动释放
- **后付费欠费**：部署资源保留并继续计费 24 小时后自动释放
- **模型导入**：OSS Bucket 不支持归档/冷归档存储类型；不支持访问 Bucket 根目录文件；首次导入需完成 OSS 服务关联角色授权并添加 `bailian-datahub-access` 标签
- **权限要求**：API Key 的归属业务空间需有模型部署权限，归属账号需在对应业务空间中有操作权限

## 来源文档

- [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)

