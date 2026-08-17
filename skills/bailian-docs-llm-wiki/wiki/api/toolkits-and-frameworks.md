# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量处理、对话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移，大幅降低集成成本。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/curl）及 LangChain 等主流框架。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按能力分层：

- **基础文本生成**：`chat/completions` 接口支持 Qwen 系列（`qwen-plus`、`qwen-flash`、`qwen3.*-max/plus/flash`）、DeepSeek-V4、Kimi、GLM、MiniMax 等数十种模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **增强智能体能力**：`/responses` 接口原生支持联网搜索、网页抓取、代码解释器等内置工具，且简化上下文管理，通过 `previous_response_id` 自动关联多轮对话 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **长文档与[文件处理](../concepts/file-processing.md)**：`/files` 接口支持 `purpose=file-extract`（用于 Qwen-Long/Qwen-Doc-Turbo）、`purpose=batch`（批量推理输入）、`purpose=fine-tune`（调优数据集上传）三类用途 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；  
- **多模态理解**：`chat/completions` 兼容 Vision 接口，支持 `qwen-vl-plus`、`qven3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，接受 `image_url` 或 Base64 图片输入；  
- **向量嵌入**：`/embeddings` 接口支持 `text-embedding-v1` 至 `v4` 全系列模型，最高 8,192 token 单行输入，支持多语种及可选维度（`v3/v4` 支持 `dimensions` 参数）；  
- **批量处理**：提供两种模式——`Batch File API`（异步，JSONL 文件输入，50% 成本优势）和 `Batch Chat API`（同步阻塞式，单请求低延迟）；  
- **对话状态管理**：`/conversations` 接口支持创建、检索、更新、删除会话，并通过 `/items` 子路径追加消息，实现跨设备上下文持久化；  
- **代码补全专用**：`/completions` 接口专为 `qwen-coder-turbo` 设计，支持前缀+后缀双向补全（如函数签名→实现），不支持纯后缀补全。

> **注意**：`qwen-audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；多模态 Embedding 模型（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用专用多模态向量 API。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 服务端点地址 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐；`/responses` 和 `/conversations` 接口必须使用新版路径 `/compatible-mode/v1/xxx`，旧路径 `/api/v2/...` 即将停用 |
| `model` | string | 模型标识符 | 不同接口支持模型不同：`/completions` 仅支持 `qwen-coder-turbo`；`/responses` 仅支持 `qwen3.*` 及 `deepseek-v4-*` 等指定型号；`/embeddings` 仅限 `text-embedding-*` 系列 |
| `stream` / `stream_options` | boolean / object | [流式输出](../concepts/streaming-output.md)控制 | `stream_options={"include_usage": true}` 可在流式最后一块返回 token 统计；`/responses` 接口默认不返回 `output_text` 字段，需显式访问 `response.output_text` |
| `previous_response_id` | string | 上一轮响应 ID | 仅 `/responses` 接口有效，值为顶层 `id`（UUID 格式），**非** `output` 数组内消息的 `id`；有效期 7 天 |
| `enable_thinking` | boolean | 思考模式开关 | 仅 Batch 场景下对 `qwen3.*` 系列生效，默认开启，建议显式设置以避免意外 token 开销；必须作为 JSONL 请求体顶层字段，不可置于 `extra_body` 内 |
| `dimensions` | integer | 向量维度 | 仅 `text-embedding-v3/v4` 支持，取值范围见文档；`v1/v2` 不支持该参数 |

## 使用方式

### 通用初始化（Python 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)
```

### 各接口典型调用
- **Chat Completions**（标准对话）：`client.chat.completions.create(model="qwen-plus", messages=[...])`  
- **Responses API**（智能体增强）：`client.responses.create(model="qwen3.8-max", input="你好")`；多轮传 `previous_response_id=response1.id`  
- **Files API**（文件上传）：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`  
- **Batch File**（异步批量）：先 `client.files.create(..., purpose="batch")`，再 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`  
- **Batch Chat**（同步批量）：`client.chat.completions.create(...)`，但 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`  
- **Embeddings**：`client.embeddings.create(model="text-embedding-v4", input="文本", dimensions=1024)`  
- **Conversations**：`client.conversations.create(items=[{"role":"system","content":"..."}])`，后续通过 `conversation.id` 追加消息  

### LangChain 集成
- **OpenAI 兼容层**（部分模型）：`langchain_openai.ChatOpenAI`，需配置 `base_url` 和 `model`；  
- **DashScope 原生层**（全模型支持）：`langchain_community.chat_models.tongyi.ChatTongyi`，需安装 `dashscope` 包；  
两者均支持流式、工具调用等高级特性，详见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与模型绑定**：`deepseek-v4-*` 仅支持华北2（北京）与新加坡；`qwen3.*` 系列在弗吉尼亚/法兰克福等地域不可用；`qwen-vl-*` 在日本（东京）地域暂未列出支持；  
- **文件配额**：`/files` 接口总存储上限为 10,000 个文件或 100 GB，无自动过期机制，需手动清理；`file-extract` 单文件 ≤150 MB，`batch`/`fine-tune` 单文件 ≤500 MB/300 MB；  
- **Batch 超时**：`Batch Chat` 默认等待 3600 秒（1 小时），超时断连；`Batch File` 最长处理窗口为 24 小时；  
- **[Token](../concepts/token.md) 计费差异**：`/responses` 接口返回 `usage.output_tokens_details.reasoning_tokens`，思考 token 单独计费；`/chat/completions` 无此细分；  
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；SDK 调用时优先使用 `with_options(timeout=...)` 设置合理超时，避免无限等待；  
- **错误处理**：所有接口均遵循 OpenAI 错误格式（`{"error": {"message": "...", "code": "..."}}`），需统一捕获解析，参考 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


