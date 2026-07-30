# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、[知识库](../concepts/knowledge-base.md)检索服务及大模型智能体/工作流应用。当前重点支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖 Python 和 Java 技术栈，所有集成均基于百炼统一的 API 网关与云端[知识库](../concepts/knowledge-base.md)/应用服务。

## 支持的模型与功能

- **RAG 构建**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端[知识库](../concepts/knowledge-base.md)的端到端 RAG 流程，包括文档上传、智能切分、向量索引构建、多阶段后处理（相似度过滤 + GTE 重排）及问答生成。
- **知识库检索**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，支持在 Spring Boot 应用中直接检索已创建的云端知识库（默认使用 `qwen-max` 模型生成回答）。
- **大模型应用调用**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用百炼平台创建的**智能体应用**和**工作流应用**，支持非流式与 SSE 流式响应，并可获取思考链（thoughts）、文档引用（docReferences）等结构化元数据。

> **注意**：文档 1 明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及嵌入模型控制能力；三者均未提供对百炼私有部署知识库（如 VPC 内网部署）的支持，仅面向公有云知识库服务。

## 关键参数

| 参数 | 作用 | 示例值 | 来源 |
|------|------|--------|------|
| `model_name`（LlamaIndex） | 指定 RAG 中生成回答所用的大模型 | `"qwen-max"`, `"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `similarity_top_k` / `similarity_cutoff` / `top_n` | 控制检索结果数量、最低相似度阈值及重排后返回数 | `5`, `0.4`, `1` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API 认证密钥（环境变量名不一致） | `sk-xxx` | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY` → **注意命名冲突** |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID（可选） | `ws-xxx` | 文档 2 使用 `AI_DASHSCOPE_WORKSPACE_ID`，文档 3 使用 `WORKSPACE_ID` → **注意命名冲突** |
| `INDEX_NAME`（Spring AI Alibaba） | 待检索知识库名称（需提前在控制台创建） | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID`（Spring AI Alibaba） | 智能体或工作流应用 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |

## 使用方式

- **LlamaIndex（Python）**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 上传本地文件并构建云端知识库；  
  3. 调用 `index.as_query_engine()` 配置检索策略（含 `node_postprocessors`），再执行 `.query()`。  
  > 完整流程见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

- **Spring AI Alibaba（Java）**：  
  - **知识库检索**：注入 `DashScopeDocumentRetriever` 并传入 `INDEX_NAME`，结合 `ChatClient` 与 `DocumentRetrievalAdvisor` 实现 RAG；  
  - **应用调用**：初始化 `DashScopeAgent`，通过 `.call()` 或 `.stream()` 方法传入 `Prompt` 与 `APP_ID` 即可触发百炼应用。  
  > 详细配置与代码见 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 和 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## 限制和注意事项

- **知识库能力限制**：所有框架均依赖百炼云端知识库服务，不支持自定义嵌入模型、自定义分块策略或本地向量存储；文档切分与向量化由百炼后台统一完成。
- **环境兼容性**：  
  - LlamaIndex 方案要求 Python 3.9+；  
  - Spring AI Alibaba 方案要求 JDK 17+ 且 Spring Boot 3.x（文档 2 和 3 均明确要求）。
- **API Key 环境变量命名不一致**：文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；实际开发中需按所用模块选择对应变量名，避免认证失败。
- **应用类型限制**：Spring AI Alibaba 仅支持集成**智能体应用**和**工作流应用**，不支持调用“对话应用”或“API 应用”类型（见文档 3 明确限定）。
- **计费说明**：框架本身免费，但调用过程中产生的模型推理（如 `qwen-max` 调用）、知识库检索、应用执行等均按百炼计费项单独计费。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


