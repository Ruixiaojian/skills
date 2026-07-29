# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可按需选择零代码、低代码或专业编码方式，快速构建具备知识增强、工具调用、多步推理与企业级运维能力的生产级 AI 服务。

## 支持的模型/功能

百炼 LLM Application 支持三类核心构建模式，各自适配不同技术栈与业务复杂度：

- **智能体（Agent）应用**：以提示词驱动，支持自主意图理解、多步规划与工具调度。新版智能体（Agent 2.0）将知识库、MCP 服务统一为可规划调用的工具，显著提升过程透明性与任务泛化能力；旧版（Agent 1.0）则采用“先检索后决策”的串行逻辑，适合意图单一、流程固定的场景。详细对比见 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **工作流（Workflow）应用**：基于可视化节点编排，支持大模型节点、意图分类、变量处理、智能体群组等十余类节点，实现确定性、可复现的多步骤自动化。典型场景包括诈骗识别、智能导购、日程管理等，其执行链路完全由预定义逻辑控制，不依赖模型动态规划 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向专业开发者，提供完整的 Python 工程化部署能力，支持 Serverless Function 与 K8s 两种运行时，内置 MCP 工具接入、前端定制（Spark Design）、API 网关与可观测性等企业级能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有模式均支持主流千问系列模型（如 Qwen-Max、Qwen-Plus、Qwen-VL 系列），并兼容部分 DeepSeek 及开源模型。文件问答能力覆盖文档、图片、音视频，提供全文引用、切片检索（RAG）和自定义处理三种模式，具体支持格式与参数详见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 2 与文档 3 对智能体能力描述存在关键差异——文档 2 将知识库与插件视为独立能力模块，而文档 3 明确将其统一为“工具”并纳入 ReAct 规划调度体系。实际开发应以 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 的架构为准，旧版已不推荐新项目使用。

## 关键参数

| 类别 | 参数名 | 说明 | 可配置位置 |
|--------|---------|------|-------------|
| **模型层** | `temperature` | 控制生成随机性，取值 0–2，推荐 0.1–0.7 保证稳定性 | 智能体/工作流节点的模型参数配置器 |
| | `enable_thinking` | 是否开启思考模式（仅限支持模型），影响规划链路可视化 | [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 的模型参数配置器 |
| | `ReAct 最大轮次` | 单次会话中工具调用最大次数（1–50），超限则终止调用并生成终局回复 | 新版智能体「运行与结果分析」区域 |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下，单个文件提取 token 上限，超出从末尾截断 | [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 的全文引用配置页 |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下，控制 RAG 检索精度与上下文开销 | [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 的切片检索配置页 |
| **会话控制** | `短期记忆轮数` | 新版智能体支持 0–30 轮上下文传递，0 表示禁用多轮记忆 | [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 的「记忆」配置项 |
| | `historyList` / `imageList` | 工作流预置会话变量，用于跨节点传递对话历史与图片列表 | [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 的「开始/结束」节点说明 |

## 使用方式

### 创建与配置
- **智能体**：控制台 → 应用管理 → 创建应用 → 选择「智能体应用」→ 优先选用 Agent 2.0；配置模型、系统提示词、知识库（作为工具）、MCP 服务及技能。
- **工作流**：控制台 → 应用管理 → 创建应用 → 选择「工作流应用」→ 拖拽节点（开始/大模型/意图分类/结束等）→ 连线配置 → 启用「自定义缓存」以支持多轮上下文。
- **高代码应用**：控制台 → 创建应用 → 选择「高代码应用」→ 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）与资源规格 → 一键部署。

### 发布与调用
- 所有应用**必须发布后方可调用**（未发布状态仅支持控制台调试）。发布操作位于应用配置页右上角「发布」按钮，发布前需确认 RAM 权限（如 `ram:CreateServiceLinkedRole`）。
- API 调用路径统一：应用详情页 → 「发布渠道」页签 → 「API 调用」→ 查看 endpoint 与鉴权方式（Bearer [Token](../concepts/token.md) + API Key）。
- 文件上传支持三种方式：聊天窗口直接上传（会话级有效）、`file_list`/`image_list` 传公网 URL（需 OSS 等可公开访问）、调用文件上传 API 获取 `session_file_id`（推荐生产环境使用）。

### 集成扩展
- 智能体与工作流均可通过「应用组件」能力复用已发布应用（如将智能体嵌入工作流作为子节点）。
- 高代码应用支持通过「工具」Tab 一站式关联知识库、MCP 服务，并在代码中调用 `agentscope` SDK 实现深度集成。
- 所有模式均支持发布至钉钉、微信公众号等第三方渠道，或通过 API 网关暴露为标准 RESTful 接口。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；聊天窗口上传的文件仅在当前会话有效，刷新即失效；通过 `session_file_id` 上传的文件有效期为 24 小时。
- **调用限频**：每个智能体应用默认限流 100 次/分钟，该配额被所有 API 请求共享（含文件问答、普通对话等）。
- **模型兼容性**：`enable_thinking` 参数仅对 Qwen-Max 等明确标注支持思考模式的模型生效；千问-VL 系列模型在「自定义处理」模式下可直接解析图片，无需开启预解析。
- **计费要点**：
  - 模型调用费用按输入/输出 [Token](../concepts/token.md) 计费，RAG 检索内容、[长期记忆](../concepts/long-term-memory.md)体、文件解析文本均计入输入 [Token](../concepts/token.md)；
  - 知识库、MCP 服务、工具调用可能产生独立费用（如第三方 API 费用由服务商收取）；
  - 上下文缓存仅支持隐式缓存（自动生效，按 20% 输入单价计费），暂不支持显式缓存配置。
- **版本隔离**：Agent 1.0 与 Agent 2.0 架构不兼容，无法升级或降级，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


