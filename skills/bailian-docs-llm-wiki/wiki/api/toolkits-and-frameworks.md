# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及主流框架集成能力，支持开发者快速迁移现有应用或构建新场景。核心包括 Chat、Responses、Conversations、Embedding、Vision、Files、Batch（文件输入/单请求）、Completions 等标准化接口，以及 LangChain、LangChain4j 等生态框架的原生适配。所有接口均基于统一的 `compatible-mode/v1` 路径设计，通过切换 `base_url` 和模型名即可复用 OpenAI SDK 代码。

## 支持的模型/功能

百炼支持的 OpenAI 兼容功能覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、批量处理、对话管理、文件上传与调优等全栈能力：

- **Chat 接口**：支持 `qwen-plus`、`qwen-flash`、`deepseek-r1`、`kimi`、`glm`、`minimax` 等数十种文本与[多模态](../concepts/multi-modal.md)模型（含 Qwen-VL、Qwen-Coder、Qwen-Omni），但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses 接口**：专为智能体（Agent）优化，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-plus`、`qwen3.5-397b-a17b`、`qwen3-coder-next` 等新一代大模型，显著简化上下文管理和[工具调用](../concepts/tool-use.md)流程。
- **Conversations 接口**：用于跨设备/长时间会话状态管理，支持创建、查询、更新、删除会话及追加消息项，配合 Responses API 实现无状态客户端的上下文自动注入。
- **Embedding 接口**：兼容 `text-embedding-v1` 至 `v4` 全系列模型，支持多语种（含 100+ 主流语言及编程语言）和可选维度（如 `dimensions=1024`），但 [多模态 Embedding 模型（如 qwen3-vl-embedding）不支持 OpenAI 兼容接口](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Vision 接口**：支持 `qwen3-vl-plus`、`qven3-vl-flash`、`qwen-ocr` 等视觉模型，接受结构化 `content`（含 `text` + `image_url` 或 Base64），[QVQ 模型仅支持流式输出](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Files 接口**：用于文档分析（`purpose=file-extract`）、批量推理（`purpose=batch`）和模型调优（`purpose=fine-tune`），分别对接 Qwen-Long、Qwen-Doc-Turbo 及 Fine-tuning 服务。
- **Batch 接口**：分为 **文件输入模式**（异步处理 JSONL，成本降低 50%）和 **单请求同步模式**（Batch Chat，保持同步调用体验），两者模型支持范围存在差异（例如 `qwen3.5-omni-plus` 在 Batch 文件模式下不支持语音输出）。
- **Completions 接口**：专用于代码补全等前缀/中缀生成任务，当前仅支持 `qwen-coder-turbo` 单一模型，且仅限华北2（北京）地域。

> **注意**：文档 1 与文档 2 均提及“业务空间专属域名迁移建议”，但文档 1 未列出德国（法兰克福）地域的专属域名，而文档 2 明确包含 `eu-central-1.maas.aliyuncs.com`；文档 4 的 Batch 文件接口“适用范围”中北京地域支持 `qwen3.7-max` 等模型，但文档 5 的 Batch Chat 接口同样列出这些模型——二者虽同属 Batch 场景，但底层实现与 [Token](../concepts/token.md) 限制（如 256K 上下文）一致，故无实质矛盾，仅需按具体接口类型选用。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数，部分接口扩展特定字段：

- `base_url`：必须配置为地域专属地址，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`（北京：`cn-beijing`；新加坡：`ap-southeast-1`；东京：`ap-northeast-1`；弗吉尼亚：`dashscope-us.aliyuncs.com`；法兰克福：`eu-central-1`）。旧域名（如 `dashscope.aliyuncs.com`）仍可用但**不推荐**。
- `api_key`：使用百炼控制台获取的对应地域 API Key，强烈建议通过环境变量 `DASHSCOPE_API_KEY` 配置以规避泄露风险。
- `model`：模型名称需严格匹配支持列表，例如 `qwen3.7-plus`（Responses）、`text-embedding-v4`（Embedding）、`qwen3-vl-plus`（Vision）。
- `stream` & `stream_options`：通用流式开关，`stream_options={"include_usage": true}` 可在流式结尾返回 [Token](../concepts/token.md) 统计。
- `enable_thinking`：Batch 场景下控制思考模式（`true`/`false`），`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启，需作为 `body` 顶层参数传入，**不可置于 `extra_body` 中**（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- `previous_response_id`（Responses）：用于多轮对话，值为上一轮响应的顶层 `id`（UUID 格式），非 `output` 内 `msg_xxx` ID。
- `dimensions`（Embedding）：仅 `text-embedding-v3`/`v4` 支持，用于指定向量维度（如 `1024`）。
- `prompt`（Completions）：使用特殊分隔符 `<tool_call>{prefix}<tool_call>{suffix}</tool_call>` 实现中缀生成，不支持后缀生成前缀。

## 使用方式

### SDK 调用（推荐）
安装最新版 `openai` SDK（`pip install -U openai`），初始化时指定 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# Chat
client.chat.completions.create(model="qwen-plus", messages=[...])
# Responses
client.responses.create(model="qwen3.7-plus", input="Hello")
# Files
client.files.create(file=Path("doc.pdf"), purpose="file-extract")
# Conversations
client.conversations.create(items=[{"role":"system","content":"..."}])
```

### LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（如 `qwen-plus`），依赖 `base_url` 切换。
- **DashScope 方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`（Python）或 `@langchain/community/chat_models/alibaba_tongyi`（JS），支持全部百炼文本模型及部署模型，需安装 `dashscope` 和 `langchain-community`。

### HTTP 直连
构造标准 OpenAI 兼容请求头与 payload，例如 Embedding：
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-v4","input":"hello","dimensions":1024}'
```

## 限制和注意事项

- **地域与模型绑定**：部分模型仅在特定地域可用（如三方直供模型仅限中国内地），且各接口支持的模型列表不同（如 Completions 仅支持 `qwen-coder-turbo`），务必查阅对应文档确认。
- **域名迁移强制性**：北京、新加坡地域已上线业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧域名虽暂兼容，但[官方明确建议迁移以获得更高性能与稳定性](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件服务配额**：Files 接口总存储上限为 100 GB / 10,000 个文件，超限后上传失败；`file-extract` 单文件 ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB。
- **Batch 超时机制**：Batch Chat 单次请求最长等待 3600 秒（1 小时），超时断连返回错误；Batch 文件模式 `completion_window` 最长支持 `24h`。
- **参数位置约束**：`enable_thinking` 必须作为 JSONL 请求体 `body` 的顶层字段（与 `model` 同级），违反此规则将导致参数被忽略（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- **功能缺失声明**：Qwen-Audio、[多模态](../concepts/multi-modal.md) Embedding 模型、旧版 `/api/v2/apps/...` 路径均明确不支持或即将下线，开发中需主动规避。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)


