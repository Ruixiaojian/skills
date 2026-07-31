# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦模型调用的核心路径，涵盖可用模型、关键参数、接入方式及生产注意事项。

## 支持的模型与功能

百炼提供多系列千问模型（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.7-flash`）及 DeepSeek、Kimi、GLM 等第三方模型，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解与生成、领域专用任务等场景。模型按能力与成本分层：  
- **qwen3.7-max**：推理能力最强，适合复杂多步任务；  
- **qwen3.7-plus**：效果、速度与成本均衡，是多数生产场景的推荐选择；  
- **qwen3.7-flash**：低延迟、高性价比，适用于简单高频响应任务。  

所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope SDK 及 Anthropic 兼容协议。详细模型列表及地域支持情况请参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 1 中称 `qwen3.7-max` 为“最新旗舰”，但文档 3 显示 `qwen3.8-max-preview` 已上线（仅限 [Token](../concepts/token.md) Plan 用户）。实际可用模型以控制台[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)实时列表为准，旧版文档中未标注的 preview 模型可能受限于订阅计划。

## 关键参数

调用模型需明确以下核心参数：

- **`model`**：模型 ID，如 `"qwen3.7-plus"`。不同地域支持的模型略有差异，例如 DeepSeek 仅在北京地域可用（见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）；  
- **`base_url`**：必须与所选地域和计费方案匹配。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）为生产环境推荐，DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）用于兼容存量调用，试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）仅限快速验证；  
- **`api_key`**：需通过[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)页面创建，并配置为环境变量 `DASHSCOPE_API_KEY` 以保障安全（详见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）；  
- **`workspace_id`**：使用业务空间专属域名时必需，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)中获取。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；  
- 开通百炼服务，在控制台创建 API Key 并配置环境变量；  
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope SDK）。

### 2. 发起调用（OpenAI 兼容示例）
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

> **注意**：文档 4 与文档 6 对德国（法兰克福）、日本（东京）地域的 DashScope 域名支持描述矛盾——文档 4 列出其 DashScope 域名，而文档 6 明确标注“不支持”。实际接入应以[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)为准，优先使用业务空间专属域名。

### 3. 多地域适配
各地域 Base URL 不通用，且 API Key 不跨地域生效。例如：  
- 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`  
- 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（无 WorkspaceId）  

完整接入信息请参考[地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- **限流策略**：按主账号维度统一计算 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗），不同模型额度独立。例如 `qwen3.7-plus` 在北京地域默认为 30,000 RPM / 5,000,000 TPM，而 `qwen3.7-plus-2025-07-28` 仅为 60 RPM / 1,000,000 TPM。突发流量可能触发 `Request rate increased too quickly` 保护机制（见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）；  
- **生产建议**：  
  - 生产环境务必使用**业务空间专属域名**，其 SLA 99.9%、超时 3600 秒、支持 WebSocket/WebRTC，优于 DashScope 域名（600 秒超时）；  
  - 避免硬编码 API Key，始终通过环境变量注入；  
  - 监控调用量：数据约 1 小时后可在[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)查看；  
- **费用控制**：  
  - 新用户免费额度仅限北京地域，用完后自动转按量付费（已认证用户）或停止服务（未认证用户）；  
  - 如需避免意外扣费，可开启“免费额度用完即停”开关（仅限北京地域）；  
  - Coding Plan 用户须使用专属 Base URL（如 `https://coding.dashscope.aliyuncs.com/v1`）和专属 API Key，混用将导致按量计费。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


