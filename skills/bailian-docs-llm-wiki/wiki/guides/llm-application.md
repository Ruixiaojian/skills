# llm application

`llm application` 是阿里云百炼平台面向业务场景构建 AI 应用的核心抽象，它通过封装模型调用、外部能力集成与执行逻辑编排，使开发者无需从零实现推理服务即可快速交付具备私有知识理解、实时工具调用和多步任务规划能力的生产级 AI 应用。该能力覆盖零代码（智能体）、低代码（工作流）和专业代码（高代码）三类开发范式，适用于客服、报告生成、日程管理、内容创作等广泛业务场景。

## 支持的模型/功能

百炼 `llm application` 支持三大应用类型，各自适配不同复杂度与可控性要求：

- **智能体（Agent）应用**：以提示词驱动自主决策，支持动态规划、知识库检索（RAG）、MCP 工具调用、文件处理（全文引用/切片检索/自定义处理）及短期记忆。新版智能体（Agent 2.0）将知识库与 MCP 统一为可规划工具，并完整展示“思考-执行-反思”链路，显著提升复杂任务处理能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：通过可视化节点（大模型、意图分类、变量处理、智能体群组等）编排确定性执行流程，支持多轮对话状态维护（`historyList`）、会话变量全局共享及结构化输出控制，适合固定路径的自动化任务 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，基于 Python 项目一键部署为 Serverless Function 或 K8s 服务，支持 MCP 工具一站式接入、自定义前端（Spark Design）、API 网关与企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有类型均支持千问系列模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-plus`），其中[多模态](../concepts/multi-modal.md)任务需选用 `qwen-vl-*` 等视觉理解模型；文件问答功能明确支持 `.docx`、`.pdf`、`.png`、`.mp4` 等十余种格式，单文件上限 10MB [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在架构不兼容声明：“不支持将旧版智能体升级到新版本”，且新版已将知识库作为可规划工具纳入统一调度体系，而旧版仍将其视为独立模块。实际开发应优先采用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，旧版仅用于存量维护。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|-------------|
| **模型基础** | `temperature` | 控制生成随机性，取值 0–2，推荐 0.3–0.7 保证稳定性 | 模型选择器右侧参数配置器（[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)） |
| | `max_tokens` | 模型生成回复的最大长度（不含提示词） | 同上 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用），影响 ReAct 过程中“Thinking”步骤的展示 | 同上 |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下单文件截断阈值，超长部分从末尾丢弃 | 文件处理配置面板（[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)） |
| | `召回片段数` | 切片检索模式下返回的相关文本片段数量上限 | 同上 |
| **执行控制** | `ReAct 最大轮次` | 单次会话中工具调用最大次数（1–50），超限则终止调用并生成最终回复 | 新版智能体“运行与结果分析”章节（[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)） |
| **记忆与上下文** | 短期记忆轮数 | 设置 0–30 轮多轮对话上下文传递（0 表示禁用） | 新版智能体“记忆”模块（[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)） |

## 使用方式

1. **创建与配置**：  
   - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → Agent 2.0 → 配置模型、系统提示词、知识库、MCP 工具等。  
   - 工作流：同上 → 选择“工作流应用” → 拖拽节点（开始/大模型/意图分类/结束等）→ 连接连线 → 配置各节点参数（如大模型节点的提示词、用户提示词 `${sys.query}`）。  
   - 高代码：同上 → 选择“高代码应用” → 选择部署方式（Serverless/K8s）→ 提交代码（模板或 .whl 包）→ 部署。

2. **测试与调试**：  
   - 所有类型均提供右侧面板“文本对话体验”，支持上传文件、输入文本并实时查看响应与执行轨迹（智能体展示卡片流，工作流显示节点日志）。  
   - 高代码应用额外提供“API测试”模式，可手动调用 `/health`、`/process` 等接口。

3. **发布与集成**：  
   - **必须发布后方可调用**：点击应用配置页右上角“发布”按钮确认变更。  
   - API 调用：在“发布渠道”页签 → “API调用” → “查看API”，获取 endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）。  
   - 文件问答 API 需按预设模式（全文引用/切片检索）调用，无法动态切换；生产环境推荐使用 `session_file_id` 方式上传大文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **强制发布要求**：所有应用类型均需完成“发布”操作才能通过 API 或第三方渠道调用，未发布应用仅限控制台内测试 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **文件生命周期**：通过聊天窗口上传的文件**仅在当前会话有效**，刷新或关闭页面即失效；通过 API 上传的 `session_file_id` 有效期为 24 小时 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费关键点**：  
  - 模型调用费用按输入/输出 [Token](../concepts/token.md) 计费，**知识库召回内容计入输入 [Token](../concepts/token.md)**，可能显著增加成本；  
  - 全文引用模式因整文件入参，Token 消耗远高于切片检索模式；  
  - MCP 工具调用可能产生第三方费用（如天气 API），百炼平台不收取该部分费用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **权限依赖**：RAM 子账号创建应用并发布时，需提前授予 `ram:CreateServiceLinkedRole` 权限，否则发布失败 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域），其他地域暂不可用 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


