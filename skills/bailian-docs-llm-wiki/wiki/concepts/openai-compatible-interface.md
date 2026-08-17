# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API，严格遵循 OpenAI 的 RESTful 协议规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等），使开发者无需修改业务逻辑即可将现有基于 OpenAI SDK 或生态工具（如 LangChain、LlamaIndex、Cursor、Dify）的应用快速迁入百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套按能力分层、按用途定制的协议族，在百炼中主要应用于以下四类核心场景：

- **模型直调（Chat/Completions）**：面向 Qwen、DeepSeek、GLM 等文本大模型，通过 `POST /compatible-mode/v1/chat/completions` 调用标准对话能力。适用于已有 OpenAI 代码库的平滑迁移，迁移成本最低。
- **智能体增强调用（Responses）**：专为新版智能体（Agent 2.0）设计，端点为 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。内置联网搜索、代码解释器、网页提取等工具，自动维护多轮上下文，**无需手动传 `session_id` 或拼接历史消息**，适合需开箱即用推理能力的场景。
- **[多模态](multi-modal.md)与专项能力**：支持 Vision（图文混合输入）、Embedding（向量生成）、Code（补全）、Batch（批量处理）等子协议，均复用 OpenAI 路径结构（如 `/v1/chat/completions` for VL, `/v1/embeddings` for text-embedding-v1），但模型支持范围有明确约束（例如 Qwen-VL 支持 Vision 接口，但 `qwen3-vl-embedding` 不支持 Embedding 接口）。
- **开发工具与客户端集成**：所有主流 AI 工具（如 Hermes Agent、Qoder IDE、Claude Code、Postman）均可直接配置百炼的 OpenAI 兼容 `base_url` 和 `api_key`，零代码接入；不同计费方案（[Token](token.md) Plan、Coding Plan、按量计费）对应不同域名，但协议完全一致。

> ⚠️ 注意：OpenAI 兼容接口**不支持** Anthropic Messages 协议（如 `tool_use` 显式控制）、也不支持 DashScope 原生接口的全部能力（如流式响应中的 `delta.tool_calls` 结构、`pre_response_id` 多轮管理）。若需这些能力，请切换至 Anthropic 兼容或 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | 必填，服务入口地址，**必须匹配计费方案与地域**：<br>• [Token](token.md) Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Coding Plan：`https://coding.dashscope.aliyuncs.com/compatible-mode/v1`<br>• 按量计费：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台获取；旧域名 `dashscope.aliyuncs.com` 已弃用，不推荐使用 |
| `api_key` | string | 必填，与 `base_url` 严格绑定，不可跨方案混用（如 [Token](token.md) Plan Key 不能用于按量计费域名） | 推荐通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码 |
| `model` | string | 必填，模型 ID，区分大小写与版本后缀（如 `"qwen3.8-max"`、`"qwen2.5-7b-instruct"`） | 不同接口支持模型不同：`responses` 支持 `qwen3.*` 系列，`completions` 仅支持 `qwen-coder-turbo`，`embeddings` 仅支持 `text-embedding-*` |
| `messages` | array | 必填（Chat/Completions/Responses），格式为 `[{"role":"user","content":"..."}]`；支持 `system`、`user`、`assistant` 角色 | `system` 提示词计入上下文长度；总 tokens 不得超过模型上下文上限（如 `qwen-max` 为 32768） |
| `stream` | boolean | 可选，启用流式响应（默认 `false`）；`stream_options={"include_usage": true}` 可在末尾返回 token 统计 | QVQ 模型**仅支持流式**；工作流应用需在节点中显式开启「[流式输出](streaming-output.md)」开关 |
| `tools` + `tool_choice` | array + string | 可选，定义工具并触发调用（如 `"tool_choice": "auto"`） | 工具执行由服务端托管，结果统一返回在 `content` 字段中；不支持客户端解析 `delta.tool_calls` |
| `previous_response_id` | string | Responses API 多轮对话专用，值为上一轮响应的顶层 `id`（UUID） | 用于自动注入上下文，替代手动维护 `messages` 数组；不可用 `output` 内消息的 `id` 替代 |

## 面向开发者，简洁实用

- ✅ **快速上手**：用任意 OpenAI SDK（如 Python `openai==1.40.0+`），仅需替换 `base_url` 和 `api_key`，一行代码即可调用：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}]
  )
  print(response.choices[0].message.content)
  ```

- ✅ **调试建议**：
  - 首先用 `curl` 验证基础连通性（见各文档示例）；
  - 若报错 `401`，检查 `api_key` 是否与 `base_url` 方案匹配；
  - 若报错 `400`，检查 `model` 是否在该接口支持列表中，或 `messages` 是否超长；
  - 流式响应请确保客户端正确处理 `data:` 分块（非 JSON 对象）。

- ❌ **避坑提示**：
  - 不要尝试在 OpenAI 兼容接口中传 `session_id` 或 `conversation_id` —— 它们被忽略；
  - 不要期望 `delta.tool_calls` 流式结构 —— 工具结果始终在 `content` 中以字符串返回；
  - 不要混用 `base_url` 和 `api_key` 方案（如 Token Plan Key + 按量计费域名）；
  - [多模态](multi-modal.md)（图像/文件）输入仅在 `responses` 和 `vision` 接口中支持，`chat/completions` 默认仅文本。

如需更高控制力（如显式工具调用、思考链管理、会话状态托管），请评估切换至 [Anthropic 兼容接口](Anthropic 兼容-Messages) 或 [DashScope 原生接口](DashScope 原生接口)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [bailian application calling](../guides/bailian-application-calling.md)


