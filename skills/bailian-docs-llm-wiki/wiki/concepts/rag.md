# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大语言模型生成响应前，先从私有知识库中实时检索相关片段，并将检索结果作为上下文注入提示词（Prompt），从而提升回答的准确性、时效性与领域专业性。该机制有效弥补了大模型固有的知识截止、幻觉和泛化偏差问题，实现“用数据驱动生成”。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一接口，而是贯穿多个能力层的统一增强范式，按使用方式可分为三类：

- **知识库直检（底层 RAG）**：通过 `application component API` 的 `Retrieve` 接口或 `knowledge base` 控制台能力，执行向量召回 + 重排，返回原始文本切片（chunk）。适用于需自定义 Prompt 构造、多阶段编排或调试召回质量的开发者场景。
  
- **知识增强型应用网关（中层 RAG）**：通过 `knowledge` API（如 `/api/v1/indices/knowledge/search` 和 `/api/v2/apps/knowledge/chat`）调用封装好的语义检索与端到端问答服务。后者支持流式 SSE 响应（含 `planning`/`tool_call`/`message` 事件），天然适配对话式交互，无需手动拼接 Prompt。

- **智能体/工作流集成（高层 RAG）**：在 `llm application`（智能体或工作流）中，将知识库作为可调度工具启用。系统自动完成检索、过滤、注入与生成全流程；支持标签过滤、相似度阈值控制及“必定调用”策略，与 MCP 工具、内置沙箱能力统一编排。

此外，`frameworks`（LlamaIndex / Spring AI Alibaba）提供框架级集成，屏蔽底层细节；`application use cases`（如网站/钉钉客服）则通过 AppFlow 无代码对接，RAG 作为可选但强推荐的知识增强模块嵌入渠道链路。

## 关键参数和配置

RAG 效果由检索与生成两个阶段的关键参数协同决定，开发者需根据场景平衡精度、延迟与成本：

| 参数名 | 所属层级 | 说明 | 典型取值 | 注意事项 |
|--------|----------|------|-----------|-----------|
| `retrieval_top_k` / `similarity_top_k` | 检索阶段 | 初步向量召回切片数 | 10–50 | 过高增加重排 [Token](token.md) 消耗，过低易漏召；默认 50（知识库）、3–5（智能体应用） |
| `similarity_threshold` | 检索阶段 | 重排后分数过滤阈值 | 0.3–0.7 | 0 表示不过滤；低于阈值的切片不进入生成上下文 |
| `max_retrieved_chunks` / `max_chunks_to_pass` | 检索阶段 | 最终传给 LLM 的切片数量上限 | 1–20 | 受模型上下文长度硬限制（如 qwen-max 输入上限约 32K token） |
| `retrieval_mode` | 应用层 | 知识库调用策略 | `"always"`（必定调用）或 `"on-demand"`（按需触发） | `"always"` 保障知识生效，`"on-demand"` 降低非必要开销 |
| `temperature` / `top_p` | 生成阶段 | 控制生成稳定性 | `temperature=0.1–0.5`, `top_p=0.8–0.95` | 客服等确定性场景建议低 temperature |

> ⚠️ 注意：所有参数均需在对应能力上下文中配置——知识库控制台配置影响 `knowledge base` 和 `knowledge` API；智能体应用配置影响 `llm application` 调用；框架集成（如 LlamaIndex）需在 SDK 初始化时设置 `similarity_top_k` 等字段。

## 面向开发者，简洁实用

- **快速验证**：用控制台「知识库」→「命中测试」输入 Query，直接查看召回切片、分数、元数据，无需写代码。
- **最小可行集成**：
  - 直检：调用 `POST /api/v1/indices/knowledge/search`，传 `query` 和 `index_ids`，解析返回 `chunks` 数组；
  - 网关问答：调用 `POST /api/v2/apps/knowledge/chat`，`messages` 用 ChatML 格式，处理 SSE 流中的 `event: message` 字段；
  - 智能体：创建应用时绑定知识库 → 发布 → API 调用时自动生效，无需额外参数。
- **避坑指南**：
  - Base URL 固定为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，不可替换为 `dashscope.aliyuncs.com`；
  - `index_ids` 在检索接口中为可选，但未指定将扫描 workspace 下所有已发布知识库，存在性能与权限风险；
  - 知识库仅支持华北2（北京）地域，国际站用户需注意区域隔离；
  - 流式接口（如 `/knowledge/chat`）必须保持长连接，客户端需正确处理 `event:` 分隔的 SSE 响应。

RAG 不是黑盒功能，而是可观察、可调优、可组合的工程能力。建议从「命中测试」起步，逐步叠加标签过滤、多知识库联合、多轮智能模式（Agentic 搜索）等高级特性。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


