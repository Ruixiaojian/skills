# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力的对接，覆盖云端知识库管理、大模型调用、[检索增强生成](../concepts/rag.md)等核心场景。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台中已创建的应用或知识库资源使用。

## 支持的模型/功能

- **RAG 构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、自动切分（仅限 `.txt`/`.docx`/`.pdf`）、向量化（固定官方向量模型）及 `qwen-max` 等千问系列模型生成回答。
- **智能体与工作流集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，适用于复杂任务编排、多步骤决策等场景。
- **知识库直接检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，可对接控制台中已创建的知识库（如 `测试知识库`），默认使用 `qwen-max` 模型生成答案，并支持自定义提示词模板与模型切换（如 `qwen-plus`）。

> **注意**：LlamaIndex 方案明确不支持自定义文档切分方式或嵌入模型（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)），而 Spring AI Alibaba 的知识库检索方案未提及该限制，但实际仍依赖百炼后台统一向量服务，因此二者在底层能力上一致，均不开放嵌入模型替换。

## 关键参数

| 参数 | 说明 | 来源/示例 |
|------|------|-----------|
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API Key，必须配置为环境变量；两文档使用不同变量名，推荐统一采用 `DASHSCOPE_API_KEY` 避免混淆 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 智能体或工作流应用 ID，仅 Spring AI Alibaba 调用应用时必需 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，用于跨空间访问应用或知识库；两文档变量名不一致，建议以 `WORKSPACE_ID` 为准 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `INDEX_NAME` | 知识库名称，Spring AI Alibaba 知识库检索必需，LlamaIndex 中对应 `cloud_index_name` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，支持 `similarity_top_k`、`similarity_cutoff`、`DashScopeRerank` 等后处理配置；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成**：  
  - **调用应用**：引入 `spring-ai-alibaba-starter-dashscope`，配置 `APP_ID` 和 `DASHSCOPE_API_KEY`，使用 `DashScopeAgent` 实例执行非流式/流式调用。  
  - **检索知识库**：引入相同 starter，配置 `AI_DASHSCOPE_API_KEY`，注入 `DashScopeApi`，通过 `DashScopeDocumentRetriever` 绑定 `INDEX_NAME`，结合 `ChatClient` 与 `DocumentRetrievalAdvisor` 实现 RAG 流程。

## 限制和注意事项

- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文件上传与解析，不支持 Excel、PPT 等格式（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **模型绑定限制**：LlamaIndex 示例中 `Settings.llm = DashScope(model_name="qwen-max")` 明确指定模型，但未说明是否支持其他模型；Spring AI Alibaba 知识库检索示例中注释指出可通过 `.defaultOptions(...)` 切换模型（如 `qwen-plus`），表明其模型选择更灵活。
- **知识库部署模式**：LlamaIndex 方案仅支持**云端知识库**，且强调“不支持自定义文档切分方式或自定义嵌入模型”；若需本地部署或深度定制，需参考其他方案（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **环境兼容性**：Spring AI Alibaba 要求 JDK 17+ 和 Spring Boot 3.x，两个 Spring 相关文档对此要求一致，但 LlamaIndex 文档仅要求 Python 3.9+，无 Java 版本约束。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


