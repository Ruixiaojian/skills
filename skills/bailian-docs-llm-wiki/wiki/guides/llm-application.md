# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可基于零代码、低代码或专业编码方式，快速构建具备知识增强、工具调用、多步推理与企业级运维能力的生产级 AI 应用。

## 支持的模型与功能

百炼 LLM Application 支持多种模型类型与核心能力组合：

- **模型支持**：  
  - 文本模型：`千问-Max`、`千问-Plus-Latest`、`千问-Turbo`、`千问-Long`、`千问3-Coder-Plus` 及开源系列（Qwen2/Qwen2.5/Qwen3）；  
  - 多模态模型：`千问-VL-Max`、`千问-VL-Plus`、`千问-VL-OCR`，支持直接解析图片/视频（[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)）；  
  - 注意：`enable_thinking` 参数仅对支持思考模式的模型（如 `千问-Max`）生效，旧版模型或 Turbo 系列不支持该配置 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **核心功能**：  
  - **知识库（RAG）**：支持切片检索与全文引用两种模式，可与上传文件混合检索；  
  - **工具调用**：统一通过 MCP 协议接入（含官方 MCP 广场服务与自定义 MCP），旧版插件已逐步迁移至 MCP 架构；  
  - **文件处理**：提供全文引用、切片检索、自定义处理三类模式，适配文档/图片/音视频等 10MB 内文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；  
  - **技能（Skill）**：预置可复用能力包（如联网搜索、代码执行），支持一键挂载至智能体；  
  - **数据连接器**：作为智能体、工作流、知识库访问外部数据源的统一桥梁；  
  - **应用组件化**：已发布的智能体或工作流可作为工具嵌入其他应用，实现能力复用。

> **注意**：文档 3（智能体应用）中仍提及“插件”概念，而文档 2（新版智能体应用）明确将所有外部能力统一为 MCP 工具，并指出“插件也支持一键转换为 MCP 服务”。实际开发中应优先使用 MCP，插件为历史兼容项，新项目不应依赖插件接口。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型参数** | `temperature` | 控制生成随机性，范围 0–1，推荐 0.3–0.7 | 模型选择器右侧参数配置器 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| | `max_tokens`（最长回复长度） | 限制模型输出 token 数，不含提示词 | 同上 |
| | `enable_thinking` | 开启思考模式以展示“规划-执行-反思”链路，仅限支持模型 | 同上 |
| **文件处理** | 单文件最大解析长度 / 最大拼装长度（token） | 全文引用模式下截断策略控制 | 文件处理配置面板 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| | 召回片段数 / 最大拼装长度 | 切片检索模式下召回与拼接控制 | 同上 |
| **运行控制** | `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数，超限则终止并返回结果 | 新版智能体“运行与结果分析”章节 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| **记忆** | 短期记忆轮数（0–30） | 控制多轮对话上下文长度，0 表示禁用 | 新版智能体“记忆”配置项 |

## 使用方式

### 创建与配置
- **智能体应用**：控制台 → 应用管理 → 创建应用 → 选择 **Agent 2.0**（推荐）或 Agent 1.0；配置模型、系统提示词、知识库、MCP 工具、文件处理模式等；必须发布后方可调用。
- **工作流应用**：通过可视化节点编排（开始/大模型/意图分类/变量处理/结束等），支持多分支条件、会话变量（`query`/`historyList`/`imageList`）全局传递；需发布后调用。
- **高代码应用**：支持控制台模板创建或 CLI 上传 `.whl` 包；部署方式可选 Serverless Function（轻量无状态）或 K8s（高性能长程任务）；工具、网关、前端均通过 Tab 管理。

### 调用方式
- **API 调用**：所有应用发布后，在“发布渠道”页签获取 API Endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）；  
  - 智能体/工作流：使用标准 `/v1/applications/{app_id}/invoke` 接口；  
  - 高代码应用：调用 `/process` 端点，支持流式响应；  
  - 文件上传：推荐先调用文件上传 API 获取 `session_file_id`，再于对话请求中传入，避免 URL 可访问性问题 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **前端集成**：支持钉钉/微信公众号发布，高代码应用还可通过 Spark Design 框架自定义 WebUI。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；上传文件仅在当前会话有效，刷新即失效；生产环境务必使用 `session_file_id` 方式上传。
- **计费逻辑**：
  - 模型调用按输入/输出 token 计费，**知识库召回内容计入输入 token**；
  - 全文引用模式 token 消耗显著高于切片检索模式；
  - MCP 工具按调用次数或第三方 API 收费，百炼不收取中间费用；
  - [长期记忆](../concepts/long-term-memory.md)存储免费，但其内容注入 [prompt](prompt.md) 后产生的 token 消耗**暂不计费**（见文档 3）。
- **版本与兼容性**：
  - Agent 1.0 与 Agent 2.0 **架构不兼容，无法升级/降级**，需重新创建应用；
  - 工作流中“意图分类”节点的记忆选项（自定义缓存 vs 本节点缓存）影响上下文范围，需按需启用；
  - 高代码应用部署地域必须与网关地域一致。
- **安全与权限**：
  - RAM 账号创建应用时，发布前需确保拥有 `ram:CreateServiceLinkedRole` 权限；
  - 敏感凭证（如 API Key）应通过“环境”配置注入，禁止硬编码在技能代码中。

> **注意**：文档 4（工作流应用）中案例三“日程管理助手”要求先创建并**发布**子智能体应用，但未强调子智能体必须为 **Agent 2.0** 版本；若使用 Agent 1.0 子智能体，可能因工具调度机制差异导致群组节点决策失败。建议所有嵌套智能体统一采用 Agent 2.0。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


