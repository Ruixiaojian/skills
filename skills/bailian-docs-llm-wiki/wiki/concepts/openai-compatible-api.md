# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 协议规范（v1）的标准化模型服务入口，允许开发者复用现有 OpenAI 客户端代码、SDK（如 `openai==1.0+`）、框架（LangChain、LlamaIndex 等）和工具链，无需重写逻辑即可接入 Qwen 及其他百炼托管模型。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有应用**：若你已基于 OpenAI 的 `chat/completions` 或 `embeddings` 接口开发完成，只需将 `base_url` 替换为百炼的兼容 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入百炼颁发的 API Key，即可直接调用 `qwen-max`、`qwen-plus`、`qwen3.8-max` 等文本模型，以及 `text-embedding-v1` 等向量模型。  
- **智能体（Agent）开发**：使用 `Responses API`（即 `/v1/chat/completions` + `response_format={"type": "auto"}`）可开箱启用联网搜索、代码解释器、网页提取等工具能力，自动管理对话历史与工具调用生命周期，避免手动拼接 `messages`。  
- **多模态与批量任务**：视觉模型（如 `qwen3-vl-plus`）支持 OpenAI 标准 `image_url` 消息格式；文件上传（`/files`）、异步批量处理（`/batches`）和会话管理（`/conversations`）也统一通过 `/compatible-mode/v1` 路径暴露，与 OpenAI 原生行为高度一致。  
- **IDE/CLI 工具集成**：Cursor、Qwen Code、Hermes Agent 等工具默认采用 OpenAI 兼容模式，只需配置正确的 `Base URL` 和 `Model ID`（如 `qwen3.8-max`），即可启用思考模式（`enable_thinking: true`）等百炼增强能力。

> ⚠️ 注意：并非所有百炼模型都支持 OpenAI 兼容协议——`Qwen-Audio`、`qwen3-vl-embedding`（多模态向量）、`wan2.6-t2i`（文生图）等需调用 DashScope 原生或 AIGC 专用接口。

## 关键参数和配置

| 参数 | 说明 | 开发提示 |
|------|------|----------|
| `base_url` | **必须显式配置**，推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），性能与稳定性优于通用域名（`dashscope.aliyuncs.com/compatible-mode/v1`）。`{WorkspaceId}` 从控制台「业务空间详情」获取。 | 不同计费方案（[Token](token.md) Plan / Coding Plan / 按量）对应不同 base_url，混用将返回 `401 Unauthorized`。 |
| `Authorization: Bearer <API_KEY>` | 使用百炼颁发的 API Key（非 OpenAI key），需与 `base_url` 所属地域和计费方案严格匹配。 | [Token](token.md) Plan 个人版 Key 仅限 CLI/桌面客户端使用，禁止用于 Dify、Postman 等工作流平台。 |
| `model` | 模型标识符，大小写不敏感（如 `qwen-max`、`QWEN-MAX`、`qwen3.8-max` 均有效）。部分工具要求别名（如 Cursor 中 `glm-5.2` → `glm-5-2`）。 | 调用前请通过 `GET /api/v1/models` 查询当前空间可用模型及元信息（上下文长度、定价等）。 |
| `messages` | 对话消息数组，格式为 `[{"role": "user", "content": "..."}, ...]`。`system` 角色**不被 OpenAI 兼容接口支持**（需改用 DashScope 或 Anthropic 接口）。 | 若需长期上下文，应配合 `Conversations API` 或自行维护完整 `messages`；`Responses API` 可通过 `previous_response_id` 自动关联历史。 |
| `stream` | 是否启用流式响应（`true`/`false`）。流式下每行以 `data:` 开头，末尾必须含 `\n`，否则 SDK 解析失败。 | 流式响应中，`tool_calls` 分块需按 `delta` 字段增量解析，不可依赖 `choices[0].message.tool_calls` 全量字段。 |
| `response_format` | 百炼扩展参数，设为 `{"type": "auto"}` 可激活 Responses API 的自动工具链（联网、代码执行等）。 | 该参数仅在 `/v1/chat/completions` 路径下生效，且需模型支持（如 `qwen-max`、`qwen-plus`）。 |
| `extra_body` / `thinking` | Qwen3 系列模型必需启用思考模式，例如 `"extra_body": {"enable_thinking": true}`（Qwen Code）或 `"thinking": {"type": "enabled"}`（Kilo CLI）。 | 缺失此参数将返回 `400 InternalError.Algo.InvalidParameter`。 |

## 面向开发者的小贴士

- ✅ **首选路径**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）——比通用域名延迟更低、限流更宽松。  
- ✅ **调试技巧**：用 `curl` 快速验证时，务必添加 `-H "Content-Type: application/json"`，并确保 JSON body 无语法错误（尤其注意末尾逗号）。  
- ❌ **避坑提醒**：  
  - OpenAI 兼容接口**默认禁用工具调用**，即使传入 `tools` 字段也不会触发；必须配合 `response_format={"type": "auto"}` 或使用 Responses API。  
  - `input_tokens + output_tokens` 总和不能超模型限制（如 `qwen-turbo` 为 8K），否则返回 `400 Bad Request`。  
  - 文件类请求（`/files`）需额外添加请求头 `X-DashScope-OssResourceResolve: enable` 才能解析 `oss://` URL。  
- 📦 **SDK 建议**：Python 推荐 `openai>=1.30.0`（已内置百炼兼容适配），Java 推荐 `dashscope-sdk-java` 并启用连接池（`connectionPoolSize=32`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


