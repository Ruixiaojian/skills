# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。本文档面向开发者，聚焦模型调用的核心路径与关键约束。

## 支持的模型与功能

百炼提供文本生成、[多模态](../concepts/multimodal.md)理解与生成、嵌入向量、领域专用模型（如法律、意图识别、长文本处理）等能力。主力模型包括：

- **Qwen 系列**：`qwen3.8-max`（效果最优，推荐用于复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，[官方文档明确标注为多数场景的推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟、高性价比，适合简单响应）。
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型（如 DeepSeek）仅限华北2（北京）地域使用 [详见模型选择页](../../raw/model-user-guide/get-started-with-models/models.md)。
- **接入协议**：同时支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、Anthropic 兼容接口和 DashScope 原生 SDK，满足不同技术栈需求。

> **注意**：文档 7 中 `qwen3.8-max` 在华北2（北京）的 RPM/TPM 限流值为 `30,000 / 5,000,000`，而文档 3 中同模型在相同地域的动态 TPM 限流档位为 `500w / 1000w / 2000w`（对应月消费 ≤10w / (10w,100w] / >100w）。二者不矛盾：文档 7 给出的是**基础静态限流值**，文档 3 描述的是**基于消费档位的动态软限流机制**，实际可用 TPM 不低于该档位值，且可能更高。开发者应以控制台实时额度为准。

## 关键参数

调用模型必需的三个核心参数为：

- **API Key**：在 [API Key 管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，需按地域单独获取，**不可跨地域复用**。
- **Base URL**：决定接入点与服务范围。必须与 API Key 所属地域及计费方案严格匹配：
  - **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需先在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 `WorkspaceId`。
  - **Dashscope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）。
  - **试用域名**：如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅用于快速验证。
  - 更多细节请参考 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **Model ID**：如 `qwen3.8-max`，必须与所选地域支持的模型列表一致。各地域模型可用性不同，例如德国（法兰克福）和日本（东京）地域暂不支持模型调优与应用开发功能 [参见地域文档](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

1. **开通与准备**：注册阿里云账号 → 实名认证 → 开通百炼服务 → 创建 API Key → （如需业务空间专属域名）创建并获取 WorkspaceId。
2. **环境配置**：将 `DASHSCOPE_API_KEY` 配置为系统环境变量（[详细步骤见首次调用指南](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)），避免硬编码。
3. **发起请求**：使用 OpenAI Python SDK（推荐）或 DashScope SDK，示例代码如下（北京地域，`qwen3.8-max`）：
   ```python
   import os
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   completion = client.chat.completions.create(
       model="qwen3.8-max",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   print(completion.choices[0].message.content)
   ```
4. **调试与监控**：调用后约一小时，可在 [模型监控页面](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看 [Token](../concepts/token.md) 消耗、成功率等指标。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国、德国、日本）的 API Key、Base URL、模型列表、功能支持均相互独立，**严禁混用**。例如，北京地域的 Key 无法调用新加坡地域的模型。
- **限流机制**：
  - 默认按主账号维度聚合所有子账号、业务空间、API Key 的调用量，对 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）进行限制。
  - 部分模型（如 `qwen3.8-max`）采用动态限流，TPM 基线随百炼月消费金额自动提升，但需注意该机制仅适用于特定地域（如北京、新加坡），且不支持自助提额 [参考动态限流文档](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
  - 触发限流时错误码为 `429`，常见原因包括 `Requests rate limit exceeded`（RPM 超限）、`Allocated quota exceeded`（TPM 超限）或 `Request rate increased too quickly`（瞬时爆发）。应对策略包括平滑请求速率、添加备选模型、拆分大任务或使用 Batch API（不受实时限流约束）。
- **费用与安全**：
  - 百炼本身开通免费，但模型调用、微调、部署均按量计费。新用户享有北京地域专属免费额度，用完后已认证用户自动转为按量付费，未认证用户则停止服务。
  - 所有传输数据全程加密，阿里云承诺**不会将用户数据用于模型训练**，符合隐私合规要求。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


