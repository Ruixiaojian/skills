# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者快速迁移现有应用或构建新场景。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 三要素即可接入，无需重写核心逻辑。各接口在功能定位、模型支持和使用约束上存在明确分工，需按场景选型。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力覆盖文本、多模态、向量、文件处理与对话管理五大类：

- **Chat Completions**：兼容标准 `chat/completions` 接口，支持 Qwen 系列（`qwen-plus`, `qwen-flash`, `qwen3-*`）、Qwen-VL、Qwen-Coder、DeepSeek、Kimi、GLM、MiniMax 等数十种模型，但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses API**：作为 Chat Completions 的演进版本，专为智能体（Agent）设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3-*` 全系列及 `deepseek-v4-flash` 等模型，[文档明确指出其优势在于简化上下文管理与内置工具调用](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision（图像理解）**：通过 `chat/completions` 接口支持 `qwen3-vl-plus`, `QVQ`, `Qwen-OCR` 等视觉模型，要求输入格式为 `messages` 中包含 `image_url` 或 Base64 编码内容。
- **Embedding**：提供 `text-embedding-v1` 至 `v4` 四代文本向量模型，支持多语种及可变维度（`v3/v4` 支持 `dimensions` 参数），但 [多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 OpenAI 兼容接口](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Files & Batch**：`files` 接口支持 `file-extract`（文档分析）、`batch`（批量推理）、`fine-tune`（微调数据集）三种用途；`batches` 接口支持异步批量处理，费用为实时调用的 50%，适用于数据分析、评测等非实时场景。
- **Conversations**：提供会话生命周期管理（创建、查询、更新、删除、追加消息），配合 Responses API 实现跨设备上下文延续，[其新版路径已统一为 `/compatible-mode/v1/conversations`](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 1 与文档 2 均提及“业务空间专属域名迁移”，但文档 1 未列出德国（法兰克福）地域的 `base_url`，而文档 2 明确给出 `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`。实际开发中应以文档 2 的地域列表为准。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源 |
|------|------|------|------|------|
| `base_url` | string | 是 | 服务端点，必须匹配地域与接口类型。北京/新加坡需填 `{WorkspaceId}`；弗吉尼亚/东京/法兰克福等地域无 WorkspaceId（见文档 2）。旧域名（如 `dashscope.aliyuncs.com`）已逐步淘汰。 | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 是 | 模型名称，严格区分大小写与版本后缀（如 `qwen3.8-max` vs `qwen3.7-max`）。部分模型仅限特定地域（如 DeepSeek 仅支持北京/新加坡）。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `stream` | boolean | 否 | 控制输出模式。`true` 时返回流式 chunk；`false`（默认）返回完整响应。Vision 模型（QVQ）强制流式。 | [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `stream_options` | object | 否 | 仅当 `stream=true` 时有效，设 `{"include_usage": true}` 可在最后一 chunk 返回 token 统计。 | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `previous_response_id` | string | 否 | Responses API 专用，用于自动关联上下文，值为上一轮响应的顶层 `id`（非 `output` 内 `msg_xxx`）。有效期 7 天。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `purpose` | string | 是（Files） | 文件上传必需字段，取值 `file-extract` / `batch` / `fine-tune`，决定文件用途与格式校验规则。 | [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) |

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

# Chat Completions
resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])

# Responses API（推荐用于 Agent 场景）
resp = client.responses.create(model="qwen3.8-max", input="你能做什么？")

# Embedding
resp = client.embeddings.create(model="text-embedding-v4", input="hello world", dimensions=1024)

# Files upload
file_obj = client.files.create(file=Path("doc.pdf"), purpose="file-extract")
```

### LangChain 集成
- **`langchain_openai`**：仅支持 OpenAI 兼容模型（如 `qwen-plus`），配置 `base_url` 即可：
  ```python
  from langchain_openai import ChatOpenAI
  llm = ChatOpenAI(model="qwen-plus", base_url="https://.../compatible-mode/v1")
  ```
- **`langchain_community`（`ChatTongyi`）**：支持百炼全量模型（含非 OpenAI 兼容模型），需安装 `dashscope` 包：
  ```python
  from langchain_community.chat_models.tongyi import ChatTongyi
  llm = ChatTongyi(model="qwen-long", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
  ```

### 批量处理（Batch）
- **文件批量**：上传 JSONL 文件（每行一个请求），调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`。
- **单请求批量**：直接修改 `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数不变，服务端同步等待并返回结果。

## 限制和注意事项

- **地域与模型绑定**：DeepSeek、Qwen-VL 等部分模型仅在北京/新加坡地域可用；德国法兰克福地域仅支持 Responses API（文档 2），不支持 Chat Completions（文档 1 未覆盖）。
- **[Token](../concepts/token.md) 限制**：Batch 场景下 `qwen3-*` 系列模型单次请求上下文最大 256K tokens；`qwen3.5-omni-plus` 不支持语音输出；`qwen-coder-turbo`（Completions 接口）仅支持华北2（北京）地域。
- **兼容性边界**：
  - Qwen-Audio 不支持 OpenAI 协议，必须使用 DashScope 原生接口。
  - `completions` 接口（文档 3）仅支持 `qwen-coder-turbo`，且不支持后缀生成前缀。
  - Conversations API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/conversations`。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码；生产环境禁用 `stream_options={"include_usage": true}`（可能暴露 token 统计）。
- **错误处理**：所有接口遵循 OpenAI 错误格式（`error.code`, `error.message`），通用错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


