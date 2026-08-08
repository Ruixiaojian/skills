# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可开始集成。平台同时支持可视化应用构建、模型微调与部署等进阶能力，覆盖从快速验证到生产落地的完整链路。

## 支持的模型/功能

百炼提供多模态、多场景的模型服务，包括文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等。核心文本模型按能力与成本分层：

- **qwen3.8-max**：旗舰模型，适合复杂多步骤任务；[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)明确指出其“推理能力全面超越前代，推荐选用”。
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的**推荐选择**。
- **qwen3.7-flash**：高性价比、低延迟，适用于简单高频任务。

此外，平台还集成 DeepSeek、Kimi、GLM 等第三方模型（DeepSeek 仅支持北京地域），并提供长文本、法律、翻译、意图理解等细分领域模型。所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、Anthropic 兼容接口及 DashScope 原生 SDK 调用。详细模型列表与地域支持情况请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 5 中列出的 `qwen-plus-2025-07-14` TPM 限流值为 `100,000`，而文档 4 中动态限流机制下同地域同档位的 `qwen3.8-max` 最低档位为 `500w`，二者量级差异巨大。实际限流策略以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 文档为准——该机制已取代静态限流成为 Qwen-3.x 系列主力模型的默认策略，文档 5 中的静态数值仅适用于部分快照版本或非动态限流模型。

## 关键参数

调用模型需正确配置以下关键参数：

- **API Key**：在 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，不同地域 Key 不通用。
- **Base URL**：必须与 API Key 所属地域及计费方案匹配。推荐使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与业务空间级隔离；Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）仍可用但建议迁移；试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）限流严格，仅用于验证。详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **WorkspaceId**：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域必需，在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取；美国（弗吉尼亚）地域使用 `dashscope-us.aliyuncs.com`，无需 WorkspaceId。
- **模型 ID**：如 `"qwen3.8-max"`，需与所选地域支持的模型一致（例如 DeepSeek 仅在北京地域可用）。

## 使用方式

1. **开通与准备**  
   使用阿里云主账号开通百炼服务，完成实名认证，并在控制台创建 API Key 与业务空间（如需）。

2. **环境配置**  
   将 `DASHSCOPE_API_KEY` 配置为环境变量（避免硬编码），参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 Linux/macOS/Windows 配置指南。

3. **代码调用（OpenAI SDK 示例）**  
   ```python
   import os
   from openai import OpenAI

   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
   )

   completion = client.chat.completions.create(
       model="qwen3.8-max",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   print(completion.choices[0].message.content)
   ```

4. **其他接入方式**  
   支持 Node.js SDK、curl、DashScope Python SDK 及 Anthropic 兼容接口。批量推理（Batch API）适用于非实时场景，且不受实时 RPM/TPM 限流约束。

## 限制和注意事项

- **地域隔离**：各地域 Endpoint、API Key、模型列表、价格及功能均独立，不可混用。例如德国（法兰克福）不支持 Dashscope 域名，美国（弗吉尼亚）暂不支持业务空间专属域名。
- **限流机制**：Qwen-3.8 等主力模型采用 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 配额按账号月消费金额分档（如北京地域 ≤10w 档为 500w TPM），每月 15 日生效；而部分快照模型（如 `qwen3.7-max-2026-05-20`）仍沿用静态限流（文档 5）。触发限流时错误码为 `429`，常见原因包括 RPM/TPM 超限或请求速率激增（`Request rate increased too quickly`）。
- **费用控制**：模型调用按 [Token](../concepts/token.md) 用量计费，知识库（RAG）单独计费；新用户享有北京地域免费额度，可开启“免费额度用完即停”避免意外扣费；生产环境务必使用业务空间专属域名并监控 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 数据（调用后约一小时可见）。
- **安全与合规**：平台不会使用客户数据训练模型，所有传输数据加密；建议始终使用 HTTPS 并避免在代码中硬编码 API Key。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


