# llm application

`llm application` 是阿里云百炼平台面向大语言模型（LLM）构建的三类核心应用范式之一，专为突破模型原生能力边界而设计。它通过提示词驱动、自主规划与工具协同，将私有知识库、实时数据源、代码执行等外部能力无缝集成到对话流中，适用于开放式意图理解与动态任务求解场景，如智能客服、知识问答、旅行规划等。开发者可零代码配置，亦可通过 API 或高代码方式深度定制。

## 支持的模型/功能

- **核心模型要求**：推荐选用具备强工具调用与多步推理能力的模型，如 `千问-Max` 系列；`千问-VL` 系列模型在关闭预解析时仍可直接处理图片/视频，此特性在[新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)中有明确说明。
- **关键能力模块**：
  - **知识库（RAG）**：作为可调度工具接入新版智能体（Agent 2.0），支持标签过滤以提升检索精度；旧版智能体（Agent 1.0）仅支持静态检索增强 [智能体应用 (raw/application-user-guide/llm-application/single-agent-application.md)](../../raw/application-user-guide/llm-application/single-agent-application.md)。
  - **MCP 工具**：统一通过 MCP 协议接入，包括官方 MCP 广场服务与自定义 MCP，支持多步、非固定顺序调用；[插件](../concepts/plugin.md)（Plugin）在旧文档中仍被提及，但新版已全面迁移至 MCP 架构 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  > **注意**：文档3（`single-agent-application.md`）仍使用“[插件](../concepts/plugin.md)”术语并描述其调用逻辑，而文档1（`new-single-agent-application.md`）已明确将所有外部能力统一为 MCP 工具，并强调“[插件](../concepts/plugin.md)也支持一键转换为 MCP 服务”。因此，**新项目应基于 MCP 架构开发，避免依赖旧插件接口**。
  - **文件处理模式**：支持三种模式——全文引用（适合短文档总结）、切片检索（RAG 风格，适合长文档问答）、自定义处理（模型自主调用工具，如图像风格转换）。不同模式对 [Token](../concepts/token.md) 消耗与适用场景差异显著，详见[文件问答 (raw/application-user-guide/llm-application/file-q-a.md)](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 关键参数

- **`enable_thinking`**：控制是否开启思考模式，仅对支持该能力的模型生效；开启后可在运行中展示“规划-执行-反思”链路，用于调试决策路径。
- **`ReAct 最大轮次`**：取值范围 1–50，限制单次会话中工具调用总次数；超限后自动终止调用并生成最终回复。
- **文件处理参数**：
  - 全文引用模式：`单文件最大解析长度（token）`（截断位置为文件末尾）、`最大拼装长度（token）`（截断位置为最后拼接文件末尾）。
  - 切片检索模式：`召回片段数`、`最大拼装长度`（按相关性得分丢弃低分片段）。
- **记忆配置**：短期记忆支持 0–30 轮上下文；[长期记忆](../concepts/long-term-memory.md)当前为计划中功能，暂未开放。

## 使用方式

- **创建与配置**：在百炼控制台「应用管理」→「创建应用」→ 选择「智能体应用」→ **优先选用 Agent 2.0（新版）**；配置模型、系统提示词（支持自定义变量）、知识库、MCP 工具及文件处理策略。
- **交互方式**：
  - 文本对话：支持多轮会话，输入文本或上传文件（单次最多 10 个，单文件 ≤10MB）。
  - 文件问答：依据所选模式（全文引用/切片检索/自定义处理）自动触发对应处理逻辑。
- **发布与调用**：
  - 应用必须**发布后**方可调用；
  - API 调用需通过「发布渠道」→「API 调用」获取 endpoint 与鉴权方式；
  - 高代码应用可进一步封装为 Serverless Function 或 K8s 服务，并通过 API 网关暴露生产级接口。

## 限制和注意事项

- **版本不兼容**：Agent 1.0 与 Agent 2.0 基于不同技术架构，**不支持升级、降级或互转**；如需迁移，须重新创建新版应用 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **文件有效期**：聊天窗口上传的文件**仅在当前会话有效**，刷新或关闭页面即失效；生产环境推荐使用文件上传 API 获取 `session_file_id`（有效期通常 24 小时）。
- **计费要点**：
  - 模型调用费用取决于输入/输出 [Token](../concepts/token.md) 数量，其中知识库召回内容、文件解析文本均计入输入 [Token](../concepts/token.md)；
  - 全文引用模式 Token 消耗显著高于切片检索模式，长文档场景务必优先评估 RAG 策略；
  - MCP 工具调用可能产生额外费用（如第三方 API 调用），由服务提供方收取，百炼平台不加收。
- **隐式缓存支持**：智能体自动启用上下文前缀缓存（如系统提示词、知识库内容），命中部分 Token 按标准单价 20% 计费；但**暂不支持显式缓存配置**。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


