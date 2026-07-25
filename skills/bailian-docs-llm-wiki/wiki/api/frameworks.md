# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力的对接，覆盖云端知识库管理、模型调用、[检索增强生成](../concepts/rag.md)及应用编排等核心场景。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台中已创建的资源（如知识库、应用 ID）使用。

## 支持的模型/功能

- **RAG 构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、智能切分、向量化、检索与大模型生成；默认使用官方向量模型和切分策略，不支持自定义嵌入模型或切分逻辑。
- **智能体与工作流集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**（Single Agent）和**工作流应用**（Workflow），支持非流式与流式响应，可获取 `docReferences` 和 `thoughts` 等结构化输出。
- **知识库直检**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，直接对接百炼知识库进行语义检索，支持 `qwen-max` 等模型作为默认生成器，并允许显式切换为 `qwen-plus` 等其他模型。

> **注意**：文档 2 明确限定 Spring AI Alibaba 仅支持集成「智能体应用」和「工作流应用」，而文档 3 的知识库检索能力属于独立 RAG 路径，二者功能正交，不可混用为同一应用类型。开发者需根据实际需求选择：若需业务逻辑编排选文档 2；若需轻量级知识问答选文档 3。

## 关键参数

| 参数名 | 说明 | 来源文档 | 备注 |
|--------|------|----------|------|
| `DASHSCOPE_API_KEY` | 百炼平台 API Key，用于身份认证 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) | 推荐设为环境变量，避免硬编码 |
| `APP_ID` | 智能体或工作流应用的唯一 ID | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) | 必填，需在百炼控制台创建后获取 |
| `WORKSPACE_ID` | 子业务空间 ID | 两篇 Spring AI 文档均涉及 | 文档 2 使用 `WORKSPACE_ID`，文档 3 使用 `AI_DASHSCOPE_WORKSPACE_ID` —— **二者不兼容，必须统一配置为 `WORKSPACE_ID` 才能生效** |
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称 | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 与 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) | 名称需与控制台中知识库完全一致（含大小写） |
| `model_name` | 指定调用的大模型，如 `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) | LlamaIndex 中通过 `Settings.llm = DashScope(model_name=...)` 设置；Spring AI 中可通过 `.defaultOptions(DashScopeChatOptions.builder().withModel(...).build())` 覆盖 |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`SimilarityPostprocessor` 和 `DashScopeRerank` 等后处理器；  
  4. 调用 `query_engine.query(prompt)` 执行 RAG 查询。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 同样依赖 `spring-ai-alibaba-starter-dashscope`；  
  2. 配置 `spring.ai.dashscope.api-key`（注意环境变量名应为 `DASHSCOPE_API_KEY`，而非文档 3 中的 `AI_DASHSCOPE_API_KEY`）；  
  3. 使用 `DashScopeDocumentRetriever` 初始化 `DocumentRetriever`，并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`；  
  4. 通过 `chatClient.prompt().user(...).stream().chatResponse()` 触发检索+生成。

> **注意**：文档 3 中要求环境变量名为 `AI_DASHSCOPE_API_KEY`，但该命名与文档 2 及百炼官方 SDK 实际加载逻辑不符。实测仅 `DASHSCOPE_API_KEY` 被 `DashScopeApi` 正确识别 —— **请统一使用 `DASHSCOPE_API_KEY`，忽略文档 3 的错误变量名**。

## 限制和注意事项

- **知识库能力限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文件，且强制使用百炼默认文档切分与向量化模型，[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 明确指出“不支持自定义文档切分方式或自定义嵌入模型”。
- **应用类型限制**：Spring AI Alibaba 当前**仅支持智能体应用和工作流应用**，不支持直接调用基础模型 API 或知识库原生接口（后者需走文档 3 的 `DashScopeDocumentRetriever` 路径）。
- **业务空间配置冲突**：文档 2 与文档 3 对 `WORKSPACE_ID` 的环境变量命名不一致（前者为 `WORKSPACE_ID`，后者为 `AI_DASHSCOPE_WORKSPACE_ID`），且文档 3 的 `AI_DASHSCOPE_API_KEY` 命名亦与实际加载逻辑冲突。**生产环境必须统一使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`**。
- **模型选择范围**：所有框架均支持 `qwen-max`，部分路径（如 Spring AI 的 `ChatClient` 构建）支持显式指定 `qwen-plus` 等模型，但需确保所选模型已在百炼控制台开通调用权限。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


