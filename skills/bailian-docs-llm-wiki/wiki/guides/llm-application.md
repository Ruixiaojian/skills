# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。它提供三种互补的技术路径：以提示词驱动自主决策的智能体（Agent）、以可视化节点编排实现确定性执行的工作流（Workflow），以及面向专业开发者的高代码应用（Rich Code）。三者统一基于 MCP 协议集成外部能力，并共享知识库、记忆、[数据连接](../concepts/data-connection.md)器等基础设施。

## 支持的模型与功能

- **模型支持**：所有 LLM Application 类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-*`）及部分开源/第三方模型。其中，新版智能体（Agent 2.0）**强烈推荐使用具备强[工具调用](../concepts/tool-use.md)能力的模型**（如 `千问-Max` 系列），以保障多步规划效果；而文件问答场景需按文件类型匹配模型——文本类任务适用 `qwen-plus` 等文本模型，图片理解必须选用 `千问-VL` 系列视觉模型 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **核心能力矩阵**：
  - **智能体（Agent）**：支持知识库（RAG）、MCP 工具（含官方 MCP 广场与自定义服务）、内置沙箱工具（`bash`/`read`/`write` 等）、技能（Skill）、短期记忆（0–30 轮）、预解析文件（全文引用/切片检索/自定义处理）及环境变量注入 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - **工作流（Workflow）**：通过节点化编排组合大模型、意图分类、变量处理、智能体群组等能力，支持会话变量全局传递、自定义缓存记忆及多模态输入（`query`/`historyList`/`imageList`） [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - **高代码应用**：基于 Python 项目部署 Serverless Function 或 K8s 服务，支持 MCP 一站式接入、自定义前端（Spark Design）、API 网关、可观测性及企业级运维能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先采用 Agent 2.0，旧版仅用于存量维护。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用场景 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制生成随机性，值越高输出越多样 | 所有应用类型通用 |
| | `enable_thinking` | 开启思考模式以增强反思能力，**仅支持特定模型** | 新版智能体（Agent 2.0） |
| | `ReAct 最大轮次`（1–50） | 限制单次会话中[工具调用](../concepts/tool-use.md)总次数，超限则终止调用链 | 新版智能体 |
| **文件处理** | `单文件最大解析长度` / `最大拼装长度` | 全文引用模式下截断策略参数，单位为 token | 文件问答（智能体） |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 检索范围与上下文长度 | 文件问答（智能体） |
| **记忆与会话** | 短期记忆轮数（0–30） | 控制多轮对话上下文窗口大小 | 新版智能体、工作流（需启用“自定义缓存”） |
| | `historyList` 变量 | 工作流中预置的对话历史列表，供支持记忆的节点引用 | 工作流应用 |

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择 **智能体应用 > Agent 2.0** → 配置模型、系统提示词、知识库、MCP 等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接执行流 → 在节点内配置模型、提示词、变量映射 → 发布后测试 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - 高代码应用：控制台创建 → 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 部署后通过 API 测试或网关发布 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **调用方式**：
  - 所有应用**必须先发布**才能被调用（发布是前提条件）。
  - API 调用统一通过「发布渠道」页签获取 endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）。
  - 文件上传支持三种方式：聊天窗口直传（会话级有效）、`file_list`/`image_list` URL 参数（需公网可访问）、`session_file_id`（推荐生产环境，通过文件上传 API 获取） [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制与注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；聊天窗口上传的文件**仅在当前会话有效**，刷新即失效；生产环境务必使用 `session_file_id` 方式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **计费逻辑**：
  - 模型调用费用按实际输入/输出 [Token](../concepts/token.md) 计费，**知识库召回内容、记忆体内容、预解析文本均计入输入 [Token](../concepts/token.md)**；
  - 工作流中每个节点独立触发模型调用，复杂流程可能产生多次计费；
  - MCP 工具费用分两类：百炼官方 MCP 按模型调用计费；第三方 MCP 产生的费用由第三方收取，百炼不代收 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **能力边界**：
  - 新版智能体**暂不支持[长期记忆](../concepts/memory.md)**（计划未来迭代）；
  - 自定义插件超时限制为 **5 秒**（旧版智能体文档明确说明）；
  - 工作流中“智能体群组”节点依赖子智能体已**发布**，未发布的智能体无法被引用 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **地域限制**：文件问答功能目前**仅支持中国大陆版（北京地域）** [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


