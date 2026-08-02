# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，仅需配置 API Key 和 Base URL 即可发起首次请求，适用于内容生成、摘要、问答等通用场景。平台同时支持可视化应用构建与高代码开发模式，兼顾业务人员与工程师需求。

## 支持的模型与功能

百炼提供覆盖文本、图像、音频、视频的多模态模型服务，核心文本生成模型包括：

- **Qwen 系列旗舰模型**：`qwen3.7-max`（复杂任务首选）、`qwen3.7-plus`（效果/速度/成本均衡，[推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、`qwen3.7-flash`（低延迟、高性价比）；
- **细分能力模型**：长文本（`qwen-long`）、代码（`qwq-plus`）、轻量推理（`qwen-turbo`）等；
- **第三方模型**：DeepSeek、Kimi、GLM 等（部分模型地域受限，如 DeepSeek 仅支持华北2（北京））。

所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、Anthropic 兼容接口及 DashScope 原生接口。[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档详细列出了各模型在不同地域的可用性、Base URL 及接入方式。

> **注意**：文档中 `qwen3.7-max` 的限流值存在矛盾——[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格显示华北2（北京）RPM 为 30,000，而 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 文档称其 TPM 限流值随月消费档位动态调整（如 ≤10w 档为 500w）。实际生效值以控制台实时展示为准，且动态限流机制下“实际可用 TPM 不低于限流值”，属软限流行为。

## 关键参数

调用模型必需的核心参数如下：

- `api_key`：从 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取，**按地域独立**，不可跨地域复用；
- `base_url`：必须与 API Key 所属计费方案匹配，常见类型包括：
  - **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，需先在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 中获取 WorkspaceId；
  - **DashScope 域名**（兼容存量）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（华北2）或 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，限流严格，仅用于验证；
- `model`：模型 ID，如 `"qwen3.7-plus"`，必须与所选地域实际支持的模型一致；
- `messages`：遵循 OpenAI 格式，含 `role`（`system`/`user`/`assistant`）和 `content` 字段。

完整参数说明与错误码参考请见 [通义千问 API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建密钥；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量（[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供了 Linux/macOS/Windows 全平台配置指南）；
- （可选）为避免依赖冲突，建议使用 Python 虚拟环境。

### 2. 发起调用
支持多种 SDK 和协议：

- **OpenAI Python SDK**（推荐）：
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

- **DashScope Python SDK**：
  ```python
  from dashscope import Generation
  response = Generation.call(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你是谁？"}],
      api_key=os.getenv("DASHSCOPE_API_KEY")
  )
  ```

- **curl**（调试用）：
  ```bash
  curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"你是谁？"}]}'
  ```

详细代码示例与错误处理见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

- **地域隔离**：各地域（华北2、新加坡、美国、德国、日本）的 API Key、Base URL、模型列表、计费策略相互独立，**严禁混用**。例如，美国地域的 `qwen3.7-plus-us` 模型不可在华北2 Base URL 下调用。
- **限流机制**：
  - 默认按主账号维度聚合 RPM（每分钟请求数）与 TPM（每分钟 Token 数），子账号、业务空间、API Key 共享额度；
  - 各模型限流值独立，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格；
  - 动态限流模型（如 `qwen3.8-max`）的 TPM 基线随月消费金额自动调整，每月 15 日生效；
  - 触发限流时返回 `429` 错误，通常 60 秒内自动恢复；可采用指数退避、备选模型切换（见 [限流 FAQ 示例代码](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）或提额解决。
- **费用控制**：
  - 新用户享有北京地域免费额度，用完后已认证用户自动转按量付费，未认证用户将停止服务；
  - 可开启 [免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92) 避免意外扣费；
  - 模型推理与[知识库](../concepts/knowledge-base.md)（RAG）计费完全独立，前者按 Token 用量，后者按规格时长+调用次数。
- **安全与合规**：所有传输数据加密，平台**不会使用您的数据训练模型**，符合隐私保护要求（详见 [合规资质与隐私说明](https://help.aliyun.com/zh/model-studio/privacy-notice)）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


