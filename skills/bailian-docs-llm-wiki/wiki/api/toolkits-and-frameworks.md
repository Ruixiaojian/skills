# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的 API 接口（toolkits），覆盖文本生成、视觉理解、嵌入向量、批量推理、文件管理及会话状态管理等场景，支持主流 SDK（如 OpenAI Python/Node.js SDK、LangChain）无缝集成。所有接口均基于统一的 `compatible-mode/v1` 路径设计，通过调整 `base_url`、`api_key` 和 `model` 即可迁移现有 OpenAI 应用。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为以下几类：

- **通用对话（Chat）**：兼容 `chat/completions`，支持 Qwen 系列大语言模型（如 `qwen3.7-plus`、`qwen-plus`）、Qwen-VL、Qwen-Coder、Qwen-Omni 及部分第三方模型（DeepSeek、Kimi、GLM 等）。详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **智能体原生响应（Responses）**：作为 Chat Completions 的演进，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 简化上下文管理，适用于复杂任务编排。[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 明确列出华北2（北京）、新加坡、美国（弗吉尼亚）等多地支持的 `qwen3.*` 模型列表。
- **文本补全（Completions）**：专为代码补全、内容续写设计，当前仅支持 `qwen-coder-turbo`（中国内地北京地域），支持前缀生成与“前缀+后缀”中间生成两种模式。
- **视觉理解（Vision）**：兼容 `chat/completions` 多模态调用，支持 `qwen3-vl-plus`、`qwen-vl-ocr` 等模型，接受 `image_url` 或 Base64 图像输入。
- **嵌入向量（Embedding）**：支持 `text-embedding-v1` 至 `v4` 系列，提供不同维度与语种覆盖，但多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议，需使用专用接口。
- **文件管理（Files）**：用于上传文档供 Qwen-Long/Qwen-Doc-Turbo 进行问答或作为 Batch 输入，`purpose` 可设为 `file-extract`、`batch` 或 `fine-tune`。
- **批量推理（Batch）**：含两种形态——**文件输入式 Batch**（异步，支持 JSONL 多请求）和 **同步式 Batch Chat**（单请求阻塞等待），均享 50% 成本优惠。[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 与 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 分别详述其适用模型与工作流。
- **会话管理（Conversations）**：配合 Responses API 实现跨设备上下文延续，支持创建、查询、更新、删除会话及追加消息项。

> **注意**：文档 4（OpenAI Chat接口兼容）称支持 Qwen-Audio，但明确标注“Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议”；而文档 3（OpenAI Vision接口兼容）未提及 Qwen-Audio，二者一致。此处以文档 4 的明确声明为准。

## 关键参数

| 参数 | 类型 | 说明 | 来源示例 |
|------|------|------|----------|
| `base_url` | string | 必填，服务端点。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）仍可用但即将停用。 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)、[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `model` | string | 必填，模型名称。不同接口支持范围不同：`completions` 仅限 `qwen-coder-turbo`；`embeddings` 仅限 `text-embedding-*`；`responses` 支持 `qwen3.*` 全系列。 | 文档 1、2、8 |
| `input` / `messages` / `prompt` | string / array / string | 根据接口类型选择：`responses` 接受字符串或消息数组；`chat/completions` 使用 `messages`；`completions` 使用 `prompt`；`embeddings` 使用 `input`。 | 文档 1、4、2、8 |
| `stream` | boolean | 控制输出方式。`true` 启用流式，`false`（默认）为完整响应。`stream_options={"include_usage": true}` 可在流末尾返回 token 统计。 | 文档 1、4、8 |
| `enable_thinking` | boolean | 仅 Batch 场景下有效（文档 6、7），控制是否启用思考模式（产生额外 reasoning tokens）。`qwen3.5/3.6/3.7` 系列默认开启，建议显式设置。 | [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

# Chat 示例
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)

# Responses 示例（带工具）
response = client.responses.create(
    model="qwen3.7-plus",
    input="查一下今天北京的天气",
    tools=[{"type": "function", "function": {"name": "get_current_weather", ...}}]
)

# Embedding 示例
embedding = client.embeddings.create(
    model="text-embedding-v4",
    input="hello world",
    dimensions=1024
)
```

### LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：仅支持文档 4 所列部分模型，配置简单：
  ```python
  from langchain_openai import ChatOpenAI
  llm = ChatOpenAI(
      model="qwen-plus",
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      api_key=os.getenv("DASHSCOPE_API_KEY")
  )
  ```
- **DashScope 原生层**（`langchain-community`）：支持全部百炼文本模型，需安装 `dashscope`：
  ```python
  from langchain_community.chat_models.tongyi import ChatTongyi
  llm = ChatTongyi(
      model="qwen-plus",
      dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
  )
  ```

### HTTP 直连（curl）
```bash
# Chat
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"hi"}]}'

# File upload
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --form 'file=@"doc.pdf"' \
  --form 'purpose="file-extract"'
```

## 限制和注意事项

- **地域与模型绑定**：并非所有模型在所有地域均可用。例如 `qwen3.5-ocr` 仅在华北2（北京）支持；`qwen3.7-max` 在德国法兰克福仅支持部分 `qwen3.5-*` 子型号。务必查阅各文档的“支持的模型”表格确认地域可用性。
- **路径与域名迁移**：`/api/v2/apps/protocols/...` 等旧路径（如文档 1、9 中提及）已废弃，必须迁移到 `/compatible-mode/v1/` 新路径；同时建议从 `dashscope.aliyuncs.com` 迁移至业务空间专属域名以获得更高稳定性。
- **Batch 特殊约束**：
  - 文件输入式 Batch 要求 JSONL 格式，每行一个请求，`url` 字段需与 `endpoint` 参数一致；
  - 同步 Batch Chat（文档 7）的超时时间上限为 3600 秒，需在客户端显式配置（如 Python 的 `with_options(timeout=1800)`）；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出。
- **文件服务配额**：百炼文件存储上限为 10,000 个文件且总大小 ≤100 GB；单个 `file-extract` 文件 ≤150 MB，`batch` 文件 ≤500 MB，`fine-tune` 文件 ≤300 MB。
- **Embedding 维度控制**：仅 `text-embedding-v3` 和 `v4` 支持 `dimensions` 参数；`v1`/`v2` 固定维度不可调。
- **Qwen-Audio 不兼容**：明确不支持 OpenAI 协议，必须使用 DashScope 原生 API。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


