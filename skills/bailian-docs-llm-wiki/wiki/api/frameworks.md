# frameworks

百炼平台通过标准化的 SDK 和框架集成能力，支持开发者基于主流 AI 开发框架（如 LlamaIndex、Spring AI Alibaba）快速构建 RAG 应用或调用百炼大模型应用。这些框架封装了知识库检索、模型调用、Agent 编排等底层细节，使开发者可聚焦于业务逻辑。所有集成均依赖百炼统一的 API Key 认证与服务网关，不提供原生模型直连。

## 支持的模型/功能

- **RAG 场景**：支持通过 LlamaIndex 构建云端知识库驱动的[检索增强生成](../concepts/rag.md)应用，适用于私域知识问答、客服助手等场景；也支持 Spring AI Alibaba 的 `DashScopeDocumentRetriever` 实现 Java 生态下的知识库检索 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **大模型应用调用**：支持 Spring AI Alibaba 的 `DashScopeAgent` 调用百炼已发布的智能体应用（Single Agent）和工作流应用（Workflow），实现复杂任务编排与多步骤推理 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **模型选择**：RAG 场景中默认使用 `qwen-max` 生成回答，但可通过 `Settings.llm = DashScope(model_name="...")` 或 `DashScopeChatOptions.builder().withModel(...)` 显式指定其他千问系列模型（如 `qwen-plus`、`qwen-turbo`）；具体可用模型列表见[文本生成-千问](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。

> **注意**：文档 1 中明确说明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 2 和 3 均未提及该限制，但实际调用时仍受百炼云端知识库服务约束——所有向量构建、切分、重排均由百炼后台统一执行，开发者无法覆盖。此为平台级限制，非框架层可配置项。

## 关键参数

| 参数 | 作用 | 示例值 | 来源 |
|------|------|--------|------|
| `cloud_index_name` / `INDEX_NAME` | 云端知识库名称（需提前在控制台创建） | `"my_first_index"` / `"测试知识库"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)、[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md) |
| `model_name` | RAG 回答生成所用大模型 | `"qwen-max"` | [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) |
| `APP_ID` | 百炼大模型应用 ID（仅限智能体/工作流应用） | `"app-xxx"` | [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md) |
| `AI_DASHSCOPE_API_KEY` / `DASHSCOPE_API_KEY` | 百炼 API Key 环境变量名 | — | 文档 2 使用 `AI_DASHSCOPE_API_KEY`，文档 3 使用 `DASHSCOPE_API_KEY`；二者等效，但推荐统一使用 `DASHSCOPE_API_KEY` 以避免混淆 |

> **注意**：文档 2 要求环境变量名为 `AI_DASHSCOPE_API_KEY`，而文档 3 使用 `DASHSCOPE_API_KEY`。Spring AI Alibaba 官方 starter 实际兼容两种命名，但为一致性起见，建议统一采用 `DASHSCOPE_API_KEY`。

## 使用方式

- **LlamaIndex 集成**：  
  1. 安装 `llama-index` 及 `llama-index-readers-dashscope` 等依赖；  
  2. 使用 `DashScopeCloudIndex.from_documents()` 上传本地文件并构建云端知识库；  
  3. 通过 `index.as_query_engine()` 创建查询引擎，支持 `similarity_top_k`、`similarity_cutoff`、`DashScopeRerank` 等后处理配置。

- **Spring AI Alibaba 集成**：  
  1. 添加 `spring-ai-alibaba-starter-dashscope` 依赖；  
  2. 在 `application.yml` 中配置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`；  
  3. 使用 `DashScopeDocumentRetriever`（知识库检索）或 `DashScopeAgent`（应用调用）进行非流式/流式交互；流式响应需设置 `produces="text/event-stream"` 并返回 `Flux<String>`。

## 限制和注意事项

- **知识库部署模式限制**：所有基于 LlamaIndex 的云端方案仅支持百炼托管的知识库，不支持自定义切分逻辑、嵌入模型或本地向量存储 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **应用类型限制**：Spring AI Alibaba 仅支持集成百炼的「智能体应用」和「工作流应用」，不支持直接调用基础模型（如 `qwen-max`）或「对话应用」。
- **[业务空间隔离](../concepts/workspace-isolation.md)**：若知识库或大模型应用部署在子业务空间，必须显式配置 `AI_DASHSCOPE_WORKSPACE_ID`（文档 2）或 `WORKSPACE_ID`（文档 3），否则默认访问主账号空间。
- **文件格式支持**：LlamaIndex 方案仅支持 `.txt`、`.docx`、`.pdf` 等非结构化文档解析，不支持 Excel、PPT 或图像类文件。
- **计费说明**：框架本身免费，但调用产生的模型推理费用按百炼计费规则结算，详情参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#c1fabcbe9fklk)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


