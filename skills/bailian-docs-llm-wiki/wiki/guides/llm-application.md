# llm application

`llm application` 是阿里云百炼平台面向业务场景构建 AI 应用的核心能力层，提供智能体（Agent）、工作流（Workflow）和高代码应用三种互补的构建范式，分别覆盖零代码决策、低代码编排与专业级代码部署需求。三者均基于大模型驱动，通过集成知识库、MCP 工具、数据连接器等能力突破模型原生局限，支持私有知识问答、实时信息获取、多步任务规划与系统级集成。

## 支持的模型/功能

- **智能体（Agent）**：以提示词驱动自主规划，统一调度知识库、MCP、内置工具（如 `bash`、`read`、`edit`）及应用组件。新版 Agent 2.0 将知识库与 MCP 均抽象为可动态调用的工具，支持完整“思考-执行-反思”链路回溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：通过可视化节点（大模型、意图分类、变量处理、智能体群组等）编排确定性执行流，支持多轮对话记忆（`historyList`）、会话变量全局共享及混合调用本地文件与知识库内容 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：基于 Python 项目结构部署 Serverless Function 或 K8s 服务，支持 MCP 工具一站式接入、自定义前端（Spark Design 框架）及企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
- **文件处理模式**：智能体中支持三种文件交互方式——**全文引用**（整文入上下文）、**切片检索**（RAG 式召回）、**自定义处理**（模型自主调用工具），适配文档总结、长文问答、图片风格转换等不同需求 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”，开发者需根据场景选型新建应用，不可迁移配置。

## 关键参数

| 类别 | 参数名 | 说明 | 取值范围/示例 |
|--------|--------|------|----------------|
| **通用** | `temperature` | 控制生成随机性 | 0.0–1.0，默认 0.8 |
| | `max_tokens` | 模型生成的最大 token 数 | 正整数，如 2048 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | `true`/`false` |
| **智能体专属** | `ReAct 最大轮次` | 单次会话中工具调用最大次数 | 1–50 |
| | `短期记忆轮数` | 多轮对话保留的历史轮数 | 0–30（0 表示禁用） |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下单文件截断位置 | 正整数，从文件末尾截断 |
| | `召回片段数` | 切片检索模式下返回的最大相关片段数 | 正整数，如 3 |
| **工作流专属** | `自定义缓存` | 节点级记忆开关，决定是否继承全局 `historyList` | 启用/禁用 |

## 使用方式

- **创建入口**：全部应用均通过控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → **创建应用** 进入，按类型选择模板。  
- **配置核心**：  
  - 智能体：在「规划」模块配置模型、系统提示词（支持自定义变量 `/var_name`）、知识库标签过滤、MCP 接入及文件处理模式；  
  - 工作流：拖拽节点至画布，配置各节点的模型、提示词、输入变量（如 `${sys.query}`）及连接逻辑；  
  - 高代码：选择部署方式（Serverless/K8s）、上传 `.whl` 包或使用模板，通过「工具」Tab 关联 MCP 服务。  
- **调试与发布**：所有类型均支持右侧面板「文本对话体验」实时测试；**发布是 API 调用前提**，发布后可在「发布渠道」页签获取 API Endpoint 与鉴权方式。  
- **API 调用**：遵循统一 RESTful 规范，请求体需包含 `input`（消息数组）、`session_id` 等字段；文件需通过 `file_list`（URL）或 `session_file_id`（上传 API 返回）传递 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **计费约束**：  
  - 模型调用费用按输入/输出 token 计费，知识库召回内容计入输入 token；  
  - 文件上传本身免费，但全文引用模式因整文入参易导致 token 消耗激增，建议长文档优先选用切片检索模式；  
  - 自定义[插件](../concepts/plugin.md)超时限制为 5 秒（见文档 3），MCP 服务可能产生第三方费用。  
- **技术限制**：  
  - 智能体暂不支持显式上下文缓存配置，仅支持平台自动隐式缓存（命中部分 token 按 20% 计费）；  
  - 上传文件仅在当前会话有效，刷新页面即丢失；生产环境推荐使用 `session_file_id` 方式上传；  
  - 工作流中 `imageList` / `historyList` 等预置变量需在支持「记忆」功能的节点（如大模型、意图分类）中显式启用「自定义缓存」才生效。  
- **安全与权限**：  
  - 发布应用需 RAM 账号具备 `ram:CreateServiceLinkedRole` 权限；  
  - 高代码应用部署需授权函数计算（FC）与 API 网关服务角色；  
  - 环境变量（如 API Key）应在「部署」→「配置」中设置，避免硬编码于技能代码中。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


