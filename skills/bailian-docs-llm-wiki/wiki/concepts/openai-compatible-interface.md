# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI 官方 REST 接口规范（如 `/v1/chat/completions`、`/v1/embeddings` 等），使开发者无需修改业务逻辑即可复用现有 OpenAI SDK、LangChain 集成、CLI 工具或前端框架，实现从 OpenAI 或其他兼容服务到百炼的平滑迁移。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套覆盖多类能力的协议族，在百炼中按功能分层支持：

- **文本生成**：通过 `chat/completions` 接口调用 `qwen-max`、`qwen-plus`、`qwen3.7-plus` 等 Qwen 系列模型，以及 DeepSeek、Kimi、GLM 等第三方直供模型；不支持 `qwen-vl`（[多模态](multi-modal.md)）和 `qwen-audio`（语音）模型。
- **智能体增强调用**：`responses` 接口（路径 `/v1/responses`）在标准 Chat Completions 基础上内置联网搜索、代码解释器、网页提取等工具链，适用于需轻量级 RAG 或自动化执行的 Agent 场景，支持全系 Qwen3 模型及 `qwen-plus`。
- **[多模态](multi-modal.md)理解**：`vision` 接口兼容 OpenAI [多模态](multi-modal.md)消息格式（含 `image_url`），支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型；但 `qwen-vl` 仍需 DashScope 原生接口调用。
- **向量嵌入**：`embeddings` 接口支持 `text-embedding-v4` 等文本嵌入模型；注意：多模态嵌入模型（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议。
- **会话管理与批量处理**：`conversations` 接口用于跨设备/长时间上下文持久化；`batch/chat` 和 `batch/file` 接口支持异步批量推理，适用于评测、标注等非实时任务。
- **文件管理**：`files` 接口支持上传文档用于分析（`purpose="file-extract"`）、批量任务（`purpose="batch"`）或微调（`purpose="fine-tune"`）。
- **应用调用**：通过 `application-call` 的 OpenAI 兼容模式（`/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）调用已发布的智能体或工作流，便于复用 LangChain Agent 工具链。

> ⚠️ 注意：  
> - 所有 OpenAI 兼容接口**均不支持** `qwen-audio`、`qwen-vl`（除 Vision API 外）、私有调优模型（仅 DashScope 原生接口可用）；  
> - 子业务空间（Workspace）调用时，**必须使用 Workspace 专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不可复用全局 `dashscope.aliyuncs.com`；  
> - Responses API 不支持自动会话续写（无 `session_id`），需显式传入完整 `messages` 数组。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `model` | string | 是 | 模型标识符，如 `"qwen3.7-plus"`、`"text-embedding-v4"` | 不同接口支持模型不同，务必查阅对应文档确认取值范围；`qwen-turbo` 不支持 Anthropic 接口，`qwen-coder-turbo` 仅支持 `completions` 接口 |
| `base_url` | string | 是 | 服务端点，**强烈推荐使用 Workspace 专属域名** | 示例：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（[Token](token.md) Plan）<br>`https://{WorkspaceId}.cn-shanghai.maas.aliyuncs.com/compatible-mode/v1`（子空间） |
| `api_key` | string | 是 | DashScope API Key（非阿里云 AccessKey），建议通过环境变量 `DASHSCOPE_API_KEY` 注入 | Key 与 `base_url` 必须匹配计费方案（[Token](token.md) Plan / Coding Plan / 按量计费）和地域，否则返回 `401` |
| `messages` | array | 条件必填 | 对话消息列表，格式为 `[{"role": "user", "content": "..."}]` | `responses` 接口支持简化输入（`input: string`），其余接口必需此字段 |
| `stream` | boolean | 否（默认 `false`） | 是否启用流式响应 | 设为 `true` 时，响应为 SSE 流；可搭配 `stream_options={"include_usage": true}` 获取末尾 token 统计 |
| `temperature` | number | 否（默认 `1.0`） | 控制输出随机性 | 取值范围 `[0.0, 2.0]`（OpenAI 兼容），而 DashScope 原生为 `[0.0, 1.0]`，迁移时需归一化 |
| `max_tokens` | integer | 否 | **仅限制响应长度**（completion tokens），不影响 [prompt](../guides/prompt.md) 截断 | DashScope 原生接口中该参数表示 total tokens（[prompt](../guides/prompt.md) + completion），行为不同 |
| `stop` | string \| array | 否 | 指定停止生成的字符串或字符串数组 | 如 `["\n", "。"]` |
| `seed` | integer | 否 | 设置后提升结果确定性 | 推荐用于测试与调试 |

## 面向开发者，简洁实用

✅ **快速上手四步法**：  
1. **选对 endpoint**：优先使用 Workspace 专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；  
2. **配好凭证**：设置 `DASHSCOPE_API_KEY` 环境变量，确保与 `base_url` 方案/地域一致；  
3. **填准 model**：查文档确认目标模型是否支持该接口（例如 `qwen-vl-plus` 仅支持 Vision API，不支持 Chat Completions）；  
4. **发请求**：用任意 OpenAI SDK（如 `openai==1.40.0`）或 curl 调用，仅需替换 `base_url` 和 `api_key`：

```bash
curl -X POST "https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": false
  }'
```

✅ **避坑提示**：  
- ❌ 不要混用 `temperature` 和 `top_p`；  
- ❌ 不要用 `dashscope.aliyuncs.com` 调用子空间模型（会失败）；  
- ❌ 不要在 `responses` 接口依赖 `session_id` —— 它不生效；  
- ✅ 流式响应中，`delta.content` 字段即增量文本，末尾 `usage` 仅在 `stream_options.include_usage=true` 时返回；  
- ✅ 多模态输入请用 `image_url` 格式（Vision API），或先上传文件获取 `oss://` URL 再传入（需 Header 加 `X-DashScope-OssResourceResolve: enable`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


