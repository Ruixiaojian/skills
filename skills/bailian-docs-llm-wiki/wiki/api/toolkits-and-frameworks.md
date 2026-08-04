# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，支持开发者无缝迁移现有应用。核心能力覆盖文本生成、多模态理解、向量嵌入、批量推理、[文件处理](../concepts/file-processing.md)及对话状态管理等场景，所有接口均基于标准 OpenAI REST API 协议设计，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速接入。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **Chat Completions**：兼容标准 `/chat/completions` 端点，支持 Qwen 系列（`qwen-plus`、`qwen3.7-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax），但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses API**：作为 Chat Completions 的演进版本，专为智能体（Agent）场景优化，内置联网搜索、网页抓取、代码解释器等工具，并支持通过 `previous_response_id` 自动关联上下文，显著简化多轮对话实现。支持模型包括 `qwen3-max`、`qwen3-plus`、`qwen3-flash` 及 `qwen3-coder-*` 全系列（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **Vision（多模态）**：兼容 `/chat/completions` 的图像理解请求格式，支持 `qwen3-vl-plus`、`qven-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，要求输入 `messages` 中包含 `image_url` 类型内容。
- **Embedding**：兼容 `/embeddings` 端点，支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，其中 `v3` 和 `v4` 支持 `dimensions` 参数指定向量维度；**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，需使用原生多模态向量 API。
- **Completions（文本补全）**：专用于代码/文本续写，当前仅支持 `qwen-coder-turbo`，采用 `prompt` 字符串而非 `messages` 数组，且仅限华北2（北京）地域。
- **Files & Batch**：`/files` 接口支持 `purpose=file-extract`（文档分析）、`purpose=batch`（批量任务输入）、`purpose=fine-tune`（调优数据集）；`/batches` 接口支持两种模式：文件式批量（异步）和同步式 Batch Chat（单请求阻塞等待），后者适用于数据标注等无需实时响应的场景。
- **Conversations**：提供会话生命周期管理（创建、查询、更新、删除、追加消息），配合 Responses API 实现跨设备上下文持久化，避免手动维护消息历史。

> **注意**：文档 1 和文档 2 均强调业务空间专属域名迁移（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），但文档 6 的 Batch 接口示例仍使用旧域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，而文档 7 的 Batch Chat 明确要求 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"` —— 这表明 Batch Chat 是独立服务端点，**不适用业务空间域名**，与文档 1/2/4/8 的通用兼容接口存在架构差异。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源参考 |
|------|------|------|------|----------|
| `base_url` | string | 是 | 接口服务地址。Chat/Vision/Embedding/Responses/Conversations 使用业务空间域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；Batch Chat 固定为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；Completions 和 Files 当前仍用 `https://dashscope.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 需从控制台获取。 | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 是 | 模型名称。不同接口支持范围不同：Chat 支持 Qwen 全系及第三方模型；Responses 仅支持 `qwen3-*` 系列；Completions 仅 `qwen-coder-turbo`；Embedding 仅 `text-embedding-*`；Vision 仅 `qwen3-vl-plus` 等视觉模型。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)。默认 `false`；设为 `true` 时需配合 `stream_options={"include_usage": true}` 获取最终 token 统计。 | [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| `enable_thinking` | boolean | 否 | Batch 场景下控制思考模式开关（影响 token 成本）。`qwen3.5/3.6/3.7` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内**。 | [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `previous_response_id` | string | 否 | Responses API 多轮对话关键参数，值为上一轮响应的顶层 `id`（UUID 格式），非 `output` 内 `msg_*` ID。有效期 7 天。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |

## 使用方式

### 基础 SDK 调用（Python 示例）
```python
from openai import OpenAI
import os

# 通用配置（Chat/Vision/Embedding/Responses/Conversations）
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

# Chat Completions
resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])

# Responses API（推荐用于 Agent）
resp = client.responses.create(model="qwen3.7-plus", input="你能做什么？")

# Embedding
resp = client.embeddings.create(model="text-embedding-v4", input="测试文本", dimensions=1024)

# Conversations（创建会话）
conv = client.conversations.create(items=[{"role":"system","content":"你是助手"}])
```

### Batch Chat（同步阻塞式）
```python
# 注意：base_url 与 Chat 不同，且需设置 timeout
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"
).with_options(timeout=1800.0)  # 最长 3600 秒

resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
```

### LangChain 集成
- **`langchain_openai`**：仅支持部分 OpenAI 兼容模型（如 `qwen-plus`），依赖 `base_url` 和 `model` 配置。
- **`langchain_community.chat_models.tongyi`**（Python）或 **`@langchain/community/chat_models/alibaba_tongyi`**（JS）：支持百炼全部文本模型，无需 OpenAI 兼容层，直接对接原生 DashScope SDK。  
详情参见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与域名约束**：业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）目前仅支持华北2（北京）、新加坡、日本（东京）、德国（法兰克福）及美国（弗吉尼亚）地域，且需在控制台开通对应业务空间；旧域名 `dashscope.aliyuncs.com` 仍可用但性能与稳定性较低。
- **模型可用性差异**：同一模型在不同接口中支持情况不同。例如 `qwen3-vl-plus` 在 Vision 接口可用，但在 Chat Completions 接口可能因地域未开通而返回 404；`qwen-long` 仅支持通过文件 ID 进行问答，不支持直接 `messages` 调用。
- **文件服务配额**：`/files` 接口总存储上限为 100 GB 或 10,000 个文件，任一达到即拒绝新上传；单文件大小限制依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB。
- **Batch [异步任务](../concepts/asynchronous-task.md)限制**：Batch 文件输入任务最长等待时间为 24 小时（`completion_window="24h"`），超时后状态变为 `expired`；测试模型 `batch-test-model` 有严格限制（文件 ≤ 1 MB、行数 ≤ 100、并发 ≤ 2）。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，**禁止硬编码于源码中**；各 SDK 示例均明确警示此风险。

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


