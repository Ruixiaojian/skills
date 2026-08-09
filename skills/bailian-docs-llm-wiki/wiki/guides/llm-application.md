# llm application

`llm application` 是阿里云百炼平台面向大模型应用开发的核心能力层，提供三种互补的构建范式：智能体（Agent）用于动态任务规划与自主工具调用；工作流（Workflow）用于确定性、可复现的多步骤流程编排；高代码应用（Rich Code Application）则面向专业开发者，支持全量 Python 代码部署与企业级运维。三者共同覆盖从零代码业务配置到深度定制 AI 后端的完整开发光谱。

## 支持的模型/功能

百炼 `llm application` 支持统一的模型底座与差异化能力扩展：

- **模型兼容性**：所有应用类型均支持千问系列主流模型（如 `qwen-plus-latest`、`qwen-max`、`qwen-vl-plus`），以及 DeepSeek 等第三方模型。视觉理解任务需显式选用 `qwen-vl-*` 系列模型，其原生支持图片/视频解析，即使关闭预解析亦可直接处理图像文件 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **核心能力矩阵**：
  - **智能体（Agent）**：以提示词驱动自主决策，集成知识库（RAG）、MCP 工具、内置沙箱工具（`bash`/`read`/`write` 等）、数据连接器及技能（Skill）包。新版 Agent 2.0 将知识库与 MCP 统一为可规划工具，显著提升复杂任务处理能力 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - **工作流（Workflow）**：通过可视化节点（大模型、意图分类、变量处理、智能体群组等）编排执行链路，支持会话变量（`query`/`historyList`/`imageList`）跨节点共享与自定义缓存 [原文标题](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - **高代码应用**：基于 Python 项目一键部署为 Serverless Function 或 K8s 服务，支持 MCP 工具一站式接入、自定义前端（Spark Design 框架）及企业级可观测能力 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版 Agent 2.0）在能力架构上存在根本性差异——旧版将知识库与 MCP 分离调度，而新版将其统一为可规划工具；二者不兼容且无法升级，必须重新创建应用 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 关键参数

各应用类型的关键可配置参数如下：

| 类别 | 参数名 | 说明 | 取值范围/示例 |
|--------|--------|------|----------------|
| **通用** | `temperature` | 控制生成随机性 | `0.0`（确定性）~ `1.0`（高多样性） |
| **智能体** | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | `true`/`false` |
| | `ReAct 最大轮次` | 单次会话中工具调用上限 | `1`–`50` |
| | `短期记忆轮数` | 多轮对话上下文保留轮数 | `0`（禁用）~ `30` |
| | `单文件最大解析长度`（全文引用） | 截断位置在文件末尾 | token 数，影响输入成本 |
| | `召回片段数`（切片检索） | RAG 检索返回的最大文本块数 | 正整数 |
| **工作流** | `记忆`（节点级） | 启用自定义缓存或本节点缓存 | `自定义缓存`（全局）/`本节点缓存` |
| **高代码** | `最小实例数` | Serverless 实例保活数 | `0`（冷启动）或 `≥1`（热启动） |
| | `单实例并发度` | 单个实例并行处理请求数 | `1`–`100` |

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → 指定 Agent 2.0 版本 → 配置模型、系统提示词、知识库、MCP 等 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接逻辑 → 配置各节点模型、提示词、变量映射 → 测试后发布 [原文标题](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - 高代码：选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 部署 → 通过 API 测试或文本对话调试 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **文件处理（智能体专属）**：
  - 三种模式：`全文引用`（整文件入上下文）、`切片检索`（RAG 增强）、`自定义处理`（模型自主调用工具）。千问-VL 模型在自定义处理下支持“模型处理+规划”，即先理解图片再决定是否调用 MCP [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。

- **调用集成**：
  - 所有应用**必须发布后**方可调用；
  - API 调用统一通过“发布渠道”页签获取 endpoint 与鉴权方式；
  - 文件问答 API 不支持运行时切换处理模式，严格遵循应用内配置 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；上传文件仅在当前会话有效，刷新页面即失效 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **计费要点**：
  - 模型调用费用按实际输入/输出 [Token](../concepts/token.md) 计费，`全文引用`模式因整文件入参导致 [Token](../concepts/token.md) 消耗显著高于 `切片检索`；
  - 知识库检索内容计入模型输入 [Token](../concepts/token.md)，可能推高推理费用；
  - MCP 工具调用费用独立于模型费用，部分由第三方收取 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **能力边界**：
  - 智能体暂不支持[长期记忆](../concepts/long-term-memory.md)（计划未来迭代）；
  - 自定义[插件](../concepts/plugin.md)超时限制为 5 秒；
  - 工作流中 `imageList`/`fileList` 参数仅接受公网可访问 URL，推荐使用 OSS 生成 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **版本与兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，无升级路径，需新建应用迁移配置 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


