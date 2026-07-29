# frameworks

阿里云百炼平台通过标准化的 SDK 和框架集成能力，支持开发者快速将大模型能力嵌入现有技术栈。当前主要提供对 LlamaIndex 和 Spring AI Alibaba 两大主流 AI 开发框架的原生支持，覆盖 RAG 应用构建、知识库检索及智能体/工作流调用等核心场景。所有集成均基于 DashScope API 封装，需配置有效的 `DASHSCOPE_API_KEY`（或 `AI_DASHSCOPE_API_KEY`）方可使用。

## 支持的模型/功能

- **LlamaIndex 集成**：支持通过 `DashScopeCloudIndex` 构建云端 RAG 应用，依赖百炼托管的知识库（文档上传、切分、向量化均由平台完成），并支持 `qwen-max`、`qwen-plus` 等千问系列模型作为生成器 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **Spring AI Alibaba 智能体/工作流调用**：支持集成百炼平台创建的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，通过 `DashScopeAgent` 实现非流式与流式响应 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **Spring AI Alibaba 知识库检索（RAG）**：支持直接检索百炼已创建的知识库（`INDEX_NAME` 指定），自动完成检索 + 大模型生成闭环，默认使用 `qwen-max`，可通过 `DashScopeChatOptions.builder().withModel(...)` 切换 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  

> **注意**：LlamaIndex 方案明确不支持自定义文档切分方式或自定义嵌入模型；而 Spring AI Alibaba 的知识库检索方案未说明是否支持自定义切分/嵌入，但其底层依赖百炼知识库服务，因此实际能力应与 LlamaIndex 方案一致——即仅支持平台默认处理流程。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` 或 `AI_DASHSCOPE_API_KEY` | 认证凭据，必须配置为环境变量 | `sk-xxx` | 所有文档均要求 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | Spring AI Alibaba 调用智能体/工作流应用时必需 | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` 或 `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间场景下必需，环境变量名不统一（前者用于应用调用，后者用于知识库检索） | `ws-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` / `withModel()` | 指定生成模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `INDEX_NAME` | Spring AI Alibaba 知识库检索时指定知识库名称 | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

## 使用方式

- **LlamaIndex**：  
  1. 安装 `llama-index`, `llama-index-readers-dashscope`, `llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeParse` 解析本地 `.txt`/`.docx`/`.pdf` 文件；  
  3. 调用 `DashScopeCloudIndex.from_documents()` 创建云端知识库；  
  4. 通过 `index.as_query_engine()` 构建查询引擎，支持 `SimilarityPostprocessor` 和 `DashScopeRerank` 后处理。  

- **Spring AI Alibaba（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `agent.call()`（非流式）或 `agent.stream()`（流式）。  

- **Spring AI Alibaba（知识库检索）**：  
  1. 添加相同 starter 依赖；  
  2. 配置 `spring.ai.dashscope.api-key`（及可选 `workspace-id`）；  
  3. 使用 `DashScopeDocumentRetriever` 绑定 `INDEX_NAME`，注入 `DocumentRetrievalAdvisor` 到 `ChatClient`，实现端到端 RAG。  

## 限制和注意事项

- **知识库能力限制**：所有框架均依赖百炼平台托管的知识库服务，因此**不支持自定义文档切分逻辑、不支持自定义嵌入模型、不支持本地部署知识库索引**。如需此类能力，需参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval) [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化格式上传；Spring AI Alibaba 知识库检索方案未明确说明输入格式，但其知识库创建环节受相同限制约束。  
- **环境变量命名冲突**：Spring AI Alibaba 文档中存在两套环境变量命名规范——应用调用使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`，知识库检索使用 `AI_DASHSCOPE_API_KEY` 和 `AI_DASHSCOPE_WORKSPACE_ID`。实际使用时需按所选集成路径严格匹配，否则初始化失败。  
- **计费说明**：框架本身免费，但所有模型调用（含 RAG 中的生成、智能体执行、工作流节点推理）均按 [模型推理调用计费](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


