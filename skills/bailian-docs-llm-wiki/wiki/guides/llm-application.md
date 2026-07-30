# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种互补模式，分别覆盖零代码决策、低代码流程编排与专业级代码开发需求。三者均基于大语言模型能力，通过集成[知识库](../concepts/knowledge-base.md)（RAG）、MCP 工具、记忆机制等扩展能力边界，支持私有知识调用、实时信息获取与复杂任务规划。

## 支持的模型/功能

- **智能体（Agent）**：以提示词驱动自主规划，支持[知识库](../concepts/knowledge-base.md)检索、插件/MCP 调用、文件多模态理解（含全文引用、切片检索、自定义处理三种模式）及短期记忆（0–30 轮）。新版智能体（Agent 2.0）将[知识库](../concepts/knowledge-base.md)与 MCP 统一为可规划工具，支持完整“思考-执行-反思”链路回溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，支持大模型节点、意图分类、变量处理、智能体群组等节点类型，适用于固定路径的自动化任务（如日程管理、智能导购）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：基于 Python 项目部署 Serverless 或 K8s 后端服务，支持 MCP 工具一站式接入、自定义前端（Spark Design 框架）、API 网关与企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

> **注意**：文档 2（`single-agent-application.md`）中提及“[长期记忆](../concepts/memory.md)”为已发布功能，但文档 3（`new-single-agent-application.md`）明确说明“[长期记忆](../concepts/memory.md)该功能计划在未来的迭代中支持”，二者存在矛盾。当前实际可用的仅为短期记忆（0–30 轮），[长期记忆](../concepts/memory.md)尚未上线。

支持的模型覆盖千问全系列（Qwen-Max/Plus/Turbo/Long/QwQ/VL 等）、DeepSeek 及开源模型，具体以控制台内实时列表为准。多模态任务需选用千问-VL 系列模型；文件处理能力（如图片 OCR、视频帧分析）依赖模型原生能力或预置解析器，详见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **通用** | `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数，超限后强制生成最终回复（仅新版智能体） |
| **智能体** | `enable_thinking` | 开启后启用模型内置思考模式，增强规划与反思能力（仅支持模型可用） |
| **文件处理** | `单文件最大解析长度` / `最大拼装长度`（token） | 全文引用模式下控制输入截断位置；切片检索模式下控制召回片段总长度 |
| **工作流** | `historyList` / `imageList` | 预置会话变量，用于跨节点传递多轮对话历史与上传文件（需在支持记忆的节点中启用“自定义缓存”） |
| **高代码** | `最小实例数` / `单实例并发度` | Serverless 部署时影响冷启动延迟与吞吐量，时延敏感业务建议 ≥1 |

## 使用方式

1. **创建与配置**  
   - 智能体：控制台 → 应用中心 → 创建应用 → 选择 **Agent 2.0**（推荐）或 Agent 1.0；配置模型、系统提示词、知识库、MCP 工具等。  
   - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接执行流 → 在节点内配置模型、提示词、变量映射（如 `${sys.query}`）。  
   - 高代码：选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 一键部署。  

2. **调试与测试**  
   - 智能体/工作流：右侧对话面板直接交互，新版智能体支持卡片流展示规划过程；工作流支持分步运行与变量查看。  
   - 高代码：页面右侧面板提供“文本对话体验”与“API 测试”，支持 `GET /health`、`POST /process` 等接口调用。  

3. **发布与集成**  
   - **必须发布后方可调用**：所有应用类型均需在配置页右上角点击 **发布**，确认变更后生效。  
   - API 调用：智能体与工作流在“发布渠道”页签获取 API Endpoint 与鉴权方式；高代码应用需开启网关并配置 [Token](../concepts/token.md) 鉴权，示例请求见 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
   - 第三方集成：支持发布至钉钉、微信公众号，或作为组件被其他智能体/工作流调用（需先发布为组件）。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；会话内上传文件仅当前会话有效，刷新即失效；生产环境推荐使用 `session_file_id` 文件上传 API 处理大文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **调用限流**：智能体应用默认限流 **100 次/分钟**，此配额共享于所有 API 请求（含文件问答、普通对话等）。  
- **模型兼容性**：`enable_thinking` 参数仅对支持思考模式的模型（如 Qwen-Max）生效；千问-VL 系列模型在关闭预解析时仍可直接解析图片/视频，但其他模型必须开启预解析才能处理非文本文件 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **版本隔离**：Agent 1.0 与 Agent 2.0 架构不兼容，无法升级或降级，需重新创建应用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **计费要点**：知识库检索内容计入模型输入 [Token](../concepts/token.md)；长期记忆存储免费但内容注入 Prompt 会增加 [Token](../concepts/token.md) 消耗；MCP 调用费用由第三方收取（如高德地图 API），百炼不额外收费 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)


