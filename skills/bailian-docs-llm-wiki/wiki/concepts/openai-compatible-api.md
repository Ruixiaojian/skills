# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、字段命名与语义规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（如 `openai==1.0+`）和代码逻辑，无需修改业务逻辑即可将 OpenAI 模型调用无缝迁移至百炼的 Qwen 等国产大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：已集成 `openai` SDK 的应用，只需替换 `base_url` 和 `api_key`（或设为 `OPENAI_API_KEY` 环境变量），即可调用 `qwen-max`、`qwen-plus` 等模型，实现零代码改造上线。  
- **构建[多模态](multi-modal.md)智能体**：通过 `chat/completions` 接口，在 `messages.content` 中传入 `image_url`（支持 Qwen-VL 系列），直接复用 OpenAI 图像理解调用模式。  
- **启用自动工具调用**：使用 `responses.create()`（OpenAI 兼容 Responses API），平台自动解析用户意图、触发联网搜索、代码解释器等内置工具，并维护完整对话上下文，适合快速搭建智能助手。  
- **接入第三方 AI 工具链**：Cursor、Dify、Hermes Agent、OpenClaw 等 CLI/IDE/桌面工具，只要支持 OpenAI 协议，配置百炼专属 `base_url`（如 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`）后即可直连调用。  
- **批量与文件处理**：通过兼容的 `/v1/batches` 和 `/v1/files` 接口，复用 OpenAI 批量推理与文档分析工作流，单请求同步处理多条 [prompt](../guides/prompt.md) 或上传 PDF/TXT/DOCX 文件进行内容提取。  
- **调用已发布应用**：部分智能体/工作流应用支持通过 OpenAI 兼容的 `responses` 接口调用（需应用配置启用），此时 `input` 字段传入标准 `messages` 数组，实现与原生 Chat Completions 一致的会话体验。

> ⚠️ 注意：Qwen-VL、Qwen-Audio、Qwen-Coder-Turbo 等特定模型**不支持所有 OpenAI 兼容接口**——前者仅限 `chat/completions`（非 `completions`），后者**仅支持 `completions` 接口**，不支持 `chat/completions` 或 `responses`；[多模态](multi-modal.md)能力（图像/文件）需模型本身支持且在兼容接口中显式启用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | string | ✓ | OpenAI 兼容接口专属端点，**必须使用业务空间专属域名**（非通用 `dashscope.aliyuncs.com`） | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | ✓ | 推荐使用 `DASHSCOPE_API_KEY` 环境变量；若用 `openai` SDK，也可设为 `OPENAI_API_KEY` | `sk-xxx`（百炼生成的密钥） |
| `model` | string | ✓ | 模型 ID 必须严格匹配[官方支持列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)，大小写与连字符敏感 | `qwen3.8-max`、`qwen-vl-plus`、`text-embedding-v4` |
| `messages` | array | ✓（`chat/completions`） | 标准 OpenAI 格式：`[{ "role": "user", "content": "..." }]`；`system` 角色支持，但部分模型可能忽略 | `[{"role":"system","content":"你是一名助手"},{"role":"user","content":"你好"}]` |
| `previous_response_id` | string | ✓（`responses.create`） | 多轮对话必需：传入上一轮响应的顶层 `id`（UUID），用于上下文自动注入 | `"resp_abc123..."` |
| `stream` | boolean | ✗ | 设为 `true` 启用流式响应；注意字段路径为 `delta.content`（非 `output.text`） | `true` |
| `enable_thinking` | boolean | ✗（Qwen3 系列推荐） | 显式开启推理链模式，提升复杂任务准确性（部分工具需额外勾选 R1 格式开关） | `true` |

> ✅ 提示：`temperature`、`top_p`、`max_output_tokens` 等通用参数均被支持；但 `enable_search`、`seed`、`tool_choice` 等 DashScope 原生参数在 OpenAI 兼容层会被忽略或静默转换，如需精确控制，请切换至 DashScope 原生接口。

## 面向开发者，简洁实用

- **三步启动**：  
  1. 安装 SDK：`pip install openai`（或 `pip install dashscope`）；  
  2. 配置凭证：`export OPENAI_API_KEY=sk-xxx` + `export OPENAI_BASE_URL=https://ws-xxx.region.maas.aliyuncs.com/compatible-mode/v1`；  
  3. 发起调用：  
     ```python
     from openai import OpenAI
     client = OpenAI()
     response = client.chat.completions.create(
         model="qwen3.8-max",
         messages=[{"role": "user", "content": "用 Python 写一个快速排序"}]
     )
     print(response.choices[0].message.content)
     ```

- **调试技巧**：  
  - 若返回 `404 Not Found`，检查 `base_url` 是否含 `/compatible-mode/v1` 后缀；  
  - 若报 `model not found`，确认模型名拼写（如 `qwen-vl-plus` ≠ `qwen_vl_plus`）及计费方案是否支持该模型（[Token](token.md) Plan 不支持[多模态](multi-modal.md)）；  
  - 流式响应请监听 `delta.content` 字段，而非 `choices[0].message.content`；  
  - 多轮对话务必使用 `responses.create()` 并传 `previous_response_id`，避免手动拼接 `messages` 导致上下文丢失。

- **避坑提醒**：  
  - ❌ 不要混用 `DASHSCOPE_API_KEY` 和 `OPENAI_API_KEY` 环境变量；  
  - ❌ 不要对 `qwen-coder-turbo` 调用 `chat/completions`；  
  - ❌ 不要在 `base_url` 中省略 `{workspace_id}` 和 `{region}` —— 这是强制要求，非可选占位符。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [bailian application calling](../guides/bailian-application-calling.md)


