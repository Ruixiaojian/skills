# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。本文档面向开发者，聚焦模型调用的核心路径与关键约束。

## 支持的模型与功能

百炼提供多模态、多场景的模型服务，覆盖文本生成、视觉理解、语音合成等能力。主力文本模型按能力与成本分层：

- **qwen3.7-max**：效果最强，适合复杂多步任务；[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)明确推荐其为“Qwen 系列效果最好的模型”。
- **qwen3.7-plus**：效果、速度与成本均衡，是多数生产场景的**推荐选择**；该结论在[原文标题](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)中被直接强调。
- **qwen3.6-flash**：高性价比、低延迟，适用于简单、高频响应任务。

此外，平台还支持 DeepSeek、Kimi、GLM 等第三方模型（DeepSeek 仅限北京地域），以及长文本、法律、意图理解等细分领域模型。所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope SDK 和 Anthropic 兼容接口三种调用方式。

> **注意**：文档 3 中列出的 `qwen3.8-max-preview` 标注“仅 Token Plan 可用”，但文档 1 和文档 6 均未提及该模型，且文档 6 的限流表格中无此型号。该模型当前状态存疑，建议以控制台实际可用模型列表为准，避免依赖预览版 ID。

## 关键参数

调用模型需正确配置以下核心参数：

- **API Key**：必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，且**按地域独立管理**，不可跨地域复用。
- **Base URL**：决定接入点与服务边界，必须与 API Key 所属地域严格匹配。支持三类域名：
  - **业务空间专属域名**（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需提前在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)中获取 WorkspaceId；
  - **Dashscope 域名**（兼容旧版）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**：`https://trial.{region}.maas.aliyuncs.com/compatible-mode/v1`，仅限临时验证，RPM 限流为 1000，不建议用于生产。
- **模型 ID**：如 `"qwen3.7-plus"`，必须与所选地域实际支持的模型一致（参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key；
- 获取业务空间 ID（仅北京、新加坡、东京、法兰克福地域需要）；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量（[原文标题](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)详细说明了 Linux/macOS/Windows 各系统配置方法）。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

### 3. 多地域适配
不同地域使用独立 Base URL（详见[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）：
- 北京：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`dashscope-us.aliyuncs.com`（无 WorkspaceId）
- 德国（法兰克福）/日本（东京）：需在业务空间中显式选择服务部署范围（欧盟/日本）

## 限制和注意事项

- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。限流分 RPM（每分钟请求数）和 TPM（每分钟 Token 消耗）两维，超出任一即拒绝请求。例如 `qwen3.7-plus` 在北京地域默认限流为 RPM=30,000 / TPM=5,000,000，而快照版本（如 `qwen-plus-2025-07-28`）仅为 RPM=60 / TPM=1,000,000。
- **地域隔离**：API Key、Base URL、模型列表、监控数据均**不可跨地域混用**。文档 4 明确指出：“每个地域有独立的接入域名、API Key 和模型列表，不能跨地域混用”。
- **费用控制**：模型调用按 Token 用量实时计费。新用户享有北京地域免费额度，用尽后自动转为按量付费；如需规避意外扣费，可开启“免费额度用完即停”开关（仅限北京地域）。
- **安全与合规**：所有传输数据全程加密，平台**不会将用户数据用于模型训练**；数据存储位置由所选地域决定，需根据合规要求选择服务部署范围（如中国内地、欧盟、美国等）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


