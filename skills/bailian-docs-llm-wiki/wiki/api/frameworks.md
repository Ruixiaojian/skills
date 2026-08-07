# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大框架，覆盖云端知识库托管、本地代码集成、流式/非流式调用等典型场景。所有集成均基于 DashScope API 统一底座，需提前配置 API Key 并满足对应框架的运行环境要求。

## 支持的模型/功能

- **LlamaIndex**：支持通过 `DashScopeCloudIndex` 构建云端 RAG 应用，依赖百炼托管的知识库（文档自动切分 + 官方向量模型），适用于私域问答、客服支持等场景；[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 提供完整端到端示例。
- **Spring AI Alibaba**：支持两类集成路径：
  - 调用已部署的**智能体应用或工作流应用**（需提供 `APP_ID`），适用于复杂逻辑编排与多步骤任务；
  - 直接**检索百炼知识库**（需提供 `INDEX_NAME`），适用于轻量级 RAG 场景，底层使用 `DashScopeDocumentRetriever`。
- 所有框架默认使用 `qwen-max` 模型生成回答，但允许显式指定其他千问系列模型（如 `qwen-plus`），详见 [文本生成-千问](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。

> **注意**：文档 2 明确限定 Spring AI Alibaba 仅支持集成“智能体应用”和“工作流应用”，而文档 3 描述的是“知识库检索”能力——二者属于不同调用路径（应用 ID vs 知识库名称），不构成矛盾，但需开发者根据实际需求选择对应集成方式。

## 关键参数

| 参数名 | 来源框架 | 说明 | 必填 |
|--------|----------|------|------|
| `DASHSCOPE_API_KEY` 或 `AI_DASHSCOPE_API_KEY` | LlamaIndex / Spring AI Alibaba | 百炼 API Key，推荐通过环境变量注入 | 是 |
| `APP_ID` | Spring AI Alibaba（应用调用） | 智能体/工作流应用 ID，从控制台获取 | 是（仅应用调用场景） |
| `WORKSPACE_ID` 或 `AI_DASHSCOPE_WORKSPACE_ID` | Spring AI Alibaba | 子业务空间 ID，仅当应用/知识库不在主账号空间时需配置 | 否（默认为主空间） |
| `INDEX_NAME` | Spring AI Alibaba（知识库检索） | 已创建的云端知识库名称，大小写敏感 | 是（仅知识库检索场景） |
| `model_name`（LlamaIndex） / `withModel(...)`（Spring AI） | 两者均支持 | 指定生成模型，如 `"qwen-max"`、`"qwen-plus"` | 否（有默认值） |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeParse` 解析本地 `.txt`/`.docx`/`.pdf` 文件并上传至百炼；  
  3. 通过 `DashScopeCloudIndex.from_documents()` 创建云端索引，再调用 `as_query_engine()` 构建 RAG 引擎；  
  4. 可配置 `similarity_top_k`、`similarity_cutoff`、`DashScopeRerank` 等后处理器优化检索质量。详细步骤见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

- **Spring AI Alibaba 集成**：  
  - **应用调用**：添加 `spring-ai-alibaba-starter-dashscope` 依赖，配置 `spring.ai.dashscope.agent.app-id`，使用 `DashScopeAgent` 实例调用；支持非流式（`agent.call()`）和流式（`agent.stream()`）两种模式。  
  - **知识库检索**：添加相同 starter 依赖，配置 `spring.ai.dashscope.api-key`，在 Service 中初始化 `DashScopeDocumentRetriever` 并注入 `ChatClient`，利用 `DocumentRetrievalAdvisor` 自动拼接上下文。该方式无需预先创建应用，直接对接知识库，参考 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 2 与文档 3 的依赖版本存在差异——文档 2 使用 `spring-ai-alibaba-starter-dashscope:1.0.0.2`，而文档 3 示例未声明版本号。建议以 [Spring AI Alibaba 官方仓库](https://github.com/spring-ai-alibaba/spring-ai-alibaba-examples) 的最新稳定版为准，避免兼容性问题。

## 限制和注意事项

- **LlamaIndex 云端知识库限制**：不支持自定义文档切分逻辑或嵌入模型，所有解析与向量化均由百炼后台完成；若需完全控制切分与嵌入，请改用本地知识库方案（参见 [基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)）。
- **Spring AI Alibaba 应用调用限制**：仅支持智能体应用和工作流应用，**不支持直接调用基础大模型 API（如 `qwen-max` 的 raw chat 接口）**；知识库检索路径亦不支持自定义嵌入或重排序模型，仅提供 `gte-rerank` 等内置重排器。
- **环境一致性**：LlamaIndex 示例要求 Python 3.9+；Spring AI Alibaba 要求 JDK 17+ 且 Spring Boot 3.x，JDK 8 或 Spring Boot 2.x 不兼容。
- **计费说明**：框架本身免费，但所有模型调用（含 RAG 中的 LLM 生成、智能体执行、知识库检索后的回答生成）均按 [模型推理计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk) 单独计费。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


