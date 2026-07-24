# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼能力（如云端知识库、大模型服务、智能体引擎）的深度对接，覆盖 Python 和 Java 生态。所有集成均依赖百炼统一的 DashScope API 层，需配置有效的 API Key。

## 支持的模型与功能

- **RAG 场景**：支持基于云端知识库的[检索增强生成](../concepts/rag.md)，包括文档上传、自动切分、向量化（使用官方向量模型）、语义检索与重排（`gte-rerank`）、多模型响应生成（如 `qwen-max`、`qwen-plus`）。  
- **知识库检索**：仅支持已创建的云端知识库（非本地部署），不支持自定义切分逻辑或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **大模型应用调用**：支持集成百炼平台上的**智能体应用**（Single Agent）和**工作流应用**（Workflow），但**不支持直接调用基础大模型 API**（如 `qwen-max` 的 raw chat 接口）；该能力需通过 `DashScopeAgent` 封装调用 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **语言生态**：Python（LlamaIndex）、Java（Spring Boot 3.x + JDK 17+）双栈支持。

> **注意**：文档 1 明确指出“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及此限制，但其示例均基于云端知识库默认处理流程。实际开发中应以文档 1 的约束为准，避免尝试覆盖默认切分/嵌入行为。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称（必须提前在控制台创建） | `"my_first_index"`、`"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | RAG 中生成回答所用的大模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | 百炼智能体或工作流应用的唯一 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API 密钥（环境变量名不一致） | — | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；二者等效，但需按对应框架示例配置 |
| `AI_DASHSCOPE_WORKSPACE_ID` / `WORKSPACE_ID` | 子业务空间 ID（可选） | `"ws-xxx"` | 文档 2 与文档 3 的环境变量名不同，但语义一致 |

> **注意**：API Key 环境变量命名存在不一致——文档 2 要求 `AI_DASHSCOPE_API_KEY`，文档 3 要求 `DASHSCOPE_API_KEY`。实际使用时请严格遵循所选框架的文档要求，不可混用。

## 使用方式

### Python（LlamaIndex）
1. 安装 `llama-index` 及百炼适配器：`pip install llama-index llama-index-readers-dashscope llama-index-indices-managed-dashscope`  
2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库（自动上传并索引）  
3. 通过 `index.as_query_engine()` 创建查询引擎，配置 `similarity_top_k`、`SimilarityPostprocessor`、`DashScopeRerank` 等后处理器  
4. 调用 `query_engine.query()` 执行 RAG 查询  

### Java（Spring AI Alibaba）
1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 `1.0.0.2`）  
2. 配置 `application.yml`：设置 `spring.ai.dashscope.api-key`、`spring.ai.dashscope.agent.app-id`（RAG 场景用 `DashScopeDocumentRetriever`，应用调用场景用 `DashScopeAgent`）  
3. 注入 `DashScopeDocumentRetriever`（知识库检索）或 `DashScopeAgent`（应用调用）Bean  
4. 调用 `.retrieve()`（非流式）或 `.stream()`（SSE 流式）执行请求  

## 限制和注意事项

- **知识库部署模式**：仅支持云端知识库；若需本地部署与自定义切分/嵌入，请参考[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)（非本框架范畴）[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文档，不支持 Excel、PPT 等格式。  
- **应用类型限制**：Spring AI Alibaba 仅支持集成智能体应用和工作流应用，**不支持集成知识库本身或基础模型 API** [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **并发与性能**：`create_cloud_index.py` 中 `num_workers` 控制上传并发数，过高可能导致请求限频；`rag.py` 中 `similarity_top_k` 过大会增加延迟，建议从 `3–5` 起调优。  
- **计费说明**：框架本身免费，但调用百炼服务（知识库检索、模型推理、应用执行）均按实际用量计费，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


