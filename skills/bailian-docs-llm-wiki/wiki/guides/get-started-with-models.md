# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速调用千问（Qwen）及第三方模型。开发者无需部署和运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。本文档聚焦核心接入路径，涵盖模型选择、参数配置、调用方式及关键限制，适用于生产环境快速落地。

## 支持的模型与功能

百炼当前提供覆盖文本、图像、音频、视频等多模态能力的模型服务，其中千问系列是主力推荐模型：

- **旗舰模型**：`qwen3.8-max`（效果最优，适合复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡，[推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟、高性价比，适合简单高频场景）。
- **地域覆盖**：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）五大地域，各地域模型列表与服务能力存在差异，详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。
- **兼容协议**：支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、Anthropic 兼容接口及原生 DashScope 接口，同一模型在不同协议下 Base URL 不同，需严格匹配。

> **注意**：文档 2 中列出的 `qwen3.8-max` 在多个地域重复展示 Base URL 格式，但未明确区分不同协议（OpenAI/Anthropic/DashScope）的实际可用性；而文档 5 明确指出 Anthropic 兼容接口在德国（法兰克福）和日本（东京）地域仅支持业务空间专属域名，且美国（弗吉尼亚）地域不支持业务空间专属域名。实际使用请以 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 中的表格为准。

## 关键参数

调用模型必需的核心参数包括：

- **API Key**：用于身份认证，必须通过 [百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，并建议[配置为环境变量 `DASHSCOPE_API_KEY`](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 以避免硬编码泄露。
- **Base URL**：模型服务入口地址，**必须与 API Key 所属地域及计费方案严格匹配**。例如：
  - 华北2（北京）业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 美国（弗吉尼亚）DashScope 域名：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
  - 试用域名（仅限测试）：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **模型 ID**：如 `qwen3.8-max`，需与所选地域支持的模型列表一致，不可跨地域混用。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在控制台创建业务空间（Workspace）并获取 `WorkspaceId`；
- 创建 API Key 并配置环境变量（Linux/macOS/Windows 各系统配置方法详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）。

### 2. SDK 调用示例（Python + OpenAI SDK）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 1 中示例代码末尾被截断（`from` 后无内容），但完整逻辑已在 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 的 Python 示例中给出，应以此为准。

### 3. 多语言支持
除 Python 外，Node.js、curl 等调用方式均支持，Base URL 地域规则一致（见文档 7）。所有语言均需确保 `base_url` 与地域、协议、API Key 三者匹配。

## 限制和注意事项

- **限流机制**：
  - 默认按主账号维度对 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗）进行限流，不同模型额度独立（如 `qwen3.8-max` 华北2 地域为 30,000 RPM / 5,000,000 TPM）；
  - 部分模型（如 `qwen3.8-max`）采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 基线随百炼月消费金额自动提升，实际可用值 ≥ 限流值；
  - 业务空间可单独设置限流值，未设置则共享账号级配额。

- **地域与域名约束**：
  - API Key、Base URL、模型 ID 必须同地域；跨地域混用将返回 401 错误；
  - 推荐使用**业务空间专属域名**（更高并发、更低时延、流量隔离），存量业务可参考 [迁移至业务空间专属域名](../../raw/model-user-guide/get-started-with-models/regions.md) 文档平滑升级；
  - 试用域名限流严格（RPM=1000），**禁止用于生产环境**。

- **其他关键约束**：
  - 模型调用量统计延迟约 1 小时，监控数据请在 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面查看；
  - Coding Plan 和 [Token](../concepts/token.md) Plan 专属 API Key 仅限交互式工具（如 Claude Code），**不可用于后端服务调用**；
  - 数据隐私保障：百炼不会使用用户数据训练模型，所有传输加密，详见 [合规资质与隐私说明](https://help.aliyun.com/zh/model-studio/privacy-notice)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)


