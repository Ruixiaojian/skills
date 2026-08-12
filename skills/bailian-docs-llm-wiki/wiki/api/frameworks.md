# frameworks

阿里云百炼平台提供多种主流 AI 开发框架的集成支持，帮助开发者快速构建 RAG 应用、智能体/工作流应用及知识库检索服务。当前主要通过 LlamaIndex 和 Spring AI Alibaba 两大生态实现与百炼底层能力（如云端知识库、大模型服务、文档解析与向量检索）的对接。所有方案均依赖百炼 API Key 和统一的身份认证机制，不提供独立 SDK，而是以适配器（Adapter）或托管索引（Managed Index）形式嵌入框架原生流程。

## 支持的模型/功能

- **RAG 场景**：支持基于 LlamaIndex 构建端到端云端 RAG 应用，使用百炼托管的知识库与默认向量模型（`gte-rerank` 等），适用于私域问答、客服助手等场景 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **智能体与工作流调用**：Spring AI Alibaba 支持集成百炼创建的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，实现业务逻辑编排与多步推理 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。  
- **知识库直检**：Spring AI Alibaba 同样支持直接检索百炼已建知识库（非应用封装），通过 `DashScopeDocumentRetriever` 拉取上下文并交由 `ChatClient` 生成回答，适用于轻量级 RAG 集成 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  

> **注意**：LlamaIndex 方案中明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而 Spring AI Alibaba 的知识库检索方案未提及该限制，但其底层仍依赖百炼托管的向量化能力，实际亦无法替换嵌入模型。二者在能力边界上一致，文档表述差异属信息粒度不同，非实质性矛盾。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `APP_ID` | 智能体/工作流应用唯一标识 | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` | 百炼 API 认证密钥（环境变量名不统一） | `"sk-xxx"` | 前者见 [Spring AI Alibaba集成应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)，后者见 [Spring AI Alibaba检索知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `WORKSPACE_ID` / `AI_DASHSCOPE_WORKSPACE_ID` | 子业务空间 ID（可选） | `"ws-xxx"` | 同上，环境变量命名不一致需注意 |
| `INDEX_NAME` | 云端知识库名称（LlamaIndex 与 Spring AI Alibaba 均需） | `"my_first_index"` 或 `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 与 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | 指定生成模型（LlamaIndex）或默认模型（Spring AI Alibaba） | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中 `Settings.llm = DashScope(model_name="qwen-max")`；Spring AI Alibaba 示例中注释提示可设为 `"qwen-plus"` |

## 使用方式

- **LlamaIndex 集成**：  
  1. 使用 `DashScopeParse` 解析本地 `.txt/.docx/.pdf` 文件；  
  2. 通过 `DashScopeCloudIndex.from_documents()` 上传并构建云端知识库；  
  3. 调用 `index.as_query_engine()` 构建查询引擎，支持 `SimilarityPostprocessor` 与 `DashScopeRerank` 后处理；  
  4. 最终通过 `query_engine.query()` 执行 RAG 查询。  

- **Spring AI Alibaba 集成（应用调用）**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 配置 `APP_ID` 和 `DASHSCOPE_API_KEY`；  
  3. 使用 `DashScopeAgent` 实例调用 `agent.call()`（非流式）或 `agent.stream()`（流式）；  
  4. 响应中可通过 `metadata.get("output")` 提取 `docReferences` 与 `thoughts`。  

- **Spring AI Alibaba 集成（知识库直检）**：  
  1. 配置 `AI_DASHSCOPE_API_KEY`（注意变量名差异）；  
  2. 创建 `DashScopeDocumentRetriever` 并指定 `INDEX_NAME`；  
  3. 将其注入 `DocumentRetrievalAdvisor`，绑定至 `ChatClient`；  
  4. 调用 `chatClient.prompt().user(...).stream().chatResponse()` 触发检索+生成。  

## 限制和注意事项

- **文件格式限制**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 三类非结构化文件上传与解析，不支持 Excel、PPT 等格式 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **环境变量命名不一致**：Spring AI Alibaba 两篇文档分别使用 `DASHSCOPE_API_KEY` 和 `AI_DASHSCOPE_API_KEY`，开发者需按所选路径严格匹配，否则初始化失败。  
- **知识库不可本地部署**：所有框架集成均依赖百炼云端知识库，若需本地知识库控制权（如自定义切分、嵌入模型），必须采用 [基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval) 方案，而非本页所述框架集成路径。  
- **计费归属**：框架本身不产生费用，但所有模型调用（含 `qwen-max` 推理、`gte-rerank` 重排）均按百炼模型计费项结算，详见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


