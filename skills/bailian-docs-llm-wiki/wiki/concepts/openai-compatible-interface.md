# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 接入层，遵循 OpenAI 官方 REST API 协议规范（如 `/chat/completions`、`/responses`、`/embeddings` 等路径），使开发者能直接复用现有 OpenAI SDK（如 `openai==1.0+`）、工具链（LangChain、LlamaIndex）或客户端（Cursor、Dify、Hermes Agent），无需修改业务逻辑即可调用千问（Qwen）及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移存量应用**：已有基于 OpenAI SDK 的 Python/Node.js 项目，只需替换 `base_url` 和 `api_key`，即可零代码改造接入 Qwen 系列模型（如 `qwen3.7-plus`），适用于试点验证或轻量级生产部署。  
- **智能体（Agent）开发**：通过 `compatible-mode/v1/responses` 接口调用内置工具能力（联网搜索、网页提取、代码解释器），自动管理对话历史，适合构建无需自维护会话状态的轻量级智能体。  
- **多模态与专项任务**：按需选用兼容子接口——`/vision/chat/completions`（Qwen-VL/QVQ 图像理解）、`/embeddings`（文本向量化）、`/files` + `/batches`（文档解析与批量推理），各接口共用统一鉴权与配额体系。  
- **跨框架集成**：支持 LangChain 的 `ChatOpenAI`、LlamaIndex 的 `OpenAIEmbedding` 等原生类，也兼容 Cursor、Cherry Studio、Dify（按量付费方案）等客户端，降低工具链切换成本。  
- **应用层调用**：在调用已发布的智能体或工作流时，可选 `Responses API` 路径（`/apps/{APP_ID}/compatible-mode/v1/responses`），复用 OpenAI 消息格式，但需注意其不支持 `session_id`，必须显式传入完整 `messages` 历史。

> ⚠️ 注意：OpenAI 兼容接口是协议层抽象，**不等于模型能力完全对齐**。例如标准 `/chat/completions` 不支持工具调用；`/responses` 仅限 `qwen3-*` 系列；`/embeddings` 不支持多模态模型（如 `qwen3-vl-embedding`）。

## 关键参数和配置

| 参数 | 说明 | 百炼特有约束 |
|------|------|--------------|
| `base_url` | 必填。服务端点，决定地域、计费方案与 SLA | - 业务空间专属：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（推荐，99.9% SLA）<br>- [Token](token.md) Plan：`https://token-plan.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>- 按量付费旧域名（不推荐）：`https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填。模型 ID，严格区分大小写与版本号 | - `/chat/completions`：支持 `qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.2` 等（不含 `qwen-audio`）<br>- `/responses`：**仅限 `qwen3-*` 系列**（如 `qwen3.7-flash`），不接受 `qwen-plus`<br>- 模型名需与 `base_url` 所属计费方案匹配（如 `qwen3.8-max-preview` 仅 [Token](token.md) Plan 可用） |
| `messages` | 必填（除 `/completions`）。标准 OpenAI 格式：`[{ "role": "user/system/assistant", "content": "..." }]` | - `system` 消息被支持，但部分模型（如 `qwen-coder-turbo`）可能忽略<br>- 多轮对话需显式传递全部历史（`/responses` 不自动维护会话） |
| `stream` | 可选。启用流式响应（SSE） | - 流式中 `tool_calls` 可能分片，需按 `index` 和 `id` 合并<br>- 异步调用（`background=true`）不支持流式 |
| `stream_options` | 可选。控制流式行为 | `{"include_usage": true}` 可在末尾 chunk 返回 token 统计（所有兼容接口均支持） |
| `temperature` / `top_p` | 可选。采样控制 | - `temperature` 范围：`[0.0, 2.0)`（非 OpenAI 的 `[0, 2]`）<br>- 二者互斥，建议只设其一<br>- `qwen3.8-max-preview` 思考模式下 `temperature` 下限为 `0.6`（低于自动修正） |
| `max_tokens` | 可选。响应长度上限 | 仅截断输出，**不影响模型实际生成长度**；超限内容将被静默丢弃 |

## 面向开发者，简洁实用

- ✅ **立即上手**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 百炼控制台获取
      base_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}]
  )
  print(resp.choices[0].message.content)
  ```

- ✅ **关键检查清单**：  
  - ✅ `base_url` 地域、计费方案、WorkspaceId 三者必须一致；  
  - ✅ `model` 名称严格按 [模型市场](https://bailian.console.aliyun.com/#/model-market) 实际列表填写（注意 `-` 与 `_`）；  
  - ✅ 工具调用务必用 `/responses`，不用 `/chat/completions`；  
  - ✅ 流式响应需自行聚合 `delta.tool_calls`，勿依赖单 chunk 完整性；  
  - ❌ 不要混用 [Token](token.md) Plan Key 与按量付费 Key，否则返回 `401 Unauthorized`。

- ✅ **调试建议**：  
  - 优先使用 `curl` 或 Postman 验证基础请求，排除 SDK 版本兼容问题；  
  - 查看响应头 `X-RateLimit-Remaining` 和 `X-Usage-Token-Count` 监控配额；  
  - 遇到 `429` 错误时，检查 RPM/TPM 限流（按主账号全局统计，含所有子账号与业务空间）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


