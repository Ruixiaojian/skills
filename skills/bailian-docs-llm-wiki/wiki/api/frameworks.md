# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的原生集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大框架，覆盖云端知识库托管、本地代码集成、流式/非流式调用等典型场景。所有集成均基于 DashScope SDK 封装，统一使用 `DASHSCOPE_API_KEY`（或 `AI_DASHSCOPE_API_KEY`）进行身份认证。

## 支持的模型与功能

- **LlamaIndex**：支持通过 `DashScopeCloudIndex` 构建云端 RAG 应用，内置文档解析（`.txt`/`.docx`/`.pdf`）、向量索引、相似度检索、重排（`gte-rerank`）及 `qwen-max` 等模型的端到端编排。详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba**：支持两类核心集成：
  - **应用调用**：对接已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，支持非流式与流式响应；
  - **知识库检索**：通过 `DashScopeDocumentRetriever` 直接检索云端知识库，自动注入上下文并调用大模型生成回答（默认 `qwen-max`，可配置为 `qwen-plus` 等）。
- > **注意**：文档 2 明确限定 Spring AI Alibaba *仅支持集成智能体应用和工作流应用*；而文档 3 则完整描述了其对知识库的直接检索能力。二者功能不冲突，但需区分“应用调用”与“知识库检索”两种模式——前者面向已部署的业务逻辑封装，后者面向原始知识片段召回。

## 关键参数

| 参数 | 说明 | 来源/示例 |
|------|------|-----------|
| `APP_ID` | 智能体或工作流应用的唯一 ID，必需 | 文档 2 中 `spring.ai.dashscope.agent.app-id` |
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼平台 API 密钥，推荐设为环境变量 | 文档 2 使用 `DASHSCOPE_API_KEY`；文档 3 使用 `AI_DASHSCOPE_API_KEY` —— **二者等效，但命名不一致，建议统一采用 `DASHSCOPE_API_KEY` 避免混淆** |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，仅在非主账号空间下创建资源时必需 | 同上，命名差异同理，应统一为 `WORKSPACE_ID` |
| `INDEX_NAME` | 云端知识库名称，用于 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 初始化 | 文档 1 中 `"my_first_index"`；文档 3 中 `"测试知识库"` |
| `model_name` | 大模型标识符，如 `"qwen-max"`、`"qwen-plus"` | 文档 1 中 `Settings.llm = DashScope(model_name="qwen-max")`；文档 3 注释中明确支持切换 |

## 使用方式

### LlamaIndex 集成
1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；
2. 使用 `DashScopeParse` 解析本地文件，调用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；
3. 通过 `index.as_query_engine()` 创建检索引擎，配置 `similarity_top_k`、`SimilarityPostprocessor`、`DashScopeRerank` 等后处理器；
4. 调用 `query_engine.query()` 执行 RAG 查询。完整流程见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

### Spring AI Alibaba 集成
- **应用调用**：引入 `spring-ai-alibaba-starter-dashscope`，配置 `APP_ID` 和 `API_KEY`，注入 `DashScopeAgent` 实例，调用 `.call()`（非流式）或 `.stream()`（流式）；
- **知识库检索**：引入相同 starter，配置 `API_KEY`，使用 `DashScopeDocumentRetriever` 绑定 `INDEX_NAME`，结合 `ChatClient` 与 `DocumentRetrievalAdvisor` 实现自动上下文注入与生成。参考 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **LlamaIndex 云端模式限制**：不支持自定义文档切分策略与嵌入模型，仅使用百炼默认的智能切分与官方向量模型；若需本地控制，请参考 [基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval) —— 此限制在 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中已明确声明。
- **Spring AI Alibaba 版本兼容性**：要求 JDK 17+、Spring Boot 3.x，且 starter 版本需匹配（文档 2 指定 `1.0.0.2`）；文档 3 示例未显式声明版本，但实际依赖一致。
- **环境变量命名不一致**：文档 2 与文档 3 对 API Key 和 Workspace ID 的环境变量名定义不同（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），**建议以文档 2 的命名为准，并在工程中统一配置**，避免运行时缺失。
- **知识库与应用隔离**：LlamaIndex 方案操作的是“知识库”实体（`DashScopeCloudIndex`），Spring AI Alibaba 的应用调用方案操作的是“应用”实体（`DashScopeAgent`），二者底层资源独立，不可混用索引或会话状态。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


