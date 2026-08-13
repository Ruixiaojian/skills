# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `/v1/chat/completions`、`/v1/embeddings` 等路径与字段结构），使开发者无需修改业务代码即可将现有 OpenAI 生态应用（如 LangChain、LlamaIndex、各类 SDK 或 CLI 工具）快速迁移到百炼，复用已有工程实践。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用迁移**：当已有应用基于 `openai>=1.0.0` SDK 调用 `client.chat.completions.create()` 时，只需将 `base_url` 替换为百炼专属兼容地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并保持 `api_key` 为百炼 API Key，即可直接运行，无需重写逻辑。适用于 `qwen-max`、`qwen-plus`、`qwen-turbo` 等文本模型及 `text-embedding-v3` 等向量模型。

- **智能体（Agent）集成**：通过 `OpenAI 兼容-Responses API`（`/v1/responses`）调用已发布的智能体应用，支持 `messages` [多模态](multimodal.md)输入（含 `image_url`）、`stream` [流式输出](streaming-output.md)、`background` 异步模式，并自动集成联网搜索、网页提取等内置工具能力——这是唯一原生支持“开箱即用智能体增强”的 OpenAI 兼容入口。

- **[多模态](multimodal.md)能力适配**：`OpenAI 兼容-Vision API` 支持 `qwen-vl-plus`、`qwen3-vl-plus` 等视觉模型，允许在 `messages.content` 中混用文本与 `{"type":"image_url","image_url":{"url":"..."}}` 结构，但注意 `qwen-vl` 基础版暂不支持该接口。

- **批量与长上下文任务**：`Batch Chat` 和 `Batch File` 场景支持 `qwen3.8-max` 等长上下文模型，通过 `openai.Batch` 或自定义 HTTP 批量请求调用 `/v1/batches`，兼容 OpenAI 批处理语义（需启用 `enable_thinking` 以激活完整推理链）。

- **框架无缝接入**：LangChain 可直接使用 `langchain_openai.ChatOpenAI`（配置 `base_url` + `api_key`），Dify、Flowise、FastAPI 应用亦可复用标准 OpenAI 客户端，大幅降低迁移成本。

> ⚠️ 注意：并非所有百炼模型都支持全部 OpenAI 接口类型。例如 `Qwen-Audio` 不支持 OpenAI Audio 协议；`qwen-coder-turbo` 仅兼容 `completions` 接口，不可用于 `chat/completions`；`qwen-vl` 在 OpenAI 兼容接口中不支持[多模态](multimodal.md)输入（需用 DashScope 原生接口）。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | **必须配置**，指向业务空间专属域名（推荐 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 性能较低 | 各地域域名不同（如新加坡为 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`），且 `WorkspaceId` 是 URL 组成部分 |
| `model` | 必填字符串，值必须与 [模型列表](https://help.aliyun.com/zh/model-studio/models) 中的兼容模型名完全一致（如 `qwen3.8-max`、`text-embedding-v4`） | 模型与接口强绑定：`qwen-coder-turbo` 仅用于 `completions`，`qwen-vl-plus` 仅用于 `chat/completions` 或 `vision` |
| `messages` | Chat 类接口必填，数组格式，每项含 `role`（`system`/`user`/`assistant`）和 `content`（纯文本或含 `type`/`text`/`image_url` 的对象） | `system` 角色仅支持单条，且不能出现在 `messages` 末尾；图像 URL 需为公网可访问地址或 OSS 临时 URL（需加 Header `X-DashScope-OssResourceResolve: enable`） |
| `stream` | 布尔值，默认 `false`。设为 `true` 启用流式响应（SSE 格式） | 流式响应中 `delta.content` 可能为空，需同时检查 `delta.tool_calls`（Responses API）或 `delta.refusal` 字段 |
| `stream_options` | 对象，可选 `{ "include_usage": true }`，在流式响应末尾返回 token 统计（`usage` 字段） | 仅部分接口支持，非全局可用 |
| `enable_search` | 布尔值，默认 `false`。仅 `Responses API` 和 DashScope 原生接口支持，OpenAI 兼容 `chat/completions` **不支持** | 若需联网能力，请优先选用 `Responses API`（`/v1/responses`）而非 `chat/completions` |
| `temperature` / `top_p` | 二者互斥，**只设置其中一个**（文档明确建议），避免行为不可控 | `temperature` 范围 `0.0–2.0`，`top_p` 范围 `0.0–1.0` |

## 面向开发者，简洁实用

- ✅ **快速起步**：  
  ```bash
  curl -X POST "https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
    -H "Authorization: Bearer sk-xxx" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen3.8-max",
          "messages": [{"role": "user", "content": "你好"}],
          "stream": true
        }'
  ```

- ✅ **SDK 推荐用法（Python）**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",
      base_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "解释量子纠缠"}],
      stream=True
  )
  for chunk in response:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
  ```

- ✅ **避坑提示**：  
  - 返回字段（如 `choices[0].message.content`）与 OpenAI 一致，但 `usage.prompt_tokens` 等字段可能为 `null`，**实际计费以 DashScope 控制台日志为准**；  
  - `messages` 总长度受模型上下文限制（如 `qwen-max` ≤ 32768 tokens），超限将返回 `400` 错误；  
  - 文件类输入（PDF/Word）请使用 `Files API` 上传后获取 `file_url`，再传入 `messages`，**不要直接上传二进制文件到 OpenAI 兼容接口**；  
  - 调试时优先使用 `curl` 或 Postman 验证 endpoint 和参数，再集成 SDK。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


