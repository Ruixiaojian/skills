# llm application

百炼平台的 LLM Application 是面向业务场景构建 AI 应用的核心能力层，提供智能体（Agent）、工作流（Workflow）和高代码应用三种范式，分别覆盖零代码决策、低代码编排与专业级代码开发需求。三者统一基于大模型驱动，通过知识库增强、工具调用（MCP/插件）、多模态[文件处理](../concepts/file-processing.md)及记忆机制等能力扩展模型边界，支持从快速原型到生产级服务的全周期落地。

## 支持的模型/功能

- **智能体（Agent）**：以提示词驱动自主规划，支持动态工具调度（知识库、MCP、内置沙箱工具）、多轮上下文记忆（短期记忆 0–30 轮）、文件自定义处理（全文引用/切片检索/自定义处理）及技能（Skill）封装。新版 Agent 2.0 将知识库与 MCP 统一为可规划工具，显著提升复杂任务处理能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，支持大模型节点、意图分类、变量处理、智能体群组等核心节点，并可跨节点共享会话变量（如 `query`、`historyList`、`imageList`）。适用于需强可控性的自动化场景，如诈骗识别、智能导购、日程管理等 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向开发者提供完整 Python 工程部署能力，支持 Serverless Function 与 K8s 两种部署方式，集成 MCP 工具接入、API 网关、可观测性及 Spark Design 前端框架，可一键发布为公网可访问的 AI 后端服务 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先选用 Agent 2.0，旧版仅用于存量维护。

支持的模型按能力分层：
- **工具调用与多步规划**：推荐 `千问-Max` 系列（如 `qwen-max-latest`），需启用 `enable_thinking` 参数以激活 ReAct 链路；
- **多模态理解**：`千问-VL-Max`/`VL-Plus`/`VL-OCR` 可直接解析图片/视频，无需预解析；
- **长文本处理**：`千问-Long` 适配全文引用模式；`千问-Plus`/`Turbo` 平衡效果与成本，广泛用于工作流节点；
- **代码与推理**：`千问3-Coder-Plus` 在工具调用与代码生成场景表现更优。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `enable_thinking` | 智能体（Agent 2.0） | 开启后展示“思考→工具调用→反思”全过程，仅对支持思考模式的模型生效；[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 明确指出该参数不可在不支持模型上配置。 |
| `ReAct 最大轮次`（1–50） | 智能体（Agent 2.0） | 限制单次会话中工具调用总次数，超限则终止调用并生成最终回复；是防止无限循环的关键安全阈值。 |
| `单文件最大解析长度` / `最大拼装长度`（token） | 文件问答（全文引用模式） | 控制文件内容截断位置（末尾截断），直接影响输入 [Token](../concepts/token.md) 消耗与信息完整性；超长文件建议切换至切片检索模式。 |
| `召回片段数` / `最大拼装长度`（切片检索） | 文件问答 & 知识库 | 决定 RAG 检索结果的数量与总长度，系统按相关性得分从低到高丢弃片段以满足长度限制。 |
| `记忆`（自定义缓存 / 本节点缓存） | 工作流节点（大模型/意图分类） | 全局记忆需选“自定义缓存”，否则仅保留当前节点内对话历史；与智能体短期记忆逻辑不同，工作流记忆依赖显式配置。 |

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用（Agent 2.0）” → 配置模型、系统提示词、知识库、MCP 及[文件处理](../concepts/file-processing.md)模式；
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接执行流 → 配置各节点参数（含变量引用 `${sys.query}`）→ 测试并发布；
  - 高代码：控制台创建空白应用 → 选择部署方式（Serverless/K8s）→ 提交模版代码或 `.whl` 包 → 部署后通过 API 或文本对话测试。

- **API 调用**：
  - 所有应用必须**先发布**方可调用（见各文档“重要”提示）；
  - 智能体/工作流 API 请求需携带 `Authorization: Bearer <API Key>`，参数结构统一为 `input` 数组（含 role/content）；
  - 文件上传推荐使用 `session_file_id`（调用文件上传 API 获取），而非直接传公网 URL，以规避访问限制与超时问题 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

- **调试与验证**：
  - 智能体：右侧对话窗口实时查看卡片流（Thinking/Tool Call），支持回溯每一步决策；
  - 工作流：点击“测试”按钮，输入 query 观察各节点输出与变量传递；
  - 高代码：部署页右侧面板提供“文本对话体验”与“API 测试”，支持手动构造请求。

## 限制和注意事项

- **[文件处理](../concepts/file-processing.md)限制**：
  - 单会话最多上传 10 个文件，单文件 ≤10MB；刷新页面即丢失会话文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 全文引用模式下，文件内容直接计入模型输入 [Token](../concepts/token.md)，易触发上下文超限；切片检索模式更经济，但效果依赖切片策略与检索质量。

- **计费关键点**：
  - 模型调用费用 = 输入 [Token](../concepts/token.md) + 输出 Token × 对应单价，知识库召回内容、记忆体内容、文件解析文本均计入输入 Token；
  - MCP 工具调用可能产生额外费用（如第三方 API），百炼仅收取模型调用费；
  - 高代码应用部署后即开始计费（函数实例、网关、存储等），停止服务可暂停费用。

- **安全与权限**：
  - 应用发布需 RAM 账号具备 `ram:CreateServiceLinkedRole` 权限（见文档 3）；
  - 生产环境建议关闭测试域名的“公网访问”，并通过 API 网关 + Token 鉴权控制访问；
  - 自定义 MCP 或插件超时限制为 5 秒（见文档 3），需确保外部服务响应及时。

- **版本与兼容性**：
  > **注意**：Agent 1.0 与 Agent 2.0 不兼容，无法升级。若需新特性，必须新建 Agent 2.0 应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  > **注意**：工作流中“智能体群组”节点调用的子智能体必须已**发布**，未发布状态将导致节点执行失败（见文档 5 案例三）。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)


