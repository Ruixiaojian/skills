# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建范式，旨在突破大语言模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三类核心模式，开发者可基于零代码、低代码或专业编码方式，快速集成知识库、MCP 工具、记忆、[多模态](../concepts/multi-modal.md)能力等，构建可控、可复现、可运维的生产级 AI 应用。

## 支持的模型/功能

- **模型支持**：  
  - 智能体与工作流应用主要支持千问系列模型（如 `千问-Max`、`千问-Plus-Latest`、`千问-VL-Max`），其中新版智能体（Agent 2.0）[推荐选用具备强工具调用能力的模型](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，如 `千问-Max`；工作流节点明确要求模型支持多轮记忆与结构化输出（见[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)案例中统一选用 `千问-Plus-latest`）；高代码应用支持所有百炼平台已上线文本及[多模态](../concepts/multi-modal.md)模型。  
  - 文件问答能力依赖模型类型：文本模型仅支持文档/音视频内容解析；视觉理解模型（如 `千问VL-Max`）可直接处理图片并支持“模型处理+规划”双路径 [详见文件问答文档](../../raw/application-user-guide/llm-application/file-q-a.md)。

- **核心功能**：  
  - **智能体（Agent）**：以提示词驱动自主规划，统一调度知识库、MCP、内置工具（`bash`/`read`/`edit` 等沙箱能力）、数据连接器与应用组件；支持短期记忆（0–30 轮）、ReAct 最大轮次限制（1–50）、思考链（Thinking）可视化；新版 Agent 2.0 将知识库作为可规划工具，支持标签过滤 [参见新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - **工作流（Workflow）**：通过可视化节点编排（开始/结束/大模型/意图分类/变量处理/智能体群组等）实现确定性流程；支持会话变量（`query`/`historyList`/`imageList`）全局传递、自定义缓存记忆、多分支条件路由；典型用于客服分流、日程管理、智能导购等固定路径场景 [见工作流应用文档](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - **高代码应用**：基于 Python 项目部署 Serverless Function 或 K8s 服务；支持 MCP 工具一站式接入、Spark Design 前端框架定制、API 网关生产发布；适用于需深度集成企业系统、私有算法或长时运行任务的场景 [参考高代码应用指南](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 2（旧版智能体）与文档 3（新版智能体）存在架构级不兼容——旧版将知识库与 MCP 分离调度，新版统一为工具并支持动态规划；二者无法升级/降级，必须重新创建 [原文明确说明：“不支持将旧版智能体升级到新版本”](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值范围/示例 |
|----------|--------|------|----------------|
| **模型层** | `temperature` | 控制生成随机性 | 0.0–1.0（默认 0.8） |
| | `max_output_tokens` | 模型单次回复最大长度 | ≥1（如 2048） |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | `true`/`false` |
| **[文件处理](../concepts/file-processing.md)** | 单文件最大解析长度（token） | 全文引用模式下截断位置 | 由模型上下文决定，建议 ≤ 8192 |
| | 召回片段数 | 切片检索模式下返回的最大相关片段数 | 1–10（默认 3） |
| | ReAct 最大轮次 | 智能体单次会话最多工具调用次数 | 1–50（默认 10） |
| **记忆与会话** | 短期记忆轮数 | 多轮对话保留的历史轮数 | 0–30（0 表示禁用） |
| | `historyList` / `imageList` | 工作流中预置的会话变量，用于跨节点传递上下文 | — |
| **安全与限流** | API 调用频率 | 每个智能体应用默认限流 | 100 次/分钟（含所有 API 请求） |

## 使用方式

- **创建与配置**：  
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择 **智能体应用（Agent 2.0）** → 配置模型、系统提示词、知识库/MCP/技能/环境变量 → 设置[文件处理](../concepts/file-processing.md)模式（全文引用/切片检索/自定义处理）→ 发布。  
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接执行流 → 在大模型节点中配置 `用户提示词`（如 `${sys.query}`）与 `记忆`（推荐选“自定义缓存”）→ 测试 → 发布。  
  - 高代码：控制台 → 创建高代码应用 → 选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）与资源 → 部署 → 在“工具”Tab 关联 MCP → 在“网关”Tab 开通生产域名。

- **调用方式**：  
  - 所有应用**必须先发布**方可调用（[发布是前提条件](../../raw/application-user-guide/llm-application/single-agent-application.md)）。  
  - API 调用：通过“发布渠道”页签获取 Endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）；文件需通过 `file_list`（通用文件 URL）、`image_list`（图片 URL）或 `session_file_id`（文件上传 API 返回 ID）传入；参数格式严格遵循 [文件问答 API 参考](../../raw/application-user-guide/llm-application/file-q-a.md)。  
  - 集成：支持钉钉/微信公众号嵌入、作为组件被其他智能体或工作流调用、通过 API 网关接入企业后端系统。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；聊天窗口上传的文件**仅当前会话有效**，刷新即失效；生产环境推荐使用 `session_file_id` 方式上传 [详见文件问答文档](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **模型上下文**：知识库检索结果、文件解析内容、记忆历史均计入模型输入 token；超限将触发截断（默认从末尾丢弃），可能导致信息丢失；切片检索模式比全文引用更节省 token。  
- **工具超时**：自定义[插件](../concepts/plugin.md)调用超时为 5 秒；MCP 服务超时取决于第三方实现，平台不干预。  
- **计费要点**：  
  - 仅调用产生费用，创建/配置不收费；  
  - 模型调用按输入+输出 token 计费；知识库检索本身按量计费（[知识库计费说明](../../raw/application-user-guide/llm-application/new-single-agent-application.md)）；MCP 若涉及第三方 API，费用由第三方收取；  
  - 上下文缓存支持隐式缓存（自动生效，命中部分 token 按 20% 计费），但**暂不支持显式缓存配置** [见新版智能体计费说明](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域） [原文明确标注](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


