# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议实现，完全遵循 OpenAI 官方 REST API 的路径、请求/响应格式、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能直接复用现有 OpenAI SDK（Python/Node.js 等）、工具链（Cursor、Dify、Postman）或代码逻辑，**零修改迁移**即可调用百炼托管的 Qwen 及第三方大模型。

## 在百炼平台的不同场景中如何使用

- **快速原型开发与生态迁移**：已有基于 `openai>=1.0` SDK 的项目，只需替换 `base_url` 和 `api_key`，无需重写业务逻辑，即可接入 `qwen-plus`、`qwen3.8-max`、`text-embedding-v4`、`qwen-vl-plus` 等全系列模型。
- **多模态与向量服务统一接入**：图像理解（VL 模型）、文本嵌入、批量处理（Batch）、文件解析（Files API）等能力均通过同一套 OpenAI 兼容协议暴露，降低客户端适配复杂度。
- **智能体与工作流应用集成**：通过 `Responses` 接口（`/compatible-mode/v1/responses`）调用已发布的智能体应用，支持自动上下文管理、[插件](plugin.md)参数透传（`biz_params`）及同步/异步模式切换。
- **CLI 工具与 IDE [插件](plugin.md)直连**：Hermes Agent、Qoder、Cline、Claude Code 等工具仅需配置百炼专属 `Base URL` 与对应方案的 API Key，即可开箱即用，无需定制适配器。
- **跨地域与多方案部署**：支持按计费方案（[Token](token.md) Plan、Coding Plan、按量计费）和地域（北京、新加坡、东京、法兰克福）动态生成专属 `base_url`，实现资源隔离与合规部署。

> ⚠️ 注意：`Qwen-Audio` 不支持 OpenAI 兼容协议；`application call` 中的旧版智能体（Agent 1.0）默认使用 DashScope 原生接口，如需 OpenAI 风格，须显式选用 `Responses` 路径。

## 关键参数和配置

| 参数 | 类型 | 说明 | 百炼特有约束 |
|------|------|------|--------------|
| `base_url` | string | 必填。必须使用业务空间专属域名，**强烈推荐**：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>（旧域名 `dashscope.aliyuncs.com` 仍可用但性能较低） | 不同计费方案（[Token](token.md) Plan / Coding Plan / 按量）对应不同子域名，**不可混用** |
| `api_key` | string | 必填。从控制台对应方案页面获取（如 [Token](token.md) Plan 个人版 Key 不能用于 Coding Plan） | Key 与 `base_url` 地域、方案必须严格匹配，否则返回 `401` |
| `model` | string | 必填。模型 ID，如 `qwen-plus`、`qwen3.8-max`、`text-embedding-v4`、`qwen-vl-plus` | 不区分大小写，但需与控制台支持列表**完全一致**；部分工具要求别名（如 `kimi-k2-6`） |
| `messages` | array | 必填（Chat Completions）。标准 OpenAI 格式：`[{ "role": "user/system/assistant", "content": "..." }]` | `system` 角色在 OpenAI 兼容接口中**不生效**（仅 DashScope/Anthropic 原生支持）；`Responses` 接口虽宣称“自动管理历史”，但仍需传入完整 `messages` 数组 |
| `stream` | boolean | 否。启用流式响应 | 支持 `stream_options={"include_usage": true}`，在流末尾返回 token 统计 |
| `temperature` / `top_p` | number | 否。控制输出随机性 | 互斥，建议只设其一；OpenAI 兼容接口默认 `temperature=1.0`（DashScope 原生为 `0.8`） |
| `max_tokens` | integer | 否。硬截断上限 | 超限内容将被丢弃，不报错 |
| `enable_thinking` | boolean | 否。仅 Batch 和 Responses 接口支持 | 默认 `true`（启用推理链），关闭可降本；`qwen3.8-max` 等[长上下文](long-context.md)模型默认开启 |

## 面向开发者：简洁实用提示

- ✅ **三步启动**：  
  1. 获取对应方案的 `DASHSCOPE_API_KEY`（控制台 → 密钥管理）；  
  2. 构造 `base_url`（参考 [计费方案对照表](https://bailian.console.aliyun.com/#/plan)）；  
  3. 使用标准 OpenAI SDK 初始化客户端并调用 `chat.completions.create()`。

- ✅ **调试技巧**：  
  - 报 `401 Incorrect API key provided`？→ 检查 Key 与 `base_url` 是否来自同一方案且地域一致；  
  - 报 `400 InvalidParameter`？→ 检查 `model` 名称是否拼写正确、是否在该方案支持列表中；  
  - 流式无响应？→ 确认 `stream=true` 且后端服务已启用流式开关（尤其工作流应用）。

- ❌ **避坑提醒**：  
  - 不支持 `response_format`（JSON Schema 强约束），需用 DashScope 原生接口；  
  - `qwen-turbo` 不支持 `tool_use` 和 `system` 角色，调用前请降级模型；  
  - `session_id` 模式下会话有效期仅 1 小时、最多 50 轮，生产环境推荐显式传 `messages` 自主管理上下文。

- 📦 **推荐组合**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # Token Plan 个人版
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "用 Python 写一个斐波那契数列生成器"}],
      temperature=0.3,
      stream=True
  )
  ```

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


