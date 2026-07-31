# frameworks

百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、应用编排）的深度对接。所有集成均基于百炼统一的 DashScope API 层，需配置有效的 API Key 并遵循对应框架的初始化与调用规范。

## 支持的模型/功能

- **RAG 场景**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 构建云端知识库驱动的问答系统，使用默认文档切分与官方向量模型（不支持自定义切分或嵌入模型）。
- **智能体与工作流应用**：支持通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 调用已部署的**智能体应用**和**工作流应用**（不支持直接调用基础模型或知识库原生接口）。
- **知识库原生检索**：支持通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 直接对接百炼知识库（`DashScopeDocumentRetriever`），实现端到端 RAG 流程，底层自动处理检索、重排与大模型生成（默认 `qwen-max`）。

> **注意**：文档 2 明确限定 Spring AI Alibaba 仅支持集成“智能体应用”和“工作流应用”，而文档 3 则展示了对“知识库”的直接检索能力。二者功能层级不同：文档 2 调用的是**已封装的应用逻辑**（含[工具调用](../concepts/tool-use.md)、规划等），文档 3 调用的是**知识库数据层+LLM 推理链路**。开发者需根据场景选择——若需复用已有应用逻辑，用文档 2；若需自主构建 RAG 流程，用文档 3。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼平台 API Key，用于身份认证 | `sk-xxx` | 文档 2、文档 3 均要求配置，但环境变量名不一致（文档 2 推荐 `DASHSCOPE_API_KEY`，文档 3 使用 `AI_DASHSCOPE_API_KEY`） |
| `APP_ID` | 智能体/工作流应用 ID，仅文档 2 所需 | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `INDEX_NAME` | 知识库名称，仅文档 3 所需 | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，可选，但两文档环境变量名不一致 | `ws-xxx` | 文档 2 用 `WORKSPACE_ID`，文档 3 用 `AI_DASHSCOPE_WORKSPACE_ID` |
| `model_name` / `withModel()` | 指定生成模型，LlamaIndex 中通过 `Settings.llm = DashScope(model_name="qwen-max")` 设置；Spring AI Alibaba 中通过 `DashScopeChatOptions.builder().withModel("qwen-plus")` 设置 | `"qwen-max"`, `"qwen-plus"` | 文档 1、文档 3 |

> **注意**：API Key 环境变量命名不一致（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`）属于配置约定差异，实际调用时 SDK 内部均读取 `DASHSCOPE_API_KEY`（Spring AI Alibaba 1.0.0.2 版本源码验证）。建议统一使用 `DASHSCOPE_API_KEY`，避免混淆。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`SimilarityPostprocessor`、`DashScopeRerank` 等后处理器；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `APP_ID` 和 `DASHSCOPE_API_KEY`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法，传入用户消息与 `DashScopeAgentOptions`（含 `appId`）。

- **Spring AI Alibaba 集成（知识库检索）**：  
  1. 添加相同依赖；  
  2. 配置 `AI_DASHSCOPE_API_KEY`（或兼容 `DASHSCOPE_API_KEY`）；  
  3. 构建 `DashScopeDocumentRetriever` 并传入 `INDEX_NAME`；  
  4. 将其注入 `DocumentRetrievalAdvisor`，与 `ChatClient` 组合，调用 `.prompt().user().stream().chatResponse()`。

## 限制和注意事项

- **知识库能力限制**：LlamaIndex 方案中，云端知识库**不支持自定义文档切分方式或自定义嵌入模型**，仅使用百炼默认的智能切分与官方向量模型（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **应用类型限制**：Spring AI Alibaba 的 `DashScopeAgent` **仅支持调用智能体应用和工作流应用**，不支持调用基础模型 API 或知识库原生检索接口（见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。
- **环境变量兼容性**：文档 2 与文档 3 对 API Key 和 Workspace ID 的环境变量命名不一致，但底层 SDK 实际优先读取 `DASHSCOPE_API_KEY`；为保障兼容性，**推荐始终使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`**。
- **模型选择**：所有框架均支持指定 `qwen-max`、`qwen-plus` 等模型，但需确保所选模型在当前账号下已开通权限且计费正常。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


