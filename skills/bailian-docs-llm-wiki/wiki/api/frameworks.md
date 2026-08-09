# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、智能体应用）的深度对接。所有集成均基于百炼 DashScope API 封装，需配合有效的 API Key 使用。

## 支持的模型/功能

- **RAG 场景**：支持通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 构建端到端云端 RAG 应用，包括文档上传、智能切分、向量化、检索与生成全流程；默认使用官方向量模型（如 `gte-rerank`）和千问系列大模型（如 `qwen-max`）。
- **知识库检索**：Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，可直接检索已创建的百炼云端知识库，支持相似度过滤与重排，适用于 Java 生态的 RAG 集成。
- **大模型应用调用**：Spring AI Alibaba 通过 `DashScopeAgent` 支持非流式/流式调用百炼**智能体应用**和**工作流应用**（不支持对话应用或基础模型直调），并可获取思考链（thoughts）、文档引用（docReferences）等结构化输出。

> **注意**：文档 1 明确指出“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制，但实际调用中仍受限于百炼云端知识库的托管能力——所有知识库检索均依赖百炼后台统一处理，开发者无法替换底层嵌入模型或切分逻辑。此为平台级约束，非框架层可绕过。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `model_name`（LlamaIndex） | 指定生成回答所用的大模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API 密钥环境变量名 | — | 文档 2 使用前者，[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)；文档 3 使用后者，[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `INDEX_NAME` | 知识库名称（LlamaIndex 或 Spring AI Alibaba 均需提前在控制台创建） | `"my_first_index"`、`"测试知识库"` | 两文档均要求知识库已存在且名称匹配 |
| `APP_ID` | 百炼大模型应用 ID（仅 Spring AI Alibaba 调用智能体/工作流时必需） | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID（可选，用于跨空间访问） | `"ws-xxx"` | 文档 2 与文档 3 的环境变量命名不一致，需按实际框架版本确认 |

> **注意**：API Key 环境变量名在文档 2 和文档 3 中存在差异（`AI_DASHSCOPE_API_KEY` vs `DASHSCOPE_API_KEY`），Spring AI Alibaba 1.0.0.2 版本实际兼容两者，但推荐统一使用 `DASHSCOPE_API_KEY` 以保持与百炼官方 SDK 一致性。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-llms-dashscope`、`llama-index-readers-dashscope` 等配套包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 上传本地文件并构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建检索引擎，配置 `similarity_top_k`、`node_postprocessors`（如 `DashScopeRerank`）等参数；  
  4. 调用 `query_engine.query()` 执行 RAG 查询。

- **Spring AI Alibaba 集成**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `application.yml` 中的 `spring.ai.dashscope.api-key` 和 `app-id`（知识库场景无需 `app-id`）；  
  3. 知识库检索：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并绑定至 `ChatClient`；  
  4. 大模型应用调用：注入 `DashScopeAgentApi`，实例化 `DashScopeAgent`，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）。

## 限制和注意事项

- **知识库托管模式限制**：所有基于 LlamaIndex 或 Spring AI Alibaba 的知识库检索，均依赖百炼云端知识库服务，**不支持本地部署知识库**；文档 1 明确说明“将知识库部署在本地……请参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)”，即框架集成仅面向云端知识库。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化格式上传，不支持 Excel、PPT 等（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **应用类型限制**：Spring AI Alibaba 仅支持集成**智能体应用**和**工作流应用**，不支持对话应用、基础模型直调或知识库应用本身（见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。
- **Java 版本要求**：Spring AI Alibaba 集成要求 JDK 17+ 与 Spring Boot 3.x，不兼容 JDK 8 或 Spring Boot 2.x。
- **计费说明**：框架本身免费，但调用百炼知识库检索、大模型推理或应用执行均产生对应计费项，详见百炼计费文档。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


