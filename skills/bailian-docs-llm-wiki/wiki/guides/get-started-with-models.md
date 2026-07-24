# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 API 快速调用千问（Qwen）及第三方模型。本文面向开发者，聚焦模型调用的核心路径：从环境准备、模型选择到实际请求，涵盖关键参数、地域适配与常见限制。

## 支持的模型与功能

百炼提供覆盖文本、[多模态](../concepts/multi-modal.md)及领域专用的模型服务，核心为千问系列（`qwen3.x-max`/`plus`/`flash`），并支持 DeepSeek、Kimi、GLM 等第三方模型 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型按能力与成本分层：

- **`qwen3.7-max`**：效果最优，适合复杂多步任务；
- **`qwen3.7-plus`**：效果、速度与成本均衡，**推荐作为多数场景的默认选择**；
- **`qwen3.6-flash`**：高性价比、低延迟，适用于简单快速响应任务。

所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope SDK 及 Anthropic 兼容协议，并覆盖文本生成、嵌入向量、视觉理解等能力 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 2 中示例使用 `qwen3.7-plus`，而文档 1 的 Python 示例中使用 `qwen-plus`（旧版命名）。实际调用应以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 页面列出的最新模型 ID 为准，如 `qwen3.7-plus`，避免使用已下线或限流更严的快照版本（如 `qwen-plus-2025-07-28`）。

## 关键参数

调用模型需配置以下三项核心参数，缺一不可：

- **`DASHSCOPE_API_KEY`**：在 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，**必须与 Base URL 所属地域匹配**，跨地域使用将返回 401 错误。
- **`base_url`**：模型服务接入地址，格式取决于地域与域名类型：
  - 业务空间专属域名（**生产环境推荐**）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
  - DashScope 域名（兼容存量）：如华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；
  - 各地域完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **`model`**：模型 ID，例如 `"qwen3.7-plus"`，必须与所选地域支持的模型一致（如 DeepSeek 仅支持北京地域）。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台获取 API Key 和业务空间 ID；
- **强烈建议**将 `DASHSCOPE_API_KEY` 配置为系统环境变量，避免硬编码泄露风险 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. SDK 选择与调用
支持 OpenAI Python SDK 或 DashScope Python SDK：

**OpenAI SDK 示例（推荐）**
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

**DashScope SDK 示例**
```python
from dashscope import Generation
import os

# 注意：DashScope SDK 使用不同 base_url 格式
import dashscope
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
    result_format="message"
)
```

其他语言（Node.js、curl）和可视化工具（Chatbox）详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，**不可跨地域混用**。例如北京地域的 Key 无法调用新加坡地域的模型 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **限流策略**：按主账号维度合并计算 RPM（每分钟请求数）与 TPM（每分钟 [Token](../concepts/token.md) 数），超出即返回 429。`qwen3.7-plus` 在北京地域默认限流为 30,000 RPM / 5,000,000 TPM，而快照版本（如 `qwen-plus-2025-07-28`）仅为 60 RPM / 1,000,000 TPM [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **域名与 SLA 差异**：业务空间专属域名提供 3600 秒超时、99.9% SLA 及更高并发；DashScope 域名超时为 600 秒；试用域名限流严格（RPM=1000），**严禁用于生产环境** [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **费用控制**：调用按量计费，新用户享有北京地域免费额度。为避免意外扣费，建议开启“免费额度用完即停”或设置消费告警 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


