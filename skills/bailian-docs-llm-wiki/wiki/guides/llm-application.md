# llm application

`llm application` 是阿里云百炼平台面向业务场景构建 AI 应用的核心抽象，旨在突破大模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种范式，开发者可零代码、低代码或专业编码方式，快速集成知识库、MCP 工具、记忆、多模态[文件处理](../concepts/file-processing.md)等能力，交付稳定、可控、可运维的生产级 AI 服务。

## 支持的模型/功能

百炼 LLM 应用统一支持千问系列主流模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-max`）及部分开源模型（如 `qwen2.5`、`deepseek`），具体可用模型以控制台实时列表为准。不同应用类型对模型能力有差异化要求：

- **智能体应用**：推荐选用具备强工具调用与多步推理能力的模型（如 `qwen-max` 系列）。新版智能体（Agent 2.0）明确要求模型支持 `enable_thinking` 参数以启用反思链路；而旧版（Agent 1.0）无此要求，但规划能力较弱 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流应用**：节点级模型选择灵活，常见于大模型节点与意图分类节点，支持 `qwen-plus-latest` 等通用模型，强调确定性输出与上下文稳定性。
- **高代码应用**：完全由开发者代码控制模型调用逻辑，支持任意百炼平台已接入的模型，包括 Serverless 或 K8s 部署环境下的自定义模型路由。

核心功能覆盖：
- **知识库（RAG）**：支持切片检索与全文引用，新版智能体将知识库作为可自主调度的“工具” [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
- **MCP 工具接入**：统一协议接入官方 MCP（如高德地图、文生图）与自定义服务，智能体可动态规划调用顺序，工作流与高代码应用均支持一站式关联；
- **多模态[文件处理](../concepts/file-processing.md)**：支持文档、图片、音视频上传与问答，提供全文引用、切片检索、自定义处理三种模式，其中千问-VL 系列模型在关闭预解析时仍可直接理解图像/视频 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
- **技能与组件复用**：技能（Skill）封装高频任务逻辑，应用组件可将已发布智能体/工作流作为子节点嵌入新流程。

> **注意**：文档 4（智能体应用）中提及“插件”为旧术语，文档 2 和文档 3 已统一升级为“MCP”协议；实际开发应以 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 和 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) 中的 MCP 描述为准，避免使用已弃用的插件配置路径。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用范围 |
|----------|--------|------|----------|
| **模型控制** | `temperature` | 控制生成随机性，取值 0–2，推荐 0.3–0.7 用于确定性任务 | 所有应用类型 |
| | `max_tokens`（最长回复长度） | 模型生成内容的最大 token 数，不含提示词 | 智能体、工作流大模型节点 |
| | `enable_thinking` | 是否开启思考模式，仅支持部分模型（如 `qwen-max`），影响 ReAct 链路展示 | 新版智能体（Agent 2.0）专属 |
| **[文件处理](../concepts/file-processing.md)** | 单文件最大解析长度 / 最大拼装长度 | 全文引用模式下截断策略参数，单位 token | [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| | 召回片段数 / 最大拼装长度 | 切片检索模式下控制 RAG 输入规模 | [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| **会话与记忆** | 短期记忆轮数（0–30） | 控制多轮对话上下文窗口大小，0 表示禁用 | 新版智能体 |
| | `ReAct 最大轮次`（1–50） | 限制单次请求中工具调用总次数，超限则终止调用并生成终答 | 新版智能体 |
| **安全与调试** | 展示回答来源 | 开启后在回复末尾以角标标注知识库/网页来源 | 新版智能体、工作流（需配合知识库） |

## 使用方式

### 创建与配置
- **智能体应用**：控制台 → 应用中心 → 创建应用 → 选择“智能体应用” → 优先选用 **Agent 2.0**（新版）；配置模型、系统提示词（支持变量注入）、知识库、MCP 工具、文件处理模式 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流应用**：通过可视化画布拖拽节点（开始、大模型、意图分类、变量处理、结束等），配置各节点模型、提示词、记忆策略及变量引用；支持会话变量全局共享 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：支持控制台模板创建或 CLI 上传 `.whl` 包；部署方式可选 Serverless Function（轻量无状态）或 K8s（高性能长程任务）；工具、网关、前端均可独立配置 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

### 调用与集成
- **所有应用均需先发布**：发布是 API 调用、第三方平台集成（钉钉/微信）及组件复用的前提。
- **API 调用**：
  - 智能体：使用 `/v1/agents/{agent_id}/chat` 接口，传入 `input`（含 `role`/`content`）、`session_id`；
  - 工作流：使用 `/v1/workflows/{workflow_id}/invoke`，支持 JSON 输入；
  - 高代码：通过 API 网关或函数计算触发器调用，协议详见 [API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)。
- **文件上传**：支持聊天窗口直传（会话级有效）、`file_list`/`image_list` URL 传参（需公网可访问）、或先调用文件上传 API 获取 `session_file_id` 后复用（推荐生产环境）。

## 限制和注意事项

- **版本不兼容**：Agent 1.0 与 Agent 2.0 架构隔离，**不支持升级/降级**，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；聊天窗口上传的文件仅在当前会话有效，刷新即失效；`session_file_id` 方式有效期通常为 24 小时 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **计费要点**：
  - 模型调用费用按输入/输出 token 计费，**知识库召回内容计入输入 token**；
  - 全文引用模式 token 消耗显著高于切片检索，长文档务必评估成本；
  - MCP 工具调用可能产生额外费用（如第三方 API 调用），由服务方收取，百炼不加收。
- **能力边界**：
  - 新版智能体暂不支持[长期记忆](../concepts/long-term-memory.md)（计划迭代中），仅提供短期记忆（0–30 轮）；
  - 工作流中的“自定义缓存”记忆作用域为全局会话，但需在各节点显式启用；
  - 高代码应用的隐式缓存自动生效，但**不支持显式缓存配置**（如 `cache_key`）。
- **调试建议**：
  - 智能体未按预期调用工具时，优先检查系统提示词是否清晰描述工具功能与触发条件；
  - 工作流输出异常，应验证节点间变量引用语法（如 `${sys.query}`、`大模型1/result`）及数据类型匹配；
  - 文件问答效果不佳，优先排查文件解析质量（如扫描件 OCR 准确率）、提问明确性及切片策略。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


