# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼底层能力（如云端知识库、大模型服务、应用托管）的对接。所有集成均依赖百炼统一的 API Key 认证机制，不强制要求本地部署模型或向量基础设施。

## 支持的模型/功能

- **RAG 场景**：支持通过 LlamaIndex 构建端到端云端 RAG 应用，使用百炼托管的知识库（含自动文档解析、默认向量模型嵌入），并可调用 `qwen-max`、`qwen-plus` 等千问系列模型生成回答 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **智能体与工作流应用集成**：Spring AI Alibaba 支持调用百炼已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，适用于需编排多步骤逻辑或外部工具调用的复杂场景 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **知识库直接检索**：Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，可对接百炼已创建的知识库进行语义检索，并自动注入上下文至 `ChatClient`，支持流式响应 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：LlamaIndex 方案明确声明“不支持自定义文档切分方式或自定义嵌入模型”；而 Spring AI Alibaba 的知识库检索方案未提及该限制，但其 `DashScopeDocumentRetriever` 实际仍依赖百炼云端知识库的预处理结果（即同样受限于百炼默认切分与嵌入策略）。二者在知识库能力层面无本质差异，仅接入路径不同。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `DASHSCOPE_API_KEY` 或 `AI_DASHSCOPE_API_KEY` | 百炼 API 密钥，用于身份认证 | `sk-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID` | 智能体/工作流应用 ID，仅用于应用调用场景 | `app-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `WORKSPACE_ID` 或 `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，用于跨空间访问知识库或应用 | `ws-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name`（LlamaIndex） / `withModel(...)`（Spring AI） | 指定生成模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `INDEX_NAME` | 百炼知识库名称（字符串），用于检索定位 | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库，或 `DashScopeCloudIndex("index-name")` 加载已有知识库；  
  3. 调用 `as_query_engine()` 并配置 `similarity_top_k`、`node_postprocessors`（如 `DashScopeRerank`）等参数构建检索引擎。

- **Spring AI Alibaba 集成**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 ≥ `1.0.0.2`）；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.api-key` 及可选的 `app-id`、`workspace-id`；  
  3. 根据场景选择：  
     - 调用已发布应用 → 注入 `DashScopeAgent`；  
     - 检索知识库 → 使用 `DashScopeDocumentRetriever` + `ChatClient` 组合。

## 限制和注意事项

- **知识库能力限制**：所有框架均依赖百炼云端知识库，因此不支持自定义文本切分规则、嵌入模型或向量存储后端。若需完全控制切分与嵌入流程，应采用[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化格式上传；Spring AI Alibaba 知识库检索方案未明确列出支持格式，但实际依赖百炼控制台知识库的上传能力，建议保持一致。  
- **环境兼容性**：Spring AI Alibaba 要求 JDK 17+ 与 Spring Boot 3.x；LlamaIndex 方案要求 Python 3.9+。两者均不支持低版本运行时。  
- **计费说明**：框架本身免费，但通过百炼调用模型（如 `qwen-max` 推理）或知识库检索服务将产生对应费用，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio) [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


