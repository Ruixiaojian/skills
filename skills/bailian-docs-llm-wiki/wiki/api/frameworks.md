# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖云端知识库托管、本地化 RAG 构建、大模型应用调用等典型场景。所有集成均基于百炼统一的 API 网关与模型服务层，无需自行维护底层模型推理基础设施。

## 支持的模型/功能

- **RAG 场景**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、智能切分、向量化、检索与生成；默认使用官方向量模型（如 `gte-rerank`）和文本生成模型（如 `qwen-max`），不支持自定义嵌入模型或切分逻辑。
- **智能体/工作流调用**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，可获取结构化输出（如 `docReferences`、`thoughts`）及流式响应。
- **知识库直检**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，直接对接百炼知识库索引（`INDEX_NAME`），支持非应用形态的知识检索，底层仍复用百炼向量引擎与 `qwen-max` 默认生成模型。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 中 `DashScopeDocumentRetriever` 的行为未说明是否允许自定义切分或嵌入模型。实际能力以百炼控制台知识库配置项为准——当前控制台仅开放索引名称、检索 top-k、相似度阈值等参数，**不开放嵌入模型或切分策略的用户侧配置**，因此三者能力一致，无实质矛盾。

## 关键参数

| 参数名 | 作用 | 示例值 | 来源文档 |
|--------|------|--------|----------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库唯一标识符 | `"my_first_index"` 或 `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | 指定生成模型（LLM） | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `similarity_top_k` | 检索返回的最大片段数 | `5` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `similarity_cutoff` | 检索结果最低相似度阈值 | `0.4` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `top_n`（重排） | 重排后返回的最相关片段数 | `1` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | 百炼智能体/工作流应用 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API 密钥环境变量名 | — | 文档 2 与文档 3 使用不同变量名，见下文注意事项 |

> **注意**：文档 2 要求环境变量名为 `DASHSCOPE_API_KEY`，文档 3 要求为 `AI_DASHSCOPE_API_KEY`。二者不兼容，**必须按所用 SDK 版本严格匹配**：`spring-ai-alibaba-starter-dashscope` 1.0.0.2（文档 2）使用前者；`spring-ai-alibaba-examples`（文档 3）使用后者。混用将导致认证失败。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端索引；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）优化检索质量。

- **Spring AI Alibaba（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。

- **Spring AI Alibaba（知识库直检）**：  
  1. 添加相同 starter 依赖；  
  2. 配置 `spring.ai.dashscope.api-key`（注意变量名差异）；  
  3. 构造 `DashScopeDocumentRetriever` 并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`，实现 [prompt](../guides/prompt.md)-aware 检索+生成一体化流程。

## 限制和注意事项

- **知识库部署模式限制**：LlamaIndex 方案仅支持**云端知识库**，不支持本地部署知识库；若需本地切分或自定义嵌入模型，须改用其他方案（如 LangChain + 自托管向量库）。参见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中的明确说明。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文档解析，不支持 `.xlsx`、`.pptx` 或图像类文件。
- **环境变量命名冲突**：Spring AI Alibaba 的两个集成路径（应用调用 vs 知识库直检）使用**互不兼容的 API Key 环境变量名**（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），务必根据所用示例工程和 starter 版本严格区分，否则初始化失败。
- **业务空间隔离**：在子业务空间中创建的应用或知识库，必须显式配置 `WORKSPACE_ID`（文档 2）或 `AI_DASHSCOPE_WORKSPACE_ID`（文档 3），否则默认访问主账号空间资源。
- **计费归属**：所有框架调用最终均产生百炼模型调用费用（按 token 计费），百炼应用本身不单独收费。详见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 中的计费说明。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


