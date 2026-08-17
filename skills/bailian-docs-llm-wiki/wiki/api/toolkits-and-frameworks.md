# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与专用工具链，支持开发者快速集成大模型能力。核心包括标准 Chat/Completions 接口、面向特定场景的 Responses 和 Conversations API、批量处理（Batch）与文件管理能力，以及 Embedding 和[多模态](../concepts/multi-modal.md)（Vision）等专项接口。所有接口均通过统一的 `compatible-mode/v1` 路径暴露，仅需调整 `base_url`、`api_key` 和 `model` 即可迁移现有 OpenAI 应用。

## 支持的模型/功能

- **文本生成**：覆盖全系列 Qwen 模型（如 `qwen3.8-max`、`qwen-plus`、`qwen-flash`）、DeepSeek-V4、GLM-5.2 等，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **代码补全**：专有 `completions` 接口支持前缀/前后缀补全，当前仅支持 `qwen-coder-turbo`，详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)；
- **视觉理解**：Qwen-VL、QVQ、Qwen-OCR 等模型通过 OpenAI Vision 兼容接口调用，支持图文混合输入，详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **智能体原生能力**：Responses API 内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3-max`、`qwen3-plus` 等系列模型；
- **长上下文与文档分析**：Qwen-Long、Qwen-Doc-Turbo 依赖文件上传接口（`purpose=file-extract`），支持 PDF、DOCX、图片等多种格式；
- **向量化**：`text-embedding-v1` 至 `v4` 系列模型支持 OpenAI Embedding 接口，但[多模态](../concepts/multi-modal.md) Embedding（如 `qwen3-vl-embedding`）**不支持**该协议；
- **批量处理**：Batch Chat（单请求同步等待）与 Batch File（JSONL 文件异步提交）两种模式，分别适用于低并发高延迟容忍与海量任务场景。

> **注意**：文档 5（Batch File）与文档 9（Batch Chat）对同一模型（如 `qwen3.7-plus`）的上下文长度限制描述一致（256K），但文档 9 明确要求 `enable_thinking` 参数须与 `model` 同级传入，而文档 5 未强调此约束，实际使用中应以文档 9 的说明为准。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 服务端点，**必须按地域和用途选择正确域名**：<br>- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`<br>- Batch Chat 专用：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台获取；旧域名（如 `dashscope.aliyuncs.com`）仍可用但**不推荐**，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 模型名称，严格区分大小写与版本后缀（如 `qwen3.7-plus-2026-05-26`） | 不同接口支持模型不同，例如 `completions` 仅支持 `qwen-coder-turbo`，而 `responses` 支持数十种 `qwen3.*` 变体 |
| `stream` / `stream_options` | boolean / object | 控制[流式输出](../concepts/streaming-output.md)行为；`stream_options={"include_usage": true}` 可在末尾返回 token 统计 | 所有 Chat/Completions/Responses 接口均支持，但 QVQ 模型**仅支持流式**（见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)） |
| `enable_thinking` | boolean | 控制是否启用思考模式（产生 reasoning tokens），影响成本与延迟 | 仅 Batch 场景下生效，且**必须作为 JSONL `body` 的顶层字段**，不可置于 `extra_body` 中（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |
| `previous_response_id` | string | Responses API 多轮对话的关键参数，用于自动注入上下文 | 必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)） |

## 使用方式

### 1. 基础调用（Chat/Completions）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# Chat Completions
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
# Completions（代码补全专用）
response = client.completions.create(
    model="qwen-coder-turbo",
    prompt="<tool_call>def quick_sort(arr):</tool_call>"
)
```

### 2. 批量处理
- **Batch Chat（单请求同步）**：替换 `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数与实时 Chat 完全一致；
- **Batch File（JSONL 异步）**：先调用 `client.files.create(file=..., purpose="batch")` 上传文件，再调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")` 提交任务。

### 3. 文件与会话管理
- **文件上传**：`purpose` 决定用途——`file-extract`（文档问答）、`batch`（批量输入）、`fine-tune`（调优数据集）；
- **会话持久化**：通过 Conversations API 创建 `conversation_id`，后续请求可复用该 ID 实现跨设备上下文延续。

### 4. LangChain 集成
- **OpenAI 兼容层**（`langchain_openai.ChatOpenAI`）：仅支持部分模型，配置 `base_url` 和 `model` 即可；
- **DashScope 原生层**（`langchain_community.chat_models.tongyi.ChatTongyi`）：支持全部百炼文本模型，需安装 `dashscope` 包。

## 限制和注意事项

- **地域与模型绑定**：DeepSeek-V4 模型**仅支持华北2（北京）与新加坡地域**；Qwen-Audio **不支持 OpenAI 兼容协议**，仅限 DashScope 协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **[Token](../concepts/token.md) 限制**：Batch 场景下 `qwen3.8-max` 等模型最大上下文为 256K tokens，但 `qwen3.5-omni-plus` **不支持语音输出**；
- **文件配额**：百炼存储空间上限为 **10,000 个文件** 或 **100 GB 总大小**，超限时新上传将失败；
- **URL 迁移强制性**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 两个旧路径**即将停止维护**，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）；
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，**禁止硬编码到源码或客户端**（所有文档均明确提示此风险）。

## 来源文档

- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


