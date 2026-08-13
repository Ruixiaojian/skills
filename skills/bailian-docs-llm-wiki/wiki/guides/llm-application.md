# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可按需选择零代码、低代码或专业编码方式，快速集成知识库、MCP 工具、记忆、[多模态](../concepts/multimodal.md)能力等核心组件，构建可落地、可运维、可扩展的生产级 AI 应用。

## 支持的模型/功能

百炼 LLM Application 支持三类主流能力构建路径，对应不同抽象层级与控制粒度：

- **智能体（Agent）**：以提示词驱动，支持自主意图理解、动态任务规划与工具调用。新版智能体（Agent 2.0）将知识库、MCP 等统一为可调度工具，支持完整“思考-执行-反思”链路回溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。旧版（Agent 1.0）采用分阶段调度（先检索后决策），适用于意图单一、流程固定的轻量场景。
  
- **工作流（Workflow）**：基于可视化节点编排，将多步骤任务固化为确定性执行流。支持大模型节点、意图分类、变量处理、智能体群组等多种节点类型，适用于报告生成、订单审批、日程管理等强流程约束场景 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向专业开发者，提供完整的 Python 项目部署能力，支持 Serverless Function 或 K8s 部署，内置 MCP 工具接入、可观测性、API 网关与自定义前端（Spark Design） [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有模式均支持千问系列模型（Qwen-Max、Qwen-Plus、Qwen-VL 等）、DeepSeek 及部分开源模型；文件问答能力覆盖文档、图片、音视频，支持全文引用、切片检索（RAG）和自定义处理三种模式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 2（`single-agent-application.md`）中提及“智能体支持插件”，而文档 3（`new-single-agent-application.md`）明确将插件统一纳入 MCP 协议体系，并强调“插件支持一键转换为 MCP 服务”。实际开发中应优先使用 MCP 方式接入外部能力，插件接口已逐步收敛。

## 关键参数

| 类别 | 参数 | 说明 | 典型取值/范围 |
|--------|------|------|----------------|
| **模型层** | `temperature` | 控制输出随机性 | 0.0–1.0（默认 0.8） |
| | `max_tokens` | 模型生成长度上限（不含 [prompt](prompt.md)） | 512–4096 |
| | `enable_thinking` | 是否开启思考模式（仅限支持模型） | `true`/`false` |
| **文件处理** | 单文件最大解析长度（token） | 全文引用模式下截断位置 | ≥1024，建议 ≤2048 |
| | 召回片段数 | 切片检索模式下返回的最大相关片段数 | 1–10 |
| | 最大拼装长度（token） | 所有召回片段总 token 上限 | ≤4096（受模型上下文限制） |
| **运行控制** | ReAct 最大轮次 | 新版智能体单次会话工具调用上限 | 1–50 |
| | 短期记忆轮数 | 多轮对话上下文保留轮数 | 0–30（0 表示禁用） |
| **工作流** | 会话变量（`query`, `historyList`, `imageList`） | 全局可引用的预置变量 | 由开始节点注入 |

> **注意**：文档 4 中“智能导购”案例对多个大模型节点均配置了 `自定义缓存`，但文档 3 明确指出新版智能体仅支持短期记忆（0–30 轮），且[长期记忆](../concepts/memory.md)“计划在未来的迭代中支持”。当前工作流中的 `自定义缓存` 实际作用域为该节点内，非跨节点全局记忆。

## 使用方式

### 创建与配置
- **智能体**：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → 选择 Agent 2.0（推荐）或 Agent 1.0 → 配置模型、系统提示词、知识库、MCP 工具、技能等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流**：拖拽节点（开始、大模型、意图分类、结束等）→ 连接执行流 → 在各节点中配置模型、提示词、用户提示词（如 `${sys.query}`）、记忆选项 → 测试 → 发布。
- **高代码应用**：控制台创建 → 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 部署 → 在“工具”Tab 关联 MCP 服务，在“前端”Tab 配置 Spark Design WebUI。

### 调用与集成
- 所有应用**必须发布后方可调用**（发布按钮位于配置页右上角）。
- API 调用统一通过“发布渠道”页签获取 endpoint 与鉴权方式：
  - 智能体：使用 `POST /v1/agents/{agent_id}/chat`，支持 `file_list`/`image_list` 传文件 URL，或 `session_file_id`（推荐生产环境）。
  - 工作流：使用 `POST /v1/workflows/{workflow_id}/run`，输入 `{"input": {"query": "..."}}`。
  - 高代码应用：`POST /process`，请求体需符合 `input` 数组格式（含 `role`/`content`），并携带网关 [Token](../concepts/token.md)。
- 文件上传：聊天窗口上传仅限当前会话；生产环境应调用独立的[文件上传 API](https://help.aliyun.com/zh/model-studio/call-single-agent-application/#30619780ddy93) 获取 `session_file_id` 后复用。

## 限制和注意事项

- **配额与限流**：每个智能体应用默认限流 **100 次/分钟**，该配额共享于所有 API 调用（含文件问答、普通对话），超限返回 `429 Too Many Requests`。
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；聊天窗口上传文件**仅在当前会话有效**，刷新即失效；通过 `session_file_id` 上传有效期为 24 小时。
- **模型兼容性**：
  - 千问-VL 系列模型可直接解析图片/视频，无需开启预解析；其他文本模型必须开启预解析才能处理非文本文件 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - `enable_thinking` 参数仅对 Qwen-Max 等明确支持思考模式的模型生效，配置无效时控制台不报错但无效果。
- **计费关键点**：
  - 知识库检索内容计入模型输入 [Token](../concepts/token.md)，显著影响费用；切片检索模式通常比全文引用更经济。
  - 记忆体内容合并入 Prompt 后增加输入 [Token](../concepts/token.md)，但**记忆体本身存储不收费**（文档 2 明确说明）。
  - MCP 工具调用费用由第三方或按模型调用计费，百炼不额外收取工具调度费。
- **版本兼容性**：Agent 1.0 与 Agent 2.0 **不兼容，无法升级或降级**，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


