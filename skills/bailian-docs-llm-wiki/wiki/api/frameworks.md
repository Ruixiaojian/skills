# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要支持 LlamaIndex 和 Spring AI Alibaba 两大框架，覆盖云端知识库托管、模型调用、检索增强、流式响应等核心能力。所有集成均基于百炼统一的 API 认证与权限体系，无需自行管理底层模型服务或向量基础设施。

## 支持的模型/功能

- **RAG 场景**：通过 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 支持基于云端知识库的端到端 RAG 流程，包括文档上传、自动切分（仅限 `.txt`/`.docx`/`.pdf`）、默认向量嵌入（官方向量模型）、相似度检索与大模型生成。支持 `qwen-max`、`qwen-plus` 等千问系列模型作为生成器。
- **智能体与工作流集成**：通过 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 支持调用已部署的**智能体应用**和**工作流应用**，可获取结构化输出（如 `docReferences`、`thoughts`）及完整执行轨迹。
- **知识库直检**：通过 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) 提供 `DashScopeDocumentRetriever`，直接对接百炼知识库（非应用层），支持自定义提示词模板与模型切换（默认 `qwen-max`，可设为 `qwen-plus` 等）。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 的 `DashScopeDocumentRetriever` 未提及切分控制能力，但其底层依赖百炼知识库的预建索引——这意味着**所有框架均无法在云端知识库场景下替换嵌入模型或修改切分逻辑**；若需该能力，必须采用本地 RAG 方案（参见文档 1 中引用的[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)）。

## 关键参数

| 参数名 | 说明 | 来源框架 | 示例值 | 备注 |
|--------|------|----------|--------|------|
| `model_name` / `withModel()` | 指定生成模型 | LlamaIndex / Spring AI Alibaba | `"qwen-max"` | 文档 1 和文档 3 均默认使用 `qwen-max`；文档 3 注释中明确支持 `qwen-plus`；文档 2 未显式指定，但实际调用应用时由应用配置决定 |
| `similarity_top_k` | 检索返回的最高相似度节点数 | LlamaIndex | `5` | 仅 LlamaIndex 可控；Spring AI Alibaba 的 `DashScopeDocumentRetriever` 未暴露该参数 |
| `similarity_cutoff` | 相似度过滤阈值 | LlamaIndex | `0.4` | LlamaIndex 特有，用于后处理过滤 |
| `top_n` (rerank) | 重排后返回结果数 | LlamaIndex | `1` | 依赖 `DashScopeRerank`，需额外启用 |
| `APP_ID` | 百炼应用 ID（智能体/工作流） | Spring AI Alibaba | `app-xxx` | 仅文档 2 要求；文档 3 不需要 |
| `INDEX_NAME` | 百炼知识库名称 | Spring AI Alibaba | `"测试知识库"` | 仅文档 3 使用；文档 2 不涉及知识库直检 |

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope`；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 构建云端知识库（文档 1）；  
  3. 通过 `index.as_query_engine()` 配置检索参数并调用 `query()` 或 `stream()`（文档 1）。

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（文档 2）；  
  2. 配置 `APP_ID`、`DASHSCOPE_API_KEY`（推荐环境变量）；  
  3. 使用 `DashScopeAgent` 调用非流式/流式接口（文档 2）。

- **Spring AI Alibaba 集成（知识库直检）**：  
  1. 同上添加依赖；  
  2. 配置 `AI_DASHSCOPE_API_KEY`（注意环境变量名不同，文档 3 使用 `AI_DASHSCOPE_API_KEY`，文档 2 使用 `DASHSCOPE_API_KEY`）；  
  3. 初始化 `DashScopeDocumentRetriever` 并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`（文档 3）。

> **注意**：文档 2 与文档 3 对 API Key 环境变量命名不一致（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），且文档 3 的 `workspace-id` 配置项名为 `AI_DASHSCOPE_WORKSPACE_ID`，而文档 2 为 `WORKSPACE_ID`。**建议统一使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID`，因其被文档 1 和文档 2 共同采用，兼容性更广；文档 3 的变量名可能为旧版遗留，实际运行时优先读取 `DASHSCOPE_API_KEY`**。

## 限制和注意事项

- **知识库能力限制**：所有云端知识库方案（LlamaIndex + DashScopeCloudIndex、Spring AI Alibaba + DashScopeDocumentRetriever）均**强制使用百炼默认的智能文档切分与官方向量模型**，不支持自定义切分规则、嵌入模型或索引类型（参见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中的明确声明）。
- **应用类型限制**：Spring AI Alibaba 仅支持集成**智能体应用**和**工作流应用**，不支持直接调用基础模型 API 或知识库 API（参见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文件上传解析（文档 1）；Spring AI Alibaba 知识库直检不涉及文件上传，仅检索已创建的知识库。
- **流式支持差异**：LlamaIndex 的 `query_engine.query()` 为同步阻塞调用，无原生流式支持；Spring AI Alibaba 在应用调用（文档 2）和知识库直检（文档 3）中均提供 `Flux<ChatResponse>` 流式接口。
- **业务空间配置**：若知识库或应用部署在子业务空间，必须配置 `WORKSPACE_ID`（文档 2、3 均要求），否则请求将路由至主账号空间。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


