# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署或运维模型，只需配置 API Key 和 Base URL 即可发起推理请求。本文档面向开发者，聚焦模型调用的核心路径与关键约束。

## 支持的模型与功能

百炼提供覆盖文本、多模态及细分领域的模型服务，包括：

- **千问系列旗舰模型**：`qwen3.7-max`（复杂任务首选）、`qwen3.7-plus`（效果/速度/成本均衡，[推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟高性价比）；
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分模型（如 DeepSeek）仅限华北2（北京）地域可用；
- **多模态能力**：文本生成、视觉理解、图像/视频生成、语音识别与合成、嵌入向量等；
- **领域专用模型**：长文本处理、法律、意图理解、角色扮演等。

> **注意**：文档中提及的 `qwen3.8-max-preview` 仅限 [Token](../concepts/token.md) Plan 订阅用户使用，而 `qwen3.7-max` 在多地可用，但 `qwen3.7-max-preview` 的 RPM 限流仅为 60（见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)），显著低于稳定版，生产环境应避免使用快照版本。

模型列表及地域支持详情请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

## 关键参数

调用模型需正确配置以下参数：

- **API Key**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并管理，不同地域的 Key 不通用；
- **Base URL**：必须与 API Key 所属地域及计费方案匹配：
  - **业务空间专属域名**（推荐用于生产）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
  - **Dashscope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**：如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅用于验证；
- **Model ID**：如 `"qwen3.7-plus"`，需与所选地域实际支持的模型一致（例如 `qwen-plus-us` 仅在美国地域有效）；
- **地域与服务部署范围**：影响数据存储位置、推理执行位置及合规性，详见 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建业务空间并获取 WorkspaceId；
- 创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（[详细步骤](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。

### 2. 调用示例（OpenAI SDK）
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(response.choices[0].message.content)
```

支持 Python、Node.js、curl 等多种调用方式，完整示例见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

### 3. SDK 选择
- **OpenAI Python SDK**：兼容 OpenAI 接口，迁移成本低；
- **DashScope Python SDK**：原生支持，提供更细粒度控制（如 `dashscope.base_http_api_url` 设置）。

## 限制和注意事项

- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。常见触发条件：
  - `Requests rate limit exceeded`：RPM（每分钟请求数）超限；
  - `Allocated quota exceeded`：TPM（每分钟 [Token](../concepts/token.md) 消耗）超限；
  - `Request rate increased too quickly`：瞬时请求激增触发保护。
  
  各模型 RPM/TPM 限值差异显著（如 `qwen3.7-plus` 北京地域为 30,000 RPM / 5,000,000 TPM，而 `qwen-plus-2025-07-28` 仅为 60 RPM / 1,000,000 TPM），详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

- **地域隔离**：各地域 Endpoint、API Key、模型列表、功能支持均独立（如批量推理仅北京/新加坡支持），不可混用；
- **域名鉴权**：业务空间专属域名仅允许对应 Workspace 的 API Key 调用；Dashscope 域名支持跨 Workspace，但限流额度共享；
- **费用控制**：
  - 新用户免费额度仅限华北2（北京）地域，用尽后可开启“免费额度用完即停”避免扣费；
  - 模型推理与[知识库](../concepts/knowledge-base.md)（RAG）计费相互独立，前者按 [Token](../concepts/token.md) 用量，后者按规格时长；
- **安全与合规**：所有传输数据加密，平台不会将用户数据用于模型训练（[隐私说明](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


