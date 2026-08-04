# llm application

`llm application` 是阿里云百炼平台面向开发者提供的核心应用构建范式，用于将大语言模型（LLM）与外部能力（如知识库、工具、数据源）深度集成，突破模型原生能力边界。它支持零代码/低代码配置与高代码定制两种路径，覆盖从开放式智能体到确定性工作流再到专业级后端服务的全场景需求，是构建生产级 AI 应用的基础载体。

## 支持的模型与功能

百炼 `llm application` 提供三类主流构建模式，各自定位清晰、能力互补：

- **智能体（Agent）应用**：由提示词驱动，具备自主意图理解、多步规划与动态工具调用能力。新版智能体（Agent 2.0）将知识库、MCP 等统一为可调度工具，支持完整“规划-执行-反思”链路回溯，适用于开放式对话、任务助理、复杂规划等场景 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：通过可视化节点编排实现确定性、可复现的多步骤执行，每个节点（如大模型、意图分类、变量处理）职责明确、逻辑可控，适用于固定流程自动化，如诈骗识别、智能导购、日程管理等 [工作流应用 (raw/application-user-guide/llm-application/workflow-application.md)](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，支持基于 Python 项目结构部署 Serverless 或 K8s 后端服务，提供完整 MCP 工具接入、自定义前端（Spark Design）、可观测性及企业级运维能力，适用于深度定制与私有算法集成 [高代码应用 (raw/application-user-guide/llm-application/rich-code-application.md)](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有类型均支持知识库（RAG）、MCP 工具（含官方与自定义）、[文件处理](../concepts/file-processing.md)（全文引用/切片检索/自定义处理）及多轮对话记忆等通用能力。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置范围/备注 |
|----------|--------|------|-----------------|
| **模型层** | `temperature` | 控制生成随机性与多样性 | 数值越高越随机；默认值依模型而异 |
| | `max_output_tokens`（或称“最长回复长度”） | 模型生成内容的 token 长度上限 | 不包含提示词；需结合上下文窗口合理设置 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | 开启后可展示推理逻辑，提升可调试性；不支持模型无法配置 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| **规划控制** | `ReAct 最大轮次` | 单次会话中工具调用的最大次数 | 1–50；超限则强制退出工具链并生成最终回复 |
| **[文件处理](../concepts/file-processing.md)** | `单文件最大解析长度（token）` | 全文引用模式下单个文件提取的 token 上限 | 超出部分从文件末尾截断 |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下召回与拼接的 token 控制 | 影响 RAG 效果与成本；相关性低的片段会被丢弃 |
| **记忆** | 短期记忆轮数 | 多轮对话中传递的历史消息数量 | 0–30 轮；0 表示不传递历史 |

> **注意**：文档 3 中提及“[长期记忆](../concepts/long-term-memory.md)的数据存储不收费”，但文档 1 明确指出“[长期记忆](../concepts/long-term-memory.md)功能计划在未来的迭代中支持”。当前版本**不支持[长期记忆](../concepts/long-term-memory.md)**，该描述已过时。

## 使用方式

1. **创建与配置**  
   - 访问百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择对应应用类型（智能体/工作流/高代码）并填写名称。  
   - 智能体：在模型选择器中指定模型（如 `千问-Max`），配置系统提示词、知识库、MCP、[文件处理](../concepts/file-processing.md)模式等 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
   - 工作流：拖拽节点（开始、大模型、意图分类、结束等）至画布，配置各节点参数与连接关系 [工作流应用 (raw/application-user-guide/llm-application/workflow-application.md)](../../raw/application-user-guide/llm-application/workflow-application.md)。  
   - 高代码：选择部署方式（Serverless/K8s），提交代码包（.whl）或使用模板，配置资源规格与环境变量 [高代码应用 (raw/application-user-guide/llm-application/rich-code-application.md)](../../raw/application-user-guide/llm-application/rich-code-application.md)。

2. **测试与调试**  
   - 所有类型均提供右侧对话/测试面板，支持文本输入、文件上传及 API 测试。  
   - 智能体支持卡片流展示“思考”与“工具调用”全过程；工作流支持节点级日志查看；高代码支持构建/运行日志实时追踪。

3. **发布与调用**  
   - **必须先发布**应用才能通过 API 或第三方渠道调用。发布后可在“发布渠道”页签获取 API 文档与调用示例。  
   - API 调用需携带有效 `Authorization: Bearer <API Key>`，请求体遵循标准格式（如 `input` 数组、`session_id`）。文件需通过 `file_list`（URL）或 `session_file_id`（上传 API 返回）传递。

## 限制和注意事项

- **兼容性限制**：旧版智能体（Agent 1.0）与新版（Agent 2.0）架构不兼容，**不支持直接升级或降级**，需重新创建应用 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件时效性**：通过聊天窗口上传的文件**仅在当前会话有效**，刷新或关闭页面即失效；通过 `session_file_id` 上传的文件有效期通常为 24 小时。  
- **模型能力约束**：  
  - `enable_thinking` 仅对明确支持思考模式的模型（如 `千问-Max`）生效；其他模型配置无效。  
  - 千问-VL 系列模型可直接解析图片/视频，无需开启预解析；其余模型及非图像/视频文件严格依赖预解析开关状态。  
- **计费关键点**：  
  - 模型调用费用按输入/输出 [Token](../concepts/token.md) 计费，**知识库召回内容、记忆体内容、文件解析文本均计入输入 [Token](../concepts/token.md)**。  
  - 切片检索模式通常比全文引用更节省 [Token](../concepts/token.md) 成本；自定义处理模式成本取决于工具调用复杂度。  
  - MCP 工具可能产生额外费用（如第三方 API 调用），由服务方收取，百炼不代收。  
- **API 限流**：每个智能体应用默认调用频率上限为 **100 次/分钟**，该配额被所有 API 请求共享（含文件问答、普通对话等）。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


