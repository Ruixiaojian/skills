# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 协议规范的标准化服务入口，允许开发者复用现有 OpenAI SDK、工具链和业务代码，无需修改核心逻辑即可接入通义千问等百炼模型。该接口在协议层（路径、请求/响应结构、字段命名）与 OpenAI 官方 API 高度一致，仅需替换 `base_url` 和 `api_key` 即可完成迁移。

## 在百炼平台的不同场景中如何使用

OpenAI 兼容接口不是单一接口，而是一系列按功能划分、统一协议风格的接口集合，覆盖主流 AI 开发场景：

- **文本生成**：  
  - `chat/completions`：标准对话接口，支持 `qwen-max`、`qwen-plus`、`qwen3.8-max` 等模型；适用于已有 OpenAI Chat SDK 的项目，零代码迁移。  
  - `responses`：增强型对话接口，内置联网搜索、代码解释器、网页提取等工具能力，自动管理上下文；支持 `previous_response_id` 实现轻量多轮续聊，适合 Agent 应用快速构建。  
  - `completions`：前缀补全专用接口，仅支持 `qwen-coder-turbo`，适用于 IDE 插件或代码补全场景。

- **[多模态](multi-modal.md)理解**：  
  `chat/completions` 接口兼容 OpenAI Vision 协议，支持 `qwen-vl-plus`、`qwen3-vl-plus` 等视觉模型，输入格式为 `{"role": "user", "content": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {"url": "..."}}]}`。

- **向量嵌入**：  
  `embeddings` 接口完全兼容 OpenAI Embedding API，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型；支持 `dimensions`（v3/v4）、`encoding_format` 等关键参数，适用于 RAG 场景。

- **文件与批量处理**：  
  `files` 接口支持文档解析（`purpose=file-extract`）、批量推理输入（`purpose=batch`）；`batches` 接口支持异步 JSONL 批量提交，费用为实时调用的 50%。

- **应用调用**：  
  通过 `compatible-mode/v1/responses` 路径调用已发布的智能体（Agent）或工作流应用，支持 `app_id` + `input` 直接触发，兼容 `stream` 流式与 `background=true` 异步模式。

- **排序（Rerank）**：  
  `qwen3-rerank` 等模型通过 OpenAI 兼容 `/rerank` 路径提供语义重排序能力，支持 `instruct` 指令定制，适用于[检索增强生成](rag.md)（RAG）后处理。

> ✅ **关键提示**：所有 OpenAI 兼容接口均不支持 DashScope 原生特有功能（如 `response_format` JSON Schema 强约束、`incremental_output`、`input_files` 文件上传），如需这些能力，请切换至 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | string | 是 | 服务端点，**必须使用地域专属域名**：<br>`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（推荐北京/新加坡/东京/法兰克福/弗吉尼亚）<br>旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐 | `https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 是 | 方案专属密钥（[Token](token.md) Plan / Coding Plan / 按量计费），**不可跨方案复用**；需与 `base_url` 所属方案及地域严格匹配 | `sk-xxx`（[Token](token.md) Plan 个人版 Key） |
| `model` | string | 是 | 模型标识符，**因接口类型而异**：<br>- `chat/completions`: `qwen3.8-max`, `qwen-vl-plus`<br>- `responses`: `qwen3.8-max`, `deepseek-v4-flash`<br>- `embeddings`: `text-embedding-v4`, `qwen3.7-text-embedding` | `qwen3.8-max` |
| `previous_response_id` | string | 否 | 仅 `responses` 接口支持；传入上一轮响应的 `id`（UUID），用于自动关联上下文，有效期 7 天 | `"resp_abc123..."` |
| `stream` | boolean | 否 | 是否启用流式响应（`true`/`false`）；`chat/completions` 和 `responses` 均支持，客户端需解析 `choices[0].delta.content` | `true` |
| `instruct` | string | 否 | 仅 `rerank` 接口支持；自定义排序指令，影响语义匹配逻辑 | `"Rank for question-answering task"` |

> ⚠️ 注意事项：  
> - `temperature` 在 OpenAI 兼容接口中接受 `[0, 2]`，但低于 `0.01` 会被静默截断为 `0.01`；  
> - 所有接口均**不支持跨账号共享模型**，`model` 必须属于当前 workspace；  
> - `messages` 总 token 数上限依模型而定（如 `qwen-max` 为 32768），超限将返回 400 错误。

## 面向开发者：快速上手建议

1. **选对 endpoint**：  
   - Chat：`{base_url}/chat/completions`  
   - Responses：`{base_url}/responses`  
   - Embeddings：`{base_url}/embeddings`  
   - Rerank：`{base_url}/rerank`  
   - Files：`{base_url}/files`  

2. **复用 OpenAI SDK**（Python 示例）：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key="sk-xxx",  # 百炼 Token Plan 或按量 Key
       base_url="https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.8-max",
       messages=[{"role": "user", "content": "你好"}],
       stream=True
   )
   ```

3. **调试技巧**：  
   - 若返回 `401 Unauthorized`，请确认 `api_key` 与 `base_url` 是否同属一个计费方案和地域；  
   - 若返回 `404 Not Found`，检查 `model` 名称是否拼写正确、是否在当前接口支持列表中；  
   - 流式响应需监听 `delta.content` 字段，而非 `output.text`（DashScope 原生格式）。

4. **进阶迁移**：  
   - 已有 OpenAI 项目 → 替换 `base_url` + `api_key`，其余代码基本无需改动；  
   - 需要工具调用 → 优先选用 `responses` 接口（自动编排），避免手动构造 `tool_calls`；  
   - 需要 JSON Schema 输出 → 切换至 DashScope 原生接口，使用 `response_format` 参数。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


