# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、[向量嵌入](../concepts/vector-embedding.md)、批量处理、对话管理等核心场景。开发者可通过统一 SDK（如 OpenAI Python/Node.js SDK）或 HTTP 直调方式快速迁移现有应用，仅需调整 `base_url`、`api_key` 和模型名即可接入。所有接口均支持[流式输出](../concepts/streaming-output.md)、[Token](../concepts/token.md) 统计、上下文管理等标准能力，并针对百炼模型特性（如[长上下文](../concepts/long-context.md)、思考模式、内置工具）进行了增强。

## 支持的模型/功能

百炼兼容接口支持三大类模型能力：

- **通用文本生成**：包括 `qwen3.8-max`、`qwen-plus`、`qwen-flash` 等全系列 Qwen 模型，以及 DeepSeek-V4、Kimi、GLM、MiniMax 等三方直供模型（仅限中国内地地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **多模态理解**：`qwen-vl-plus`、`qwen3-vl-plus`、`qwen-vl-ocr`、`QVQ` 等视觉模型，支持图像+文本混合输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **向量化与批处理**：`text-embedding-v1` 至 `v4` 全系列文本向量模型，以及 `qwen-long`、`qwen-doc-turbo` 等长文档/结构化数据专用模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)提供 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持原生 DashScope 协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且部分模型（如 `qwen3.8-max`）在 Batch 中默认开启思考模式，会产生额外 `reasoning_tokens` 成本，需显式设置 `enable_thinking=false` 关闭 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 关键参数

所有兼容接口共用以下关键参数，行为与 OpenAI 官方一致，但部分字段有百炼特有约束：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，官方强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- `model`：模型名需严格匹配控制台支持列表，例如 `qwen3.8-max`、`text-embedding-v4`、`qwen-vl-plus`，不区分大小写但不可拼错；  
- `stream` 与 `stream_options`：均支持，`stream_options={"include_usage": true}` 可在流式响应末尾返回 [Token](../concepts/token.md) 使用统计；  
- `temperature` / `top_p`：互斥，建议只设其一；`max_tokens` 为硬截断上限，超限内容将被丢弃；  
- `enable_thinking`：仅 Batch 和 Responses 接口支持，`boolean` 类型，用于控制是否启用模型内部推理链路，默认 `true`，关闭可降低费用 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 使用方式

### 基础调用（Chat Completions）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

### 批量处理（Batch Chat）
替换 `base_url` 即可切换为同步批量模式（非文件上传）：
```python
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"  # 注意此URL
).with_options(timeout=1800.0)  # 最长等待3600秒
```

### 文件处理（Files API）
用于文档问答、批量任务或微调：
```python
file_obj = client.files.create(
    file=Path("doc.pdf"),
    purpose="file-extract"  # 或 "batch", "fine-tune"
)
# 后续在 qwen-long 请求中传入 file_id
```

### 对话状态管理（Conversations API）
自动维护跨设备会话上下文：
```python
conv = client.conversations.create(
    metadata={"topic": "customer_support"},
    items=[{"role": "system", "content": "你是一名客服助手"}]
)
# 后续请求中引用 conv.id 即可复用上下文
```

## 限制和注意事项

- **地域与域名绑定**：北京、新加坡地域必须使用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 格式域名；弗吉尼亚、法兰克福、东京等地域暂未开放业务空间专属域名，仍使用 `dashscope-us.aliyuncs.com` 等全局域名；  
- **模型可用性差异**：同一模型在不同地域支持情况不同（如 `deepseek-v4-pro` 仅限北京与新加坡），务必在控制台确认 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **文件配额限制**：`files` 接口总存储上限为 10,000 个文件 / 100 GB，单文件最大 150 MB（`file-extract`）、500 MB（`batch`）、300 MB（`fine-tune`）；  
- **Responses API 的上下文机制**：`previous_response_id` 必须传入上一轮响应的顶层 `id`（如 `resp_xxx`），而非 `output` 数组内消息的 `msg_xxx` ID；  
- **LangChain 集成双路径**：推荐优先使用 `langchain_openai`（OpenAI 兼容模式，模型有限但生态成熟），若需调用全部百炼模型（如 `qwen-coder-turbo`），应改用 `langchain_community.chat_models.tongyi.ChatTongyi` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

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


