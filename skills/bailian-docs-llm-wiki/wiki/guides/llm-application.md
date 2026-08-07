# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可基于零代码、低代码或专业编码方式，快速集成知识库、MCP 工具、多模态能力与外部系统，构建可落地的生产级 AI 应用。所有模式均统一运行于百炼托管环境，共享模型调用、可观测性与企业级运维能力。

## 支持的模型/功能

百炼 LLM Application 支持三类核心构建模式，各自适用不同抽象层级与开发能力：

- **智能体（Agent）应用**：以提示词驱动，由大模型自主理解意图、规划步骤并动态调用工具（知识库、MCP、内置沙箱工具等）。适用于开放式对话、任务助理、旅行规划等需动态决策的场景。新版智能体（Agent 2.0）将知识库与 MCP 统一为可规划工具，并支持完整“思考-执行-反思”链路回溯，显著优于旧版 Agent 1.0 的固定调度逻辑 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  
- **工作流（Workflow）应用**：通过可视化节点编排（如大模型、意图分类、变量处理、智能体群组等）定义确定性执行路径。适用于报告生成、订单审批、多步骤客服等流程固化、结果可复现的自动化任务 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向专业开发者，支持上传 Python 项目（`.whl` 包）部署为 Serverless Function 或 K8s 服务，提供完整 API 网关、自定义前端（Spark Design）、MCP 一站式接入及可观测能力，适合深度定制与系统集成 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有模式均支持主流千问系列模型（Qwen-Max/Plus/Turbo/Long/VL 等）、DeepSeek 及开源模型；文件处理支持文档、图片、音视频（单文件 ≤10MB），具体格式详见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（智能体应用）中提及“插件”作为独立能力单元，而文档 2（新版智能体应用）明确将插件统一纳入 MCP 协议体系，并强调“插件支持一键转换为 MCP 服务”。二者存在术语演进，**应以新版智能体文档为准，统一使用 MCP 概念**。

## 关键参数

| 参数类别 | 关键项 | 说明 | 适用模式 |
|----------|--------|------|----------|
| **模型配置** | `temperature`、`max_tokens`、`enable_thinking` | 温度系数控制输出随机性；最长回复长度限制生成 token 数；`enable_thinking` 仅对支持思考模式的模型（如 Qwen-Max）生效，用于开启 ReAct 推理链路 | Agent（2.0） |
| **文件处理** | 全文引用 / 切片检索 / 自定义处理 | 全文引用直接拼接解析后文本（受上下文长度限制）；切片检索（RAG）按相关性召回片段；自定义处理交由模型自主调用 MCP 工具处理 | Agent（2.0）、文件问答场景 |
| **工具调度** | `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数，超限则终止调用并生成最终回复 | Agent（2.0） |
| **记忆** | 短期记忆轮数（0–30） | 控制多轮对话中传递的历史消息数量；0 表示不传递上下文 | Agent（2.0） |
| **会话变量** | `query`、`historyList`、`imageList` | 工作流全局预置变量，用于接收用户输入、维护对话历史与图片列表，可在各节点中引用 | Workflow |
| **部署资源** | vCPU/内存/最小实例数/并发度 | 高代码应用资源配置项，影响性能与成本；Serverless Function 适合无状态轻量场景，K8s 适合长程有状态任务 | Rich Code |

## 使用方式

1. **创建与配置**  
   - 在控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面选择对应类型创建应用。  
   - Agent 2.0 推荐选用 `Qwen-Max` 等强工具调用模型；Workflow 需拖拽节点并配置模型、提示词与变量映射；高代码应用支持控制台模板创建或 CLI 上传 `.whl` 包。

2. **能力扩展**  
   - Agent：通过“知识库”、“MCP”、“应用组件”（已发布的工作流/智能体）、“技能”模块挂载能力；文件处理在“规划 > 文件处理”中配置模式与参数。  
   - Workflow：通过“智能体群组”节点集成已发布的智能体，实现子任务分解；利用“会话变量”跨节点共享数据。  
   - Rich Code：在“工具”Tab 中关联知识库/MCP，在“前端”Tab 中基于 Spark Design 构建 WebUI。

3. **测试与发布**  
   - 所有模式均支持右侧调试面板实时对话测试。  
   - **发布是调用前提**：点击右上角“发布”按钮完成发布，之后方可通过 API、钉钉、微信或网关访问。未发布应用无法被外部调用。

4. **API 调用**  
   - Agent 2.0：参考 [新版智能体应用 API](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；  
   - Workflow：参考 [调用工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)；  
   - Rich Code：通过 `/process` 接口提交 `input`（含 role/content 结构化消息）与 `session_id`。

## 限制和注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 基于不同架构，**不支持升级/降级**，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件有效期**：聊天窗口上传的文件仅在**当前会话有效**，刷新或关闭即失效；通过 `session_file_id` 上传的文件有效期为 24 小时；URL 方式依赖源地址可用性 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费范围**：仅调用产生费用（模型 [Token](../concepts/token.md)、知识库检索、MCP 调用），创建/配置不收费；[长期记忆](../concepts/long-term-memory.md)内容占用 [Token](../concepts/token.md) **暂不计费**，但会增加模型输入消耗 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **限流策略**：每个智能体应用默认 **100 次/分钟** API 调用配额，该配额为应用级共享，涵盖所有接口请求 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **安全约束**：内置沙箱工具（`bash`/`write`/`read` 等）在隔离环境中运行，禁止访问宿主机敏感路径；自定义 MCP 需确保第三方服务鉴权安全。  
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域） [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


