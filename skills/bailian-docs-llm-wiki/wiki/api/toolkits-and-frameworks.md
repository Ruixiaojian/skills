# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量推理、文件管理及会话状态持久化等核心场景。所有接口均通过统一的 `compatible-mode/v1` 路径提供，支持主流 SDK（OpenAI、LangChain、LangChain4j）和原生 HTTP 调用，开发者可快速迁移现有 OpenAI 应用。

## 支持的模型/功能

- **文本生成**：支持 `qwen3-*` 系列（如 `qwen3.7-plus`, `qwen3.7-max`, `qwen3.5-flash`）、`qwen-plus`, `qwen-flash`, `qwen-coder-turbo` 等全量千问模型；第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）仅限中国内地地域可用 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **多模态理解**：`qwen3-vl-plus`, `qwen3-vl-flash`, `QVQ`, `Qwen-OCR` 支持图像/视频输入与结构化输出 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v1` 至 `v4`，支持 64–2048 维可选、100+ 语种及编程语言，但多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长上下文与文档分析**：`qwen-long`, `qwen-doc-turbo` 依赖文件 ID 进行问答与数据提取，需配合 `purpose=file-extract` 的文件上传接口 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **专用接口**：`completions` 接口专用于代码补全，仅支持 `qwen-coder-turbo` 模型；`Responses API` 内置联网搜索、网页抓取等工具链，是 `Chat Completions` 的增强演进版本 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：文档 4（Batch）与文档 10（Batch Chat）存在关键差异——前者要求 JSONL 文件输入（`/files` + `/batches`），后者为单请求同步调用（直接 POST `/chat/completions` 到 `batch.dashscope.aliyuncs.com`）。二者不可混用，且 Batch Chat 不支持 `stream=true`。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 必填服务端点，按地域区分 | 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`；美国弗吉尼亚：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`；**Batch Chat 固定为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`** |
| `model` | string | 模型名称，严格匹配文档所列 | `qwen3.7-plus` 等带时间后缀的版本（如 `qwen3.7-plus-2026-05-26`）必须精确指定；`qwen-vl-plus` 不能用于纯文本 `chat.completions` |
| `enable_thinking` | boolean | 控制思考模式开关（影响 token 成本） | 仅 `qwen3.5/3.6/3.7` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 中**（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |
| `previous_response_id` | string | Responses API 多轮对话上下文锚点 | 必须传入上一轮响应的顶层 `id`（UUID 格式 `resp_xxx`），**非 `output` 数组内消息的 `msg_xxx`** |
| `dimensions` | integer | Embedding 向量维度 | 仅 `text-embedding-v3` 和 `v4` 支持，取值范围见文档 6 |

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换 WorkspaceId
)

# Chat Completions（标准对话）
response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}]
)

# Responses API（带内置工具）
response = client.responses.create(
    model="qwen3.7-plus",
    input="搜索最新AI论文",
    previous_response_id="resp_..."  # 可选，用于多轮
)

# Embedding
response = client.embeddings.create(
    model="text-embedding-v4",
    input="hello world",
    dimensions=1024
)
```

### LangChain 集成
- **OpenAI 兼容层**（`langchain_openai.ChatOpenAI`）：仅支持部分模型（如 `qwen-plus`），适用于快速迁移 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **DashScope 原生层**（`langchain_community.chat_models.tongyi.ChatTongyi`）：支持全部千问文本模型，推荐用于生产环境。

### 文件操作（Batch & Document QA）
```python
# 上传文件（用途：file-extract / batch / fine-tune）
file_obj = client.files.create(file=Path("doc.pdf"), purpose="file-extract")
file_id = file_obj.id

# 用于 Qwen-Long 文档问答（需在后续请求中引用 file_id）
# 用于 Batch 输入（见文档 4 示例）
# 用于微调（purpose="fine-tune"）
```

## 限制和注意事项

- **域名迁移强制要求**：旧版 `https://dashscope.aliyuncs.com` 已逐步停用，华北2（北京）和新加坡地域必须迁移至业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），否则可能触发限流或失败 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **模型能力边界**：
  - `Qwen-Audio` 不支持任何 OpenAI 兼容协议，仅 DashScope 原生接口可用；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；
  - `completions` 接口仅支持 `qwen-coder-turbo`，且不支持后缀生成前缀。
- **Token 限制**：`qwen3.7-max` 等大模型在 Batch 场景下单次请求上下文最大支持 256K tokens，但实时 `chat.completions` 有更低限制（需查具体模型文档）。
- **错误处理**：所有接口返回标准 OpenAI 错误格式（`{"error": {"code": "...", "message": "..."}}`），常见错误码详见各文档末尾的错误码链接。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)


