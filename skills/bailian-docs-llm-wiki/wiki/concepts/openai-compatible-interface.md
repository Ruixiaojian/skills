# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI 官方 REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings` 等路径与请求/响应结构），使开发者能直接复用现有 OpenAI SDK（如 `openai>=1.0`）、工具链或业务代码，零改造接入千问（Qwen）及第三方大模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移存量应用**：已有基于 OpenAI SDK 构建的聊天机器人、RAG 应用或自动化工作流，只需替换 `base_url` 和 `api_key`，无需修改逻辑代码即可切换至百炼服务。
- **多模型统一调度**：通过同一套 OpenAI 接口调用 Qwen 系列（`qwen3.7-plus`、`qwen-vl-plus`）、DeepSeek、Kimi、GLM 等数十种模型，实现跨厂商能力编排。
- **工具链即插即用**：支持 Cursor、Cherry Studio、Qwen Code、Hermes Agent、Dify（按量计费模式）、Postman、cURL 等主流开发工具和低代码平台，开箱即用。
- **分层能力适配**：
  - `Chat Completions`：通用对话与文本生成，兼容 `messages` 格式与流式响应；
  - `Responses`：面向智能体（Agent）的增强接口，自动管理上下文并内置联网搜索、网页提取等工具，仅限 `qwen3-*` 系列；
  - `Vision`：支持图像理解（Qwen-VL、QVQ、Qwen-OCR），输入含 `url` 或 `base64` 的 `image_url` 字段；
  - `Embedding`：向量化服务（`text-embedding-v1` 至 `v4`），输出格式与 OpenAI 完全一致；
  - `File` 与 `Batch`：支持文件解析（`purpose="file-extract"`）和批量异步推理（单次最高 256K tokens 上下文）。

> ⚠️ 注意：并非所有模型都支持全部 OpenAI 接口类型。例如 Qwen-Audio 仅支持 DashScope 原生协议；Qwen-OCR 仅支持 Vision 接口；私有调优模型**不支持任何 OpenAI 兼容接口**，必须使用 DashScope 原生调用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | **必须配置为业务空间专属域名**，推荐格式：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（如 `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）<br>旧域名（`dashscope.aliyuncs.com/compatible-mode/v1`）仍可用，但性能与稳定性较低，官方强烈建议迁移。 |
| `api_key` | string | 是 | 必须与 `base_url` 所属地域匹配（北京 Key 不可用于新加坡 Endpoint）；建议设为环境变量 `DASHSCOPE_API_KEY`。 |
| `model` | string | 是 | 模型 ID 必须为[文档明确列出的支持型号](#)，如 `qwen3.7-plus`、`qwen-vl-plus`、`text-embedding-v1`；拼写错误或使用非兼容型号将返回 HTTP 404。 |
| `stream` | boolean | 否 | 控制是否启用流式响应（SSE）。流式末尾可加 `stream_options={"include_usage": true}` 获取 token 统计。 |
| `temperature` / `top_p` | number | 否 | 二者互斥，建议只设其一以控制输出多样性；取值范围均为 `0.0–1.0`（部分模型实测支持扩展值，但生产环境建议 ≤1.2）。 |
| `max_tokens` | integer | 否 | 仅作输出截断控制（不影响模型内部生成长度），最大值依模型而定（如 `qwen3.7-max` 为 8192）。 |

### 特定接口补充字段
- `Chat Completions`：使用 `messages: [{role: "user", content: "..."}]`，支持 `tool_choice` 和 `tools`（JSON Schema 工具定义）。
- `Responses`：使用 `input`（字符串或消息数组）+ `previous_response_id`（自动上下文管理）。
- `Vision`：`messages` 中 `content` 可包含 `{type: "image_url", image_url: {url: "data:image/png;base64,..."}}` 或 OSS 临时 URL。
- `Embedding`：使用 `input` 字符串或字符串数组，`encoding_format` 支持 `"float"` 或 `"base64"`。

## 面向开发者，简洁实用

✅ **三步上手（Python 示例）**：
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为你的 WorkspaceId + 地域
)

# 调用千问旗舰模型
response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "用 Python 写一个快速排序"}],
    temperature=0.5,
    stream=False
)
print(response.choices[0].message.content)
```

✅ **调试建议**：
- 使用 `curl -v` 查看完整请求头与响应状态码，快速定位认证或路由问题；
- 流式响应请用 `curl -N` 或 SDK 的 `stream=True` 迭代处理；
- 遇到 `404 Not Found`：检查 `model` 是否拼写正确、是否在当前地域支持列表中；
- 遇到 `401 Unauthorized`：确认 `api_key` 与 `base_url` 地域一致，且未过期；
- 遇到限流（`429 Too Many Requests`）：查看 [限流文档](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 获取 RPM/TPM 配额。

✅ **生产最佳实践**：
- 始终使用 **业务空间专属域名**（含 `WorkspaceId`），避免跨地域调用失败；
- 私有调优模型、异步任务、文件上传等高级能力，请改用 DashScope 原生接口；
- 工具调用返回字段已统一映射为 `tool_calls`（SDK 封装层），**勿直接解析原始响应中的 `function_call` 字段**；
- 文件类多模态请求，务必先调用上传接口获取 `oss://` 临时 URL，并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

> 📌 提示：所有 OpenAI 兼容接口均基于统一的 `compatible-mode/v1` 协议层，底层由百炼统一调度与计费，开发者无需关心模型部署细节。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more about models](../api/more-about-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


