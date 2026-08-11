# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的原生集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现，分别面向 Python 和 Java 生态，覆盖从数据接入、向量检索到生成式推理的完整链路。

## 支持的模型/功能

- **RAG 场景**：支持基于云端知识库的[检索增强生成](../concepts/rag.md)，包括文档上传、自动切分、向量化与语义检索；默认使用官方向量模型（如 `gte-rerank`）和千问系列大模型（如 `qwen-max`、`qwen-plus`）生成回答。
- **知识库检索**：LlamaIndex 通过 `DashScopeCloudIndex` 封装云端知识库访问逻辑；Spring AI Alibaba 提供 `DashScopeDocumentRetriever` 实现无缝集成。
- **大模型应用调用**：仅支持调用已发布的**智能体应用**（Single Agent）和**工作流应用**（Workflow），不支持直接调用基础模型或自定义 Prompt 工程应用。
- **多语言支持**：Python（LlamaIndex）、Java（Spring Boot 3.x + JDK 17+）双栈支持，均需配置百炼 API Key。

> **注意**：文档 1 明确指出“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制，但其示例代码均依赖百炼托管的向量索引与重排能力。实际开发中应以 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 的说明为准。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `model_name` | 指定生成回答所用的大模型 | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API 密钥环境变量名 | — | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)、[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `INDEX_NAME` | 云端知识库名称（必需） | `"my_first_index"` 或 `"测试知识库"` | 前两篇文档均明确要求提前创建并指定 |
| `APP_ID` | 大模型应用 ID（仅限智能体/工作流） | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID（可选） | `"ws-xxx"` | 文档 2 和 3 均要求在子空间场景下配置 |

## 使用方式

### Python（LlamaIndex）
1. 安装依赖：`pip install -r requirements.txt`（含 `llama-index`, `llama-index-readers-dashscope`, `llama-index-indices-managed-dashscope`）  
2. 构建云端知识库：调用 `DashScopeCloudIndex.from_documents(...)` 上传本地 `.txt`/`.docx`/`.pdf` 文件  
3. 创建查询引擎：设置 `similarity_top_k`、`SimilarityPostprocessor`、`DashScopeRerank` 等后处理器  
4. 执行 RAG 查询：`query_engine.query(prompt)`  

### Java（Spring AI Alibaba）
1. 添加 Maven 依赖：`spring-ai-alibaba-starter-dashscope`（v1.0.0.2+）  
2. 配置 `application.yml`：设置 `spring.ai.dashscope.api-key`、`spring.ai.dashscope.agent.app-id`（知识库检索无需 `app-id`，仅应用调用需要）  
3. 知识库检索：注入 `DashScopeDocumentRetriever` 并绑定 `ChatClient`，通过 `DocumentRetrievalAdvisor` 自动注入上下文  
4. 应用调用：使用 `DashScopeAgent` 调用智能体/工作流，支持非流式（`agent.call()`）和流式（`agent.stream()`）两种模式  

## 限制和注意事项

- **文件格式限制**：仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文档上传；不支持 Excel、PPT、图片等格式（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。  
- **知识库部署模式**：当前仅支持**云端知识库**；若需本地部署与自定义切分/嵌入，请参考官方替代方案（文档 1 中明确提示）。  
- **API Key 环境变量命名不一致**：文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；建议统一采用后者以兼容性更佳，或按框架文档严格区分。  
- **应用类型限制**：Spring AI Alibaba 调用大模型应用时，**仅支持智能体应用和工作流应用**，不支持对话应用、Prompt 应用等其他类型（见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。  
- **网络要求**：所有操作均需本地环境可访问公网（文档 1 和 2 均明确强调）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


