# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、模型微调与部署等全链路能力，适用于从快速验证到生产级落地的各类场景。

## 支持的模型与功能

百炼提供文本生成、多模态理解与生成、嵌入向量、领域专用模型（如法律、意图识别、长文本处理）等能力。核心模型包括：

- **千问系列**：`qwen3.7-max`（效果最优，适合复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，**推荐首选**）、`qwen3.7-flash`（高性价比、低延迟）；  
- **第三方模型**：DeepSeek、Kimi、GLM 等（部分模型仅限特定地域，如 DeepSeek 仅支持华北2（北京））；  
- **预览与快照版本**：如 `qwen3.7-max-preview`、`qwen3.7-plus-2025-07-28` 等，适用于灰度验证，但限流更严格（见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）。

> **注意**：文档中多次提及 `qwen3.7-plus` 为“推荐选择”，但[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)文档显示 `qwen3.8-max-preview` 已上线且标注“仅 [Token](../concepts/token.md) Plan 可用”，而 `qwen3.7-max` 在多个地域仍为最高能力稳定版。实际选型应以控制台实时模型列表为准，避免依赖过时快照名。

除基础推理外，平台还支持：
- 可视化智能体（Agent）与工作流编排；
- RAG 知识库接入与插件/MCP 外部服务调用；
- 模型微调（SFT/DPO）、专属部署与自动评测。

## 关键参数

### Base URL
必须与所选地域和计费方案匹配，**不可跨地域混用**。常见组合如下（以华北2（北京）为例）：

| 类型 | OpenAI 兼容地址 | 说明 |
|------|----------------|------|
| **业务空间专属域名（推荐）** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 需在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)中获取 `WorkspaceId`；提供更高吞吐、更低时延与流量隔离 |
| **DashScope 域名（存量兼容）** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 支持跨业务空间调用，但建议迁移至专属域名 |
| **试用域名** | `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | RPM 限流为 1000，仅用于临时验证 |

其他地域对应域名详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。美国（弗吉尼亚）等部分地域不支持业务空间专属域名，需使用 `dashscope-us.aliyuncs.com` 等中心化域名。

### API Key
- 通过 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建；
- **必须与 Base URL 所属地域一致**（例如北京地域的 Key 不能用于新加坡域名）；
- 强烈建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码（参见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。

### 模型 ID
- 使用标准模型名（如 `qwen3.7-plus`），而非快照名（如 `qwen3.7-plus-2025-07-28`），除非有明确版本控制需求；
- 不同地域支持的模型可能不同（如 DeepSeek 仅北京可用），需在[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)确认。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key 并配置环境变量；
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope SDK）。

### 2. 发起请求（OpenAI 兼容示例）
```python
import os
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

> **注意**：[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)中给出的示例代码使用 `qwen3.7-plus`，但[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)示例中使用 `qwen-plus` —— 后者为旧版命名，当前应统一使用 `qwen3.7-plus` 等新版 ID，避免调用失败。

### 3. 其他接入方式
- **curl**：直接构造 HTTP POST 请求，Header 包含 `Authorization: Bearer $DASHSCOPE_API_KEY`；
- **DashScope SDK**：使用 `dashscope.Generation.call()`，Base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`；
- **Anthropic 兼容接口**：Base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`。

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：主账号下所有子账号、业务空间、API Key 的调用量合并计算；
- **双维度限制**：每分钟请求数（RPM）和每分钟 [Token](../concepts/token.md) 消耗（TPM），任一超限即拒绝请求；
- **典型值**（华北2（北京））：
  - `qwen3.7-plus`：30,000 RPM / 5,000,000 TPM；
  - `qwen3.7-plus-2025-07-28`：60 RPM / 1,000,000 TPM（快照版限流显著更严）；
- **恢复时间**：通常 60 秒内自动恢复；
- **规避建议**：选用稳定版模型、平滑请求速率、设置备选模型重试（参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)中的示例代码）。

### 地域与功能约束
- **批量推理**：仅华北2（北京）和新加坡支持，美国、德国、日本暂不支持；
- **模型调优与应用开发**：仅华北2（北京）支持，其他地域不可用；
- **[Token](../concepts/token.md) Plan / Coding Plan**：专属域名与 API Key，**不可与按量付费混用**（如 Coding Plan 必须使用 `coding.dashscope.aliyuncs.com/v1`）。

### 安全与计费
- 数据全程加密传输，阿里云**不会将用户数据用于模型训练**；
- 模型推理与知识库（RAG）**独立计费**：前者按 Token 用量，后者按规格时长+调用次数；
- 新用户享北京地域免费额度，用完后可开启“免费额度用完即停”避免意外扣费（参见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


