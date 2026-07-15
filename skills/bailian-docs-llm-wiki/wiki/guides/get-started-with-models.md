# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）及第三方模型。开发者无需部署和运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、微调与部署等全链路能力，适用于从快速验证到生产级落地的各类场景。

## 支持的模型与功能

百炼提供多模态、多场景的模型服务，覆盖文本生成、视觉理解、语音合成、嵌入向量等能力。核心模型包括：

- **千问系列旗舰模型**：`qwen3.7-max`（效果最优，适合复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，**推荐首选**）、`qwen3.6-flash`（高性价比、低延迟）[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **第三方模型**：DeepSeek、Kimi、GLM 等，部分仅限特定地域（如 DeepSeek 仅支持华北2（北京））[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **领域专用模型**：长文本处理、法律、意图理解、角色扮演等细分场景模型；
- **多协议兼容**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)、Anthropic 兼容接口、DashScope 原生 SDK 接口 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

> **注意**：文档中 `qwen3.7-plus` 与 `qwen-plus` 指代同一类主力模型，但命名存在不一致——`qwen3.7-plus` 是当前最新稳定版标识（见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)），而 `qwen-plus` 多用于历史快照或旧文档（如[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)表格中仍大量使用）。实际调用请以[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)实时列表为准，优先选用带 `3.7` 版本号的模型。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| **API Key** | 用于身份认证，需在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 | 不同地域的 API Key **不通用**；Coding Plan 和 Token Plan 需使用专属 Key [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) |
| **Base URL** | 模型服务接入地址，决定地域、协议与鉴权范围 | 必须与 API Key 所属地域匹配；业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）为生产环境推荐方案 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) |
| **WorkspaceId** | 业务空间唯一标识，用于构造专属 Base URL | 仅华北2（北京）、新加坡、日本（东京）、德国（法兰克福）需填写；美国（弗吉尼亚）使用 `dashscope-us.aliyuncs.com` 无需 WorkspaceId [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) |
| **model** | 模型 ID，如 `qwen3.7-plus` | 模型名与地域强绑定（例如 `qwen3.7-plus-us` 仅限美国地域）；不同地域支持的模型列表不同 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) |

## 使用方式

### 1. 准备工作
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 Key；
- 若使用业务空间专属域名，需在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取 `WorkspaceId`。

### 2. 调用示例（OpenAI 兼容）
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

> 完整代码与 Node.js/curl 示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. SDK 选择
- **OpenAI Python SDK**：兼容性好，适合已有 OpenAI 项目迁移；
- **DashScope Python SDK**：原生支持，提供更细粒度控制（如 `dashscope.base_http_api_url` 设置）；
- **其他语言**：官方提供 Java、Go、C# 等 SDK，详见 [API 参考文档](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国、德国、日本）的 API Key、Base URL、模型列表、计费策略均独立，**不可混用** [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **限流策略**：
  - 按主账号维度聚合所有子账号、业务空间、API Key 的调用量；
  - 分 RPM（每分钟请求数）和 TPM（每分钟 Token 消耗）双重限制，超出任一即返回 `429`；
  - `qwen3.7-plus` 在北京地域默认限流为 **30,000 RPM / 5,000,000 TPM**，而快照版本（如 `qwen-plus-2025-07-28`）仅为 **60 RPM / 1,000,000 TPM** [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **域名选择**：
  - **业务空间专属域名**：推荐生产环境，SLA 99.9%，超时 3600 秒，支持 WebSocket/WebRTC；
  - **Dashscope 域名**（如 `dashscope.aliyuncs.com`）：兼容存量，但建议迁移；
  - **试用域名**（如 `trial.cn-beijing.maas.aliyuncs.com`）：RPM 限 1000，**禁止用于生产** [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
- **费用控制**：
  - 新用户享北京地域免费额度，用完后自动转按量付费（已认证用户）或停止服务（未认证用户）；
  - 可开启“免费额度用完即停”开关，或订阅 Coding Plan 实现月度固定预算 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


