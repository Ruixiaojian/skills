# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可基于零代码、低代码或专业代码方式，快速集成知识库、MCP 工具、记忆、[数据连接](../concepts/data-connection.md)器等能力，构建可落地的 AI 服务。三者并非互斥，而是按需组合使用的分层能力体系。

## 支持的模型与功能

### 核心应用类型
- **智能体（Agent）**：以提示词驱动，支持自主规划、工具调用与多步推理。新版智能体（Agent 2.0）将知识库、MCP 统一为可调度工具，显著提升过程透明度与复杂任务处理能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，适用于审批流、报告生成、意图路由等固定链路场景。支持大模型节点、意图分类、变量处理、智能体群组等多种节点类型 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：面向专业开发者，支持完整 Python 项目部署为 Serverless 或 K8s 服务，提供 MCP 一站式接入、自定义前端（Spark Design）、可观测性及企业级运维能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

### 文件处理能力
智能体支持三种文件问答模式：
- **全文引用**：解析后整段注入上下文，适合短文档总结；
- **切片检索（RAG）**：对长文档切片并检索相关片段，降低 [Token](../concepts/token.md) 消耗，推荐用于知识库增强场景；
- **自定义处理**：模型自主决策是否调用 MCP/插件处理文件（如图片风格转换、视频分析），需显式配置工具 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（`single-agent-application.md`）中仍将“插件”作为独立能力描述，而文档 2（`new-single-agent-application.md`）已明确将插件统一纳入 MCP 协议体系，并强调“所有外部工具均以 MCP 协议接入”。实际开发应以新版 Agent 2.0 的 MCP 架构为准，旧版插件概念已逐步收敛。

### 模型支持范围
- **文本模型**：千问 Max/Plus/Turbo/Long、Qwen3-Coder-Plus、Qwen3/Qwen2.5/Qwen2 开源系列、QwQ 系列、DeepSeek 等；
- **多模态模型**：千问 VL-Max/Plus/OCR，支持直接解析图片/视频，即使关闭预解析亦可生效；
- **视觉专用模型**：仅限 VL 系列，其他文本模型处理图像需依赖 `自定义处理` + 外部工具。

## 关键参数

| 参数 | 作用 | 适用场景 | 说明 |
|------|------|----------|------|
| `enable_thinking` | 控制是否启用模型内部反思机制 | Agent 2.0 | 仅支持思考模式的模型（如千问-Max）可配置；开启后展示“思考→工具调用→反思”链路 |
| `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数 | Agent 2.0 | 超限后强制终止工具链并生成最终回复，防止死循环 |
| `短期记忆轮数`（0–30） | 控制多轮对话上下文长度 | Agent 2.0 / Workflow | 0 表示不传递历史；轮数越多相关性越强，但输入 [Token](../concepts/token.md) 增加 |
| `单文件最大解析长度` / `最大拼装长度` | 控制全文引用模式下 token 截断策略 | 文件问答 | 截断从文件末尾开始，需结合文件长度合理设置，否则丢失关键信息 |
| `召回片段数` / `最大拼装长度`（切片检索） | 控制 RAG 检索精度与上下文开销 | 文件问答 / 知识库 | 超限时按相关性得分丢弃低分片段 |

## 使用方式

### 创建与配置
- **智能体**：控制台 → 应用管理 → 创建应用 → 选择 **Agent 2.0**（推荐）；模型选择后，通过「规划」模块配置知识库、MCP、文件处理、技能等能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流**：拖拽节点（开始/大模型/意图分类/结束等）→ 连线编排 → 在大模型节点中配置模型、提示词、用户提示词（支持 `${sys.query}` 变量）→ 启用「自定义缓存」实现跨节点记忆 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：控制台创建 → 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）→ 在「工具」Tab 中关联知识库、MCP 等服务 → 通过「网关」发布生产 API [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

### API 调用前提
- 所有应用必须**先发布**（非草稿状态）方可调用；
- 文件问答 API 不支持动态切换处理模式，严格遵循应用内保存的配置（全文引用/RAG/自定义）；
- 文件上传推荐使用 `session_file_id` 方式（调用文件上传 API 获取），而非直接传公网 URL，以保障大文件稳定性与安全性 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制与注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，**无法升级或降级**，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **文件时效性**：聊天窗口上传的文件仅在**当前会话有效**，刷新或关闭即失效；通过 `session_file_id` 上传有效期为 24 小时；URL 方式依赖源地址长期可用。
- **[Token](../concepts/token.md) 计费差异**：
  - 全文引用模式：文件内容全量计入输入 Token，成本最高；
  - 切片检索模式：仅问题 + 检索片段计入输入，成本可控；
  - 自定义处理模式：Token 消耗取决于工具调用轮次与返回结果长度。
- **工具超时**：自定义 MCP/插件默认超时为 5 秒，超时将中断调用并可能影响智能体决策 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域），其他地域暂不可用 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


