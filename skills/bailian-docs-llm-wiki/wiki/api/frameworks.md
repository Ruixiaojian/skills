# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的原生集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大生态实现标准化接入，覆盖 Python 和 Java 技术栈，底层统一调用百炼的文档处理、向量索引与大模型服务。

## 支持的模型/功能

- **RAG 构建**：支持基于 LlamaIndex 构建云端 RAG 应用，自动完成文档上传、切分（默认智能切分）、向量化（默认官方向量模型）与[检索增强生成](../concepts/rag.md)；也支持通过 Spring AI Alibaba 的 `DashScopeDocumentRetriever` 检索已创建的百炼知识库 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **大模型应用集成**：支持 Spring AI Alibaba 调用百炼托管的**智能体应用**（Single Agent）和**工作流应用**（Workflow），实现复杂任务编排与私域知识联动 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **模型选择**：RAG 场景中可显式指定生成模型（如 `"qwen-max"`、`"qwen-plus"`），知识库检索与应用调用均默认使用 `qwen-max`，具体可用模型列表见[文本生成-千问](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。

> **注意**：LlamaIndex 方案明确声明“不支持自定义文档切分方式或自定义嵌入模型” [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)，而 Spring AI Alibaba 的知识库检索能力依赖百炼平台侧已构建完成的知识库，不涉及本地切分或嵌入过程，二者在能力边界上一致，无实质矛盾。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称（需提前在控制台创建） | `"my_first_index"` / `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | RAG 生成阶段调用的大模型名称 | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | 百炼智能体或工作流应用的唯一 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key 环境变量名（Spring AI Alibaba 推荐前者，LlamaIndex/Spring Boot 示例推荐后者） | — | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID（可选，仅当知识库或应用部署在子空间时必需） | `"ws-xxx"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |

## 使用方式

- **LlamaIndex（Python）**：
  1. 安装 `llama-index`, `llama-index-readers-dashscope`, `llama-index-indices-managed-dashscope`；
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；
  3. 调用 `index.as_query_engine()` 创建检索引擎，支持 `SimilarityPostprocessor` 和 `DashScopeRerank` 后处理；
  4. 通过 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba（Java）**：
  - **知识库检索**：注入 `DashScopeDocumentRetriever` 并绑定知识库名，结合 `ChatClient` 与 `DocumentRetrievalAdvisor` 实现问答；
  - **大模型应用调用**：配置 `DashScopeAgent`，传入 `APP_ID`，支持非流式（`agent.call()`）与流式（`agent.stream()`）两种调用模式。

## 限制和注意事项

- **知识库部署约束**：LlamaIndex 方案仅支持将知识库部署在百炼云端，不支持本地知识库直连；若需本地部署与自定义切分/嵌入，请参考其他方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **文件格式限制**：LlamaIndex 云端知识库构建仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文档，不支持 Excel、PPT 等格式。
- **环境兼容性**：
  - Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x；
  - LlamaIndex 示例要求 Python 3.9+。
- **API Key 配置差异**：Spring AI Alibaba 示例代码使用 `AI_DASHSCOPE_API_KEY`，而百炼通用文档推荐 `DASHSCOPE_API_KEY`；实际使用时需确保与代码中 `@Value` 或 `System.getenv()` 读取的变量名一致，避免认证失败。
- **计费说明**：百炼应用本身免费，但调用模型（含 RAG 中的 LLM 生成、智能体/工作流中的模型推理）将按实际 token 用量计费，详情参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


