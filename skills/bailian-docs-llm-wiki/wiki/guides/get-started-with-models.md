# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署和运维模型，只需配置 API Key 和 Base URL 即可发起推理请求。平台同时支持可视化应用构建、微调与部署等全链路能力，适用于从快速验证到生产级落地的各类场景。

## 支持的模型与功能

百炼提供自研千问（Qwen）全系列模型及 DeepSeek、Kimi、GLM 等主流第三方模型，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解与生成、嵌入向量、领域专用模型（如法律、意图识别、长文本）等能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。核心模型按定位分为三档：

- **qwen3.8-max**：效果最优，适合复杂多步任务；最新版本推理能力全面超越前代，推荐选用；
- **qwen3.7-plus**（或 `qwen-plus`）：效果、速度与成本均衡，是多数场景的**推荐选择**；
- **qwen3.7-flash**（或 `qwen-flash`）：高性价比、低延迟，适合简单任务与高频响应场景。

此外，平台支持多种接入协议（OpenAI 兼容、Anthropic 兼容、DashScope 原生），并提供智能体构建、RAG 知识库、[插件](../concepts/plugin.md)扩展、流程编排等应用层能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：文档中 `qwen3.8-max` 与 `qwen3.7-plus` 的命名存在版本演进不一致问题。[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档列出的是 `qwen3.8-max` 和 `qwen3.7-plus`，而 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中大量使用 `qwen3.7-max`、`qwen3.6-plus` 等旧版命名。实际调用应以控制台「模型广场」当前可用模型 ID 为准，建议优先选用无日期后缀的稳定版（如 `qwen3.8-max`、`qwen3.7-plus`），避免使用带时间戳的快照版本（如 `qwen-plus-2025-07-28`），因其限流额度显著更低（仅 60 RPM / 1M TPM）。

## 关键参数

调用模型需配置以下关键参数：

- **API Key**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，用于身份鉴权。不同地域的 API Key **不通用**，且必须与对应地域的 Base URL 配套使用，否则返回 401 错误。
- **Base URL**：模型服务入口地址，决定接入点、流量隔离与 SLA 保障。推荐使用**业务空间专属域名**（格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），其具备更高并发、3600 秒超时及 99.9% SLA；Dashscope 域名（如 `dashscope.aliyuncs.com`）为存量兼容方案，试用域名（`trial.*`）仅限临时验证 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **WorkspaceId**：业务空间唯一标识，仅在使用业务空间专属域名时必需，可在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取。华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）均需此参数，但美国地域部分模型（如 `qwen-plus-us`）还要求模型名显式带 `-us` 后缀以限定境内推理 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **model**：模型 ID，如 `"qwen3.8-max"`，需与所选地域支持的模型列表一致。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（避免硬编码）；
- 获取业务空间 ID（WorkspaceId），用于构造 Base URL。

### 2. 调用示例（OpenAI SDK）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId 和地域
)
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```
支持 Python、Node.js、curl 等多种调用方式，详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 多地域适配
各地域 Base URL 格式统一，仅 region 和域名后缀不同：
- 华北2（北京）：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 德国（法兰克福）：`{WorkspaceId}.eu-central-1.maas.aliyuncs.com`
- 日本（东京）：`{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`{WorkspaceId}.us-east-1.maas.aliyuncs.com`

> **注意**：文档 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中列出的美国地域 Base URL 示例为 `https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`，而 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 明确指出美国地域 Dashscope 域名已“不支持”，仅业务空间专属域名有效。因此，美国地域**必须使用业务空间专属域名**，不可使用 `dashscope-us.aliyuncs.com`（该域名在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中出现，但已被 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 官方标记为弃用）。

## 限制和注意事项

- **限流机制**：按主账号维度对模型调用实施 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗）双重限制，账号下所有子账号、业务空间、API Key 的调用量合并计算。`qwen3.8-max` 等主力模型采用**动态限流**，TPM 额度随百炼月消费金额分档提升（如北京地域 ≤10w 档为 500w TPM，(10w, 100w] 档为 1000w TPM），且实际可用值可能高于档位值 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。非动态限流模型（如快照版）有固定硬限流（如 `qwen-plus-2025-07-28` 仅 60 RPM），需谨慎选用。
- **地域隔离**：API Key、Base URL、模型列表均按地域独立，**严禁跨地域混用**。例如北京地域的 Key 无法调用新加坡地域的模型。
- **费用控制**：免费额度仅限华北2（北京）地域新用户，用完后自动转为按量付费；可通过开启「免费额度用完即停」开关实现主动熔断，或订阅 Coding Plan 实现固定月费 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **安全与合规**：所有传输数据加密，阿里云承诺不将用户数据用于模型训练 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


