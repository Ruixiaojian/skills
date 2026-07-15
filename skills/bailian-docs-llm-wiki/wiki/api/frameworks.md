# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力的对接，覆盖云端知识库管理、大模型调用、文档切分与重排、流式响应等关键能力。所有集成均依赖百炼统一的 API Key 认证机制，并需配合控制台创建的应用或知识库资源使用。

## 支持的模型/功能

- **RAG 场景**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 构建，包括文档上传（`.txt`/`.docx`/`.pdf`）、默认智能切分、官方向量嵌入（不可自定义）、检索引擎构建与问答生成。
- **智能体与工作流应用集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，支持非流式与流式响应，并可获取 `docReferences` 和 `thoughts` 等结构化输出。
- **知识库直接检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，支持按知识库名称（`INDEX_NAME`）检索上下文片段，并自动注入提示词模板交由大模型（默认 `qwen-max`）生成回答。

> **注意**：LlamaIndex 方案明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而 Spring AI Alibaba 的知识库检索方案未提及切分/嵌入控制能力，二者在知识库底层处理粒度上存在差异，实际选型时应以业务是否需要定制化预处理为准。

## 关键参数

| 参数名 | 来源框架 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model_name` | LlamaIndex | 设置生成回答所用的大模型 | `"qwen-max"`（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)） |
| `APP_ID` | Spring AI Alibaba（应用集成） | 智能体或工作流应用的唯一 ID | `app-xxxxxx` |
| `DASHSCOPE_API_KEY` | Spring AI Alibaba（应用集成） | 百炼 API Key 环境变量名（推荐） | — |
| `AI_DASHSCOPE_API_KEY` | Spring AI Alibaba（知识库检索） | 百炼 API Key 环境变量名（知识库场景专用） | — |
| `INDEX_NAME` | Spring AI Alibaba（知识库检索） | 待检索知识库的名称（需提前在控制台创建） | `"测试知识库"` |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | Spring AI Alibaba | 子业务空间 ID（仅当应用或知识库部署在子空间时必需） | `ws-xxxxxx` |
| `similarity_top_k`, `similarity_cutoff`, `top_n` | LlamaIndex | 检索结果数量、相似度阈值、重排后返回数 | `5`, `0.4`, `1` |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 调用 `index.as_query_engine()` 并配置 `node_postprocessors`（如 `SimilarityPostprocessor` + `DashScopeRerank`）启用过滤与重排；  
  4. 通过 `query_engine.query()` 发起 RAG 查询。

- **Spring AI Alibaba（应用集成）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.agent.app-id` 和 `api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法传入 `Prompt`。

- **Spring AI Alibaba（知识库检索）**：  
  1. 同样引入 `spring-ai-alibaba-starter-dashscope`；  
  2. 配置 `spring.ai.dashscope.api-key`（注意变量名区别）；  
  3. 构建 `DashScopeDocumentRetriever` 并绑定至 `ChatClient` 的 `DocumentRetrievalAdvisor`；  
  4. 通过 `chatClient.prompt().user(...).stream().chatResponse()` 触发带上下文的生成。

## 限制和注意事项

- **LlamaIndex 方案限制**：仅支持 `.txt`/`.docx`/`.pdf` 文件上传；知识库必须部署在云端；不支持自定义切分逻辑与嵌入模型；文件上传依赖公网访问能力。详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba 应用集成限制**：**仅支持智能体应用和工作流应用**，不支持直接调用基础大模型 API 或知识库 API；`DashScopeAgent` 不提供对检索过程的细粒度控制（如 top-k、重排器选择），其检索行为由应用内部逻辑决定。
- **环境变量命名不一致**：Spring AI Alibaba 文档中，应用集成要求 `DASHSCOPE_API_KEY`，而知识库检索要求 `AI_DASHSCOPE_API_KEY` —— 二者不可混用，否则初始化失败。> **注意**：该差异已在两篇 Spring AI Alibaba 文档中明确体现，属设计约定，非过时信息，但需开发者严格区分场景配置。
- **计费说明**：所有框架调用最终均产生模型推理费用（按 token 计费），百炼应用本身不单独收费。具体计费项参见官方文档。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


