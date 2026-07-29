# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。本文档面向开发者，聚焦模型调用的核心路径，涵盖模型选择、参数配置、接入方式及关键限制。

## 支持的模型与功能

百炼提供覆盖多模态与多场景的模型服务，核心文本生成模型按能力与成本分层：

- **Qwen Max**：效果最优，适合复杂多步骤任务（如 `qwen3.7-max`）；
- **Qwen Plus**：效果、速度与成本均衡，是多数生产场景的**推荐选择**（如 `qwen3.7-plus`）；
- **Qwen Flash**：高性价比、低延迟，适用于简单响应类任务（如 `qwen3.7-flash`）。

此外支持 DeepSeek、Kimi、GLM 等第三方模型，以及长文本、法律、意图理解等细分领域模型。所有模型均支持文本生成、嵌入向量、多轮对话等基础能力；部分模型还支持视觉理解、图像生成等扩展能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：文档 3（`models.md`）中列出的 `qwen3.8-max-preview` 标注“仅 [Token](../concepts/token.md) Plan 可用”，但文档 1（`what-is-model-studio.md`）和文档 6（`rate-limit.md`）均未提及该模型在通用调用路径中的可用性，且其限流数据缺失。建议以控制台实时模型市场为准，避免依赖预览版 ID。

## 关键参数

调用模型必需以下三个参数，且必须严格匹配同一地域与计费方案：

- **API Key**：在[API Key 管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，**各地域独立，不可跨地域复用**；
- **Base URL**：决定接入点与服务保障等级，需与 API Key 所属地域及计费类型一致；
- **Model ID**：如 `qwen3.7-plus`，必须与 Base URL 所支持的模型列表一致（例如 `qwen3.7-max-preview` 仅在 [Token](../concepts/token.md) Plan 域名下可用）。

Base URL 分为三类：
- **业务空间专属域名**（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/...`，需先在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取 WorkspaceId，提供更高并发与 SLA（99.9%）；
- **Dashscope 域名**：如 `https://dashscope.aliyuncs.com/...`，兼容存量代码，但已不推荐用于新生产环境；
- **试用域名**：如 `https://trial.cn-beijing.maas.aliyuncs.com/...`，仅限快速验证，RPM 限流为 1000，**不提供 SLA** [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key；
- （北京/新加坡/东京/法兰克福地域）获取业务空间 ID（WorkspaceId）；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. SDK 调用示例（OpenAI 兼容）
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

支持 Python（OpenAI/DashScope SDK）、Node.js、curl 等多种方式，详见各语言示例 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国弗吉尼亚、德国法兰克福、日本东京）的 API Key、Base URL、模型列表、限流策略完全独立，**严禁混用**；
- **限流规则**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。主要限制为 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗），超出即返回 429 错误。稳定版模型（如 `qwen3.7-plus`）限流额度远高于快照版（如 `qwen-plus-2025-07-28`）；
- **Token Plan 与 Coding Plan 专用性**：Token Plan 和 Coding Plan 订阅用户必须使用其专属 Base URL（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/...`）和专属 API Key，**不可与按量付费 Key 混用**，否则报错 401；
- **免费额度控制**：新用户在北京地域享有免费额度，用尽后已认证用户自动转为按量付费；如需避免意外扣费，务必开启[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)开关；
- **批量推理限制**：仅华北2（北京）和新加坡地域支持批量推理（Batch API），美国、德国、日本地域当前不支持 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


