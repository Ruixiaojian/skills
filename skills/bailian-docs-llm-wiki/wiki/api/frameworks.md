# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速将大模型能力嵌入现有技术栈。当前重点支持 LlamaIndex 和 Spring AI Alibaba 两大生态，分别面向 RAG 应用构建和 Java 企业级集成场景。所有集成均基于百炼统一的 API 网关与模型服务层，无需自行管理模型部署与推理基础设施。

## 支持的模型/功能

- **LlamaIndex 集成**：支持通过 `DashScopeCloudIndex` 构建云端托管的 RAG 应用，自动完成文档解析（`.txt`/`.docx`/`.pdf`）、向量化（默认官方向量模型）与[检索增强生成](../concepts/rag.md)全流程；支持自定义 `similarity_top_k`、`similarity_cutoff` 及重排模型（如 `gte-rerank`）[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **Spring AI Alibaba 集成**：提供两类能力：  
  - **应用调用**：支持流式/非流式调用已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)或[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，需配置 `APP_ID` [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；  
  - **知识库检索**：通过 `DashScopeDocumentRetriever` 直接检索百炼云端知识库，支持提示词模板注入与模型切换（如 `qwen-plus`），但**不支持本地知识库或自定义嵌入模型** [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 未提及该限制，但其示例代码中 `DashScopeDocumentRetriever` 仅接受 `indexName` 参数且无嵌入模型配置入口，二者实际能力一致。文档 3 中“检索默认业务空间的知识库时无需配置 `workspace-id`”与文档 2 中“子业务空间需配置 `WORKSPACE_ID`”表述一致，无矛盾。

## 关键参数

| 参数名 | 说明 | 来源框架 | 示例值 | 必填 |
|--------|------|----------|--------|------|
| `DASHSCOPE_API_KEY` | 百炼平台 API Key，用于身份认证 | LlamaIndex / Spring AI Alibaba | `sk-xxx` | 是 |
| `APP_ID` | 智能体/工作流应用 ID（仅 Spring AI Alibaba 应用调用场景） | Spring AI Alibaba | `app-abc123` | 是（应用调用） |
| `INDEX_NAME` | 云端知识库名称（仅 Spring AI Alibaba 知识库检索场景） | Spring AI Alibaba | `测试知识库` | 是（知识库检索） |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID（可选） | Spring AI Alibaba | `ws-xyz789` | 否（仅子空间需配） |
| `model_name` | 生成模型名称（LlamaIndex 中通过 `Settings.llm = DashScope(model_name=...)` 设置） | LlamaIndex | `"qwen-max"` | 是 |

## 使用方式

- **LlamaIndex**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeParse` 解析本地文件，`DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）优化检索结果。  

- **Spring AI Alibaba**：  
  1. 在 `pom.xml` 中引入 `spring-ai-alibaba-starter-dashscope`（v1.0.0.2+）；  
  2. `application.yml` 中配置 `spring.ai.dashscope.api-key` 及 `app-id` 或 `index-name`；  
  3. 应用调用：注入 `DashScopeAgent`，调用 `.call()` 或 `.stream()`；知识库检索：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并集成至 `ChatClient` 的 `DocumentRetrievalAdvisor`。  

## 限制和注意事项

- **知识库能力限制**：所有框架均**仅支持百炼云端知识库**，不支持本地部署知识库或自定义嵌入模型；文档切分逻辑由百炼平台统一处理，开发者无法干预 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **模型绑定约束**：LlamaIndex 中 `DashScopeCloudIndex` 默认使用 `qwen-max`，但可通过 `Settings.llm` 覆盖；Spring AI Alibaba 知识库检索默认也使用 `qwen-max`，可通过 `DashScopeChatOptions.builder().withModel(...)` 切换，但**不支持指定嵌入模型**。  
- **环境兼容性**：Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x；LlamaIndex 示例基于 Python 3.9+，需确保 `pip install -r requirements.txt` 安装完整依赖（含 `dashscope` SDK）。  
- **计费说明**：框架本身免费，但调用百炼模型（如 `qwen-max`）或应用服务时按实际调用量计费，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


