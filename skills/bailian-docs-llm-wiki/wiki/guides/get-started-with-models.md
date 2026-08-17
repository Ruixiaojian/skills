# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦模型调用的核心路径，涵盖模型选型、参数配置、接入方式及关键约束。

## 支持的模型与功能

百炼提供多模态、多场景的模型服务，覆盖文本生成、视觉理解、语音合成等能力。核心文本模型按性能-成本-延迟三角进行分层：

- **旗舰模型**：`qwen3.8-max`（效果最优，适合复杂多步任务），文档明确推荐为当前最新主力版本 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **均衡模型**：`qwen3.7-plus`（效果、速度与成本平衡，多数场景的**推荐选择**）；
- **轻量模型**：`qwen3.7-flash`（高性价比、低延迟，适合简单响应场景）。

此外，平台还支持 DeepSeek、Kimi、GLM 等第三方模型（如 `deepseek-v4-pro-0813`），但部分模型地域受限（例如 DeepSeek 仅支持北京地域）[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。所有模型均按地域独立发布，各地域支持的模型列表、上下文长度及价格详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.7-plus` 和 `qwen3.7-flash` 模型 ID 与文档 1 中强调的 `qwen3.8-max` 存在版本代际差异；实际使用应以控制台最新模型市场为准，`qwen3.8-max` 为当前推荐旗舰型号，旧版 `qwen3.7-*` 系列已逐步被替代。

## 关键参数

调用模型必需以下参数，缺一不可：

- **API Key**：在 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，需与 Base URL 所属地域和计费方案严格匹配；
- **Base URL**：决定接入点、限流策略与 SLA，必须与 API Key 同一计费方案（如按量付费 Key 不可搭配 [Token](../concepts/token.md) Plan 域名）。业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）为生产环境推荐选项，提供更高并发与隔离性 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
- **WorkspaceId**：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域必需，在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面获取；美国（弗吉尼亚）地域部分模型（如 `qwen-plus-us`）则通过模型后缀限定部署范围，无需显式 WorkspaceId [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **Model ID**：必须与所选地域支持的模型完全一致（如 `qwen3.8-max` 在北京可用，在新加坡亦可用但限流值不同），不支持跨地域通用模型名。

## 使用方式

### 1. 环境准备
- 完成阿里云账号实名认证并开通百炼服务；
- 创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（避免硬编码泄露）；
- 获取对应地域的 WorkspaceId（如适用）。

### 2. SDK 调用（OpenAI 兼容）
使用 OpenAI Python SDK 时，仅需替换 `base_url` 和 `model` 参数即可迁移现有代码：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为真实 WorkspaceId
)
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
```
完整示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 多协议支持
除 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)外，百炼同时支持 Anthropic 兼容（`/apps/anthropic`）和 DashScope 原生接口（`/api/v1`），各协议 Base URL 独立，需按需选用 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

## 限制和注意事项

- **地域隔离**：各地域的 API Key、Base URL、模型列表完全独立，**不可混用**。例如北京地域的 Key 无法调用新加坡地域的模型 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **动态限流**：`qwen3.8-max` 等主力模型采用动态 TPM 限流，额度按账号月消费金额分档（如北京地域 ≤10w 档为 500 万 TPM），每月 15 日自动生效 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。该机制为“软限流”，实际可用 TPM 可能高于档位值。
- **硬性限流**：除动态限流外，所有模型均有基础 RPM/TPM 上限（如北京 `qwen3.8-max` 默认 30,000 RPM / 5,000,000 TPM），超出即返回 429 错误 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **域名与 SLA 差异**：试用域名（`trial.*`）RPM 仅为 1000，且无 SLA 保障；业务空间专属域名提供 99.9% SLA 和 3600 秒超时，而 Dashscope 域名超时仅 600 秒 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **数据隐私承诺差异**：按量付费和 [Token](../concepts/token.md) Plan 团队版承诺“不使用客户数据训练模型”，但 [Token](../concepts/token.md) Plan 个人版与 Coding Plan 明确说明输入/输出内容将用于服务优化，使用前须审阅条款 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


