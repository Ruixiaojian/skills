# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、视觉理解、向量嵌入、批量推理、文件管理、对话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按协议类型划分：

- **Chat Completions**：支持 Qwen 系列（`qwen-plus`、`qwen3.7-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；但 **Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 原生协议。
- **Responses API**：专为智能体设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3-max`、`qwen3-plus`、`qwen3-flash` 及其各版本后缀（如 `qwen3.7-plus-2026-05-26`），并支持通过 `previous_response_id` 自动管理多轮上下文（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **Vision（多模态）**：支持 `qwen3-vl-plus`、`qwen3-vl-flash`、`QVQ`（流式专用）、`Qwen-OCR`，输入格式兼容 OpenAI 的 `image_url` + `text` 混合 content 数组（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 全系列，其中 `v3`/`v4` 支持 `dimensions` 参数指定向量维度；**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **Completions（文本补全）**：当前仅支持 `qwen-coder-turbo`，适用于代码续写与中间补全（如函数体生成），不支持后缀生成前缀（详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）。
- **Files & Batch**：`files` 接口支持 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集）三类用途；`batch` 接口分两种形态：基于文件的异步批量（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）和同步等待的单请求批量（[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **Conversations**：提供会话生命周期管理（create/retrieve/update/delete）及消息项增删，用于跨设备持久化对话状态（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

> **注意**：文档 7（Batch 文件）与文档 9（Batch Chat）对同一模型（如 `qwen3.7-plus`）的上下文长度限制描述一致（256K），但文档 9 明确要求 `enable_thinking` 必须作为 `body` 顶层参数传入，而文档 7 未强调此约束，实际调用时应以文档 9 的说明为准。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 服务端点地址 | **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐；各地域路径一致，仅 host 不同（北京/新加坡/弗吉尼亚/东京/法兰克福） |
| `model` | string | 模型名称 | 需严格匹配文档中列出的支持列表，大小写敏感；`qwen3-vl-plus` 等视觉模型不可用于纯文本 `chat/completions` |
| `stream` | boolean | 是否启用[流式输出](../concepts/streaming-output.md) | 默认 `false`；视觉模型 `QVQ` **强制要求 `stream=True`**（见文档 5） |
| `stream_options` | object | 流式控制选项 | 设置 `{"include_usage": true}` 可在最后一 chunk 返回 token 统计 |
| `dimensions` | integer | 向量维度 | 仅 `text-embedding-v3`/`v4` 支持，`v1`/`v2` 不支持该参数（见文档 6） |
| `previous_response_id` | string | 上一轮 Responses ID | 用于多轮对话，值为响应顶层 `id`（UUID 格式），**非 `output` 内 `msg_xxx`**（见文档 2） |
| `enable_thinking` | boolean | 是否启用思考模式 | `qwen3.5+` 系列默认开启，若需关闭必须显式传入且与 `model` 同级（见文档 7 和 9） |

## 使用方式

### 通用初始化（Python 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)
```

### 各接口典型调用
- **Chat Completions**：`client.chat.completions.create(model="qwen-plus", messages=[...])`
- **Responses**：`client.responses.create(model="qwen3.7-plus", input="...")` 或带 `previous_response_id`
- **Vision**：`messages` 中 `content` 为含 `{"type":"image_url","image_url":{"url":"..."}}` 的数组
- **Embedding**：`client.embeddings.create(model="text-embedding-v4", input="...", dimensions=1024)`
- **Files**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`
- **Batch（文件）**：先 `client.files.create(..., purpose="batch")`，再 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`
- **Batch Chat（同步）**：切换 `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数同 Chat Completions
- **Conversations**：`client.conversations.create(items=[{"role":"system","content":"..."}])`，后续通过 `conversation_id` 管理

### LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（见文档 10）；
- **DashScope 原生方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼文本模型（见文档 10）。

## 限制和注意事项

- **地域与域名绑定**：API Key 与地域强绑定（北京 Key 不能用于新加坡服务），且必须使用对应地域的 `base_url`；业务空间专属域名（`{WorkspaceId}.xxx.maas.aliyuncs.com`）为性能与稳定性最佳实践，旧域名将逐步淘汰。
- **文件限制**：`files` 接口总容量 ≤100 GB、总数 ≤10000 个；`file-extract` 单文件 ≤150 MB，`batch`/`fine-tune` 单文件分别 ≤500 MB / ≤300 MB。
- **模型能力差异**：
  - `Qwen-Audio` 不支持 OpenAI 兼容协议（见文档 1）；
  - `QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)（见文档 5）；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出（见文档 7 和 9）；
  - 多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见文档 6）。
- **参数兼容性**：`dimensions` 仅对 `text-embedding-v3`/`v4` 有效；`enable_thinking` 必须置于请求 body 顶层，不可嵌套于 `extra_body`（见文档 7 和 9）。
- **错误处理**：所有接口均返回标准 OpenAI 错误结构（`{"error":{"message":...,"code":...}}`），需检查 `code` 字段（如 `invalid_api_key`）进行诊断（见文档 3 和 6）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


