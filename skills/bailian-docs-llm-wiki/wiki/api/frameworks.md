# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖云端知识库托管、本地化模型调用、流式响应等关键能力。所有集成均基于百炼统一的 API 网关与认证体系（API Key），无需直接管理底层模型服务。

## 支持的模型/功能

- **RAG 场景**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 构建，内置文档解析（`.txt`/`.docx`/`.pdf`）、向量化（默认官方向量模型）和[检索增强生成](../concepts/rag.md)流程。
- **智能体与工作流**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已发布的**智能体应用**和**工作流应用**，适用于需编排多步骤逻辑或外部工具调用的复杂任务。
- **知识库直检**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，可直接对接百炼已创建的知识库（无需封装为应用），实现轻量级 RAG 集成。

> **注意**：LlamaIndex 方案明确不支持自定义文档切分方式或嵌入模型（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)），而 Spring AI Alibaba 的知识库检索方案虽未声明限制，但其 `DashScopeDocumentRetriever` 实际依赖百炼平台侧的向量索引能力，同样不开放嵌入模型替换接口。二者在向量化环节均受限于平台托管能力。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `model_name`（LlamaIndex） | 指定生成阶段调用的大模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID`（Spring AI Alibaba） | 智能体/工作流应用唯一标识 | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY`（Spring AI Alibaba） | 百炼 API Key 环境变量名（知识库场景） | `sk-xxx` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `DASHSCOPE_API_KEY`（Spring AI Alibaba） | 百炼 API Key 环境变量名（应用调用场景） | `sk-xxx` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `INDEX_NAME`（Spring AI Alibaba） | 待检索知识库名称 | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

> **注意**：API Key 环境变量名在 Spring AI Alibaba 的两类场景中不一致——应用调用使用 `DASHSCOPE_API_KEY`，知识库检索使用 `AI_DASHSCOPE_API_KEY`。若混用可能导致认证失败。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 调用 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`node_postprocessors` 等参数；  
  4. 执行 `query_engine.query()` 发起 RAG 查询。

- **Spring AI Alibaba（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `spring.ai.dashscope.agent.app-id` 和 `spring.ai.dashscope.api-key`；  
  3. 注入 `DashScopeAgent`，调用 `.call()`（非流式）或 `.stream()`（流式）方法。

- **Spring AI Alibaba（知识库检索）**：  
  1. 添加相同 starter 依赖；  
  2. 配置 `spring.ai.dashscope.api-key`（注意变量名差异）；  
  3. 使用 `DashScopeDocumentRetriever` 初始化 `DocumentRetriever`；  
  4. 通过 `ChatClient` 绑定 `DocumentRetrievalAdvisor` 实现自动上下文注入。

## 限制和注意事项

- **知识库部署模式**：LlamaIndex 方案仅支持**云端知识库**，不支持本地部署（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）；Spring AI Alibaba 的知识库检索方案亦仅对接百炼控制台创建的云端知识库，无本地向量库适配。
- **文件格式限制**：LlamaIndex 方案明确限定支持 `.txt`、`.docx`、`.pdf`（见[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）；Spring AI Alibaba 文档未说明格式限制，但实际依赖百炼知识库上传能力，应保持一致。
- **业务空间隔离**：跨子业务空间调用需显式配置 `WORKSPACE_ID`（应用调用场景）或 `AI_DASHSCOPE_WORKSPACE_ID`（知识库检索场景），否则默认使用主账号空间。
- **计费归属**：所有框架调用均按底层模型推理计费（如 `qwen-max` 调用次数），百炼应用本身不单独收费（见[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


