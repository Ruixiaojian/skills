# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、微调与部署等进阶能力，覆盖从快速验证到生产落地的完整链路。

## 支持的模型与功能

百炼提供[多模态](../concepts/multimodal.md)、多场景的模型服务，核心包括：

- **千问（Qwen）旗舰系列**：`qwen3.8-max`（效果最优，推荐用于复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，多数场景首选）、`qwen3.7-flash`（低延迟、高性价比，适合简单响应）；[详见模型列表](https://help.aliyun.com/zh/model-studio/models)。
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型地域受限（如 DeepSeek 仅支持华北2（北京））。
- **[多模态](../concepts/multimodal.md)能力**：文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等。
- **领域增强模型**：长文本处理、法律、意图理解、角色扮演、数据挖掘等细分方向专用模型。

> **注意**：文档中 `qwen3.8-max` 被多次强调为“最新旗舰”，但 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中列出的最新稳定版实为 `qwen3.7-plus` 和 `qwen3.7-flash`；`qwen3.8-max` 在多个示例中出现，但未在限流表（文档5）或地域支持表（文档7）中明确标注其部署范围与限流值，需以控制台实时模型市场为准。

## 关键参数

调用模型必需配置以下参数，且必须匹配同一计费方案与地域：

- **API Key**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，不同地域 Key 不通用。
- **Base URL**：决定接入点与服务保障等级，有三类：
  - **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需先在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 WorkspaceId；
  - **Dashscope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**（仅限验证）：如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，RPM 限流仅为 1000。
- **Model ID**：如 `"qwen3.7-plus"`，必须与 Base URL 所属地域和计费方案（如 Coding Plan、[Token](../concepts/token.md) Plan）兼容；[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档提供了各模型在不同地域的完整 Base URL 映射。

## 使用方式

1. **开通与准备**  
   - 注册阿里云账号并完成实名认证；
   - 开通百炼服务，创建业务空间（非北京/新加坡地域必需）；
   - 在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建 Key，并按 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 文档配置为环境变量（如 `DASHSCOPE_API_KEY`）。

2. **代码调用（OpenAI SDK 示例）**  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   ```

3. **其他方式**  
   - CLI：使用 `curl` 直接调用（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）；
   - 可视化：通过控制台 [模型体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text) 页面零代码测试；
   - 高级场景：批量推理（Batch API）、模型微调、知识库（RAG）集成等，参见对应功能文档。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国、德国、日本）Endpoint、API Key、模型列表、价格、功能均独立，**不可混用**；跨地域调用将返回 401 或 404。
- **限流机制**：
  - 默认按主账号维度限制 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗），例如 `qwen3.7-plus` 在北京地域为 30,000 RPM / 5,000,000 TPM；
  - 部分模型（如 `qwen3.8-max`）采用 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 档位随月消费金额自动调整（如 ≤10 万档为 500w TPM）；
  - 试用域名 RPM 固定为 1000，不建议用于压测或生产。
- **安全与合规**：所有传输数据加密，平台**不会使用用户数据训练模型**；静态数据存储于所选地域，符合本地合规要求。
- **费用控制**：新用户享北京地域免费额度；可开启“免费额度用完即停”避免意外扣费；建议通过 [额度管理](https://bailian.console.aliyun.com/#/efm/quota-management) 页面监控实时限流值。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


