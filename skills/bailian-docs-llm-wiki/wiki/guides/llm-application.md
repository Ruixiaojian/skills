# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大模型在私有知识接入、实时信息获取、流程可控性及复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种互补模式，开发者可按需选择零代码、低代码或专业编码方式，快速构建具备知识增强、工具调用、多步推理与企业集成能力的生产级 AI 应用。

## 支持的模型/功能

- **模型支持**：所有应用类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-plus`），部分能力对模型有特定要求：
  - 新版智能体（Agent 2.0）推荐使用 `千问-Max` 系列以保障多步规划效果；[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 明确指出“为确保多步规划效果，推荐选用具备强工具调用能力的模型”。
  - 文件问答功能明确列出支持的文本与视觉模型，包括 `qwen-vl-max`、`qwen-vl-ocr` 等；[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 文档详细说明了各处理模式下的模型适配性。
  - 工作流节点中大模型节点支持 `千问-Plus-latest` 等通用模型，且意图分类、多轮记忆等能力依赖模型对上下文的理解能力。

- **核心功能矩阵**：
  | 功能                | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
  |---------------------|----------------|---------------------|------------|
  | 自主规划与工具调用  | ✅（Agent 2.0 统一调度知识库/MCP） | ❌（流程固定，无自主决策） | ✅（通过 MCP SDK 编程控制） |
  | 可视化编排          | ❌              | ✅（节点拖拽+连线） | ❌          |
  | Python 全栈开发     | ❌              | ❌                  | ✅（Serverless/K8s 部署） |
  | 知识库（RAG）集成   | ✅（作为可规划工具） | ✅（通过大模型节点调用） | ✅（一站式 MCP 接入） |
  | 多模态文件处理      | ✅（全文引用/切片检索/自定义处理） | ⚠️（仅限大模型节点支持图片输入，无专用文件解析配置） | ✅（需代码实现解析逻辑） |

> **注意**：文档 4（旧版智能体）与文档 2（新版智能体）存在关键矛盾——文档 4 称“插件”是核心扩展能力，而文档 2 已将插件全面升级为标准化 MCP 协议接入，并强调“外部工具均以 MCP 协议接入……纳入调度体系”。实际开发应以 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 为准，旧版插件能力已逐步迁移至 MCP 生态。

## 关键参数

- **通用参数**：
  - `temperature`：控制生成随机性（范围通常 0–1），适用于所有模型节点。
  - `max_tokens`（最长回复长度）：限制模型输出 token 数，不包含提示词。
  - `enable_thinking`：仅对支持思考模式的模型（如 `qwen-max`）生效，开启后可展示推理链路。

- **智能体特有参数**：
  - `ReAct 最大轮次`（1–50）：限制单次会话中工具调用总次数，超限则终止调用并生成最终回复。
  - `短期记忆轮数`（0–30）：控制多轮对话上下文长度，0 表示禁用。
  - 文件处理模式三选一：`全文引用`（拼接全文）、`切片检索`（RAG）、`自定义处理`（交由模型规划调用工具）。

- **工作流特有参数**：
  - `会话变量`（如 `query`, `historyList`, `imageList`）：全局可用，支撑多轮状态传递。
  - 节点级 `记忆` 配置：支持“本节点缓存”或“自定义缓存”（即全局记忆），影响大模型节点对历史信息的感知范围。

- **高代码应用特有参数**：
  - 部署规格（vCPU/内存/磁盘）、最小实例数、单实例并发度，直接影响性能与成本。
  - 环境变量与触发器配置，用于注入密钥、设置 HTTP 入口等。

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用中心 → 创建应用 → 选择 **智能体应用（Agent 2.0）** → 配置模型、系统提示词、知识库、MCP 工具等；[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 提供完整向导。
  - 工作流：通过可视化画布拖拽节点（开始/大模型/意图分类/结束等），配置各节点参数并连线；典型案例如“识别诈骗信息”“智能导购”已在 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 中详述。
  - 高代码应用：支持控制台模板创建或 CLI 上传 `.whl` 包；部署方式可选 Serverless Function（轻量无状态）或 K8s（高性能长时任务）。

- **调试与测试**：
  - 所有类型均提供右侧对话面板进行实时交互测试。
  - 智能体（Agent 2.0）支持卡片流展示“思考→工具调用→反思”全过程。
  - 工作流支持逐节点日志查看与变量值追踪。
  - 高代码应用提供“文本对话体验”与“API 测试”双模式，并支持 Spark Design 前端定制。

- **发布与集成**：
  - **必须发布后方可调用**：发布操作位于应用配置页右上角，发布后生成 API 接口。
  - API 调用统一遵循标准 REST 协议，请求头需携带 `Authorization: Bearer <API Key>`。
  - 高代码应用建议启用 **API 网关**，配置自定义域名与 [Token](../concepts/token.md) 鉴权，实现生产环境安全访问。

## 限制和注意事项

- **文件处理限制**：
  - 单会话最多上传 10 个文件，单文件 ≤ 10MB；上传文件仅在当前会话有效，刷新页面即丢失。
  - 全文引用模式受模型上下文长度硬约束，长文档易被截断；推荐长文档优先使用切片检索（RAG）模式。
  - 视觉模型（如 `qwen-vl-*`）即使关闭预解析，也能直接解析图片/视频；但其他模型或非图像文件仍严格依赖预解析开关状态。

- **计费关键点**：
  - 模型调用费用 = 输入 [Token](../concepts/token.md) × 输入单价 + 输出 [Token](../concepts/token.md) × 输出单价；知识库召回内容、记忆体内容、文件解析文本均计入输入 Token。
  - 工具调用（MCP）单独计费：部分官方 MCP 按调用次数收费，第三方 MCP 费用由服务商收取。
  - 高代码应用部署后即开始计费（函数实例、网关、存储等），停止服务可暂停费用。

- **版本与兼容性**：
  - Agent 1.0 与 Agent 2.0 **完全不兼容**，无法升级/降级，需重新创建应用。
  - 工作流中“智能体群组”节点可复用已发布的智能体应用，但子智能体必须已发布，否则工作流运行失败。
  - API 调用时，文件处理模式由应用配置固化，**无法在请求时动态切换**（如不能对同一应用一次用全文引用、一次用切片检索）。

- **安全与运维**：
  - 内置工具（`bash`/`write`/`read` 等）在沙箱中执行，隔离性高；但需谨慎开放 `bash` 权限。
  - 高代码应用的环境变量（如 API Key）应在控制台“部署 > 配置”中设置，避免硬编码。
  - 所有应用均支持日志查看、可观测性分析与告警配置，高代码应用额外提供调用链追踪能力。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


