# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议层，严格遵循 OpenAI 的 `chat/completions`、`completions`、`embeddings` 等核心端点规范与请求/响应格式，使开发者能直接复用 OpenAI 官方 SDK（如 `openai==1.0+`）、现有代码逻辑和生态工具（如 LangChain、LlamaIndex），实现零代码迁移或快速集成。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：若应用已基于 OpenAI SDK 开发，只需替换 `api_key` 和 `base_url`，即可调用 Qwen 全系列（`qwen3.7-plus`、`qwen3.7-max`、`qwen-flash` 等）、DeepSeek、Kimi、GLM 等模型，无需修改业务逻辑。
- **[多模态](multi-modal.md)与专用模型接入**：支持 `qwen-vl-plus`（视觉理解）、`text-embedding-v1~v4`（向量嵌入）、`qwen-mt-plus`（机器翻译）、`farui-plus`（法律）等垂直模型，但需注意：`Qwen-Audio` 和 `qwen-deep-research` 明确不支持该协议。
- **会话与批量任务**：通过 `responses` 接口实现自动上下文管理（传 `previous_response_id` 即可续聊）；通过 `batch` 模式提交异步批量请求（文件输入式）或同步保序批量推理（`/v1/chat/completions` + `batch: true`）。
- **开发工具直连**：支持 Cursor、Cherry Studio、Qoder、Dify（HTTP 节点）等主流 AI 工具，配置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` 后即可调用。
- **生产环境部署**：推荐使用**业务空间专属域名**（如 `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），获得更高吞吐、更低延迟与流量隔离能力；旧域名 `dashscope.aliyuncs.com` 仅用于兼容验证。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | 接口根地址。生产环境必须使用业务空间专属域名（含 `WorkspaceId` 和 `region`）；地域示例：<br>• 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`<br>• 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（无 WorkspaceId） |
| `model` | string | 是 | 模型 ID，大小写敏感。支持范围广，如 `qwen3.7-plus`、`deepseek-chat`、`kimi-k2.6`；但 `completions` 接口仅限 `qwen-coder-turbo`，`responses` 接口仅限 `qwen3-*` 系列及 `qwen-plus`。 |
| `messages` | array | 是 | 标准 OpenAI 格式：`[{ "role": "user", "content": "..." }]`；部分专用模型（如 `tongyi-intent-detect-v3`）需在 `system` 消息中声明 `Response in INTENT_MODE.` 才生效。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 时返回 `text/event-stream` 流式响应；流式 chunk 中 `delta.tool_calls` 可能缺失参数，建议非流式模式验证工具调用。 |
| `stream_options` | object | 否 | 如 `{"include_usage": true}`，可在末尾 chunk 返回 token 统计（`usage` 字段）。 |
| `extra_body` | object | 否 | 用于传递 OpenAI 原生不支持的扩展参数，例如：<br>• `qwen-mt-plus`: `{"translation_options": {"source_lang": "zh", "target_lang": "en"}}`<br>• `qwen3.8-max-preview`: `{"enable_thinking": true}`（强制启用）<br>• `gui-plus`: `{"vl_high_resolution_images": true}` |
| `previous_response_id` | string | 否 | `responses` 接口专用，传入上一轮响应 ID（如 `resp_abc123`），平台自动注入历史消息，免手动维护对话状态。 |

> ⚠️ 注意事项：
> - 不支持 `response_format`（如 JSON Schema 强约束），需结构化输出请改用 DashScope 原生接口；
> - `temperature` 仅接受 `0.0–1.0`（DashScope 原生支持 `0.0–2.0`）；
> - 所有请求均需 `Authorization: Bearer <DASHSCOPE_API_KEY>`，API Key 须与 `base_url` 所属地域及计费方案严格匹配；
> - 单次 `messages` 总长度上限依模型而异（如 `qwen3.7-max` 为 32768 tokens），超限返回 `400 Bad Request`。

## 面向开发者，简洁实用

✅ **三步启动**：  
1. 控制台创建 API Key（环境变量 `DASHSCOPE_API_KEY`）；  
2. 获取 `WorkspaceId` 和地域，拼出 `base_url`；  
3. 用 OpenAI SDK 发起请求：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

resp = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=False
)
print(resp.choices[0].message.content)
```

✅ **调试建议**：  
- 优先使用 `stream=False` 验证基础功能；  
- 查看响应中的 `x-request-id` 头，用于问题排查与日志回溯；  
- 生产环境务必启用业务空间专属域名，避免限流与性能瓶颈；  
- 专用模型（OCR、意图识别等）请查阅对应文档确认 `extra_body` 参数格式。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


