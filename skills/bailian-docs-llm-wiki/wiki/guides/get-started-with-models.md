# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署运维，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦模型调用的入门路径，涵盖模型选择、参数配置、调用方式及关键限制。

## 支持的模型与功能

百炼提供多系列千问模型（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.7-flash`）及 DeepSeek、Kimi、GLM 等第三方模型，覆盖文本生成、多模态理解与生成、嵌入向量等能力 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型按能力与成本分层：`qwen3.7-max` 适合复杂任务；`qwen3.7-plus` 是效果、速度与成本的均衡推荐；`qwen3.7-flash` 适用于低延迟简单任务。部分模型（如 `qwen3.8-max-preview`）仅限 [Token](../concepts/token.md) Plan 订阅用户使用 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 1 中称 “qwen3.7-max 推理能力全面超越前代”，而文档 5 的限流表中列出 `qwen3.7-max` RPM/TPM 为 30,000/5,000,000，但同表中 `qwen3.7-max-2026-06-08` 等快照版本限流仅为 600/1,000,000。这表明高限流额度仅适用于稳定版（无日期后缀），而非所有带版本号的变体。实际选型应以[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)文档中的具体数值为准。

## 关键参数

- **API Key**：必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，不同地域的 Key 不通用。
- **Base URL**：必须与 API Key 所属地域和计费方案严格匹配。生产环境**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与流量隔离；Dashscope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）为兼容性保留，试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）仅限快速验证 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **WorkspaceId**：在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域调用业务空间专属域名时必需，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面获取。
- **模型 ID**：如 `qwen3.7-plus`，需与所选地域实际支持的模型一致（例如 DeepSeek 仅支持北京地域）。

## 使用方式

1. **环境准备**：注册阿里云账号并完成实名认证；开通百炼服务；创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（避免硬编码）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。
2. **代码调用**：使用 OpenAI Python SDK 或 DashScope SDK。OpenAI SDK 示例：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   ```
3. **地域适配**：不同地域 Base URL 不通用。美国（弗吉尼亚）使用 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`；新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 限制和注意事项

- **限流策略**：按主账号维度合并计算所有子账号、业务空间和 API Key 的调用量。触发条件包括每分钟请求数（RPM）或 [Token](../concepts/token.md) 数（TPM）超限，或请求速率突增（`Request rate increased too quickly`）。`qwen3.7-plus` 在北京地域 RPM/TPM 为 30,000/5,000,000，而同模型在新加坡地域为 15,000/5,000,000 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **地域约束**：各地域 API Key、Base URL、模型列表相互独立，不可混用。德国（法兰克福）和日本（东京）地域不支持 DashScope 域名，美国（弗吉尼亚）地域不支持业务空间专属域名 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **费用控制**：模型调用按量付费，知识库（RAG）功能计费独立。新用户可享北京地域免费额度，建议开启“免费额度用完即停”开关防止意外扣费 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


