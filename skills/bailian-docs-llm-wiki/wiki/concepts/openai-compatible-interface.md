# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `/v1/chat/completions`、`/v1/embeddings` 等路径），支持使用标准 `openai` SDK（Python、Node.js 等）或通用 HTTP 客户端快速接入，无需修改业务逻辑即可调用百炼托管的多种大模型与能力。

## 在百炼平台的不同场景中如何使用

OpenAI 兼容接口不是单一接口，而是一套按能力分层、按场景隔离的协议族，开发者需根据目标功能选择对应子接口：

- **通用对话（Chat Completions）**：适用于多轮文本交互，支持 `qwen-plus`、`qwen3.7-plus`、`Qwen-VL`、`DeepSeek`、`Kimi`、`GLM` 等数十个模型；不支持 `Qwen-Audio`。  
- **智能体响应（Responses API）**：面向 Agent 场景的增强型接口，内置联网搜索、网页抓取等工具调用能力，仅支持 `qwen3-*` 系列模型（如 `qwen3.7-plus`），**不兼容旧版 `qwen-coder-turbo` 等模型**。  
- **代码补全（Completions）**：专用于代码生成与补全，当前**仅支持 `qwen-coder-turbo`**，且仅限华北2（北京）地域。  
- **多模态理解（Vision）**：支持图像输入的 `Qwen-VL`、`QVQ`、`Qwen-OCR`，其中 `QVQ` 仅支持[流式输出](streaming-output.md)。  
- **文本向量化（Embedding）**：支持 `text-embedding-v1` 至 `v4`，但**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不兼容该协议**。  
- **文件管理（Files）**：用于文档上传、批量推理（Batch）、模型微调（Fine-tune）等，单文件上限依用途为 150 MB / 500 MB / 300 MB。  
- **异步批量处理（Batch）**：含两种模式：  
  - *文件输入*（JSONL 格式）：适用于大规模任务，费用为实时调用的 50%；  
  - *Batch Chat*（同步阻塞）：保持实时 API 调用习惯，同样享 5 折优惠，**必须使用专用域名 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`**。  
- **会话管理（Conversations）**：配合 Responses API 实现跨设备上下文延续，支持创建、查询、更新、删除会话及添加消息项。  
- **应用调用（Application Call）**：通过 `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` 同步或异步调用已发布的智能体/工作流应用，支持 `stream=true` [流式输出](streaming-output.md)或 `background=true` 异步触发。

> ⚠️ 注意：不同子接口的 `base_url`、地域、API Key 和模型支持范围均严格隔离，混用将导致 401 或 404 错误。

## 关键参数和配置

所有 OpenAI 兼容接口共用以下核心配置项，必须正确设置：

| 参数 | 说明 | 必填 | 示例值 |
|------|------|------|--------|
| `base_url` | 接口根地址，**按子接口和地域严格区分**：<br>• Chat/Responses/Vision/Embedding/Conversations：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）<br>• Files/Batch（文件输入）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（中国内地）<br>• Batch Chat：**必须为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`** | ✅ | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `api_key` | DashScope API Key，**必须与 `base_url` 所属地域一致**（如北京 Key 不可用于新加坡 endpoint） | ✅ | `sk-xxx` |
| `model` | 模型 ID，**必须从对应子接口的支持列表中精确选取**（大小写敏感，不可拼写错误） | ✅ | `"qwen3.7-plus"`、`"text-embedding-v4"`、`"qwen-coder-turbo"` |
| `stream` | 布尔值，控制是否启用流式响应（`true`/`false`），部分接口（如 Batch Chat）不支持 | ❌ | `true` |

常用请求体参数（以 `/v1/chat/completions` 为例）：
- `messages`: OpenAI 标准格式数组，如 `[{"role":"user","content":"你好"}]`  
- `temperature`: 控制随机性（0.0–2.0），默认 `0.7`  
- `top_p`: 核采样阈值（0.0–1.0），默认 `1.0`  
- `max_tokens`: 最大生成 token 数，建议显式设置以防超限  
- `tools` / `tool_choice`: 仅 Responses API 及部分模型支持，用于[函数调用](function-calling.md)  

## 面向开发者：简洁实用指南

1. **选对接口**：先明确需求——是通用对话？还是调用智能体？需要嵌入向量？还是批量处理？再查对应子接口文档，确认模型支持与地域限制。  
2. **配对三要素**：`base_url` + `api_key` + `model` 必须同地域、同协议、同能力域，缺一不可。  
3. **用标准 SDK**：推荐 `openai==1.40.0+`（Python）或 `@openai/openai-node`（Node.js），只需设置 `base_url` 和 `api_key`，其余调用方式与 OpenAI 完全一致：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key="sk-xxx",
       base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你好"}]
   )
   print(response.choices[0].message.content)
   ```  
4. **避坑提示**：  
   - `qwen-vl` 图像输入仅支持 base64 或公网 URL，不支持本地路径；  
   - 所有接口**不返回 `delta.tool_calls`**（仅返回完整 `tool_calls`），需按 `finish_reason: "tool_calls"` 解析；  
   - `stream=true` 时，`usage` 字段仅在末尾 chunk 中出现；  
   - 工作流应用调用**仅支持华北2（北京）地域**，智能体应用建议保持地域一致。  

如遇 401（认证失败）、404（模型不支持）或 422（参数错误），请优先核对 `base_url` 域名、`api_key` 地域归属、`model` 名称拼写及子接口适用范围。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


