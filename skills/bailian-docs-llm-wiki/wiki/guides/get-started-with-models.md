# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦模型调用的核心路径，涵盖模型选择、参数配置、接入方式及关键约束。

## 支持的模型与功能

百炼提供文本生成、多模态理解与生成、嵌入向量、领域专用模型等能力，覆盖通用推理与垂直场景。主力模型包括：

- **qwen3.7-max**：效果最优，适用于复杂多步任务，[详见模型详情](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/detail/qwen3.7-max)  
- **qwen3.7-plus**：效果、速度与成本均衡，是多数生产场景的**推荐选择**（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）  
- **qwen3.7-flash**：高性价比、低延迟，适合简单高频任务  

此外支持 DeepSeek、Kimi、GLM 等第三方模型（仅限北京地域），以及长文本、法律、意图识别等细分领域模型。所有模型均按地域独立提供，不同地域支持的模型列表存在差异，例如 `qwen3.7-max-preview` 仅限 [Token](../concepts/token.md) Plan 用户且仅在华北2（北京）可用（见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）。

> **注意**：文档1中称“DeepSeek 仅支持北京地域”，而文档4的模型列表页未明确标注地域限制，但实际控制台界面显示其仅在北京地域可见。以控制台实时状态为准。

## 关键参数

调用模型需明确以下核心参数：

- **`model`**：模型 ID，如 `"qwen3.7-plus"`；注意带日期后缀的快照版本（如 `qwen-plus-2025-07-28`）限流更严格（见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）  
- **`base_url`**：必须与所选地域和计费方案匹配，**不可跨地域混用**（见 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）。常用格式如下：
  - 业务空间专属（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`  
  - Dashscope 兼容（存量迁移）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）等  
- **`api_key`**：必须使用与 `base_url` 所属地域和计费方案（按量付费 / [Token](../concepts/token.md) Plan / Coding Plan）配套的 API Key，否则返回 401 错误（见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）

## 使用方式

### 1. 前置准备
- 注册阿里云账号并完成实名认证  
- 开通百炼服务，在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建 Key  
- 若使用业务空间专属域名，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 `WorkspaceId`

### 2. 配置与调用
推荐将 `DASHSCOPE_API_KEY` 设为环境变量（避免硬编码），再使用 OpenAI SDK 或 DashScope SDK 调用：

```python
# OpenAI SDK 示例（兼容模式）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)
response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
```

完整步骤与多语言（Node.js/curl）示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

- **地域隔离**：各地域 API Key、Base URL、模型列表、功能支持均相互独立。例如德国（法兰克福）不支持批量推理，美国（弗吉尼亚）暂无业务空间专属域名（见 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）  
- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。触发限流时返回 `429`，常见原因包括 RPM（每分钟请求数）或 TPM（每分钟 [Token](../concepts/token.md) 数）超限。稳定版模型（如 `qwen3.7-plus`）限流额度显著高于快照版（如 `qwen-plus-2025-07-28`）（见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）  
- **费用控制**：模型推理按 Token 用量计费，知识库（RAG）单独计费且不支持节省计划；新用户可开启“免费额度用完即停”避免意外扣费（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）  
- **安全与合规**：所有传输数据加密，阿里云不会使用客户数据训练模型（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


