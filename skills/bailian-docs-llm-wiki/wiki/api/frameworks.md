# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、智能体引擎）的深度对接。所有集成均基于百炼 DashScope API 封装，需配合有效的 API Key 使用。

## 支持的模型/功能

- **RAG 场景**：支持通过 LlamaIndex 构建端到端云端 RAG 应用，包括文档上传、自动切分、向量化、检索与生成全流程；也支持 Spring AI Alibaba 的 `DashScopeDocumentRetriever` 实现知识库检索增强问答 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **大模型应用调用**：支持通过 Spring AI Alibaba 的 `DashScopeAgent` 调用已发布的百炼智能体应用（Single Agent）和工作流应用（Workflow），支持非流式与流式响应 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **模型选择**：RAG 中生成阶段默认使用 `qwen-max`，但可显式指定其他千问系列模型（如 `qwen-plus`、`qwen-turbo`）；智能体调用时模型由应用内部配置决定，SDK 层不暴露模型切换参数。

> **注意**：文档 1 明确指出“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及嵌入模型控制能力，说明当前所有框架集成均依赖百炼托管的向量模型（如 `gte-rerank` 仅用于重排，非嵌入）。该限制在三份文档中一致，无需修正。

## 关键参数

| 参数名 | 来源框架 | 说明 | 示例值 |
|--------|----------|------|--------|
| `cloud_index_name` / `INDEX_NAME` | LlamaIndex / Spring AI Alibaba | 云端知识库名称（需提前在控制台创建） | `"my_first_index"` |
| `model_name` | LlamaIndex（`Settings.llm`） | RAG 生成阶段调用的大模型 | `"qwen-max"` |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | Spring AI Alibaba（两种命名） | 百炼 API Key 环境变量名，文档 2 与文档 3 使用不同命名 | — |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | Spring AI Alibaba（两种命名） | 子业务空间 ID 环境变量名，命名不一致需注意配置兼容性 | — |
| `app-id` | Spring AI Alibaba（智能体） | 百炼大模型应用 ID，通过控制台获取 | `"app-xxx"` |

> **注意**：文档 2 使用 `AI_DASHSCOPE_API_KEY` 和 `AI_DASHSCOPE_WORKSPACE_ID`，而文档 3 使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`。实际运行时需按所用 SDK 版本匹配环境变量名；Spring AI Alibaba 1.0.0.2 默认读取 `DASHSCOPE_API_KEY`（见文档 3 的 `pom.xml` 示例与 `application.yml` 配置），文档 2 的命名可能为旧版遗留或笔误，建议以文档 3 为准 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等配套包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 创建云端知识库；  
  3. 通过 `index.as_query_engine()` 构建检索引擎，支持 `similarity_top_k`、`similarity_cutoff`、`node_postprocessors`（如 `DashScopeRerank`）等参数定制检索逻辑 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

- **Spring AI Alibaba 集成**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 `1.0.0.2`）；  
  2. 配置 `application.yml` 中 `spring.ai.dashscope.*` 相关属性；  
  3. 对知识库场景，注入 `DashScopeDocumentRetriever` 并结合 `DocumentRetrievalAdvisor`；对智能体场景，使用 `DashScopeAgent` 调用 `call()` 或 `stream()` 方法。

## 限制和注意事项

- **知识库部署模式**：仅支持云端知识库，不支持本地知识库直连；文档切分与向量化完全由百炼托管，无法自定义解析器或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化格式，不支持 Excel、PPT 或数据库直连。
- **环境要求**：Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x；LlamaIndex 方案要求 Python 3.9+。
- **业务空间隔离**：跨子业务空间访问知识库或应用时，必须正确配置 `workspace-id`（文档 2/3 均强调此点），否则请求将失败。
- **计费说明**：框架本身免费，但所有模型调用（含 RAG 生成、智能体执行）均按百炼模型推理计费，详情见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


