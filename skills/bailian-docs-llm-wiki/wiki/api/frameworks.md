# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG、智能体、工作流等大模型应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼服务（包括云端知识库、大模型 API、智能体/工作流应用）的对接。所有集成均依赖统一的 DashScope SDK 底层能力，但各框架在功能覆盖、参数控制粒度和部署模式上存在差异。

## 支持的模型/功能

- **LlamaIndex**：支持构建基于云端知识库的 RAG 应用，涵盖文档上传、自动切分、向量化、检索与生成全流程；支持指定 `qwen-max` 等千问系列模型作为生成器，并可配置 `gte-rerank` 等重排模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba（智能体/工作流集成）**：仅支持调用已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，不支持直接访问知识库或自定义 RAG 流程 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **Spring AI Alibaba（知识库检索）**：支持通过 `DashScopeDocumentRetriever` 检索云端知识库，底层复用百炼知识库服务，但需预先创建知识库并指定 `index_name`；默认使用 `qwen-max` 生成回答，可通过 `.defaultOptions(DashScopeChatOptions.builder().withModel("qwen-plus").build())` 切换模型 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 2 明确限定 Spring AI Alibaba 仅支持“智能体应用”和“工作流应用”，而文档 3 提供了独立的知识库检索能力。二者属于同一 SDK 的不同模块（`dashscope-agent` vs `dashscope-rag`），并非矛盾，但需注意功能边界——知识库检索不可用于调用已发布的智能体应用，反之亦然。

## 关键参数

| 参数 | 说明 | 所属框架 | 示例值 |
|------|------|----------|--------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称（必须提前在控制台创建） | LlamaIndex / Spring AI Alibaba（RAG） | `"my_first_index"` |
| `model_name` | 生成模型名称（传给 `DashScope` 或 `DashScopeChatOptions`） | LlamaIndex / Spring AI Alibaba（RAG） | `"qwen-max"`, `"qwen-plus"` |
| `APP_ID` | 百炼智能体或工作流应用的唯一 ID | Spring AI Alibaba（智能体/工作流） | `"app-xxx"` |
| `WORKSPACE_ID` | 子业务空间 ID（非主账号空间时必需） | 全部框架 | `"ws-xxx"` |
| `similarity_top_k`, `similarity_cutoff`, `top_n` | 检索结果数量、相似度阈值、重排后返回数 | LlamaIndex | `5`, `0.4`, `1` |

## 使用方式

- **LlamaIndex**：  
  1. 使用 `DashScopeParse` 解析本地 `.txt`/`.docx`/`.pdf` 文件；  
  2. 调用 `DashScopeCloudIndex.from_documents()` 上传并构建云端知识库；  
  3. 通过 `index.as_query_engine()` 构建查询引擎，支持 `node_postprocessors`（如 `SimilarityPostprocessor`、`DashScopeRerank`）定制检索逻辑。

- **Spring AI Alibaba（智能体/工作流）**：  
  1. 在 `application.yml` 中配置 `spring.ai.dashscope.agent.app-id` 和 `api-key`；  
  2. 注入 `DashScopeAgent`，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）发起请求；  
  3. 响应中可提取 `docReferences` 和 `thoughts` 等结构化元数据。

- **Spring AI Alibaba（知识库 RAG）**：  
  1. 配置 `spring.ai.dashscope.api-key`（注意环境变量名是 `AI_DASHSCOPE_API_KEY`，非 `DASHSCOPE_API_KEY`）；  
  2. 使用 `DashScopeDocumentRetriever` 绑定知识库名；  
  3. 通过 `DocumentRetrievalAdvisor` 将检索结果注入 `ChatClient` 提示词模板，实现端到端 RAG。

## 限制和注意事项

- **知识库能力限制**：LlamaIndex 方案中，云端知识库使用默认智能切分与官方向量模型，**不支持自定义切分规则或嵌入模型** [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。若需完全控制切分与嵌入，请使用本地知识库方案。
- **框架功能隔离**：Spring AI Alibaba 的 `dashscope-agent` 模块与 `dashscope-rag` 模块互不兼容——前者只能调用已发布的应用，后者只能检索知识库，无法混合使用同一客户端同时触发应用执行与知识库检索。
- **环境变量命名不一致**：文档 2 推荐 `DASHSCOPE_API_KEY`，文档 3 使用 `AI_DASHSCOPE_API_KEY`；实际运行时需按所用模块对应配置，否则初始化失败。
- **依赖版本约束**：Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x；LlamaIndex 示例基于 Python 3.9+，且依赖 `llama-index-readers-dashscope` 等特定包版本，需严格匹配文档中 `requirements.txt` 或 `pom.xml` 的版本声明。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


