# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI 官方 REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings` 等），使开发者能直接复用 OpenAI SDK、LangChain、LlamaIndex 等生态工具，无需修改业务逻辑代码即可迁移接入千问（Qwen）及第三方大模型。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有项目**：若你已使用 `openai==1.0+` SDK 调用 GPT 系列模型，只需将 `base_url` 替换为百炼的兼容端点，并设置 `model="qwen3.8-max"` 等合法模型名，即可零代码切换至 Qwen 或 DeepSeek、Kimi 等第三方模型。
- **构建智能体（Agent）**：优先选用 **OpenAI 兼容-Responses API**（端点 `/v1/responses`），它内置联网搜索、代码解释器、网页提取三类工具，自动维护上下文与工具执行链，适合快速搭建问答助手、数据分析 Bot 等应用；支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-plus` 等主力模型。
- **多模态交互**：调用 `qwen-vl-plus`、`qvq` 等视觉模型时，使用标准 OpenAI `messages` 格式，通过 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` 传入图像，无需适配私有协议。
- **向量检索与批量处理**：Embedding 接口（`/v1/embeddings`）兼容 `text-embedding-v1` 至 `v4` 全系列，支持 `dimensions` 参数；Batch Chat 支持同步阻塞式批量请求（端点 `/batch/v1/chat/completions`），适用于评测、标注等离线任务。
- **应用级集成**：通过 Responses API 调用已发布的智能体或工作流应用（端点 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`），复用 OpenAI SDK 的 `.responses.create()` 方法，同时支持 `session_id` 维持多轮对话状态。

> ⚠️ 注意：并非所有模型都支持全部 OpenAI 兼容能力。例如 `qwen-turbo` 和 `qwen3-flash` 仅支持基础 Chat Completions，不支持 Responses 工具链；`qwen-audio` 和 `qwen3-vl-embedding` 不支持 OpenAI 兼容协议，必须使用 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `model` | string | ✅ | 模型 ID，需与所选接口支持列表匹配。不同协议支持范围不同（见上文）。 | `"qwen3.8-max"`, `"text-embedding-v4"` |
| `base_url` | string | ✅ | **必须使用业务空间专属域名**（推荐），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名 `dashscope.aliyuncs.com` 已不推荐。美国（弗吉尼亚）地域无 WorkspaceId，使用 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`。 | `"https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"` |
| `api_key` | string | ✅ | 百炼 API Key（非 OpenAI key），建议通过环境变量 `DASHSCOPE_API_KEY` 注入。 | `"sk-xxx"` |
| `stream` | boolean | ❌（默认 `false`） | 启用流式响应。流式 chunk 中含 `delta.content` 字段，末尾可加 `stream_options={"include_usage": true}` 获取 token 统计。 | `true` |
| `temperature` / `top_p` | number | ❌（二选一） | 控制生成多样性；二者不可同时设置。OpenAI 兼容接口默认 `temperature=1.0`（DashScope 原生默认 `0.8`）。 | `0.7` |
| `max_tokens` | integer | ❌ | 输出长度软限制，超限将截断，不影响模型内部推理。 | `1024` |
| `stop` | string / array | ❌ | 指定终止字符串或数组，如 `["\n", "。"]`。 | `["\n"]` |
| `seed` | integer | ❌ | 启用确定性输出（相同 seed + 相同输入 → 相同输出）。 | `42` |

**特定接口扩展参数**：
- **Responses API**：`input`（字符串或消息数组）、`previous_response_id`（关联上一轮响应 ID，实现上下文延续）；
- **Files API**：`purpose="file-extract"`（用于长文档问答）、`purpose="batch"`（用于批量任务）；
- **Conversations API**：`items`（初始化会话消息）、`metadata`（自定义会话元数据）；
- **Application Call**：`app_id`、`session_id`（维持对话状态）、`biz_params`（透传工作流自定义参数）。

## 面向开发者：简洁实用提示

- ✅ **首选业务空间域名**：新项目务必使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/...`，它具备更高吞吐、更低延迟与业务级隔离；WorkspaceId 在控制台「业务空间管理」中获取。
- ✅ **SDK 调用最简示例**（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  for chunk in resp:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
  ```
- ⚠️ **避免混用协议字段**：OpenAI 兼容接口返回 `delta`，DashScope 原生返回 `output.text`；流式解析逻辑不可互换。
- ⚠️ **注意模型能力边界**：工具调用（tool use）在 OpenAI Chat Completions 中**不原生支持**（需自行封装），而 Responses API 的工具为预置且不可自定义；如需完全可控的[函数调用](function-calling.md)，请选用 Anthropic Messages 或 DashScope 原生接口。
- 🔍 **查错优先看 HTTP 状态码与 error.message**：401（认证失败）、404（模型不可用）、429（限流）、400（参数错误，如 messages 超 32768 tokens）—— 所有错误均返回标准 OpenAI 格式 `{ "error": { "message": "...", "type": "..." } }`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)


