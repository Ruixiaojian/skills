# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署或运维模型，只需配置 API Key 和 Base URL 即可发起推理请求。本文档聚焦模型调用的入门路径，涵盖模型选择、参数配置、接入方式及关键限制。

## 支持的模型与功能

百炼提供多系列千问模型（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.7-flash`）及 DeepSeek、Kimi、GLM 等第三方模型，覆盖文本生成、多模态理解与生成、嵌入向量等能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型按能力与成本分层：

- **qwen3.7-max**：旗舰模型，适合复杂多步骤任务，华北2（北京）地域 RPM 限流为 30,000，TPM 为 5,000,000；
- **qwen3.7-plus**：效果、速度与成本均衡，是多数场景的推荐选择，同地域限流与 max 相同；
- **qwen3.7-flash**：高性价比、低延迟，适用于简单快速响应任务，同地域限流亦为 30,000 RPM / 5,000,000 TPM。

> **注意**：文档中多次出现 `qwen3.7-plus` 与 `qwen-plus` 混用（如 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 示例代码使用 `qwen-plus`，而 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格均以 `qwen3.7-plus` 为主）。实际调用应以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中列出的模型 ID 为准，`qwen-plus` 是旧版命名，当前生产环境推荐使用带版本号的模型 ID（如 `qwen3.7-plus`），避免因快照版本过期导致调用失败。

各模型在不同地域的支持情况不同，例如 DeepSeek 仅支持华北2（北京）地域；`qwen3.8-max-preview` 仅面向 Token Plan 订阅用户 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。完整模型列表及地域支持请参考控制台模型广场。

## 关键参数

调用模型需明确以下核心参数：

- **API Key**：用于身份鉴权，需在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)；
- **Base URL**：必须与 API Key 所属地域和计费方案严格匹配。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）为生产环境推荐，Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）适用于存量迁移，试用域名限流更严 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
- **WorkspaceId**：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域需从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取，美国（弗吉尼亚）地域使用 `dashscope-us.aliyuncs.com`，无需 WorkspaceId；
- **模型 ID**：必须与 Base URL 所属地域支持的模型一致，例如 `qwen3.7-plus` 在北京地域可用，但在德国法兰克福地域需确认是否在[可用模型列表](https://modelstudio.console.aliyun.com/eu-central-1?tab=doc#/doc/?type=model&url=2840914)中存在。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`；
- 根据所选地域获取对应 Base URL（含 WorkspaceId）和模型 ID。

### 2. 调用示例（OpenAI SDK）
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

### 3. 多语言支持
除 Python 外，Node.js、curl 等方式均支持，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的代码片段。DashScope SDK 也提供同等能力，但 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)更利于现有项目迁移。

## 限制和注意事项

- **地域隔离**：各地域的 API Key、Base URL、模型列表互不通用，跨地域混用将返回 401 错误 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。触发限流时返回 `429 Too Many Requests`，错误信息包含具体类型（RPM/TPM/突发速率） [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **费用控制**：模型调用按 Token 用量计费，知识库（RAG）为独立计费项；新用户享有北京地域免费额度，用完后可开启“免费额度用完即停”开关防止意外扣费 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **域名选择**：业务空间专属域名提供更高并发、更低延迟及 SLA 保障（99.9%），试用域名 RPM 仅为 1000，不建议用于生产 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **安全合规**：用户数据不会被用于模型训练，传输全程加密；若需数据驻留，应选择符合合规要求的服务部署范围（如欧盟、日本） [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


