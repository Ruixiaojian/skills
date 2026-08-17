# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前重点支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖 Python 和 Java 技术栈，所有集成均基于百炼统一的 API Key 认证与云端服务能力（如知识库管理、向量检索、模型推理）。开发者无需自行部署基础设施，可聚焦于业务逻辑与提示工程。

## 支持的模型/功能

- **RAG 构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、智能切分、默认向量嵌入（`docmind`）、相似性检索与重排（`gte-rerank`），并支持 `qwen-max`、`qwen-plus` 等千问系列模型生成回答。
- **知识库检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，支持在 Spring Boot 应用中直接检索已创建的百炼知识库，自动注入上下文并调用默认 `qwen-max` 模型生成响应。
- **大模型应用集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用百炼平台创建的**智能体应用**和**工作流应用**，支持非流式与 SSE 流式响应，并可获取思考链（`thoughts`）与文档引用（`docReferences`）等结构化输出。

> **注意**：文档 1 明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制；但三者均未提供替代方案（如本地嵌入模型接入路径），因此该限制为当前事实约束，开发者需按此设计系统边界。

## 关键参数

| 参数名 | 作用 | 可选值/说明 | 来源 |
|--------|------|-------------|------|
| `model_name` (LlamaIndex) | 指定生成回答所用的大模型 | `"qwen-max"`, `"qwen-plus"` 等，详见[文本生成-千问](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u) | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `similarity_top_k` / `similarity_cutoff` / `top_n` | 控制检索结果数量、相似度阈值与重排后返回数 | 示例中设为 `5` / `0.4` / `1`，需根据业务效果调优 | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key 环境变量名 | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY` —— **二者不兼容，必须按对应框架要求配置** | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 和 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `APP_ID` | 百炼大模型应用 ID（仅用于智能体/工作流集成） | 必须提前在控制台创建并获取 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `workspace-id` / `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID 环境变量名 | 文档 2 使用 `AI_DASHSCOPE_WORKSPACE_ID`，文档 3 使用 `WORKSPACE_ID` —— **命名不一致，需严格匹配对应 SDK 版本** | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 和 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |

## 使用方式

- **LlamaIndex（Python）**  
  1. 安装依赖：`pip install -r requirements.txt`（含 `llama-index`, `llama-index-readers-dashscope`, `llama-index-indices-managed-dashscope`）；  
  2. 执行 `create_cloud_index.py` 上传本地 `.txt`/`.docx`/`.pdf` 文件并构建云端知识库；  
  3. 执行 `rag.py` 初始化 `DashScopeCloudIndex`，配置 `query_engine` 并启动交互式 RAG 应用。

- **Spring AI Alibaba（Java）**  
  - **知识库检索**：引入 `spring-ai-alibaba-starter-dashscope`，配置 `application.yml` 中 `spring.ai.dashscope.api-key` 与 `INDEX_NAME`，注入 `DashScopeDocumentRetriever` 并通过 `DocumentRetrievalAdvisor` 绑定至 `ChatClient`。  
  - **大模型应用调用**：同上依赖，配置 `spring.ai.dashscope.agent.app-id`，使用 `DashScopeAgent` 实例调用 `call()`（非流式）或 `stream()`（SSE 流式）方法。

## 限制和注意事项

- **知识库能力限制**：所有框架均依赖百炼平台托管的知识库，当前不支持自定义嵌入模型或文档切分策略（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）；若需完全可控的本地 RAG 流程，应参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)。
- **环境变量命名冲突**：Spring AI Alibaba 的两个集成场景（知识库 vs 大模型应用）对 API Key 和 Workspace ID 的环境变量命名不一致（`AI_DASHSCOPE_API_KEY` vs `DASHSCOPE_API_KEY`；`AI_DASHSCOPE_WORKSPACE_ID` vs `WORKSPACE_ID`），**混用将导致认证失败**，务必按目标场景严格配置。
- **应用类型限制**：Spring AI Alibaba 仅支持集成百炼的**智能体应用**和**工作流应用**，不支持直接调用基础模型（LLM）API 或对话应用（Chat Application）——该能力需通过 `DashScopeLLM` 等原生客户端实现。
- **JDK 与 Spring Boot 版本要求**：Spring AI Alibaba 集成要求 JDK 17+ 和 Spring Boot 3.x（GA 或更高版本），低于此版本将无法启动或出现类加载异常。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


