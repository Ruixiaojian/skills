# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程可控性及复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可基于零代码、低代码或专业编码方式，快速集成知识库、MCP 工具、记忆、数据连接器等能力，构建可落地的 AI 服务。所有应用均需发布后方可调用，计费以模型调用、知识库、MCP 等实际资源消耗为准。

## 支持的模型与功能

- **模型支持**：  
  - 智能体与工作流应用推荐使用 `千问-Max`、`千问-Plus-Latest` 等具备强工具调用与多步规划能力的模型；`千问-VL` 系列模型原生支持图片/视频解析，即使关闭预解析也可直接处理视觉文件 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 文件问答场景支持文本模型（如 `千问Turbo`、`千问Long`）及视觉模型（如 `千问VL-Max`、`千问VL-OCR`），具体以控制台实时列表为准 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。  
  - 高代码应用支持所有百炼托管模型，并可通过 MCP 协议接入自定义部署模型 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **核心功能**：  
  - **智能体（Agent）**：以提示词驱动自主决策，统一调度知识库、MCP、内置工具（`bash`/`read`/`edit` 等）及技能（Skill），支持 ReAct 多轮规划与过程可视化回溯。  
  - **工作流（Workflow）**：通过可视化节点编排（大模型、意图分类、变量处理、智能体群组等）实现确定性流程，支持会话变量全局共享与多轮记忆（`historyList`/`imageList`）。  
  - **高代码应用**：基于 Python 项目一键部署为 Serverless Function 或 K8s 服务，支持 MCP 工具一站式接入、自定义前端（Spark Design）、API 网关及企业级可观测能力。

> **注意**：文档 2 与文档 3 对智能体版本的描述存在关键差异——文档 2 明确指出“旧版智能体（Agent 1.0）与新版（Agent 2.0）基于不同技术架构，彼此不兼容，无法升级”，而文档 3 未提及此限制且仍提供 Agent 1.0 的独立入口。实际开发中应以文档 2 的结论为准，新项目务必选用 Agent 2.0。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用场景 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制生成随机性，值越高输出越多样 | 所有应用类型通用 |
| | `enable_thinking` | 开启后支持模型展示推理链（Thinking step），仅限支持思考模式的模型 | 新版智能体（Agent 2.0） |
| | `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数，超限则终止调用并生成最终回复 | 新版智能体 |
| **文件处理** | `单文件最大解析长度` / `最大拼装长度` | 全文引用模式下控制 token 截断位置（从文件末尾截断） | [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 检索结果数量与总 token 上限 | 同上 |
| **记忆与上下文** | 短期记忆轮数（0–30） | 控制多轮对话上下文窗口大小，0 表示禁用 | 新版智能体 |
| | `自定义缓存`（工作流） | 启用后模型可跨节点记住全局对话历史（`historyList`） | 工作流应用中的大模型/意图分类节点 |

## 使用方式

- **创建与配置**：  
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择 **智能体应用 > Agent 2.0**，配置模型、系统提示词、知识库、MCP 及工具 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）构建执行链路，通过 `${sys.query}` 引用用户输入，用 `/` 插入节点输出变量 [原文标题](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 高代码：选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）、资源规格及 MCP 工具，部署后通过 API 测试或网关发布 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **调用前提**：  
  所有应用必须先点击 **发布** 按钮完成发布，才能通过 API、SDK 或第三方渠道（钉钉/微信公众号）调用。未发布应用无法访问。

- **文件交互**：  
  智能体支持三种文件处理模式：  
  - **全文引用**：解析后全文注入 [prompt](prompt.md)，适合短文档总结；  
  - **切片检索（RAG）**：检索相关片段，适合长文档精准问答；  
  - **自定义处理**：模型自主调用 MCP/插件处理文件（如图片风格转换），需提前挂载对应工具。

## 限制与注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；上传文件仅在当前会话有效，刷新页面即失效 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。生产环境推荐使用 `session_file_id` 方式上传大文件。
- **工具超时**：自定义插件调用超时限制为 5 秒，超时将中断执行 [原文标题](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **[长期记忆](../concepts/long-term-memory.md)**：新版智能体暂不支持[长期记忆](../concepts/long-term-memory.md)功能，该能力计划在未来迭代中上线；当前仅支持短期记忆（0–30 轮上下文）。
- **计费要点**：  
  - 知识库召回内容计入模型输入 token，可能增加推理费用；  
  - 隐式缓存自动生效（公共前缀按 20% 计费），但显式缓存暂不支持；  
  - MCP 服务若涉及第三方 API（如天气、地图），其费用由第三方收取，百炼不代收。
- **地域限制**：文件问答功能目前仅支持中国大陆版（北京地域）[原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


