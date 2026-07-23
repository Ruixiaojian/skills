# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，支持开发者快速迁移现有应用。核心能力覆盖文本生成（Chat、Completions、Responses）、[多模态](../concepts/multi-modal.md)理解（Vision）、向量化（Embedding）、批量处理（Batch）、会话管理（Conversations）及文件操作（Files），并兼容主流开发框架如 LangChain。所有接口均基于统一的 `compatible-mode/v1` 路径设计，通过调整 `base_url`、`api_key` 和 `model` 即可完成集成。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分如下：

- **Chat Completions**：适用于标准对话场景，支持 Qwen 系列（`qwen-plus`、`qwen-flash` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Completions**：专为代码补全与内容续写设计，当前仅支持 `qwen-coder-turbo` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Responses**：作为 Chat Completions 的演进版，内置联网搜索、网页抓取等智能体原生工具，支持 `qwen3.7-plus`、`qwen3.6-flash` 等新一代 Qwen3 系列模型，并在华北2（北京）、新加坡、弗吉尼亚等多地部署 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision**：支持视觉理解任务，兼容 `qwen3-vl-plus`、`QVQ`、`qwen-vl-ocr` 等模型，支持图像 URL 与 Base64 输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：提供 `text-embedding-v4`、`v3`、`v2`、`v1` 四代文本向量模型，支持多语种及可选维度（如 `dimensions=1024`），但[多模态](../concepts/multi-modal.md) Embedding 模型（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Batch**：分为两种模式：  
  - **文件批量（Batch File）**：通过 JSONL 文件异步提交请求，支持 `qwen3.7-max`、`qwen3-vl-plus`、`text-embedding-v4` 等模型，费用为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；  
  - **同步 Batch Chat**：单请求同步等待返回，适用于数据标注等非实时场景，端点为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Conversations**：用于跨设备/长时间会话状态管理，配合 Responses API 自动注入历史上下文，支持创建、查询、更新、删除会话及添加消息项 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **Files**：支持上传文件用于文档问答（`purpose="file-extract"`）、批量推理（`purpose="batch"`）或模型调优（`purpose="fine-tune"`），最大单文件 150 MB（extract）、500 MB（batch）、300 MB（fine-tune） [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

> **注意**：文档 1 和文档 5 均提及旧域名迁移建议（如 `dashscope.aliyuncs.com` → `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），但文档 6 的“前提条件”中仍列出 `https://dashscope.aliyuncs.com/compatible-mode/v1` 为中国内地服务端点，与文档 1 的推荐实践存在不一致。实际生产环境应优先采用业务空间专属域名以保障性能与稳定性。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 适用接口 |
|------|------|------|------|----------|
| `base_url` | string | 是 | 接口根地址，需按地域和功能选择（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。`{WorkspaceId}` 须替换为控制台获取的实际 ID | 所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) |
| `model` | string | 是 | 模型名称，必须从各接口支持列表中选取（如 `qwen-plus`、`text-embedding-v4`） | 所有 OpenAI 兼容接口 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)，默认 `false`；流式响应中可通过 `stream_options={"include_usage": true}` 在末尾返回 token 统计 | Chat、Completions、Vision、Responses |
| `max_tokens` | integer | 否 | 最大生成 token 数，超限将截断输出（不影响模型内部生成逻辑） | Chat、Completions、Responses |
| `temperature` / `top_p` | float | 否 | 控制生成多样性，二者互斥，建议只设其一（`temperature ∈ [0,2)`，`top_p ∈ (0,1]`） | Chat、Completions、Responses |
| `enable_thinking` | boolean | 否 | Batch 场景下控制思考模式开关（`true`/`false`），影响 token 成本；须与 `model` 同级传入，不可置于 `extra_body` 内 | Batch Chat、Batch File |
| `dimensions` | integer | 否 | Embedding 接口专用，指定向量维度（仅 `text-embedding-v3`/`v4` 支持） | Embedding |
| `purpose` | string | 是（Files） | 文件上传用途：`file-extract`（文档分析）、`batch`（批量输入）、`fine-tune`（调优数据集） | Files |

## 使用方式

### 基础 SDK 配置（Python 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置至环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换 {WorkspaceId}
)
```

### 各接口典型调用
- **Chat**：`client.chat.completions.create(model="qwen-plus", messages=[...])`  
- **Completions**：`client.completions.create(model="qwen-coder-turbo", prompt="<tool_call>{code_prefix}<tool_call>")`  
- **Responses**：`client.responses.create(model="qwen3.7-plus", input="你好！")`  
- **Vision**：`client.chat.completions.create(model="qwen3-vl-plus", messages=[{"role":"user","content":[{"type":"text","text":"这是什么"},{"type":"image_url","image_url":{"url":"..."}}]}])`  
- **Embedding**：`client.embeddings.create(model="text-embedding-v4", input="文本", dimensions=1024)`  
- **Batch Chat**：使用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`，调用方式与 Chat 完全一致  
- **Conversations**：`client.conversations.create(items=[{"role":"system","content":"..."}])`  
- **Files**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`  

LangChain 集成详见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)，推荐 `langchain_openai.ChatOpenAI`（部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（全模型支持）。

## 限制和注意事项

- **地域与模型绑定**：并非所有模型在所有地域可用。例如 `qwen3.7-max` 在北京、新加坡、弗吉尼亚、法兰克福、东京均支持，但 `qwen3.5-397b-a17b` 仅在北京、新加坡、法兰克福提供；`qwen3.7-plus` 在东京仅支持日本部署范围 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **三方模型可用性**：DeepSeek、Kimi 等第三方直供模型**仅在中国站的中国内地地域可用**，且需在控制台单独开通服务 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **协议限制**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **文件配额**：百炼文件存储上限为 **10,000 个文件** 或 **100 GB 总大小**，任一达到即拒绝新上传 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch 超时**：Batch Chat 默认等待 3600 秒（1 小时），超时后连接断开并返回错误；Batch File 任务最长等待时间为 `completion_window`（如 `"24h"`），需主动轮询状态 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **API Key 隔离**：不同地域（如北京 vs 新加坡）的 API Key **不可混用**，需分别获取并配置 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


