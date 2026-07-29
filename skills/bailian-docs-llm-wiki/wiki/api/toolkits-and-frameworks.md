# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及专用工具链，支持开发者快速迁移现有应用或构建新场景。核心能力覆盖文本生成（Chat/Completions/Responses）、多模态理解（Vision）、向量嵌入（Embedding）、文件处理（Files）、批量推理（Batch）、会话管理（Conversations）以及主流框架集成（如 LangChain）。所有接口均通过统一的 `compatible-mode/v1` 路径暴露，但模型支持范围、参数行为和地域端点存在差异，需按场景谨慎选型。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **标准 Chat 接口**：兼容 `chat/completions`，支持 Qwen 系列（`qwen-plus`, `qwen-flash`, `qwen3-*`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）等 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API（智能体原生）**：专为复杂任务设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-plus`、`qwen3.5-flash`、`qwen3-coder-next` 等 20+ 个 Qwen3 系列模型及 `qwen-plus` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision 接口**：支持[多模态输入](../concepts/multi-modal-input.md)（文本+图像 URL/Base64），适配 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding 接口**：提供 `text-embedding-v1` 至 `v4` 四代文本向量模型，支持可调维度（如 `v4` 支持 64–2048）及多语种，但**多模态 Embedding（如 `qwen3-vl-embedding`）不支持 OpenAI 兼容协议** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Files 接口**：用于上传文档供 `Qwen-Long`（长文档问答）、`Qwen-Doc-Turbo`（数据提取）或 Batch/Fine-tune 任务使用，支持 TXT/DOCX/PDF/图片等格式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch 接口**：分两种模式：  
  - **文件输入（JSONL）**：异步批量处理，支持 `qwen3.7-max`（256K 上下文）、`qwen-vl-plus` 等 30+ 模型；  
  - **同步 Batch Chat**：单请求阻塞式调用，仅需切换 `base_url` 即可复用现有 Chat 代码 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **Conversations API**：管理跨设备会话状态，支持创建、查询、更新、删除会话及追加消息项，与 Responses API 配合实现上下文自动注入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **Completions 接口**：专用于代码补全，当前**仅支持 `qwen-coder-turbo` 模型**，且仅限华北2（北京）地域 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：文档 1 和文档 2 均强调业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）的性能与稳定性优势，但文档 3 的 Completions 接口示例仍使用旧域名 `https://dashscope.aliyuncs.com`，存在迁移指引不一致问题，建议以文档 1 和 2 的推荐为准。

## 关键参数

各接口共性参数与关键差异如下：

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填，服务端点。地域不同路径不同，北京/新加坡需替换 `{WorkspaceId}` | 北京/新加坡必须使用业务空间专属域名；弗吉尼亚/东京/法兰克福无需 WorkspaceId；Batch Chat 使用独立域名 `https://batch.dashscope.aliyuncs.com` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) |
| `model` | 模型名称，严格区分大小写与版本后缀（如 `qwen3.7-plus` vs `qwen3.7-plus-2026-01-23`） | Vision 接口不支持 `qwen-audio`；Completions 接口仅支持 `qwen-coder-turbo`；Embedding 不支持多模态模型 |
| `stream` / `stream_options` | 控制[流式输出](../concepts/streaming-output.md)。`stream_options={"include_usage": true}` 可在流末尾返回 token 统计 | QVQ 模型**强制[流式输出](../concepts/streaming-output.md)**，非流式调用将失败 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `enable_thinking` | Batch 场景下控制思考模式（影响 token 成本）。`qwen3.5/3.6/3.7` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body`** | 此参数在 Chat/Responses 接口中无效，仅 Batch JSONL 文件中生效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `previous_response_id` | Responses API 多轮对话的核心参数，传入上一轮响应的顶层 `id`（UUID 格式） | **不可传入 `output` 数组内消息的 `id`**（如 `msg_xxx`），否则上下文关联失败 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `dimensions` | Embedding 接口特有，指定向量维度（仅 `v3`/`v4` 支持） | `v1`/`v2` 不支持该参数，设置将导致错误 |

## 使用方式

### 通用步骤
1. **获取并配置 API Key**：通过百炼控制台获取，**强烈建议配置至环境变量 `DASHSCOPE_API_KEY`**，避免硬编码泄露风险；  
2. **选择 `base_url`**：根据地域与接口类型确定（见上表），北京/新加坡务必替换 `{WorkspaceId}`；  
3. **安装 SDK**：Python 推荐 `pip install -U openai langchain_openai`；Java/Node.js/Go 等参照对应文档；  
4. **构造请求**：按接口规范传入 `model`、`input`/`messages`/`prompt` 等核心字段。

### 典型调用示例
- **Chat（非流式）**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
  ```
- **Responses（多轮）**：  
  ```python
  # 第一轮
  resp1 = client.responses.create(model="qwen3.7-plus", input="我的名字是张三")
  # 第二轮（自动继承上下文）
  resp2 = client.responses.create(model="qwen3.7-plus", input="你还记得我的名字吗？", previous_response_id=resp1.id)
  ```
- **Vision（图文理解）**：  
  ```python
  completion = client.chat.completions.create(
      model="qwen3-vl-plus",
      messages=[{"role":"user","content":[{"type":"text","text":"这是什么"},{"type":"image_url","image_url":{"url":"https://..."}}]}],
      stream=True
  )
  ```
- **LangChain 集成**：  
  - `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型（如 `qwen-plus`）；  
  - `langchain_community.chat_models.tongyi.ChatTongyi`：支持全部百炼文本模型（含部署模型）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与模型绑定**：部分模型仅在特定地域可用（如三方直供模型仅限中国内地），需在控制台开通后方可调用；  
- **文件限制**：Files 接口上传文件总大小 ≤100 GB，总数 ≤10,000 个；`file-extract` 单文件 ≤150 MB，`batch`/`fine-tune` 单文件 ≤500 MB/300 MB；  
- **Batch 超时**：Batch Chat 同步调用默认超时 3600 秒（1 小时），不可超过此值；Batch 文件处理最长等待时间由 `completion_window` 参数控制（如 `"24h"`）；  
- **Qwen-Audio 不兼容**：明确不支持 OpenAI 兼容协议，仅能通过 DashScope 原生协议调用；  
- **旧路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已标记为“即将停止维护”，必须迁移到 `/compatible-mode/v1/{responses|conversations}`；  
- **参数作用域**：`enable_thinking` 仅在 Batch JSONL 请求体中有效，且必须与 `model` 同级；`previous_response_id` 仅适用于 Responses API，Chat 接口需自行维护消息历史。

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


