# frameworks

百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、知识库检索系统及大模型智能体/工作流应用。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大框架实现与百炼服务（包括云端知识库、向量检索、大模型推理、智能体编排）的深度对接。所有集成均基于百炼统一的 DashScope API 层，无需直接管理底层模型或向量服务。

## 支持的模型/功能

- **RAG 场景**：支持通过 LlamaIndex 构建端到端云端 RAG 应用，利用百炼托管的知识库、默认文档切分与官方向量模型（如 `gte-rerank`）完成检索与生成；[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 提供完整示例。
- **Java 生态知识库检索**：Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，可无缝接入百炼已创建的云端知识库，支持语义检索与上下文注入，适用于 Spring Boot 3+ 应用；详见 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **大模型应用调用**：Spring AI Alibaba 支持调用百炼平台创建的**智能体应用**和**工作流应用**（不支持对话应用或基础模型直调），通过 `DashScopeAgent` 实现非流式/流式响应，并可获取思考链（thoughts）、文档引用（docReferences）等结构化输出；参见 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

> **注意**：文档 1 明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制，但实际调用中 `DashScopeDocumentRetriever` 和 `DashScopeCloudIndex` 均依赖百炼云端处理流程，因此该限制对所有框架均适用。

## 关键参数

| 参数 | 作用 | 示例值 | 来源 |
|------|------|--------|------|
| `model_name`（LlamaIndex） | 指定生成回答所用的大模型 | `"qwen-max"`、`"qwen-plus"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `INDEX_NAME`（Spring AI Alibaba） | 待检索知识库的名称（需提前在控制台创建） | `"测试知识库"` | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `APP_ID`（Spring AI Alibaba） | 百炼智能体/工作流应用 ID | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key 环境变量名 | — | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；**二者不兼容，需按所选框架统一配置** |

> **注意**：API Key 环境变量名存在不一致——文档 2 要求 `AI_DASHSCOPE_API_KEY`，文档 3 要求 `DASHSCOPE_API_KEY`。实际使用时必须严格匹配对应框架的约定，混用将导致认证失败。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope`、`llama-index-indices-managed-dashscope` 等扩展包；  
  2. 使用 `DashScopeParse` 解析本地 `.txt`/`.docx`/`.pdf` 文件并上传至百炼；  
  3. 通过 `DashScopeCloudIndex.from_documents()` 创建云端索引，再调用 `as_query_engine()` 构建检索引擎；  
  4. 支持后处理器（如 `SimilarityPostprocessor`、`DashScopeRerank`）定制检索逻辑。

- **Spring AI Alibaba 集成**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖（版本 `1.0.0.2`）；  
  2. 配置 `application.yml` 中的 `spring.ai.dashscope.api-key` 和 `app-id`（或 `workspace-id`）；  
  3. 对于知识库检索：注入 `DashScopeDocumentRetriever` 并绑定 `ChatClient`；  
  4. 对于应用调用：初始化 `DashScopeAgent`，传入 `appId` 调用 `call()` 或 `stream()` 方法。

## 限制和注意事项

- **知识库能力限制**：所有框架均依赖百炼云端知识库服务，**不支持自定义嵌入模型、自定义文本切分策略或本地向量存储**；若需此类能力，须采用本地部署方案（参见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中的本地知识库指引）。
- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文档解析；Spring AI Alibaba 的知识库检索不涉及文件上传，故无此限制，但前提为知识库已在百炼控制台完成构建。
- **环境要求**：  
  - LlamaIndex 方案要求 Python 3.9+；  
  - Spring AI Alibaba 方案要求 JDK 17+ 且 Spring Boot 3.x（文档 2 和 3 均明确要求，无冲突）。
- **业务空间隔离**：跨子业务空间操作需显式配置 `workspace-id`（文档 2 使用 `AI_DASHSCOPE_WORKSPACE_ID`，文档 3 使用 `WORKSPACE_ID`），否则默认访问主账号空间。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


