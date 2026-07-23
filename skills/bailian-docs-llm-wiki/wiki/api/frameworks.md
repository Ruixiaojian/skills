# frameworks

百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、应用编排）的深度对接。所有集成均基于百炼统一的 DashScope API 层，需配置有效的 API Key 并遵循对应框架的初始化与调用规范。

## 支持的模型/功能

- **RAG 场景**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 构建云端托管的 RAG 应用，依赖百炼默认的文档解析（`DASHSCOPE_DOCMIND`）、向量化与检索能力；不支持自定义切分器或嵌入模型。
- **智能体与工作流应用集成**：支持通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 调用已发布的**智能体应用**或**工作流应用**，支持非流式与流式响应，并可获取 `docReferences` 和 `thoughts` 等结构化输出。
- **知识库直接检索**：支持通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 实现对百炼知识库的端到端 RAG 检索，底层使用 `DashScopeDocumentRetriever`，默认调用 `qwen-max` 模型生成答案，且允许通过 `DashScopeChatOptions` 显式切换模型（如 `qwen-plus`）。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 的 `DashScopeDocumentRetriever` 也未提供嵌入模型配置入口；但文档 2 中 `DashScopeAgent` 的调用逻辑未涉及嵌入层，三者在嵌入能力上保持一致限制。无矛盾。

## 关键参数

| 参数名 | 说明 | 来源框架 | 示例值 | 是否必需 |
|--------|------|----------|--------|----------|
| `DASHSCOPE_API_KEY` | 百炼平台 API 密钥 | LlamaIndex / Spring AI Alibaba | `sk-xxx` | 是 |
| `APP_ID` | 智能体或工作流应用 ID | Spring AI Alibaba（应用集成） | `app-abc123` | 是（仅用于应用调用） |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID | Spring AI Alibaba | `ws-xyz789` | 否（仅子空间场景需配置） |
| `INDEX_NAME` | 云端知识库名称 | LlamaIndex / Spring AI Alibaba（知识库检索） | `"my_first_index"` | 是（知识库场景） |
| `model_name` / `withModel()` | 生成模型标识符 | LlamaIndex（`Settings.llm`） / Spring AI Alibaba（`DashScopeChatOptions`） | `"qwen-max"`, `"qwen-plus"` | 是（默认值存在，但建议显式指定） |
| `similarity_top_k`, `similarity_cutoff`, `top_n` | 检索与重排参数 | LlamaIndex | `5`, `0.4`, `1` | 否（有合理默认值，但推荐按需调整） |

> **注意**：文档 2 使用环境变量名 `DASHSCOPE_API_KEY`，而文档 3 使用 `AI_DASHSCOPE_API_KEY`；两者均为有效配置方式，但**不可混用**。实际部署时应统一选用其一，并确保 `application.yml` 中引用的变量名与环境变量名严格一致。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）优化检索质量；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.agent.app-id` 和 `api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法，传入 `Prompt` 和 `DashScopeAgentOptions`（含 `appId`）。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 添加相同 starter 依赖；  
  2. 配置 `spring.ai.dashscope.api-key`（注意变量名差异）；  
  3. 构建 `DashScopeDocumentRetriever` 并注入 `ChatClient`，通过 `DocumentRetrievalAdvisor` 自动拼接上下文；  
  4. 调用 `chatClient.prompt().user(...).stream().chatResponse()` 触发 RAG 流程。

## 限制和注意事项

- **知识库部署模式限制**：LlamaIndex 方案仅支持**云端知识库**，不支持本地部署知识库所需的自定义切分与嵌入模型 —— 详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **应用类型限制**：Spring AI Alibaba 的 `DashScopeAgent` **仅支持智能体应用和工作流应用**，不支持直接调用基础模型 API 或知识库原生接口 —— 详见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **环境变量命名不一致**：文档 2 推荐 `DASHSCOPE_API_KEY`，文档 3 推荐 `AI_DASHSCOPE_API_KEY`；若同时引入两类集成（如既调用应用又检索知识库），需在 `application.yml` 中分别映射或统一环境变量名，否则将导致部分组件初始化失败。
- **模型选择范围**：所有框架均依赖百炼平台公开的模型列表（如 `qwen-max`, `qwen-plus`, `gte-rerank`），不支持用户私有微调模型接入；`gte-rerank` 仅可用于重排（文档 1），不可作为主生成模型。
- **计费说明**：框架本身免费，但所有模型调用（包括 RAG 中的生成、重排、检索）均按百炼 [计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk) 单独计费。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


