# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建能力，旨在突破大语言模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可基于提示词、可视化编排或 Python 代码，快速集成知识库、MCP 工具、记忆等能力，构建生产级 AI 应用。所有模式均需发布后方可通过 API 或前端渠道调用。

## 支持的模型/功能

百炼 `llm application` 支持三类应用形态，各自适配不同开发范式与业务场景：

- **智能体（Agent）应用**：以提示词驱动，支持自主意图理解、多步规划与工具调用（如知识库、MCP、内置沙箱工具）。新版 Agent 2.0 将知识库与 MCP 统一为可规划工具，并完整展示“思考-执行-反思”链路，显著优于旧版 Agent 1.0 的固定调度逻辑 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。适用于开放式对话、动态任务助理等场景。
  
- **工作流（Workflow）应用**：通过可视化节点（大模型、意图分类、变量处理等）编排确定性执行流，支持多轮记忆、会话变量传递与子智能体嵌套。典型用于结构化流程自动化，如诈骗识别、智能导购、日程管理 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向专业开发者，支持上传 `.whl` 代码包或使用模板，基于 Python 构建 Serverless Function 或 K8s 部署的 AI 后端服务。提供一站式 MCP 接入、可观测性、API 网关及 Spark Design 前端框架 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 3（[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)）中仍将“插件”作为独立能力描述，而文档 2 明确指出新版 Agent 已统一采用 MCP 协议接入外部工具（含原插件），且旧版 Agent 1.0 与新版 Agent 2.0 不兼容、无法升级。实际开发应优先采用 Agent 2.0 架构。

[文件处理](../concepts/file-processing.md)能力覆盖全文引用、切片检索（RAG）和自定义处理三种模式，支持文档、图片、音视频等多模态输入，具体能力与模型强相关：千问-VL 系列模型可直接解析图片/视频，无需预解析；而文本模型依赖预解析开关控制是否提取内容 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置范围/备注 |
|----------|--------|------|-----------------|
| **模型层** | `temperature` | 控制生成随机性，值越高越多样 | 0.0–1.0，默认 0.8 |
| | `max_tokens` | 模型输出长度上限（不含输入） | 正整数，受模型最大上下文限制 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | true/false，影响 ReAct 过程展示 |
| **[文件处理](../concepts/file-processing.md)** | `单文件最大解析长度（token）` | 全文引用模式下单文件截断位置 | 从文件末尾截断，需避免关键信息丢失 |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 输入规模 | 影响精度与 [Token](../concepts/token.md) 成本平衡 |
| **执行控制** | `ReAct 最大轮次` | 单次会话中工具调用总次数上限 | 1–50，超限则终止调用并生成终答 |
| | `短期记忆轮数` | 多轮对话中保留的历史消息数 | 0–30，0 表示无上下文，轮数越多 [Token](../concepts/token.md) 消耗越高 |
| **安全与鉴权** | 环境变量 | 用于注入技能调用所需的密钥、Endpoint 等敏感参数 | 在“环境”配置页设置，避免硬编码 |

## 使用方式

1. **创建与配置**  
   - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → 选 Agent 2.0 → 配置模型、系统提示词、知识库、MCP 工具等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
   - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连线定义执行流 → 配置各节点模型、提示词、记忆策略 → 测试后发布。  
   - 高代码：选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 部署后通过 API 测试或网关暴露服务。

2. **调试与测试**  
   - 所有应用均支持右侧对话面板实时调试，智能体可查看卡片式推理轨迹，工作流可逐节点查看输出，高代码支持文本对话与 `curl` API 测试。

3. **发布与调用**  
   - **必须发布**：未发布应用无法被 API、钉钉、微信等渠道调用。发布时会校验变更差异。  
   - **API 调用**：发布后进入“发布渠道”页签 → “API 调用” → 获取 endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）。文件需通过 `file_list`（URL）或 `session_file_id`（上传 API 返回）传入，**不可在 API 请求中动态切换[文件处理](../concepts/file-processing.md)模式** [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
   - **生产集成**：高代码应用推荐启用 API 网关并关闭测试域名公网访问；工作流与智能体可通过 SDK 或标准 HTTP 调用。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；聊天窗口上传的文件仅在当前会话有效，刷新即失效；生产环境推荐使用文件上传 API 获取 `session_file_id` [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费逻辑**：  
  - 模型调用费用按输入/输出 Token 计费，知识库召回内容计入输入 Token；  
  - 工具调用（MCP/插件）单独计费，部分涉及第三方 API 的费用由第三方收取；  
  - 高代码应用部署后即开始计费（函数、网关、存储、模型调用）；  
  - **[长期记忆](../concepts/long-term-memory.md)存储免费，但其内容注入 Prompt 后产生的 Token 消耗暂不计费**（见文档 3 计费说明）。  
- **版本与兼容性**：  
  > **注意**：Agent 1.0 与 Agent 2.0 架构不兼容，**不支持升级**。若需新特性，必须新建 Agent 2.0 应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **API 限流**：每个智能体应用默认限流 100 次/分钟，该配额共享于所有 API 请求（含文件问答、普通对话等）。  
- **地域限制**：文件问答功能目前仅支持中国大陆版（北京地域），其他地域可能不可用。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


