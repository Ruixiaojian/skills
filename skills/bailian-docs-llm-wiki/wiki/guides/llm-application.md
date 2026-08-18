# llm application

`llm application` 是阿里云百炼平台面向大模型落地的核心能力抽象，提供三种互补的构建范式：以自主决策为特征的智能体（Agent）、以流程确定性为优势的工作流（Workflow），以及以代码完全可控为特点的高代码应用。开发者可根据业务复杂度、可控性要求与团队技术栈，选择零代码、低代码或专业编码方式快速构建生产级 AI 应用。

## 支持的模型/功能

- **模型支持**：所有 `llm application` 类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-plus`），部分能力对模型有特定要求。例如，新版智能体推荐使用 `千问-Max` 系列以保障多步规划效果；文件问答中图片处理需搭配 `千问VL` 系列模型才能启用“模型处理+规划”模式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **核心功能矩阵**：
  - **智能体（Agent）**：支持知识库（RAG）、MCP 工具调用、内置沙箱工具（`bash`/`read`/`edit` 等）、短期记忆（0–30 轮）、自定义变量与标签过滤。新版（Agent 2.0）将知识库与 MCP 统一为可自主规划的工具，显著提升过程透明度与任务泛化能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - **工作流（Workflow）**：提供可视化节点编排，支持大模型节点、意图分类、变量处理、智能体群组等十余种节点类型，适用于固定流程自动化。其会话变量（`query`/`historyList`/`imageList`）可在全生命周期内跨节点引用 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - **高代码应用**：基于 Python 项目结构，支持 Serverless Function 与 K8s 两种部署方式，提供一站式 MCP 接入、API 网关、可观测性及 Spark Design 前端框架集成，适合深度定制与企业级运维场景 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“不支持将旧版智能体升级到新版本”，且新版已将知识库作为可规划工具纳入统一调度体系，而旧版仍将其视为独立能力模块。实际开发应以 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 为准。

## 关键参数

- **通用参数**：
  - `temperature`：控制生成随机性，范围通常为 0.0–1.0。
  - `max_tokens`（最长回复长度）：限制模型输出 token 数，不含提示词。
- **智能体特有参数**：
  - `enable_thinking`：仅对支持思考模式的模型生效，开启后可展示推理链路（Thinking 步骤）。
  - `ReAct 最大轮次`（1–50）：限制单次会话中工具调用总次数，超限则终止调用并生成最终回复。
  - 文件处理模式：`全文引用`（截断策略影响输入 token）、`切片检索`（召回片段数 + 最大拼装长度）、`自定义处理`（依赖工具配置）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **工作流特有参数**：
  - 节点级 `记忆` 配置：支持“本节点缓存”或“自定义缓存”（全局上下文），影响 `historyList` 的注入范围。
- **高代码应用特有参数**：
  - 部署资源规格（vCPU/内存/磁盘）、最小实例数、单实例并发度，直接影响性能与成本。

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用中心 → 创建应用 → 选择“智能体应用” → 指定 Agent 2.0 版本 → 配置模型、系统提示词、知识库、MCP 等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流：通过拖拽节点（开始/大模型/意图分类/结束等）构建执行图，配置各节点模型、提示词及变量映射 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - 高代码应用：支持控制台模板创建或 CLI 上传 `.whl` 包，需授权 FC 与 API 网关权限，并配置部署方式（Serverless/K8s）与资源规格 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。
- **发布与调用**：
  - 所有类型应用**必须发布后方可调用**。发布操作位于应用配置页右上角，发布后可获取 API Endpoint。
  - API 调用统一遵循 RESTful 规范，请求体需包含 `input`（消息数组）、`session_id` 等字段；文件需通过 `file_list`（URL）或 `session_file_id`（上传 API 返回 ID）传递 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
  - 高代码应用建议启用网关功能，通过自定义域名和 Token 鉴权接入生产环境。

## 限制和注意事项

- **功能限制**：
  - 智能体[长期记忆](../concepts/long-term-memory.md)功能当前未上线，仅支持短期记忆（0–30 轮）。
  - 工作流中 `imageList` 仅在启用“自定义缓存”的节点（如大模型、意图分类）中可用，其他节点无法直接访问。
  - 文件问答中，聊天窗口上传的文件**仅在当前会话有效**，刷新或关闭页面即失效；生产环境应使用 `session_file_id` 方式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **计费关键点**：
  - 模型调用费用按输入/输出 token 计费，其中知识库召回内容、文件解析文本、记忆体内容均计入输入 token（记忆体内容暂不计费）。
  - 工具调用（MCP/插件）可能产生额外费用，部分由第三方收取，百炼不代收。
  - 高代码应用部署后即开始计费，包括函数计算、API 网关、存储及模型调用。
- **安全与权限**：
  - 发布应用需确保 RAM 账号具备 `ram:CreateServiceLinkedRole` 权限，否则失败 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。
  - 环境变量（如 API Key）应在“环境”配置项中设置，避免硬编码于技能代码中。
- **调试建议**：
  - 新版智能体可通过“卡片流”查看完整 `Thinking → Tool Call → Reflection` 过程，是定位非预期行为的首选手段。
  - 工作流调试应逐节点验证输出变量（如 `大模型1/result`），利用会话变量追踪数据流向。
  - 文件问答若结果不准确，优先检查是否因 token 截断导致信息丢失，或切换至 `切片检索` 模式优化长文档处理。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


