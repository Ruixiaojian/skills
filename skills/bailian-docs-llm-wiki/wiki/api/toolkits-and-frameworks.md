# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、文件处理、批量推理及会话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **Chat Completions**：支持 Qwen 系列（`qwen-plus`、`qwen-max`、`qwen-flash` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek（阿里云直供及三方直供）、Kimi、GLM、MiniMax 等数十种模型；但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Vision（图像理解）**：支持 `qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr`、`QVQ`（仅[流式输出](../concepts/streaming-output.md)）等视觉模型，输入支持 `image_url` 或 Base64 编码 [详见文档](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，支持多语种及编程语言；但[多模态](../concepts/multi-modal.md) Embedding 模型（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [参见说明](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Completions（文本补全）**：当前仅支持 `qwen-coder-turbo`，适用于代码补全、函数体生成等场景，支持前缀+后缀双边界补全 [详见文档](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **Files（文件上传）**：支持 `purpose=file-extract`（用于 Qwen-Long/Qwen-Doc-Turbo）、`purpose=batch`（用于批量推理）、`purpose=fine-tune`（用于调优任务）三类用途，单文件上限分别为 150 MB / 500 MB / 300 MB [参见文档](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Batch（批量处理）**：提供两种模式：  
  - 文件批量（`/files` + `/batches`）：异步执行，支持 JSONL 格式多请求，成本为实时调用的 50%；  
  - Batch Chat（同步阻塞）：单请求同步等待，端点为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`，非文件方式 [对比参见](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **Conversations & Responses**：`Conversations API` 提供会话生命周期管理（创建/查询/更新/删除），配合 `Responses API` 实现上下文自动注入与智能体原生工具调用（联网搜索、代码解释器等），`previous_response_id` 可关联多轮对话 [详见文档](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：文档 5（`batch-interfaces-compatible-with-openai.md`）与文档 10（`openai-compatible-batch-chat.md`）对 Batch 的定义存在本质差异——前者是异步文件批量（`/batches`），后者是同步单请求批量（`/chat/completions`）。二者不可混用，且 `enable_thinking` 参数在 JSONL 文件中必须置于 `body` 顶层，而非 `extra_body` 内 [原文明确强调](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 备注 |
|------|------|------|------|------|
| `base_url` | string | 是 | 接口服务地址 | 华北2（北京）和新加坡地域**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已不推荐 [参见迁移说明](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `api_key` | string | 是 | 百炼 API Key | 各地域 Key **不通用**，需按地域分别获取并配置环境变量 `DASHSCOPE_API_KEY` |
| `model` | string | 是 | 模型名称 | 需严格匹配支持列表，如 `qwen3.8-max`、`qwen-vl-plus`、`text-embedding-v4`；`qwen-coder-turbo` 仅用于 `completions` 接口 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md) | 默认 `false`；`QVQ` 模型强制流式 [见原文](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `stream_options` | object | 否 | 流式控制 | 仅当 `stream=true` 时有效，设 `{"include_usage": true}` 可在末尾 chunk 返回 token 统计 |
| `max_tokens` | integer | 否 | 最大输出 token 数 | 超出时截断，**不影响模型内部生成过程** [原文明确说明](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| `temperature` / `top_p` | float | 否 | 采样控制 | 二者功能重叠，**建议只设置其一**，避免冲突 |
| `enable_thinking` | boolean | 否 | 思考模式开关 | 仅对 `qwen3.x` 系列模型有效，默认开启；若需关闭，必须在 JSONL 的 `body` 顶层传入，**不可放在 `extra_body` 中** [原文强调](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |

## 使用方式

### 基础调用（Python + OpenAI SDK）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议通过环境变量配置
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

# Chat 示例
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)

# Embedding 示例
embedding = client.embeddings.create(
    model="text-embedding-v4",
    input="hello world"
)

# File 上传示例
file_obj = client.files.create(file=Path("doc.pdf"), purpose="file-extract")
```

### LangChain 集成

- **OpenAI 兼容方式**（`langchain_openai`）：仅支持部分模型（如 `qwen-plus`），依赖 `base_url` 和 `model` 配置 [参见文档](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **DashScope 原生方式**（`langchain-community`）：支持全部百炼模型，需安装 `dashscope` 包，使用 `ChatTongyi` 类 [原文对比说明](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### 多语言支持

除 Python 外，Node.js、Java、Go、C#、curl 均有完整示例，关键在于：
- 正确设置 `base_url` 和 `Authorization: Bearer $DASHSCOPE_API_KEY`；
- HTTP 请求体格式严格遵循 OpenAI 规范（如 `messages` 数组、`input` 字符串等）；
- Batch 场景下注意区分 `/batches`（异步文件）与 `/chat/completions`（同步单请求）端点。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国内地地域可用**，调用前须在控制台开通对应服务 [原文注明](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **域名迁移强制性**：华北2（北京）和新加坡地域的旧域名（`dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com`）虽仍可用，但官方**强烈建议迁移至业务空间专属域名**，以获得更高性能与稳定性 [多篇文档重复强调](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件配额**：`files` 接口总存储上限为 **10,000 个文件**或 **100 GB**，任一达到即拒绝新上传；无自动过期机制，需手动清理 [原文说明](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Qwen-Audio 不兼容**：该模型完全不支持 OpenAI 协议，必须使用 DashScope 原生 SDK [明确排除](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Response ID 有效期**：`Responses API` 中 `previous_response_id` 的有效期为 **7 天**，超时需重建上下文 [原文标注](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **错误处理**：所有接口均返回标准 OpenAI 错误结构（含 `error.code` 和 `error.message`），具体错误码请查阅 [统一错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)


