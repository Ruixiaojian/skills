# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG、智能体、工作流等大模型应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大生态实现标准化接入，覆盖云端知识库检索、应用调用、流式响应等核心场景。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台中已创建的资源（如知识库、应用 ID、业务空间）使用。

## 支持的模型/功能

- **RAG 场景**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 构建基于云端知识库的[检索增强生成](../concepts/rag.md)应用，适用于私域问答、客服支持等；支持文档自动切分（仅 `.txt`/`.docx`/`.pdf`）、默认向量模型嵌入、重排（`gte-rerank`）及多模型响应（如 `qwen-max`、`qwen-plus`）。
- **智能体与工作流调用**：支持通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 调用已发布的智能体应用（Single Agent）或工作流应用（Workflow），支持非流式与流式响应，返回结构化输出（含 `docReferences`、`thoughts` 等元信息）。
- **知识库直检**：支持通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 直接对接百炼知识库，无需独立部署向量库，由平台托管索引与检索逻辑，适用于轻量级 RAG 快速落地。

> **注意**：LlamaIndex 方案明确声明“不支持自定义文档切分方式或自定义嵌入模型”（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)），而 Spring AI Alibaba 的知识库检索方案未提及此限制，但其 `DashScopeDocumentRetriever` 实际仍依赖百炼平台侧的默认切分与嵌入策略，二者在能力边界上一致，不存在实质差异。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` | 百炼平台 API Key，用于身份认证 | `sk-xxx` | 所有文档均要求配置，推荐环境变量方式 |
| `APP_ID` | 智能体/工作流应用 ID | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` | 子业务空间 ID（可选） | `ws-xxx` | 两篇 Spring AI 文档均要求，但环境变量名不同：前者用 `WORKSPACE_ID`，后者用 `AI_DASHSCOPE_WORKSPACE_ID` |
| `INDEX_NAME` | 云端知识库名称 | `"my_first_index"` 或 `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 与 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` / `withModel()` | 指定调用的大模型 | `"qwen-max"`、`"qwen-plus"` | 均支持，LlamaIndex 中通过 `Settings.llm = DashScope(model_name=...)` 设置；Spring AI 中通过 `DashScopeChatOptions.builder().withModel(...)` 设置 |

> **注意**：`WORKSPACE_ID` 的环境变量名存在不一致——[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 推荐 `WORKSPACE_ID`，而 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 使用 `AI_DASHSCOPE_WORKSPACE_ID`。实际使用时请以对应 SDK 版本的 `application.yml` 配置为准，避免因变量名错误导致初始化失败。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`similarity_cutoff`、`node_postprocessors`（如 `DashScopeRerank`）等参数；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）；  
  4. 解析返回的 `AssistantMessage` 及其 `metadata` 中的 `output` 结构。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 同样依赖 `spring-ai-alibaba-starter-dashscope`；  
  2. 配置 `spring.ai.dashscope.api-key`（及可选 `workspace-id`）；  
  3. 构建 `DashScopeDocumentRetriever` 并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`；  
  4. 通过 `chatClient.prompt().user(...).stream().chatResponse()` 触发带上下文的生成。

## 限制和注意事项

- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文件上传与解析，不支持 Excel、PPT、图片等格式（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **知识库部署模式**：LlamaIndex 方案默认使用云端知识库，若需本地部署+自定义切分/嵌入，请参考官方替代方案（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）；Spring AI 方案目前仅支持云端知识库直检，无本地知识库适配路径。
- **模型选择范围**：所有方案均依赖百炼平台已开放的模型列表，`model_name` 必须为控制台「模型中心」中可用的正式模型名（如 `qwen-max`、`qwen-plus`），不可传入未上线或私有微调模型 ID。
- **计费说明**：框架集成本身不产生费用，但每次调用均触发百炼模型推理计费（见[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


