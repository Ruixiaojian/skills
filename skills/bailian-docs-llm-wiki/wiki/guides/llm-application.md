# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，突破大模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。开发者可根据业务复杂度、可控性要求与团队技术栈，选择零代码、低代码或专业编码方式快速落地可交付的 AI 服务。

## 支持的模型/功能

- **模型支持**：所有 LLM Application 类型均支持千问系列主流模型（如 `千问-Max`、`千问-Plus-Latest`、`千问-VL-Max`），部分能力对模型有特定要求：
  - 新版智能体（Agent 2.0）推荐使用具备强工具调用能力的模型（如 `千问-Max` 系列），以保障多步规划效果 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  - 文件问答中，`千问-VL` 系列模型可直接解析图片/视频，无需开启预解析；而文本模型在“自定义处理”模式下依赖显式配置的工具 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 工作流应用中，各节点（如意图分类、大模型）可独立选择模型，常见实践选用 `千问-Plus-latest` [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **核心能力矩阵**：
  | 能力类型 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
  |----------|----------------|---------------------|-------------|
  | **知识库（RAG）** | ✅ 作为自主调用工具（Agent 2.0）或固定检索源（旧版） | ✅ 可在大模型节点中启用 RAG 或通过“切片检索”混合文件与知识库 | ✅ 一站式 MCP 接入，支持关联知识库 |
  | **外部工具** | ✅ 内置沙箱工具（`bash`/`write`/`read`等）、MCP、插件、应用组件 | ✅ 通过 API 节点、函数计算节点或 MCP 节点调用 | ✅ MCP 工具接入（知识库、工作流、插件等） |
  | **多模态支持** | ✅ 千问-VL 模型直解析；其他模型依赖预解析或工具调用 | ✅ 大模型节点支持 `image_list` 输入，需模型具备视觉能力 | ✅ 代码中可自由处理多模态输入/输出 |
  | **[长期记忆](../concepts/long-term-memory.md)** | ⚠️ 新版仅支持短期记忆（0–30 轮），[长期记忆](../concepts/long-term-memory.md)“计划未来迭代支持” [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；旧版文档提及[长期记忆](../concepts/long-term-memory.md)“不收费”，但未说明是否已上线 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md) | ✅ 通过会话变量（`historyList`）和节点级“自定义缓存”实现跨节点上下文传递 | ✅ 由开发者在 Python 代码中自主实现 |

> **注意**：关于长期记忆，[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 明确标注“该功能计划在未来的迭代中支持”，而 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md) 在计费说明中称“长期记忆的数据存储不收费”，但未确认其当前可用性。实际开发应以控制台界面显示为准，短期记忆（上下文轮数）是当前唯一稳定可用的记忆机制。

## 关键参数

- **通用参数**：
  - `temperature`：控制生成随机性（0.0–1.0），值越高越发散；
  - `max_tokens`（最长回复长度）：限制模型输出 token 数，不含提示词；
  - `enable_thinking`：仅对支持思考模式的模型（如 `千问-Max`）生效，开启后可展示推理链路。

- **智能体专属参数**：
  - `ReAct 最大轮次`（1–50）：限制单次会话中工具调用总次数，超限则终止规划并生成最终回复；
  - `短期记忆轮数`（0–30）：控制多轮对话中向模型注入的历史消息数量；
  - `预解析文件`开关：决定上传文件是直接传 URL（关闭）还是由系统解析为文本（开启）；千问-VL 模型例外，关闭时仍可直解析图片/视频。

- **文件问答专用参数**（见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)）：
  - **全文引用模式**：`单文件最大解析长度`（token）、`最大拼装长度`（token），截断策略为从末尾丢弃；
  - **切片检索模式**：`召回片段数`、`最大拼装长度`，超长时按相关性得分从低到高丢弃；
  - **自定义处理模式**：需显式挂载 MCP/插件，并在系统提示词中引导调用逻辑。

- **工作流专属参数**：
  - 会话变量（`query`, `historyList`, `imageList`）全局可用，支持跨节点引用；
  - 节点级“记忆”开关（自定义缓存 vs 本节点缓存），影响上下文范围。

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → 指定 Agent 2.0（推荐）或旧版；
  - 工作流：控制台 → 应用管理 → 创建应用 → 选择“工作流应用” → 拖拽节点（开始/大模型/意图分类/结束等）并连线配置；
  - 高代码应用：控制台 → 应用管理 → 创建应用 → 选择“高代码应用” → 选择 Serverless Function（默认）或 K8s 部署方式，上传 `.whl` 包或选模板。

- **调试与测试**：
  - 所有类型均提供右侧对话窗口实时调试；
  - 智能体（Agent 2.0）支持卡片流展示“思考→工具调用→反思”全过程；
  - 工作流支持画布内逐节点测试，查看中间变量输出；
  - 高代码应用提供“文本对话体验”与“API 测试”双模式，支持 `GET /health` 和 `POST /process`。

- **发布与集成**：
  - **必须发布后方可调用**：发布操作位于应用配置页右上角，发布前会对比变更差异；
  - API 调用：各应用在“发布渠道”页签 → “API 调用” → “查看 API”，获取 endpoint、鉴权方式（Bearer Token）及请求体格式；
  - 高代码应用额外支持网关部署：开通云原生 API 网关，配置路由与 Token 鉴权，生产环境建议禁用测试域名公网访问。

## 限制和注意事项

- **文件限制**：
  - 单次会话最多上传 10 个文件，单文件 ≤ 10 MB；
  - 会话内上传文件仅当前会话有效，刷新/关闭页面即失效；生产环境推荐使用文件上传 API 获取 `session_file_id`（有效期 24 小时）或 OSS 公网 URL [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

- **调用限制**：
  - 智能体应用默认限流 100 次/分钟，此配额被所有 API 请求共享（含文件问答、普通对话）；
  - 自定义插件超时限制为 5 秒 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)；
  - 工作流节点间数据传递受 JSON 序列化大小限制，避免在变量中塞入超大二进制内容。

- **模型与能力兼容性**：
  - `enable_thinking` 参数仅对明确支持思考模式的模型生效，不支持的模型无法配置该参数；
  - 千问-VL 模型在“自定义处理”模式下，图片可选“模型处理”或“模型处理+规划”，后者需额外挂载 MCP 工具 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 旧版智能体与新版（Agent 2.0）架构不兼容，**无法升级/降级**，需重新创建 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **计费关键点**：
  - 应用创建不收费，仅调用时产生费用；
  - 模型调用费用 = 输入 Token + 输出 Token × 对应模型单价；
  - 知识库检索内容计入输入 Token，可能推高模型费用；
  - MCP 工具费用分两类：阿里云官方 MCP 按模型调用计费；第三方 MCP 产生的费用由第三方收取，百炼不抽成。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)


