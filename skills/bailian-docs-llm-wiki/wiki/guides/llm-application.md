# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种互补模式，分别覆盖零代码决策、低代码编排与专业级工程化部署需求。开发者可根据任务复杂度、可控性要求和团队技术栈，选择最适配的构建范式，并通过统一 API 接口集成至现有系统。

## 支持的模型/功能

- **模型支持**：所有应用类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-*`），部分能力对模型有特定要求。例如，新版智能体推荐使用 `qwen-max` 等具备强工具调用能力的模型；文件问答中视觉理解需搭配 `qwen-vl-*` 系列[多模态](../concepts/multi-modal.md)模型 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；高代码应用则支持任意兼容 AgentScope 的自定义 Python 模型封装。
  
- **核心能力矩阵**：
  - **智能体（Agent）**：以提示词驱动自主规划，支持知识库（RAG）、MCP 工具调用、内置沙箱工具（`bash`/`read`/`edit` 等）、短期记忆（0–30 轮）及预解析文件控制 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - **工作流（Workflow）**：基于可视化节点编排，支持大模型节点、意图分类、变量处理、智能体群组等节点类型，强调流程确定性与可复现性 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - **高代码应用**：基于 Python 全栈开发，支持 Serverless Function 与 K8s 两种部署方式，提供 MCP 工具一站式接入、可观测性、API 网关及 Spark Design 前端框架 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 2（旧版智能体）与文档 3（新版智能体）存在架构级不兼容——新版将知识库与 MCP 统一为工具并支持动态规划，而旧版采用分阶段调度；二者无法升级或降级，需重新创建应用。

## 关键参数

| 参数类别 | 说明 | 典型配置示例 |
|----------|------|--------------|
| **模型参数** | 控制生成行为，仅对支持的模型生效 | `temperature=0.3`（降低随机性）、`enable_thinking=true`（开启思考链，仅限支持模型） |
| **文件处理** | 决定上传文件如何参与推理 | 全文引用（截断长度限制）、切片检索（召回片段数、最大拼装长度）、自定义处理（依赖工具配置） [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| **规划控制** | 限定智能体行为边界 | `ReAct 最大轮次=10`（单次会话最多调用工具 10 次）、短期记忆轮数（0–30） |
| **会话变量** | 工作流全局上下文载体 | 预置 `query`（用户输入）、`historyList`（对话历史）、`imageList`（图片列表），支持自定义变量 |
| **部署资源** | 高代码应用性能基线 | vCPU/内存规格、最小实例数（≥1 保障热启动）、单实例并发度 |

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 创建应用 → 选择 `智能体应用（Agent 2.0）` → 配置模型、提示词、知识库/MCP/技能 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接执行路径 → 在节点内配置模型、提示词、变量映射 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - 高代码应用：控制台创建 → 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）与资源 → 一键部署 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **发布与调用**：
  - 所有应用**必须先发布**才能通过 API 调用（未发布应用不可访问）。
  - API 调用统一通过 `POST /v1/applications/{app_id}/invoke` 接口，请求体需包含 `input`（消息数组）、`session_id`、`user_id`。
  - 文件上传需预先调用文件上传 API 获取 `session_file_id`，再在对话请求中传入；URL 方式（`file_list`/`image_list`）仅限公网可访问地址。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；聊天窗口上传的文件仅在当前会话有效，刷新即失效；生产环境推荐使用 `session_file_id` 方式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
  
- **计费逻辑**：
  - 模型调用按输入/输出 [Token](../concepts/token.md) 计费，知识库检索内容、记忆体内容、文件解析文本均计入输入 [Token](../concepts/token.md)；
  - 知识库、MCP 工具、[长期记忆](../concepts/long-term-memory.md)存储单独计费（[长期记忆](../concepts/long-term-memory.md)内容 [Token](../concepts/token.md) 不计费）；
  - 高代码应用部署后即开始计费（函数计算、API 网关、模型调用等）。

- **关键约束**：
  - 自定义插件超时限制为 5 秒；
  - 工作流默认限流 100 次/分钟（含所有 API 请求）；
  - 新版智能体暂不支持[长期记忆](../concepts/long-term-memory.md)（计划迭代支持）；
  - 智能体应用不支持通过 API 创建后在控制台管理（需使用 Assistant API 创建的版本）。

> **注意**：文档 2 中“记忆体内容占用的 Token 暂不计费”与文档 3 中“记忆体内容会合并到 Prompt 中传递给大模型，从而增加 Token 消耗”表述存在矛盾。根据最新计费说明（文档 3），记忆内容实际参与 Token 计算，但平台暂不对该部分收费——此为临时策略，非永久豁免。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)


