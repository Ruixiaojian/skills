# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，支持开发者快速迁移现有应用或构建新场景。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 三要素即可接入，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力覆盖文本、视觉、嵌入、[文件处理](../concepts/file-processing.md)、批量推理及对话状态管理等多个维度：

- **文本生成**：全系列 Qwen 模型（`qwen-plus`、`qwen-max`、`qwen-flash`、`qwen-long`、`qwen-coder-turbo` 等）、DeepSeek（硅基流动/快手万擎直供）、Kimi（月之暗面直供）、GLM、MiniMax 等 [三方直供模型](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **[多模态](../concepts/multi-modal.md)理解**：`qwen-vl-plus`、`qwen3-vl-plus`、`qwen-vl-ocr`、`qven-omni` 等，支持图像、视频、OCR 场景；  
- **向量嵌入**：`text-embedding-v1` 至 `v4`，支持多语种及可调维度（仅 v3/v4），但 [多模态 Embedding 模型不支持 OpenAI 兼容接口](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；  
- **[文件处理](../concepts/file-processing.md)**：`Qwen-Long`（长文档问答）、`Qwen-Doc-Turbo`（结构化数据提取）、Batch 推理及 Fine-tune 数据集上传，用途由 `purpose` 参数区分（`file-extract` / `batch` / `fine-tune`）；  
- **批量任务**：支持两种模式——[文件输入式 Batch](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)（异步、低成本、高吞吐）和 [同步式 Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)（单请求、保序、带超时控制）；  
- **会话管理**：`Conversations API` 提供会话生命周期操作（create/retrieve/update/delete），配合 `Responses API` 实现上下文自动注入与多轮记忆；  
- **专用接口**：`completions` 接口专用于代码补全等前缀/中缀生成场景，仅支持 `qwen-coder-turbo` [当前明确限定](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`completions` 接口在文档 2 中声明“仅适用于华北2（北京）地域”，但其他文档（如文档 1、3、7）均未限定地域，实际调用需以控制台可用模型为准。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源参考 |
|------|------|------|------|----------|
| `base_url` | string | 是 | 接口服务端点。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）仍可用但性能与稳定性较低 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) | [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 是 | 模型标识符。不同接口支持范围不同：`chat/completions` 支持最广；`completions` 仅支持 `qwen-coder-turbo`；`responses` 仅支持 `qwen3-*` 系列及 `qwen-plus` 等指定型号 | [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。`true` 时返回 `chat.completion.chunk` 类型响应；`false`（默认）返回完整 `chat.completion` | — |
| `stream_options` | object | 否 | [流式输出](../concepts/streaming-output.md)增强参数，设 `{"include_usage": true}` 可在末尾 chunk 返回 token 统计 | — |
| `enable_thinking` | boolean | 否 | 仅 Batch 场景下生效，控制是否启用思考模式（影响 token 成本）。必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内 | [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `previous_response_id` | string | 否 | `responses` 接口专用，用于关联上一轮响应 ID（格式为 `resp_xxx`），实现免手动维护消息历史的多轮对话 | [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |

## 使用方式

### 1. SDK 配置（通用）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)
```

### 2. 接口调用示例
- **Chat Completions**（标准对话）：
  ```python
  client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
  ```
- **Responses**（智能体原生、支持内置工具）：
  ```python
  client.responses.create(model="qwen3.7-plus", input="查一下今天北京天气", previous_response_id="resp_xxx")
  ```
- **Embeddings**（向量化）：
  ```python
  client.embeddings.create(model="text-embedding-v4", input="hello", dimensions=1024)
  ```
- **Files**（文件上传）：
  ```python
  client.files.create(file=Path("doc.pdf"), purpose="file-extract")  # 用于 Qwen-Doc-Turbo
  client.files.create(file=Path("batch.jsonl"), purpose="batch")     # 用于 Batch 推理
  ```
- **Conversations**（会话管理）：
  ```python
  conv = client.conversations.create(items=[{"role":"system","content":"你是助手"}])
  client.conversations.items.create(conv.id, items=[{"role":"user","content":"hi"}])
  ```

### 3. LangChain 集成
- **OpenAI 兼容方式**（支持部分模型）：使用 `langchain_openai.ChatOpenAI`，`base_url` 指向百炼兼容地址；  
- **DashScope 原生方式**（支持全部模型）：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，需额外安装 `dashscope` 包 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与域名**：北京、新加坡地域已全面推广业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名虽兼容但不推荐；弗吉尼亚、东京、法兰克福等地域仅提供全局域名（如 `dashscope-us.aliyuncs.com`），无 WorkspaceId 占位符；  
- **模型可用性**：三方直供模型（如 DeepSeek、Kimi）仅在中国内地站可用，且需在控制台单独开通服务；  
- **文件限制**：`file-extract` 单文件 ≤150 MB；`batch` 单文件 ≤500 MB；`fine-tune` 单文件 ≤300 MB；总存储上限为 100 GB / 10000 文件；  
- **Batch 超时**：同步 Batch Chat 默认等待 3600 秒（1 小时），最长不可超过此值；异步 Batch 最长等待窗口为 `24h`；  
- **Responses API 迁移**：旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已废弃，必须迁移到 `/compatible-mode/v1/responses`；  
- **Conversations API 迁移**：旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 即将停用，需切换至新版路径；  
- **安全实践**：API Key 务必通过环境变量注入，禁止硬编码；生产环境应启用 `stream_options={"include_usage": true}` 监控 token 消耗。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)


