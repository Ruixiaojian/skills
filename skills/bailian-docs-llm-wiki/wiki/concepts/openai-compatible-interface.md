# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 官方 API 协议（v1.0+），支持使用标准 OpenAI SDK（如 `openai>=1.0.0`）直接调用千问（Qwen）及第三方大模型，实现零代码迁移、快速验证与生产集成。

## 在百炼平台的不同场景中如何使用

- **快速迁移现有项目**：已有基于 OpenAI SDK 的应用（如 LangChain、LlamaIndex、Cursor、Dify HTTP 节点等），只需替换 `base_url` 和 `model` 参数，无需修改业务逻辑即可接入 Qwen、DeepSeek、Kimi、GLM 等模型。
- **[多模态](multi-modal.md)统一接入**：除文本生成（`/chat/completions`）外，还支持视觉理解（`/vision/completions`）、向量嵌入（`/embeddings`）、批量推理（`/batch`）、会话管理（`/conversations`）和[文件处理](file-processing.md)（`/files`）等能力，均复用同一套 OpenAI 风格请求结构。
- **开发与调试提效**：配合 Postman、cURL 或百炼 CLI，可快速验证模型行为；支持流式响应（`stream: true`）、token 统计（`stream_options={"include_usage": true}`）和错误码标准化（如 `400` 参数错误、`429` 限流、`401` 凭证无效）。
- **生产环境部署**：推荐使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），获得更高吞吐、更低延迟与独立流量隔离；避免使用已弃用的 `dashscope.aliyuncs.com` 域名。
- **跨方案适配**：[Token](token.md) Plan、Coding Plan 和按量计费方案均提供对应 Base URL（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），但 API Key 不互通，需严格匹配方案与地域。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen3.7-plus`、`text-embedding-v4`、`qwen-vl-plus`；命名需与所选方案支持列表一致（如 [Token](token.md) Plan 中 `kimi-k2.6` 需写为 `kimi-k2-6`） |
| `base_url` | string | 是 | 服务端点，**必须使用业务空间专属域名或方案专用域名**；各地域格式不同（北京：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；美国：`dashscope-us.aliyuncs.com`） |
| `api_key` | string | 是 | 百炼 API Key，建议通过环境变量 `DASHSCOPE_API_KEY` 设置，禁止硬编码 |
| `messages` | array | 是（Chat 接口） | 标准 OpenAI 格式：`[{ "role": "user", "content": "..." }]`；Anthropic 兼容模式下不适用 |
| `input` | string / array | 是（Embedding/Rerank） | 向量化输入支持字符串、字符串数组或文件 URL；Rerank 输入需按模型要求组织（如 `qwen3-rerank` 要求 `query` 与 `documents` 平级） |
| `temperature` / `top_p` | number | 否 | 控制生成多样性，范围 `0.0–1.0`（OpenAI 兼容接口限制）；二者建议只设其一 |
| `max_tokens` | integer | 否 | 限制输出长度，超限自动截断（不影响模型内部生成） |
| `stream` | boolean | 否 | 启用流式响应，默认 `true`；搭配 `stream_options={"include_usage": true}` 可在末尾返回 token 使用统计 |
| `stop` | string / array | 否 | 指定终止字符串，可用于敏感词拦截或格式控制 |
| `seed` | integer | 否 | 设置随机种子（`0–2^31−1`），获得确定性输出 |
| `dimensions` | integer | 否（Embedding 特有） | 指定向量维度（仅 `text-embedding-v3/v4`、`qwen3-vl-embedding` 等支持） |
| `enable_thinking` | boolean | 否（Qwen3.8+ 特有） | qwen3.8-max-preview 强制启用，OpenAI 兼容接口需通过 `extra_body={"enable_thinking": true}` 传入 |

> ⚠️ 注意事项：
> - 不支持 `response_format`（如 JSON Schema 强约束），需结构化输出请改用 DashScope 原生接口；
> - `tools` 自定义工具仅 DashScope 和 Anthropic 兼容接口支持，OpenAI 兼容-Responses 使用平台预置工具；
> - `system` 提示词在 OpenAI 兼容接口中作为 `messages[0]` 的 `role: "system"` 发送，无 token 截断限制（区别于 Anthropic 兼容接口）；
> - 所有 OpenAI 兼容接口默认启用流式响应，但工具调用的 `delta.tool_calls` 字段在流式 chunk 中可能不完整，建议非流式模式验证逻辑。

## 面向开发者：一句话上手

安装 SDK → 设置环境变量 → 初始化客户端 → 调用标准方法：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 文本生成
resp = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
print(resp.choices[0].message.content)

# 向量嵌入
resp = client.embeddings.create(model="text-embedding-v4", input=["hello world"], dimensions=1024)
print(resp.data[0].embedding[:5])
```

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


