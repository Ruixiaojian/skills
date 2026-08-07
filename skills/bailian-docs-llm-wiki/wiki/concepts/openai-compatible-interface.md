# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 官方 API 协议（如 `chat/completions`、`embeddings`、`reranks` 等端点），使开发者能复用现有 OpenAI 生态工具链（如 `openai>=1.0` SDK、LangChain、LlamaIndex）无缝接入百炼模型服务，无需修改业务逻辑代码。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有应用**：若项目已基于 OpenAI SDK 开发，只需将 `base_url` 替换为百炼的兼容地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并配置百炼 `DASHSCOPE_API_KEY`，即可直接调用 Qwen 系列（`qwen3.8-max`、`qwen-plus` 等）、DeepSeek、Kimi、GLM、Qwen-VL、Qwen-MT、text-embedding-v4、qwen3-rerank 等数十种模型。
- **[多模态](multi-modal.md)任务**：支持 `image_url` 和 Base64 图像输入（需 `messages.content` 为对象数组），适用于 `qwen-vl-plus`、`qwen3-vl-flash`、`qwen-ocr` 等视觉模型；但 `qwen-audio` 和 `qwen3-vl-embedding`（[多模态](multi-modal.md)向量）等部分模型**不支持** OpenAI 兼容协议，须改用 DashScope 原生接口。
- **向量与排序服务**：文本嵌入（`/embeddings`）和纯文本重排（`/reranks`）均提供 OpenAI 兼容端点，参数简洁（如 `input`、`query` + `documents`、`top_n`），适合 RAG 构建；但[多模态](multi-modal.md)嵌入（`multimodal-embedding`）和跨模态排序（`qwen3-vl-rerank`）仅支持 DashScope 原生协议。
- **批量与异步处理**：支持两种批量模式：  
  - **文件批量（异步）**：通过 `/files` + `/batches` 提交 JSONL 文件，成本降低 50%，适用于大规模离线处理；  
  - **Batch Chat（同步）**：单次请求携带多条 `messages`，端点为 `/batch/chat/completions`，适合低延迟批量推理。  
  > 注意：二者协议不互通，且 `enable_thinking` 等参数在 JSONL 中必须置于 `body` 顶层。
- **智能体增强能力**：启用 `Responses API` 后，可自动维护对话上下文、触发联网搜索/代码解释器等内置工具，开发者无需手动管理 `messages` history，适合轻量级 Agent 应用。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填。OpenAI 兼容接口根地址 | **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已不推荐；地域与 API Key 必须匹配（北京 Key 不可用于新加坡服务）。 |
| `api_key` | 必填。百炼平台生成的 `DASHSCOPE_API_KEY` | 按地域独立创建，不可跨地域复用；建议设为环境变量 `DASHSCOPE_API_KEY`。 |
| `model` | 必填。模型 ID | 需严格匹配支持列表（如 `"qwen3.8-max"`、`"text-embedding-v4"`、`"qwen3-rerank"`）；`qwen-deep-research`、`qwen-audio`、`qwen3-vl-embedding` 等**不支持**该协议。 |
| `messages` | 必填（Chat 场景）。对话历史数组 | 格式为 `[{"role":"user","content":"..."}]`；`system` 角色仅 DashScope 原生接口支持，OpenAI 兼容接口中会被忽略。 |
| `stream` | 可选。是否启用流式响应 | 默认 `false`；`QVQ` 等视觉模型强制流式；流式响应中 `delta.content` 可能为空（表示工具调用开始），需跳过空字符串判断。 |
| `temperature` | 可选。输出随机性控制 | 范围 0.0–1.0（超出部分被截断），不同于 DashScope 原生接口的 0.0–2.0。 |
| `functions` / `tools` | 可选。工具定义 | OpenAI 兼容接口使用 `functions` 字段（非 `tools`）；函数 `description` 为可选，而 DashScope 原生要求必填。 |

## 面向开发者：简洁实用提示

- ✅ **起步最快方式**：用 OpenAI Python SDK（v1.0+），仅改两处——`api_key` 设为 `DASHSCOPE_API_KEY`，`base_url` 设为业务空间专属地址。
- ✅ **调试技巧**：开启 `stream=True` 并监听 `response.choices[0].delta.content`，可实时观察 token 流出；错误时检查 HTTP 状态码 + JSON body 中的 `code`（如 `"InvalidParameter"`）。
- ⚠️ **避坑重点**：  
  - `system` 消息无效 → 改用 `messages[0]` 的 `user` 角色承载系统指令；  
  - `n > 1` 被忽略 → 百炼所有协议均不支持并行生成多个候选；  
  - 多模态模型需验证兼容性 → 查阅各模型文档确认是否支持 OpenAI 协议（如 `qwen-audio` ❌，`qwen-vl-plus` ✅）；  
  - 批量接口路径不同 → `/batches`（异步文件） vs `/batch/chat/completions`（同步单请求），勿混淆。
- 📦 **SDK 推荐**：优先使用 `openai>=1.0`（Python/Node.js/Go）或 DashScope SDK（Java/Python），后者对 `extra_body`、`vl_high_resolution_images` 等扩展字段支持更完整。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [vector and sort](../api/vector-and-sort.md)
- [get started with models](../guides/get-started-with-models.md)


