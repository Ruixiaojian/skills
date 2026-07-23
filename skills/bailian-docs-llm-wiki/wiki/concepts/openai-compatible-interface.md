# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 协议规范（v1.x），支持 `chat/completions`、`completions`、`embeddings`、`vision`、`batch`、`conversations`、`files` 等核心端点。开发者无需修改业务逻辑，仅需替换 `base_url` 和 `api_key`，即可将基于 OpenAI SDK 或生态工具（如 LangChain、LlamaIndex、Cursor、OpenClaw）构建的应用快速迁移至百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移现有应用**：已有 OpenAI 集成的项目（如 Web 应用、CLI 工具、Agent 框架），只需将 `openai.base_url` 改为百炼 OpenAI 兼容地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入百炼颁发的 `api_key`，即可零代码改动调用 Qwen 系列及第三方模型（DeepSeek、Kimi、GLM 等）。
  
- **智能体（Agent）与工作流集成**：通过 `application call` 的 OpenAI 兼容 Responses API（`/v1/chat/completions`），可直接调用已发布的智能体应用，自动启用联网搜索、网页提取、代码解释器等原生工具链；支持[多模态](multi-modal.md)输入（图像、文件）、流式响应（`stream=true`）和异步模式（`background=true`）。

- **[多模态](multi-modal.md)与向量任务统一接入**：视觉理解（`qwen3-vl-plus`）、文本嵌入（`text-embedding-v4`）、批量推理（JSONL 文件异步提交）等能力，均通过同一套 OpenAI 兼容路径暴露，避免在不同协议间切换，降低客户端维护成本。

- **开发工具链直连**：主流 AI 编程助手（Claude Code、Qwen Code）、IDE 插件（Cline、Qoder）、桌面应用（Cherry Studio、Cursor）及开源 Agent 框架（OpenClaw、QwenPaw）均可原生对接，仅需配置 `base_url`、`api_key` 和合规 `model` 名称（如 `qwen3.7-plus`），即刻启用百炼算力。

- **会话状态管理**：配合 `conversations` 接口，可创建、查询、更新长期对话上下文；该能力与 `responses` 接口协同，实现跨设备、跨请求的上下文自动注入，适用于客服机器人、个人助理等长周期交互场景。

## 关键参数和配置

| 参数 | 类型 | 必选 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `base_url` | string | 是 | OpenAI 兼容接口根地址，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不可使用通用域名 `dashscope.aliyuncs.com`（已废弃） | `{WorkspaceId}` 需从控制台获取；地域（北京/新加坡/弗吉尼亚）须与 `api_key` 所属地域一致，否则返回 401 |
| `api_key` | string | 是 | 百炼平台颁发的密钥，**按计费方案隔离**（[Token](token.md) Plan Key ≠ Coding Plan Key ≠ 按量 Key） | Key 与 `base_url` 地域、套餐类型强绑定，跨方案或跨地域复用将失败 |
| `model` | string | 是 | 模型标识符，必须从各接口支持列表中选取（如 `qwen3.7-plus`、`text-embedding-v4`、`qwen3-vl-plus`） | 不支持别名转换（如 `qwen3.8-max-preview` 不可写为 `qwen3-8-max-preview`）；部分工具（如 Cursor）对 `-` 和 `.` 敏感，需严格匹配文档命名 |
| `messages` | array | 是（Chat/Responses） | 对话历史数组，格式为 `[{"role": "user", "content": "..."}]`；支持 `user`/`assistant`/`system` 角色 | `system` 角色在所有 OpenAI 兼容接口中均有效；`tools` 字段**不接受显式传入**（由服务端自动注入） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时，响应为 SSE 格式，字段结构与 OpenAI 一致（`choices[0].delta.content`） | 流式响应末尾可通过 `stream_options={"include_usage": true}` 获取 token 统计 |
| `response_format` | object | 否 | 控制输出结构（如 `{"type": "json_object"}`），仅部分 Qwen3 模型支持 | 需模型明确声明支持（见各模型文档），否则忽略 |
| `max_tokens` | integer | 否 | 输出最大 token 数，建议显式设置以避免截断或超限 | 实际可用长度受模型上下文窗口限制（如 Qwen3 为 32768 tokens） |

> ⚠️ 重要限制：  
> - **工具调用不可定制**：OpenAI 兼容接口（尤其是 Responses）的联网搜索、代码执行等能力由服务端全自动调度，**不开放 `tools` 参数或自定义函数注册**；如需精细控制，请改用 DashScope 原生接口。  
> - **思考模式不可关闭**：`qwen3.8-max-preview` 等模型强制启用思考模式，`enable_thinking` 参数在 OpenAI 兼容接口中无效。  
> - **会话状态不共享**：`session_id` 仅 DashScope 原生接口支持；OpenAI 兼容接口需在每次请求中传递完整 `messages` 历史（或配合 `conversations` 接口管理）。

## 面向开发者，简洁实用

- ✅ **立即上手**：用 `openai` Python SDK（v1.0+）调用示例：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 百炼 API Key
      base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```

- ✅ **调试建议**：  
  - 首选 `dashscope` SDK（v1.20.0+），它内置 OpenAI 兼容模式，自动处理认证与重试；  
  - 使用 `curl` 测试时，务必携带 `Content-Type: application/json` 和 `Authorization: Bearer <api_key>`；  
  - 遇到 `401 Unauthorized`，优先检查 `base_url` 地域、`api_key` 方案类型、`model` 是否在套餐支持列表中。

- ✅ **避坑指南**：  
  - 不要尝试在 OpenAI 兼容接口中传 `tools`、`enable_search`、`top_k` 等 DashScope 专属参数——将被静默忽略；  
  - 文件上传请走 `/v1/files` 接口（非 `/v1/chat/completions` 中内联 Base64），确保符合 `purpose` 要求（`file-extract`/`batch`/`fine-tune`）；  
  - 长对话场景下，主动精简历史 `messages`，避免因上下文过长触发自动截断（尤其启用搜索时）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application component api reference](../api/application-component-api-reference.md)


