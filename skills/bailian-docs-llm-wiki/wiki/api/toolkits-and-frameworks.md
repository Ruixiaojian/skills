# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、[向量嵌入](../concepts/vector-embedding.md)、批量推理、文件管理及会话状态管理等场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#）及 HTTP 直调。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **Chat Completions**：标准对话接口，支持 `qwen-plus`、`qwen-flash`、`deepseek-v3.2`、`kimi`、`glm` 等数十种模型（含 Qwen-VL、Qwen-Coder、Qwen-Omni 等多模态与专用模型），但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **Responses API**：增强型智能体原生接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-plus`、`qwen3.5-flash`、`qwen3-coder-next` 等新一代模型，显著简化上下文管理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；
- **Vision（图像理解）**：兼容 OpenAI Vision 规范，支持 `qwen3-vl-plus`、`qvq`、`qwen-vl-ocr`，支持 `image_url` 与 Base64 输入；
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，其中 `v3`/`v4` 支持 `dimensions` 参数指定向量维度；多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；
- **Completions**：专用于代码补全等前缀/中缀生成场景，当前仅支持 `qwen-coder-turbo` 模型；
- **Files**：文件上传与管理接口，`purpose=file-extract` 用于文档问答（Qwen-Long/Qwen-Doc-Turbo），`purpose=batch` 用于批量推理输入，`purpose=fine-tune` 用于调优数据集；
- **Batch Chat**：同步式批量推理接口，适用于非实时场景，成本为实时调用的 50%，支持 `qwen3.7-max` 等长上下文模型（单次请求最大 256K tokens）；
- **Conversations**：会话状态管理接口，支持跨设备/长时间中断的上下文持久化，配合 Responses API 实现自动历史注入；
- **LangChain 集成**：提供 `langchain_openai`（限部分模型）与 `langchain-community`（支持全部百炼模型）双路径适配，后者通过 `ChatTongyi` / `ChatAlibabaTongyi` 组件实现更完整能力覆盖 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

> **注意**：文档 1 与文档 2 均声明“华北2（北京）、新加坡地域建议迁移至业务空间专属域名”，但文档 1 的 `completions` 接口示例仍使用旧域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，而文档 2、4、8、10 已统一采用新域名格式。实际生产环境应优先使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等新域名，旧域名虽暂可运行，但存在性能与稳定性风险。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 备注 |
|------|------|------|------|------|
| `base_url` | string | 是 | 接口服务地址 | 地域专属域名格式：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Batch Chat 固定为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；Embedding/Vision/Conversations 等接口需匹配对应地域域名 |
| `model` | string | 是 | 模型名称 | 不同接口支持模型不同，例如 `completions` 仅支持 `qwen-coder-turbo`，`Responses API` 不支持 `qwen-coder-turbo`；`qwen3-vl-plus` 在 Vision 接口可用，在 Chat Completions 接口亦可用，但需确认控制台开通状态 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md) | 默认 `false`；Vision 接口的 `qvq` 模型**仅支持[流式输出](../concepts/streaming-output.md)** |
| `stream_options` | object | 否 | 流式配置 | 设置 `{"include_usage": true}` 可在最后一 chunk 返回 token 使用统计 |
| `previous_response_id` | string | 否（Responses API） | 上一轮响应 ID | 用于多轮对话上下文关联，必须传入顶层 `id`（如 `resp_xxx`），而非 `output` 中消息的 `id`（如 `msg_xxx`） |
| `enable_thinking` | boolean | 否（Batch 场景） | 是否启用思考模式 | `qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型默认开启，显式设为 `false` 可避免额外思考 token 成本；该参数须与 `model` 同级，不可置于 `extra_body` 内 |
| `dimensions` | integer | 否（Embedding） | 向量维度 | 仅 `text-embedding-v3` 和 `v4` 支持，取值范围见文档 8 |

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置为环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

# Chat Completions
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)

# Responses API（推荐用于智能体）
response = client.responses.create(
    model="qwen3.7-plus",
    input="你能做些什么？"
)

# Embedding
response = client.embeddings.create(
    model="text-embedding-v4",
    input="测试文本",
    dimensions=1024
)
```

### LangChain 集成
- **轻量级兼容**：使用 `langchain_openai.ChatOpenAI`，仅支持 OpenAI 兼容模型子集；
- **全模型支持**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`（Python）或 `@langchain/community/chat_models/alibaba_tongyi.ChatAlibabaTongyi`（JS），支持所有百炼文本模型及部署模型。

### 文件与批量任务
- **文件上传**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`；
- **Batch Chat（单请求）**：切换 `base_url` 至 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；
- **Batch File（多请求）**：准备 JSONL 文件，调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`。

## 限制和注意事项

- **地域与域名绑定**：API Key 与 `base_url` 地域严格匹配（如北京地域 Key 必须配北京域名），跨地域调用将失败；
- **WorkspaceId 要求**：北京、新加坡、东京、法兰克福地域的 `base_url` 必须包含真实 `WorkspaceId`，该 ID 在百炼控制台“业务空间详情”中获取；弗吉尼亚地域无需 `WorkspaceId`；
- **模型可用性差异**：同一模型在不同接口或地域可能不可用（如 `qwen-vl-plus` 在 Vision 接口可用，在 `completions` 接口不可用；新加坡地域不支持 `deepseek-r1`）；
- **功能限制**：
  - `Qwen-Audio` 不支持 OpenAI 兼容协议，仅 DashScope 协议可用；
  - `completions` 接口暂不支持“后缀生成前缀”；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；
  - `conversations` 接口的 `items` 初始消息最多 20 条；
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；SDK 调用时优先使用 `os.getenv()` 或 `process.env` 读取；
- **错误处理**：所有接口返回标准 OpenAI 格式错误（如 `{"error": {"message": "...", "code": "invalid_api_key"}}`），需捕获异常并依据 `code` 字段处理（详见[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


