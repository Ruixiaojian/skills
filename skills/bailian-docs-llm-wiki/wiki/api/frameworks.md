# frameworks

百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、应用编排）的深度对接。所有集成均基于百炼统一的 DashScope API 层，需配置有效的 API Key 并遵循对应框架的初始化与调用规范。

## 支持的模型/功能

- **RAG 场景**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 构建云端知识库驱动的问答系统，使用默认文档切分与官方向量模型（不支持自定义切分或嵌入模型）。
- **智能体与工作流应用**：支持通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 调用已部署的**智能体应用**和**工作流应用**（不支持直接调用基础模型或知识库原生接口）。
- **知识库原生检索**：支持通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 直接对接百炼知识库，实现语义检索 + 大模型生成的端到端 RAG 流程，底层自动使用 `qwen-max`（可覆盖为 `qwen-plus` 等）。

> **注意**：文档 2 明确限定 Spring AI Alibaba 仅支持集成“智能体应用”和“工作流应用”，而文档 3 则展示了对“知识库”的直接检索能力。二者功能层级不同：文档 2 调用的是封装好的应用逻辑（含工具调用、规划等），文档 3 调用的是知识库检索原语。开发者需根据场景选择——若需复用已有应用逻辑，用文档 2；若需完全控制 RAG 流程（如自定义 [prompt](../guides/prompt.md)、后处理），用文档 3。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API Key，用于身份认证 | `sk-xxx` | 文档 2、3 均要求配置，但环境变量名不一致（见下条） |
| `APP_ID` | 智能体/工作流应用 ID，仅文档 2 所需 | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，按需配置 | `ws-xxx` | 文档 2 使用 `WORKSPACE_ID`，文档 3 使用 `AI_DASHSCOPE_WORKSPACE_ID` —— **注意变量名差异，需按对应文档配置** |
| `model_name` (LlamaIndex) / `withModel(...)` (Spring AI) | 指定生成模型 | `"qwen-max"`、`"qwen-plus"` | 文档 1 中 `Settings.llm = DashScope(model_name="qwen-max")`；文档 3 注释中给出覆盖方式 |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index`, `llama-index-readers-dashscope`, `llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeCloudIndex.from_documents(...)` 构建云端知识库；  
  3. 通过 `index.as_query_engine(...)` 创建查询引擎，支持 `similarity_top_k`、`similarity_cutoff`、`DashScopeRerank` 等后处理；  
  4. 调用 `query_engine.query(prompt)` 获取结构化响应（含 `source_nodes`）。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 使用 `DashScopeAgent` 实例调用 `agent.call()`（非流式）或 `agent.stream()`（流式）。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 同上添加依赖并配置 `api-key`；  
  2. 使用 `DashScopeDocumentRetriever` 指定 `indexName`；  
  3. 将其注入 `DocumentRetrievalAdvisor`，绑定至 `ChatClient`；  
  4. 调用 `chatClient.prompt().user(...).stream().chatResponse()` 触发 RAG 流程。

## 限制和注意事项

- **知识库能力限制**：LlamaIndex 方案中，云端知识库**不支持自定义文档切分方式或自定义嵌入模型**，仅限百炼默认处理流程 —— 此限制在 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中明确声明。
- **环境变量命名冲突**：文档 2 推荐 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`，文档 3 推荐 `AI_DASHSCOPE_API_KEY` 和 `AI_DASHSCOPE_WORKSPACE_ID`。**必须严格按所选文档的变量名配置，否则初始化失败**。
- **应用类型限制**：Spring AI Alibaba 的 `DashScopeAgent` **仅支持智能体应用和工作流应用**，不支持直接调用基础模型 API 或知识库管理 API —— 该约束出自 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **Java 版本要求**：Spring AI Alibaba 集成要求 **JDK 17+ 且 Spring Boot 3.x**，不兼容 Spring Boot 2.x 或 JDK < 17 —— 此要求在文档 2 和文档 3 的“前期准备”/“适用范围”中一致强调。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


