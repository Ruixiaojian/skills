# frameworks

百炼平台提供多种主流 AI 开发框架的官方集成支持，帮助开发者快速将大模型能力嵌入现有技术栈。当前重点支持 LlamaIndex 和 Spring AI Alibaba 两大生态，分别面向 RAG 应用构建和 Java 生态应用集成。所有集成均基于百炼统一的 API 网关与模型服务层，无需自行管理模型部署与向量计算基础设施。

## 支持的模型/功能

- **LlamaIndex 集成**：通过 `DashScopeCloudIndex` 实现云端知识库的自动构建与检索，支持 `.txt`、`.docx`、`.pdf` 等非结构化文档上传与智能切分；检索后端默认使用官方向量模型，生成阶段可自由指定 `qwen-max`、`qwen-plus` 等千问系列模型（详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **Spring AI Alibaba 集成**：支持两类核心场景：
  - 调用已发布的**智能体应用**或**工作流应用**（需应用 ID），适用于复杂逻辑编排；
  - 直接检索**云端知识库**（需知识库名称），实现轻量级 RAG，底层自动完成检索 + 上下文注入 + 大模型生成闭环（详见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 和 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 的 `DashScopeDocumentRetriever` 示例中未提及切分控制能力，但其底层依赖百炼知识库服务——这意味着所有 Spring AI Alibaba 知识库检索也受限于同一约束，即**无法在框架层覆盖百炼默认的切分与嵌入策略**。

## 关键参数

| 参数名 | 说明 | 来源框架 | 必填 | 示例值 |
|--------|------|----------|------|--------|
| `DASHSCOPE_API_KEY` 或 `AI_DASHSCOPE_API_KEY` | 百炼平台 API Key，用于身份认证 | LlamaIndex / Spring AI Alibaba | 是 | `sk-xxx` |
| `APP_ID` | 智能体/工作流应用 ID（仅 Spring AI Alibaba 调用应用时必需） | Spring AI Alibaba（应用调用） | 是（应用调用场景） | `app-abc123` |
| `INDEX_NAME` | 云端知识库名称（仅 Spring AI Alibaba 检索知识库时必需） | Spring AI Alibaba（知识库检索） | 是（知识库检索场景） | `"测试知识库"` |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID（仅在非主账号空间创建资源时需要） | 两者均支持 | 否 | `"ws-xyz789"` |
| `model_name`（LlamaIndex） / `withModel()`（Spring AI Alibaba） | 指定生成模型，影响回答质量与延迟 | LlamaIndex / Spring AI Alibaba | 否（有默认值） | `"qwen-max"` |

## 使用方式

- **LlamaIndex**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等扩展包；  
  2. 使用 `DashScopeParse` 解析本地文件，`DashScopeCloudIndex.from_documents()` 构建云端知识库；  
  3. 通过 `index.as_query_engine()` 配置 `similarity_top_k`、`SimilarityPostprocessor`、`DashScopeRerank` 等参数定制检索行为（详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。

- **Spring AI Alibaba**：  
  1. 在 `pom.xml` 中引入 `spring-ai-alibaba-starter-dashscope`（v1.0.0.2+）；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.api-key` 及 `app-id` 或 `index-name`；  
  3. 使用 `DashScopeAgent` 调用应用，或 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 构建知识库检索链路（流式/非流式均支持）。

## 限制和注意事项

- **知识库能力限制**：所有框架接入的云端知识库均采用百炼默认的智能文档切分与官方向量模型，**不支持自定义切分规则、分块大小、嵌入模型或重排序模型**（除 `DashScopeRerank` 提供的有限重排外）。如需完全可控的本地 RAG，请参考独立方案（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中的提示）。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf`；Spring AI Alibaba 知识库检索依赖百炼知识库本身支持的格式（同前），不额外扩展。
- **环境兼容性**：Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x；LlamaIndex 示例基于 Python 3.9+，无 JVM 依赖。
- **计费说明**：框架本身免费，但调用百炼模型（如 `qwen-max`）或应用服务时按实际推理 [Token](../concepts/token.md) 计费（详见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


