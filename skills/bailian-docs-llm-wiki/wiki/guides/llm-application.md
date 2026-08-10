# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，通过封装大模型能力与外部系统集成能力，支持零代码、低代码和高代码三种开发路径。它并非单纯调用大模型 API，而是提供具备知识检索、工具调度、流程编排和长期可维护性的生产级应用框架，适用于客服、报告生成、智能导购、日程管理等真实业务闭环。

## 支持的模型/功能

LLM Application 以三种形态提供差异化能力：

- **智能体（Agent）应用**：基于提示词驱动的自主决策系统，支持动态规划、多步工具调用（如知识库、MCP、内置沙箱工具）及多轮上下文记忆。新版 Agent 2.0 将知识库与 MCP 统一为可规划工具，显著提升复杂任务处理能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：通过可视化节点编排实现确定性流程控制，支持大模型节点、意图分类、变量处理、智能体群组等组件，适用于固定步骤自动化场景（如诈骗识别、智能导购） [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向开发者提供完整 Python 工程部署能力，支持 Serverless Function 或 K8s 部署，内置 MCP 工具接入、前端定制（Spark Design）、API 网关与可观测性等企业级能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有类型均支持主流千问系列模型（Qwen-Max、Qwen-Plus、Qwen-VL 等），具体支持列表以控制台实时显示为准。文件问答能力覆盖文档、图片、音视频，提供全文引用、切片检索（RAG）和自定义处理三种模式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先选用 Agent 2.0，旧版仅用于存量维护。

## 关键参数

| 类别 | 参数 | 说明 | 可配置性 |
|--------|------|------|-----------|
| **模型层** | `temperature` | 控制输出随机性，范围通常 0.0–1.0 | 所有应用类型均支持 |
| | `enable_thinking` | 开启思考模式（仅限支持模型），用于展示“规划-执行-反思”链路 | 仅 Agent 2.0 支持 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| | `ReAct 最大轮次` | 限制单次会话中工具调用次数（1–50） | 仅 Agent 2.0 支持 |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下截断位置（从文件末尾） | Agent 中可配 |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 输入规模 | Agent 中可配 |
| **工作流** | `historyList` / `query` | 预置会话变量，用于多轮对话上下文传递 | Workflow 节点内启用“自定义缓存”后生效 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) |
| **高代码** | `最小实例数` / `单实例并发度` | 控制 Serverless/K8s 资源弹性 | 高代码应用部署时配置 |

## 使用方式

1. **创建与配置**  
   - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用（Agent 2.0）”，配置模型、系统提示词、知识库、MCP 工具等。  
   - 工作流：拖拽节点（开始/大模型/意图分类/结束等），配置各节点模型、提示词、变量映射，连接执行流。  
   - 高代码：选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）、资源规格、环境变量。

2. **调试与测试**  
   - 所有类型均提供右侧对话面板实时测试；工作流支持画布内节点级调试；高代码支持 `GET /health` 和 `/process` 接口测试。

3. **发布与集成**  
   - **必须先发布**：应用发布是 API 调用、第三方平台集成（钉钉/微信）及组件复用的前提。  
   - API 调用：发布后在“发布渠道”页签获取 endpoint 与鉴权方式（Bearer [Token](../concepts/token.md)）。  
   - 文件上传：支持 `image_list`/`file_list` URL 传参，或先调用文件上传 API 获取 `session_file_id`（推荐生产环境使用）。

## 限制和注意事项

- **会话级文件有效期**：通过聊天窗口上传的文件仅在当前会话有效，刷新或关闭页面即失效；`session_file_id` 方式有效期为 24 小时 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **[Token](../concepts/token.md) 消耗差异**：全文引用模式将整个文件内容计入输入 [Token](../concepts/token.md)，切片检索模式仅计入问题+召回片段，自定义处理模式消耗取决于工具交互轮次。长文档务必优先选用切片检索。  
- **工具超时与权限**：自定义插件超时限制为 5 秒；发布应用需 RAM 账号具备 `ram:CreateServiceLinkedRole` 权限；网关部署地域必须与应用部署地域一致。  
- **计费关键点**：  
  - 模型调用费用按实际输入/输出 Token 计费；  
  - 知识库检索文本增加输入 Token，间接推高模型费用；  
  - MCP 工具费用由阿里云或第三方收取，需单独确认；  
  - [长期记忆](../concepts/long-term-memory.md)存储免费，但其内容注入 Prompt 后产生的 Token 暂不计费（文档 3 明确说明）。  

> **注意**：文档 3 声明“[长期记忆](../concepts/long-term-memory.md)的数据存储不收费”，而文档 2 未提及该费用豁免，且其“记忆”章节仅描述短期记忆（0–30 轮）。开发者应以文档 3 的计费说明为准，[长期记忆](../concepts/long-term-memory.md)功能当前仍处于计划阶段，暂不可用。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


