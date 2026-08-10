# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，支持开发者快速迁移现有应用。核心能力覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、批量推理、文件处理及对话状态管理等场景，所有接口均基于标准 OpenAI 协议设计，仅需调整 `base_url`、`api_key` 和 `model` 即可接入。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **文本生成**：包括 `chat/completions`（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）、`responses`（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）、`completions`（[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）三类。其中 `responses` 是 `chat/completions` 的增强演进，内置联网搜索、网页抓取、代码解释器等工具能力，并支持通过 `previous_response_id` 简化多轮上下文管理；`completions` 专用于代码补全等前缀/中缀生成任务，仅支持 `qwen-coder-turbo` 模型。

- **[多模态](../concepts/multi-modal.md)理解**：`chat/completions` 接口兼容视觉模型（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)），支持 `qwen3-vl-plus`、`qwen-vl-ocr` 等模型，输入支持 `text` + `image_url` 结构化消息。

- **向量嵌入**：`embeddings` 接口（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）支持 `text-embedding-v1` 至 `v4` 系列，支持指定 `dimensions`（仅 v3/v4）和 `encoding_format`。

- **文件与批量处理**：`files` 接口（[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）支持 `file-extract`（文档分析）、`batch`（批量推理输入）、`fine-tune`（调优数据集）三类用途；`batches` 接口（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）支持异步批量提交 JSONL 请求，费用为实时调用的 50%。

- **对话状态管理**：`conversations` 接口（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）提供会话生命周期管理（create/retrieve/update/delete）及消息项追加能力，配合 `responses` API 实现跨设备上下文延续。

> **注意**：文档 2 和文档 1 对 `base_url` 的路径描述存在不一致——文档 2 未明确 `responses` 接口路径，而文档 1 明确要求使用 `/compatible-mode/v1/responses`；同时文档 2 中“支持的模型列表”包含大量第三方模型（如 Kimi、GLM），但文档 1 和文档 6 均未列出这些模型在 `responses` 或 `batch` 场景下的可用性。实际开发应以具体接口文档为准，例如 `responses` 仅支持明确列出的 Qwen 系列及部分 DeepSeek 模型，Kimi/GLM 等未在 `responses` 文档中声明支持。

## 关键参数

| 参数 | 类型 | 说明 | 接口适用性 |
|------|------|------|------------|
| `base_url` | string | 必填。服务端点，地域专属域名推荐使用 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1` 格式（北京/新加坡/东京/法兰克福/弗吉尼亚）。旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐。 | 所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) |
| `model` | string | 必填。模型名称，不同接口支持范围不同：<br>- `chat/completions`: `qwen-plus`, `qwen3.8-max`, `qwen-vl-plus` 等<br>- `responses`: `qwen3.8-max`, `qwen3.7-plus`, `deepseek-v4-flash` 等（见文档 1）<br>- `completions`: 仅 `qwen-coder-turbo`<br>- `embeddings`: `text-embedding-v4`, `v3` 等 | 各接口独立约束 |
| `previous_response_id` | string | 仅 `responses` 接口支持。传入上一轮响应的顶层 `id`（UUID），用于自动关联上下文，有效期 7 天。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `purpose` | string | 仅 `files` 接口支持。取值 `file-extract`（文档分析）、`batch`（批量输入）、`fine-tune`（调优数据集）。 | [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) |
| `enable_thinking` | boolean | 仅 `batch` 场景下部分 Qwen3 系列模型支持（如 `qwen3.8-max`）。默认开启，显式设为 `false` 可关闭思考模式以降低成本。须作为 JSONL 请求体顶层字段传入。 | [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `dimensions` | integer | 仅 `embeddings` 接口支持（v3/v4）。指定输出向量维度（如 `1024`），默认值依模型而定。 | [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) |

## 使用方式

### 基础调用（Python + OpenAI SDK）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

# Chat Completions（标准对话）
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)

# Responses（带工具能力的增强对话）
response = client.responses.create(
    model="qwen3.8-max",
    input="今天北京天气如何？",
    tools=[{"type": "function", "function": {"name": "get_current_weather", "description": "..."}}]
)

# Embeddings（向量化）
response = client.embeddings.create(
    model="text-embedding-v4",
    input="hello world",
    dimensions=1024
)
```

### LangChain 集成

LangChain 提供两种集成方式：
- `langchain_openai.ChatOpenAI`：仅支持百炼 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持的模型（如 `qwen-plus`），需配置 `base_url` 和 `api_key`。
- `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全部文本模型（含非 OpenAI 兼容模型），使用原生 DashScope SDK，需安装 `dashscope` 包。

示例（Python）：
```python
# OpenAI 方式（受限于兼容模型列表）
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus"
)

# DashScope 原生方式（全模型支持）
from langchain_community.chat_models.tongyi import ChatTongyi
llm = ChatTongyi(
    model="qwen3.8-max",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
```

详细配置参见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### 批量与异步处理

- **文件批量（Batch File）**：先上传 JSONL 文件（`purpose="batch"`），再调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`。
- **单请求批量（Batch Chat）**：直接修改 `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数与 `chat/completions` 完全一致，服务端同步等待并返回结果。
- **Conversations 状态管理**：创建会话后，通过 `client.conversations.create()` 获取 `conversation_id`，后续请求可通过 `previous_response_id` 或会话 ID 关联上下文。

## 限制和注意事项

- **地域与模型绑定**：DeepSeek 模型（如 `deepseek-v4-flash`）仅支持华北2（北京）与新加坡地域；Qwen-Audio 不支持 OpenAI 兼容协议；QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)（见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **路径与域名迁移**：`responses` 和 `conversations` 接口的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 已标记为“即将停止维护”，必须迁移到 `/compatible-mode/v1/...`；业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为性能与稳定性最佳实践，强烈推荐。
- **文件配额**：`files` 接口总存储上限为 100 GB / 10000 个文件，无有效期限制，超限后新上传失败，需手动清理。
- **Batch 超时**：Batch Chat 默认超时 3600 秒（1 小时），需在客户端显式设置 `timeout` 参数（如 Python 的 `with_options(timeout=1800)`）；Batch File [异步任务](../concepts/asynchronous-task.md)最长等待时间为 24 小时（`completion_window="24h"`）。
- **参数作用域**：`enable_thinking` 在 Batch JSONL 请求中必须与 `model` 同级，不可置于 `extra_body` 内；`previous_response_id` 必须传入 `responses` 响应的顶层 `id`，而非 `output` 数组内消息的 `id`。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


