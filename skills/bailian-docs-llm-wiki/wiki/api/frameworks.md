# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建基于大模型的应用（如 RAG、智能体、工作流等）。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖 Python 和 Java 技术栈。所有集成均通过百炼统一的 DashScope API 层实现，无需直接对接底层模型服务。

## 支持的模型/功能

- **RAG 应用**：通过 LlamaIndex 或 Spring AI Alibaba 集成云端知识库，支持[检索增强生成](../concepts/rag.md)；知识库需提前在百炼控制台创建，支持 `.txt`、`.docx`、`.pdf` 等非结构化文档上传与自动切分（使用官方向量模型）[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **智能体与工作流应用**：仅支持通过 Spring AI Alibaba 调用已发布的 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 和 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，不支持直接调用基础大模型或自定义 Agent 框架 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **模型选择**：RAG 场景中默认使用 `qwen-max`，可通过 `model_name` 参数（LlamaIndex）或 `DashScopeChatOptions.builder().withModel(...)`（Spring AI Alibaba）显式指定其他千问系列模型；智能体/工作流调用时模型由应用配置决定，SDK 不暴露模型切换能力。

> **注意**：文档 1 中 `Settings.llm = DashScope(model_name="qwen-max")` 允许自由指定模型，而文档 3 明确限定 Spring AI Alibaba 仅支持集成「已发布的百炼应用」，且未提供运行时模型替换接口。二者能力边界不同——LlamaIndex SDK 直接对接百炼模型 API，Spring AI Alibaba 的 `DashScopeAgent` 则封装应用级调用，模型不可控。开发者应按场景选型：需灵活控制模型与检索逻辑时用 LlamaIndex；需复用百炼平台预置的业务逻辑编排（如多步骤工具调用、状态管理）时用 Spring AI Alibaba。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key，必需；推荐通过环境变量注入 | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID，仅当知识库或应用部署在子空间时必需 | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `INDEX_NAME` | 云端知识库名称，用于 `DashScopeCloudIndex`（LlamaIndex）或 `DashScopeDocumentRetriever`（Spring AI Alibaba）初始化 | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 百炼大模型应用 ID（智能体/工作流），仅 Spring AI Alibaba 调用应用时必需 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |

## 使用方式

- **LlamaIndex（Python）**：
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库，或 `DashScopeCloudIndex("your-index-name")` 加载已有知识库；
  3. 通过 `index.as_query_engine()` 配置检索参数（如 `similarity_top_k`、`node_postprocessors`）并发起查询。

- **Spring AI Alibaba（Java）**：
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 ≥ 1.0.0.2）；
  2. 配置 `application.yml` 中的 `spring.ai.dashscope.*` 参数；
  3. RAG 场景：注入 `DashScopeDocumentRetriever` 并结合 `ChatClient` + `DocumentRetrievalAdvisor`；  
     应用调用场景：注入 `DashScopeAgent`，通过 `agent.call()` 或 `agent.stream()` 发起非流式/流式调用。

## 限制和注意事项

- **知识库能力限制**：所有云端知识库均使用百炼默认的智能文档切分策略与官方向量模型（如 `gte-rerank`），不支持自定义切分规则、嵌入模型或向量存储后端 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **文件格式限制**：仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文档上传；不支持 Excel、PPT、图片、音视频等格式。
- **环境要求**：
  - LlamaIndex 方案要求 Python ≥ 3.9；
  - Spring AI Alibaba 方案要求 JDK ≥ 17 且 Spring Boot ≥ 3.x（GA 版本）。
- **网络要求**：所有客户端必须可访问公网（`dashscope.aliyuncs.com`），文件上传与模型调用均依赖外网连接。
- **错误处理**：当检索无结果或模型无法作答时，需在业务代码中显式判断 `resp.source_nodes`（LlamaIndex）或 `response.getResult()`（Spring AI Alibaba）并返回兜底提示，百炼 SDK 不自动降级。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


