# frameworks

阿里云百炼平台通过标准化的 SDK 和适配器，支持主流 AI 开发框架（如 LlamaIndex 和 Spring AI Alibaba）快速集成其大模型服务、知识库与应用能力。开发者可基于熟悉的技术栈，复用已有工程结构，对接百炼的云端推理、RAG 检索和智能体/工作流执行能力，无需从零实现底层通信与协议适配。

## 支持的模型与功能

- **RAG 场景**：支持通过 LlamaIndex 构建端到端[检索增强生成](../concepts/rag.md)应用，依赖百炼云端知识库（文档上传、切分、向量化、检索）与托管大模型（如 `qwen-max`、`qwen-plus`）协同完成问答；详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **智能体/工作流调用**：Spring AI Alibaba 提供 `DashScopeAgent` 组件，仅支持调用已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，不支持直接调用基础模型或自定义链式逻辑。
- **知识库直检**：Spring AI Alibaba 同时提供 `DashScopeDocumentRetriever`，可绕过应用层，直接对已创建的百炼知识库（按 `index_name`）执行语义检索，并将结果注入 `ChatClient` 生成回答；该能力独立于应用发布状态，见 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 2 声明 Spring AI Alibaba “仅支持集成智能体应用和工作流应用”，而文档 3 明确提供了对知识库的直接检索能力（`DashScopeDocumentRetriever`）。二者功能正交——前者调用封装好的业务逻辑单元，后者对接底层检索能力。不存在矛盾，但需注意适用场景差异。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `model_name` | 指定 LlamaIndex 中 `Settings.llm` 所用的大模型 | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | Spring AI Alibaba 调用智能体/工作流应用时必需的应用 ID | `app-xxxxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` | Spring AI Alibaba 推荐使用的 API Key 环境变量名（文档 3），区别于文档 2 的 `DASHSCOPE_API_KEY` | `sk-xxx` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `INDEX_NAME` | Spring AI Alibaba `DashScopeDocumentRetriever` 所需的知识库名称 | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间场景下必需，但两文档使用不同环境变量名（文档 2 用 `WORKSPACE_ID`，文档 3 用 `AI_DASHSCOPE_WORKSPACE_ID`） | `ws-xxxxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 和 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

> **注意**：API Key 和 Workspace ID 的环境变量命名在文档 2 与文档 3 中不一致（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`；`WORKSPACE_ID` vs `AI_DASHSCOPE_WORKSPACE_ID`）。实际使用时请以 `application.yml` 中配置的占位符为准，并确保环境变量名与之匹配。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`node_postprocessors`（如 `DashScopeRerank`）等参数；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成**：  
  - **调用应用**：引入 `spring-ai-alibaba-starter-dashscope`，配置 `APP_ID` 和 `DASHSCOPE_API_KEY`，注入 `DashScopeAgent` 实例，调用 `agent.call()` 或 `agent.stream()`。  
  - **检索知识库**：引入相同 starter，配置 `AI_DASHSCOPE_API_KEY`，构造 `DashScopeDocumentRetriever` 并绑定至 `ChatClient` 的 `DocumentRetrievalAdvisor`，后续通过 `chatClient.prompt().user(...).stream()` 触发检索+生成。

## 限制和注意事项

- **LlamaIndex 方案限制**：云端知识库强制使用百炼默认的文档切分策略与官方向量模型，不支持自定义切分逻辑或嵌入模型；若需本地控制，请参考其他方案（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中的说明）。
- **Spring AI Alibaba 应用调用限制**：仅支持已发布（Published）状态的智能体或工作流应用；草稿态应用不可调用。
- **知识库检索限制**：`DashScopeDocumentRetriever` 仅支持检索已成功构建且状态为“可用”的知识库；知识库名称（`INDEX_NAME`）区分大小写，且必须与控制台中显示的名称完全一致。
- **依赖版本约束**：LlamaIndex 需配合 `llama-index-readers-dashscope` 特定版本；Spring AI Alibaba 要求 Spring Boot 3.x + JDK 17+，且 starter 版本需与 Spring AI 主版本兼容（如 `spring-ai-alibaba-starter-dashscope:1.0.0.2` 对应 Spring AI 1.0.x）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


