# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力的对接，覆盖云端知识库管理、模型调用、[检索增强生成](../concepts/rag.md)等核心场景。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台中已创建的应用或知识库资源使用。

## 支持的模型/功能

- **RAG 应用构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、自动切分（默认官方向量模型）、相似性检索、重排（`gte-rerank`）及大模型生成（如 `qwen-max`、`qwen-plus`）。
- **智能体与工作流集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，适用于需编排复杂逻辑、多步骤决策或外部工具调用的场景。
- **知识库直接检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，可对接控制台中已创建的知识库（按 `index_name` 引用），实现低代码 RAG 集成，支持流式响应与自定义提示词模板。

> **注意**：LlamaIndex 方案明确声明“不支持自定义文档切分方式或自定义嵌入模型”（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)），而 Spring AI Alibaba 的知识库检索方案未提及该限制，但其底层仍依赖百炼托管的向量化能力，实际亦不开放嵌入模型替换。二者在能力边界上一致，文档表述差异属侧重点不同，非实质性矛盾。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API Key，用于身份认证。两套框架推荐环境变量名不同，需按框架要求配置 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 智能体/工作流应用 ID，仅 Spring AI Alibaba 调用应用时必需 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，跨空间访问应用或知识库时必需；环境变量名不统一，需严格匹配框架配置 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称，LlamaIndex 使用 `DashScopeCloudIndex("name")`，Spring AI Alibaba 使用 `withIndexName("name")` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | 大模型标识符，如 `"qwen-max"`，LlamaIndex 在 `Settings.llm = DashScope(model_name=...)` 中设置；Spring AI Alibaba 可通过 `DashScopeChatOptions.builder().withModel(...)` 覆盖默认值 | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeParse` 解析本地文件并调用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`node_postprocessors`（如 `SimilarityPostprocessor`、`DashScopeRerank`）及 `response_mode`。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 同样添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.api-key`（及可选 `workspace-id`）；  
  3. 构建 `DashScopeDocumentRetriever` 并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`，由框架自动完成检索+生成链路。

## 限制和注意事项

- **知识库来源限制**：LlamaIndex 方案仅支持从本地文件上传构建云端知识库，且仅限 `.txt`、`.docx`、`.pdf` 格式；不支持直接接入已有知识库或本地向量库 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **应用类型限制**：Spring AI Alibaba 的 `DashScopeAgent` 仅支持集成**智能体应用**和**工作流应用**，不支持直接调用基础模型或 RAG 应用 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **环境兼容性**：Spring AI Alibaba 要求 JDK 17+ 和 Spring Boot 3.x，LlamaIndex 示例要求 Python 3.9+；两者均需公网访问百炼服务端点。
- **计费说明**：框架本身不产生费用，但所有调用最终触发的模型推理（含 RAG 中的 LLM 生成、智能体执行、知识库检索后的回答生成）均按百炼计费项单独计费 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


