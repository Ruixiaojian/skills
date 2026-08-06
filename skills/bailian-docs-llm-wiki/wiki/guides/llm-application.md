# llm application

`llm application` 是阿里云百炼平台提供的面向大语言模型（LLM）的三类核心应用构建模式（智能体、工作流、高代码应用）的统称，用于突破模型原生能力边界，实现私有知识接入、实时信息获取、复杂任务规划与自动化执行。开发者可根据任务确定性、开发门槛和定制深度选择合适类型，所有类型均支持模型调用、知识库（RAG）、MCP 工具集成及 API 对接。

## 支持的模型/功能

- **模型支持**：智能体应用支持千问系列（Max、Plus、Turbo、Long、VL-Max/Plus/OCR 等）、QwQ、DeepSeek 等文本与[多模态](../concepts/multimodal.md)模型；[新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 明确推荐 `千问-Max` 系列以保障多步规划效果。
- **核心能力**：
  - **知识库（RAG）**：作为工具由智能体自主调用，支持标签过滤提升检索精度；[文件问答 (raw/application-user-guide/llm-application/file-q-a.md)](../../raw/application-user-guide/llm-application/file-q-a.md) 提供全文引用、切片检索、自定义处理三种文件交互模式，其中切片检索可混合关联知识库内容。
  - **工具调用**：内置 `bash`、`write`、`read` 等沙箱工具；外部服务统一通过 MCP 协议接入（含官方 MCP 广场及自定义服务），支持动态非固定顺序调用。
  - **[多模态](../concepts/multimodal.md)处理**：千问-VL 系列模型在关闭预解析时仍可直接解析图片/视频；其他模型或非图像文件需依赖预解析开关控制。
  - **记忆**：支持 0–30 轮短期记忆（上下文轮数），[长期记忆](../concepts/long-term-memory.md)暂未开放。

> **注意**：文档 3（`single-agent-application.md`）将“插件”列为独立能力，而文档 1（`new-single-agent-application.md`）已明确将插件统一纳入 MCP 协议体系，并强调“插件也支持一键转换为 MCP 服务”。因此，**插件即 MCP 的一种形态，不应视为并列能力**，应以新版 Agent 2.0 架构为准。

## 关键参数

- **模型参数**：
  - `temperature`：控制生成随机性，范围通常 0–2，值越高越多样。
  - `max_tokens`（最长回复长度）：仅限制模型输出 token 数，不含提示词。
  - `enable_thinking`：开启后支持思考链（Thinking）步骤展示，**仅对支持思考模式的模型生效**（如千问-Max），不支持的模型无法配置该参数。
- **文件处理参数**（见 [文件问答 (raw/application-user-guide/llm-application/file-q-a.md)](../../raw/application-user-guide/llm-application/file-q-a.md)）：
  - 全文引用模式：`单文件最大解析长度（token）`（截断位置：文件末尾）、`最大拼装长度（token）`（截断位置：最后拼接文件末尾）。
  - 切片检索模式：`召回片段数`、`最大拼装长度`（按相关性得分丢弃低分片段）。
- **运行控制参数**：
  - `ReAct 最大轮次`：限制单次会话中工具调用总次数（1–50），超限则终止调用并生成最终回复。
  - 短期记忆轮数：0–30，0 表示不传递历史对话。

## 使用方式

- **创建路径**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择 **智能体应用 > Agent 2.0**（推荐）或 Agent 1.0。
  - 工作流：控制台 → 应用管理 → 创建应用 → 选择 **工作流应用**，通过节点拖拽编排（开始/大模型/意图分类/结束等）。
  - 高代码应用：控制台 → 应用管理 → 创建应用 → 选择 **高代码应用**，支持模板部署或上传 `.whl` 包。
- **配置要点**：
  - 系统提示词需明确定义角色、行为约束及工具使用规则（如“当用户询问天气时，调用 `weather_mcp`”）。
  - 文件上传后，处理模式（全文引用/切片检索/自定义处理）需在应用配置中预先设定，API 调用时**无法动态切换**。
- **调用方式**：
  - 所有应用必须先**发布**（发布渠道页签提供 API 文档），方可通过 HTTP API 调用。
  - 智能体 API 支持 `image_list`（图片 URL）、`file_list`（通用文件 URL）或 `session_file_id`（文件上传 API 返回 ID）传入文件。
  - 高代码应用支持 Serverless Function 或 K8s 部署，网关配置后可通过自定义域名访问。

## 限制和注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，**不支持升级/降级**，需重新创建应用。
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；聊天窗口上传的文件**仅当前会话有效**，刷新即失效；生产环境推荐使用 `session_file_id` 方式。
- **计费逻辑**：
  - 模型调用费用按输入/输出 [Token](../concepts/token.md) 计费，知识库召回内容计入输入 [Token](../concepts/token.md)；切片检索模式通常比全文引用更省 [Token](../concepts/token.md)。
  - MCP 工具调用可能产生额外费用（第三方 API 或百炼计费项），需查阅具体工具说明。
- **超时与稳定性**：
  - 自定义插件（旧版术语）超时限制为 5 秒（见文档 3）；MCP 服务超时策略以具体服务文档为准。
  - 高代码应用部署后即开始计费，停止服务可节省费用。

> **注意**：文档 4（`workflow-application.md`）中案例二“智能导购”在多个大模型节点配置了“自定义缓存”记忆，但文档 1 明确指出新版智能体仅支持短期记忆（0–30 轮），且无“自定义缓存”概念；工作流的 `historyList` 变量属于其自身会话变量机制，与智能体记忆无关。开发者需区分不同应用类型的记忆实现机制，避免混淆配置。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


