# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种模式，分别覆盖零代码决策、低代码流程编排与专业级代码开发需求。三者统一基于大模型能力，通过知识库、MCP 工具、记忆等扩展机制突破模型原生局限，支持私有知识接入、实时信息获取与复杂任务规划。

## 支持的模型/功能

- **智能体（Agent）**：以提示词驱动自主规划，支持知识库（RAG）、MCP 工具调用、多模态文件处理（如千问VL系列）、短期记忆（0–30轮）及技能（Skill）挂载。新版智能体（Agent 2.0）将知识库与 MCP 统一为可调度工具，支持完整“规划-执行-反思”链路回溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，支持大模型节点、意图分类、变量处理、智能体群组等节点类型，并可跨应用复用已发布的智能体或工作流组件 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：基于 Python 全栈开发，支持 Serverless Function 或 K8s 部署，内置 MCP 工具接入、可观测性、API 网关与自定义前端（Spark Design 框架），适用于需深度定制与系统集成的生产级服务 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

> **注意**：文档 2（旧版智能体）与文档 3（新版智能体）存在架构不兼容问题——二者无法升级/降级，且新版 Agent 2.0 的工具调度逻辑、过程透明度与 ReAct 轮次控制均为旧版所不具备。开发者应优先选用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，除非存在明确的旧版依赖。

文件问答能力仅在**智能体应用**中提供，支持三种处理模式：  
- **全文引用**：直接注入解析后全文（受上下文长度限制）；  
- **切片检索（RAG）**：按语义召回相关片段，支持混合检索上传文件与知识库内容；  
- **自定义处理**：由模型自主决策调用 MCP 或[插件](../concepts/plugin.md)处理文件（如图片风格转换）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **模型层** | `temperature`、`max_tokens`、`enable_thinking` | 温度控制输出随机性；`max_tokens` 限制生成长度；`enable_thinking` 仅对支持思考模式的模型（如千问-Max）生效，用于开启推理链展示。 |
| **文件处理** | 单文件最大解析长度、最大拼装长度（全文引用）；召回片段数、最大拼装长度（切片检索） | 控制 [Token](../concepts/token.md) 消耗与信息完整性，超限时从末尾截断或按相关性丢弃低分片段。 |
| **执行控制** | `ReAct 最大轮次`（1–50） | 限制单次会话中工具调用总次数，超限则终止调用并生成最终回复。 |
| **记忆** | 短期记忆轮数（0–30） | 0 表示不传递历史对话；值越大上下文越连贯，但输入 [Token](../concepts/token.md) 增加。[长期记忆](../concepts/long-term-memory.md)当前未开放。 |
| **环境与安全** | 环境变量、鉴权密钥配置（通过“环境”模块） | 用于技能调用时注入敏感凭证，避免硬编码。 |

## 使用方式

1. **创建与配置**  
   - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用（Agent 2.0）”，配置模型、系统提示词、知识库、MCP 及文件处理模式。  
   - 工作流：拖拽节点（开始/大模型/意图分类/结束等），连线定义执行流，通过 `${sys.query}` 等变量引用会话上下文。  
   - 高代码：选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）、资源规格与网关路由。  

2. **测试与调试**  
   - 所有类型均支持控制台右侧对话窗口实时测试；  
   - 工作流支持多轮交互测试（如智能导购案例中连续输入“家用”→“200L”→“一级能效”）；  
   - 高代码应用提供 `GET /health` 和 `/process` API 测试入口。  

3. **发布与调用**  
   - **必须先发布**：所有应用需点击“发布”按钮生效，否则 API 调用返回 404；  
   - API 调用路径统一为：`POST https://dashscope.aliyuncs.com/api/v1/services/bailian/<app_id>/call`，需携带 `Authorization: Bearer <api_key>`；  
   - 文件上传推荐使用 `session_file_id` 方式（调用文件上传 API 获取 ID 后传入对话请求），规避公网 URL 访问限制与 10MB 单文件上限 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  

## 限制和注意事项

- **计费逻辑**：仅调用产生费用。模型调用按输入/输出 [Token](../concepts/token.md) 计费；知识库按量计费（非免费）；MCP 工具费用由官方或第三方收取；[长期记忆](../concepts/long-term-memory.md)存储免费，但其内容计入 Prompt 导致 Token 消耗增加（该部分 Token **暂不计费**）。  
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；上传文件仅在当前会话有效，刷新即失效；超大文件必须使用 `session_file_id` 方式。  
- **权限要求**：RAM 账号创建应用时，发布前需确保拥有 `ram:CreateServiceLinkedRole` 权限；高代码部署需授权函数计算（FC）与 API 网关角色。  
- **地域约束**：文件问答功能仅支持中国大陆版（北京地域）；工作流与高代码部署地域须与网关地域一致。  
- **版本隔离**：Agent 1.0 与 Agent 2.0 不兼容，无法迁移配置；工作流中引用的智能体必须已**发布为组件**方可被调用。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


