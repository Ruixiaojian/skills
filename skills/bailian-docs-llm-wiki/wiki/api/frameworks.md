# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、[知识库](../concepts/knowledge-base.md)检索系统及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼服务（包括云端[知识库](../concepts/knowledge-base.md)、向量检索、大模型推理、智能体编排）的深度对接。所有集成均基于百炼统一的 DashScope API 层，无需直接调用底层 HTTP 接口。

## 支持的模型/功能

- **RAG 场景**：支持通过 LlamaIndex 构建端到端云端 RAG 应用，利用百炼托管的[知识库](../concepts/knowledge-base.md)、默认文档切分（DocMind）、官方向量模型（如 `gte-rerank`）及重排能力；也支持通过 Spring AI Alibaba 的 `DashScopeDocumentRetriever` 实现 Java 生态下的知识库检索。
- **大模型应用集成**：仅支持集成百炼平台创建的**智能体应用**（Single Agent）和**工作流应用**（Workflow），不支持直接集成基础大模型（如 `qwen-max`）或自定义模型服务 [通过Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **模型选择**：
  - LlamaIndex 场景中，`Settings.llm = DashScope(model_name="qwen-max")` 可显式指定生成模型，支持 `qwen-max`、`qwen-plus` 等 [文本生成-千问](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u) 系列模型；
  - Spring AI Alibaba 场景中，智能体/工作流应用的模型由百炼应用内部配置决定，SDK 不暴露模型切换参数；知识库检索默认使用 `qwen-max` 生成回答 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 1 中称“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及嵌入模型可配置性。经交叉验证，百炼云端知识库当前**仅支持官方 DocMind 解析与内置向量模型**，LlamaIndex 的 `DashScopeCloudIndex` 和 Spring AI Alibaba 的 `DashScopeDocumentRetriever` 均无法绕过该限制 —— 此为平台级约束，非 SDK 限制。

## 关键参数

| 参数 | 作用 | 示例值 | 来源 |
|------|------|--------|------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称（需提前在控制台创建） | `"my_first_index"` / `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` (LlamaIndex) | 指定生成回答的大模型 | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | 百炼智能体/工作流应用 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key 环境变量名 | `sk-xxx` | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY` —— **两者均有效，但推荐统一使用 `DASHSCOPE_API_KEY`**，因其与百炼官方 SDK 一致 |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID 环境变量名 | `"ws-xxx"` | 文档 2 使用 `AI_DASHSCOPE_WORKSPACE_ID`，文档 3 使用 `WORKSPACE_ID` —— **两者均有效，但推荐统一使用 `WORKSPACE_ID`** |

## 使用方式

- **LlamaIndex 集成**：
  1. 安装 `llama-index-llms-dashscope`、`llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；
  2. 使用 `DashScopeCloudIndex.from_documents()` 上传本地文件并创建云端知识库；
  3. 调用 `index.as_query_engine()` 构建检索引擎，支持 `similarity_top_k`、`similarity_cutoff`、`node_postprocessors`（如 `DashScopeRerank`）等参数定制检索逻辑。

- **Spring AI Alibaba 集成**：
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；
  2. 配置 `application.yml` 中的 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`；
  3. 知识库检索：注入 `DashScopeDocumentRetriever` 并绑定至 `ChatClient` 的 `DocumentRetrievalAdvisor`；
  4. 大模型应用调用：使用 `DashScopeAgent` 进行同步/流式调用，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。

## 限制和注意事项

- **知识库部署模式**：仅支持**云端知识库**。LlamaIndex 方案明确不支持本地知识库部署（需另参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)）；Spring AI Alibaba 同样仅对接百炼控制台创建的云端知识库。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文档上传解析；Spring AI Alibaba 未明确列出支持格式，但实际依赖百炼知识库的解析能力，故同样受限。
- **环境要求**：
  - LlamaIndex：Python 3.9+；
  - Spring AI Alibaba：JDK 17+、Spring Boot 3.x。
- **API Key 配置差异**：文档 2 与文档 3 对 API Key 和 Workspace ID 的环境变量命名不一致，虽兼容，但建议按文档 3 的 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID` 统一配置，避免混淆。
- **计费说明**：框架本身免费，但调用百炼服务（知识库检索、模型推理、智能体执行）均按实际用量计费，详情见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


