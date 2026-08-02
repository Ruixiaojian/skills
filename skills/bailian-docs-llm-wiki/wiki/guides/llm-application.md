# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建能力，旨在突破大语言模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可零代码、低代码或专业编码方式，快速集成[知识库](../concepts/knowledge-base.md)、MCP 工具、记忆、多模态处理等能力，构建面向真实业务场景的可部署 AI 服务。

## 支持的模型/功能

百炼 `llm application` 支持三类应用形态，各自适配不同开发范式与业务需求：

- **智能体（Agent）应用**：以提示词驱动，支持自主意图理解、多步规划与工具调用（如[知识库](../concepts/knowledge-base.md)、MCP、内置沙箱工具）。新版 Agent 2.0 将[知识库](../concepts/knowledge-base.md)与 MCP 统一为可调度工具，支持完整“规划-执行-反思”链路回溯，显著提升复杂任务处理能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：基于可视化节点编排（如开始、大模型、意图分类、变量处理、结束），适用于固定流程自动化场景（如报告生成、客服多步骤分流、日程管理）。支持会话变量全局共享、自定义缓存及智能体群组嵌套调用 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，支持基于 Python 的 Serverless Function 或 K8s 部署，提供一站式 MCP 接入、可观测性、API 网关与自定义前端能力，适合深度定制与系统集成 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

文件处理能力统一由智能体承载，支持三种模式：**全文引用**（直接注入解析后全文，受上下文长度限制）、**切片检索**（RAG 检索增强，支持混合知识库与上传文件）、**自定义处理**（模型自主决策调用 MCP/插件处理文件）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先选用 Agent 2.0，旧版仅用于存量维护。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用应用类型 |
|----------|--------|------|--------------|
| **模型配置** | `model_id` | 如 `qwen-max-latest`、`qwen-vl-plus`；推荐 Agent 使用 `qwen-max` 系列以保障多步规划效果 | 全部 |
| | `temperature` | 控制输出随机性，范围通常 0.0–1.0 | 全部 |
| | `max_output_tokens` | 模型生成内容的最大 token 数 | 全部 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用）；影响 ReAct 过程中“Thinking”步骤是否展示 | Agent 2.0 |
| **文件处理** | `file_processing_mode` | 取值 `full_text` / `chunk_retrieval` / `custom`；决定文件内容如何注入模型上下文 | Agent |
| | `max_chunk_count` / `max_assembled_length` | 切片检索模式下控制召回片段数与总 token 上限 | Agent |
| **会话控制** | `history_rounds` | 短期记忆轮数（0–30），控制多轮对话上下文长度 | Agent 2.0 |
| | `react_max_steps` | ReAct 最大工具调用轮次（1–50），超限则终止调用并生成最终回复 | Agent 2.0 |
| **工作流特有** | `memory_type` | 节点级记忆选项：`node_cache`（仅本节点）或 `custom_cache`（全局会话） | Workflow |

## 使用方式

1. **创建与配置**  
   - 在控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面选择对应应用类型创建。  
   - Agent：配置模型、系统提示词（支持自定义变量）、知识库、MCP、技能、环境变量等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
   - Workflow：拖拽节点（大模型、意图分类、变量处理等），配置各节点模型、提示词、输入/输出变量，并连线形成执行流 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
   - 高代码：选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）、资源规格与环境变量 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

2. **测试与调试**  
   - 所有类型均支持右侧对话面板实时交互测试。  
   - Agent 支持卡片流展示“Thinking”与“Tool Call”过程；Workflow 支持逐节点日志查看；高代码提供 API 测试与文本对话双模式。

3. **发布与调用**  
   - **必须发布后方可调用**：发布操作位于应用配置页右上角，发布后生成稳定 API Endpoint。  
   - API 调用需使用百炼 API Key，请求体结构统一（如 `input`, `session_id`, `user_id`），具体参考各应用类型的 API 文档 [新版智能体应用 API](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference)、[调用工作流应用](https://help.aliyun.com/zh/model-studio/invoke-workflow-application/)、[高代码 API 开发指南](https://help.aliyun.com/zh/model-studio/rich-code-app-develop-guide)。  
   - 文件上传：聊天窗口上传仅限当前会话；生产环境推荐先调用文件上传 API 获取 `session_file_id`，再在对话请求中传入 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **模型与功能绑定**：千问-VL 系列模型具备原生[多模态能力](../concepts/multi-modal.md)，即使关闭预解析，也能直接解析图片/视频；而文本模型处理非图像文件时，严格依赖预解析开关状态 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；聊天窗口上传文件仅在当前会话有效，刷新即失效；通过 `session_file_id` 上传有效期为 24 小时 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费关键点**：  
  - 模型调用费用按实际输入/输出 Token 计费；知识库召回内容计入输入 Token；MCP 工具调用可能产生额外费用（第三方 API 费用由服务商收取）；  
  - Agent 的隐式缓存自动生效（公共前缀缓存，按 20% 输入单价计费），但不支持显式缓存配置 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；  
  - 高代码应用部署后即开始计费（函数计算、API 网关、模型调用等）[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
- **权限与部署**：高代码应用需授权 FC 和 API 网关服务角色；K8s 部署需提前开通 ACK 并完成授权；RAM 账号发布应用需确保拥有 `ram:CreateServiceLinkedRole` 权限 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


