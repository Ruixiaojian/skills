# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力的对接，覆盖云端知识库管理、大模型调用、[检索增强生成](../concepts/rag.md)及应用编排等核心场景。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台创建的对应资源（如知识库、应用 ID）使用。

## 支持的模型/功能

- **RAG 构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、智能切分、向量化索引构建、多级后处理（相似度过滤 + 重排）及问答生成。
- **智能体与工作流调用**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，支持非流式与流式响应，可获取 `docReferences` 和 `thoughts` 等结构化输出。
- **知识库直接检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，实现对已有知识库的语义检索，并自动注入上下文至 `ChatClient` 生成回答。

> **注意**：LlamaIndex 方案明确不支持自定义文档切分方式或自定义嵌入模型（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)），而 Spring AI Alibaba 的知识库检索方案未提及该限制，但其底层仍依赖百炼默认向量模型与切分策略，实际能力一致。开发者不应假设 Spring AI Alibaba 可绕过此限制。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API 密钥环境变量名 | `sk-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 智能体/工作流应用 ID | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID（可选） | `ws-xxx` | 两篇 Spring AI Alibaba 文档均要求配置该变量以访问子空间资源 |
| `model_name`（LlamaIndex） / `defaultOptions(...withModel(...))`（Spring AI） | 指定生成模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中明确列出可用模型；Spring AI 示例中注释提示可切换模型 |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等配套包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 调用 `index.as_query_engine()` 并配置 `similarity_top_k`、`node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）和 `response_mode`；  
  4. 执行 `query_engine.query(prompt)` 获取结构化响应（含 `source_nodes`）。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 同上配置 API Key；  
  2. 创建 `DashScopeDocumentRetriever` 并指定 `indexName`；  
  3. 将其作为 `DocumentRetrievalAdvisor` 注入 `ChatClient.Builder`；  
  4. 使用 `chatClient.prompt().user(...).stream().chatResponse()` 触发 RAG 流程。

## 限制和注意事项

- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文件上传与解析，不支持 Excel、PPT 或图像类文档（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **知识库部署模式隔离**：LlamaIndex 方案强制使用**云端知识库**，不支持本地部署模式下的自定义切分与嵌入（原文明确区分“云端”与“本地”两种路径，且云端方案禁用自定义能力）。
- **应用类型限制**：Spring AI Alibaba 的 `DashScopeAgent` **仅支持智能体应用和工作流应用**，不支持直接调用基础模型或知识库（见[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）；知识库检索需单独使用 `DashScopeDocumentRetriever`。
- **环境兼容性**：Spring AI Alibaba 两篇文档均要求 **JDK 17+** 和 **Spring Boot 3.x**，版本不匹配将导致依赖冲突或功能不可用。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


