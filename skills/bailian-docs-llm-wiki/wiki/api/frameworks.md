# frameworks

百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、智能体引擎）的对接，覆盖 Python 和 Java 生态。所有集成均依赖百炼统一的 DashScope API 层，需配置有效的 API Key。

## 支持的模型/功能

- **RAG 构建**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 在 Python 环境中构建端到端 RAG 流程，包括文档上传、云端索引构建、语义检索与大模型生成。
- **知识库检索**：Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，可直接检索百炼已创建的云端知识库，支持相似度过滤与重排（如 `gte-rerank`），并自动注入上下文至 LLM 提示词。
- **大模型应用调用**：Spring AI Alibaba 通过 `DashScopeAgent` 支持对百炼[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)的非流式/流式调用，返回结构化输出（含文档引用、思考链等元信息）。

> **注意**：文档 1 明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制，但实际调用时仍受限于百炼云端知识库的默认处理流程；开发者若需完全控制切分与嵌入，应参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)，而非本框架集成路径。

## 关键参数

| 参数 | 作用 | 示例值 | 来源 |
|------|------|--------|------|
| `model_name` | 指定生成阶段使用的千问大模型 | `"qwen-max"`, `"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API 密钥环境变量名 | — | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；二者功能等价，但命名不一致，建议统一采用 `DASHSCOPE_API_KEY` 避免混淆 |
| `INDEX_NAME` | 云端知识库名称（用于检索） | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 百炼大模型应用 ID（智能体/工作流） | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `similarity_top_k` / `similarity_cutoff` / `top_n` | 检索结果数量、相似度阈值、重排后返回数 | `5`, `0.4`, `1` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |

## 使用方式

- **LlamaIndex（Python）**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 调用 `index.as_query_engine()` 并传入 `node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）定制检索逻辑；  
  4. 通过 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba（Java）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 ≥ `1.0.0.2`）；  
  2. 配置 `application.yml` 中的 `spring.ai.dashscope.api-key` 和 `app-id`（或 `workspace-id`）；  
  3. 对知识库检索：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并集成至 `ChatClient` 的 `DocumentRetrievalAdvisor`；  
  4. 对大模型应用调用：构造 `DashScopeAgent` 实例，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）。

## 限制和注意事项

- **知识库部署模式限制**：所有框架集成均依赖百炼**云端知识库**，不支持在框架内直接管理本地向量存储；文档 1 明确指出“不支持自定义文档切分方式或自定义嵌入模型”[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化格式上传，不支持 Excel、PPT 或数据库直连。
- **环境变量命名冲突**：文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；虽底层兼容，但建议项目中统一选用后者以保持一致性。
- **业务空间隔离**：跨子业务空间操作必须显式配置 `workspace-id`（文档 2 使用 `AI_DASHSCOPE_WORKSPACE_ID`，文档 3 使用 `WORKSPACE_ID`），否则默认访问主账号空间。
- **计费说明**：框架本身不产生费用，但所有模型调用（含 RAG 生成、智能体执行）均按百炼模型推理用量计费，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


