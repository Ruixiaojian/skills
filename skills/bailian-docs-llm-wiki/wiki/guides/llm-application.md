# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，通过封装模型调用、[工具集成](../concepts/tool-integration.md)、知识增强与流程编排能力，使开发者无需从零实现推理服务即可快速交付生产级 AI 功能。其核心价值在于将大模型能力与私有数据、实时信息和业务逻辑解耦并可组合，支持从零代码到高代码的全栈开发路径。

## 支持的模型/功能

百炼提供三类应用形态，分别适配不同抽象层级的开发需求：

- **智能体（Agent）应用**：以提示词驱动，由大模型自主规划任务、调用知识库或 MCP 工具完成开放式目标。适用于意图理解复杂、需动态决策的场景，如智能客服、旅行规划等。新版智能体（Agent 2.0）统一将知识库、MCP 等作为可规划工具，支持完整“思考-执行-反思”链路回溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：通过可视化节点编排定义确定性执行路径，支持大模型节点、意图分类、变量处理、智能体群组等多种节点类型。适用于流程固定、需强可控性的自动化任务，如日程管理、诈骗识别、多步骤导购等 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，基于 Python 项目结构部署 Serverless 或 K8s 后端服务，支持 MCP 工具一键接入、自定义前端 WebUI 及企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有应用均支持文件问答能力，提供三种处理模式：**全文引用**（适合短文档总结）、**切片检索（RAG）**（适合长文档精准问答）、**自定义处理**（依赖配置的 MCP/插件进行图片风格转换、视频分析等操作）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应避免在新项目中复用 Agent 1.0 配置逻辑，而应直接采用 Agent 2.0 范式。

## 关键参数

| 类别 | 参数名 | 说明 | 适用应用类型 |
|--------|--------|------|--------------|
| **模型控制** | `temperature` | 控制生成随机性，值越高输出越多样 | 全部支持 |
| | `enable_thinking` | 开启思考模式，仅对支持该能力的模型生效（如千问-Max系列），用于提升规划效果 | 智能体（Agent 2.0） |
| | `ReAct 最大轮次` | 限制单次会话中工具调用次数（1–50），超限后强制终止调用链并生成最终回复 | 智能体（Agent 2.0） |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下截断位置，默认从文件末尾截断 | 智能体（文件问答） |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 输入规模 | 智能体（文件问答） |
| **上下文管理** | 短期记忆轮数（0–30） | 在多轮对话中向模型注入历史消息，0 表示禁用 | 智能体（Agent 2.0） |
| | `historyList` 变量 | 工作流中预置的全局会话变量，供支持记忆的节点（如大模型、意图分类）引用 | 工作流 |
| **部署配置** | 实例规格 / 并发度 / 最小实例数 | 高代码应用的资源调度参数，影响性能与成本 | 高代码应用 |

## 使用方式

1. **创建与配置**  
   - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用（Agent 2.0）”，配置模型、系统提示词、知识库、MCP 工具及文件处理模式。  
   - 工作流：拖拽节点（开始/结束/大模型/意图分类/变量处理等）→ 连接执行流 → 配置各节点参数（如提示词、模型、记忆策略）→ 测试后发布。  
   - 高代码：选择模板或上传 `.whl` 包 → 配置部署方式（Serverless Function/K8s）与资源 → 部署后通过 API 测试或文本对话调试。

2. **发布与调用**  
   - 所有应用必须**先发布**才能被外部调用。发布后可在“发布渠道”页签获取 API Endpoint 和鉴权方式。  
   - API 调用需携带 `Authorization: Bearer <API Key>`，请求体格式统一为 JSON（含 `input` 对话数组、`session_id` 等）。高代码应用网关调用需额外配置 Token 鉴权路由 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
   - 文件上传支持三种方式：聊天窗口直传（会话级有效）、`file_list`/`image_list` URL 参数（需公网可访问）、`session_file_id`（推荐生产环境，有效期 24 小时）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

3. **调试与观测**  
   - 智能体（Agent 2.0）支持卡片流展示“思考”与“工具调用”步骤，便于定位非预期行为。  
   - 工作流支持画布内实时测试，并可查看各节点输出变量（如 `大模型1/result`）。  
   - 高代码应用提供构建/部署日志、运行时日志及 API 调用链路追踪。

## 限制和注意事项

- **模型兼容性**：并非所有模型均支持全部能力。例如，`enable_thinking` 仅对千问-Max 系列等具备强工具调用能力的模型生效；千问-VL 系列模型在关闭预解析时仍可直接解析图片/视频，但其他文本模型必须开启预解析才能处理非文本文件 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；上传文件仅在当前会话有效，刷新页面即丢失；超大文件必须使用 `session_file_id` 方式上传 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费边界**：  
  - 模型调用费用按输入/输出 Token 计费，知识库召回内容计入输入 Token；  
  - 工作流中 `historyList` 的内容虽参与 Prompt 构造，但**记忆体内容占用的 Token 暂不计费**（见文档 3）；  
  - MCP 工具调用可能产生第三方费用（如高德地图 API），百炼平台不收取该部分费用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **权限要求**：RAM 子账号创建应用并发布时，需具备 `ram:CreateServiceLinkedRole` 权限，否则发布失败 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


