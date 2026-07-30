# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大生态实现标准化接入，覆盖云端知识库托管、模型调用、检索增强与流式响应等核心能力。所有集成均依赖统一的 DashScope API 层，需配置有效的 `DASHSCOPE_API_KEY`。

## 支持的模型/功能

- **RAG 场景**：支持基于 LlamaIndex 构建端到端[检索增强生成](../concepts/rag.md)应用，使用云端知识库（含自动文档切分与向量化），默认嵌入模型为官方向量模型（如 `gte-rerank`），不支持自定义切分逻辑或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **智能体与工作流**：Spring AI Alibaba 支持集成百炼平台创建的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，但**不支持直接集成知识库本身**（仅支持应用级调用） [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **知识库直检**：Spring AI Alibaba 同时提供 `DashScopeDocumentRetriever` 组件，可直接对接已创建的百炼知识库（非应用），执行语义检索并注入上下文至 `qwen-max` 等模型生成回答 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  
> **注意**：文档2称“仅支持集成智能体应用和工作流应用”，而文档3明确支持知识库直检；二者功能正交——前者调用封装好的业务逻辑应用，后者直接检索原始知识片段。开发者需根据场景选择：若需预置推理链路（如多步工具调用），选文档2；若需自主控制检索+生成流程，选文档3。

## 关键参数

| 参数名 | 说明 | 来源/示例 |
|--------|------|-----------|
| `APP_ID` | 智能体或工作流应用的唯一标识，必须配置于环境变量或 `application.yml` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `DASHSCOPE_API_KEY` | 百炼平台 API 密钥，推荐设为环境变量；Spring AI Alibaba 示例中部分使用 `AI_DASHSCOPE_API_KEY`，存在命名不一致风险 | [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID，用于跨空间访问知识库或应用；两文档使用不同环境变量名，实际调用时需按 SDK 版本对齐 | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) 和 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `INDEX_NAME` | 知识库名称（字符串），用于 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 定位目标知识库 | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 和 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |

## 使用方式

- **LlamaIndex 集成**：  
  1. 使用 `DashScopeParse` 解析本地 `.txt`/`.docx`/`.pdf` 文件；  
  2. 调用 `DashScopeCloudIndex.from_documents()` 上传并构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建检索引擎，支持 `SimilarityPostprocessor` 和 `DashScopeRerank` 后处理；  
  4. 设置 `Settings.llm = DashScope(model_name="qwen-max")` 指定生成模型。  

- **Spring AI Alibaba 集成**：  
  - **应用调用**：注入 `DashScopeAgent`，传入 `APP_ID` 调用预部署的智能体/工作流；支持非流式（`agent.call()`）与流式（`agent.stream()`）两种模式。  
  - **知识库直检**：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并绑定 `INDEX_NAME`，结合 `ChatClient` 与系统提示词模板实现 RAG 流程。  

## 限制和注意事项

- **知识库能力限制**：LlamaIndex 方案中，云端知识库强制使用默认文档切分策略与嵌入模型，不支持自定义切分规则或替换嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **环境变量命名冲突**：Spring AI Alibaba 文档中 `API Key` 的环境变量名不统一（`DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），实际使用需以所引入 SDK 版本的 `spring-ai-alibaba-starter-dashscope` 文档为准，避免配置失效。  
- **依赖版本约束**：所有 Spring AI Alibaba 方案要求 JDK 17+ 和 Spring Boot 3.x；LlamaIndex 方案要求 Python 3.9+。  
- **计费说明**：百炼应用本身不收费，但模型调用（含 RAG 中的 `qwen-max` 推理、重排模型 `gte-rerank` 调用）按实际 token 量计费，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)



