# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，通过封装大模型能力与外部系统集成能力，支持开发者和业务人员以零代码、低代码或高代码方式快速构建可交付的 AI 服务。其核心价值在于突破大模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限，提供智能体（Agent）、工作流（Workflow）和高代码应用三种互补的技术路径。

## 支持的模型/功能

百炼 LLM Application 支持三类主流构建模式，各自适配不同抽象层级与开发需求：

- **智能体（Agent）应用**：以提示词驱动，具备自主意图理解、多步规划与工具调用能力。新版智能体（Agent 2.0）将知识库、MCP 等统一为可调度工具，支持完整“规划-执行-反思”链路回溯，适用于开放式对话、动态任务助理等场景 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：基于可视化节点编排（如开始、大模型、意图分类、变量处理、结束等），实现确定性、可复现的多步骤自动化流程，适合报告生成、订单审批、智能导购等固定路径任务 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，支持完整 Python 项目部署为 Serverless 或 K8s 后端服务，内置 MCP 工具接入、可观测性与自定义前端能力，适用于需深度定制、私有算法集成或企业级运维的场景 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有类型均支持文件问答能力，提供**全文引用**、**切片检索（RAG）** 和**自定义处理**三种模式，覆盖文档、图片、音视频等[多模态](../concepts/multi-modal.md)输入 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“不支持将旧版智能体升级到新版本”，且新版已将知识库作为工具纳入统一调度体系，而旧版仍将其视为独立能力模块。实际开发应优先采用 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，避免依赖已弃用的 Agent 1.0 路径。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用场景 |
|----------|--------|------|----------|
| **模型配置** | `temperature` | 控制生成随机性，值越高越发散 | 所有应用类型通用 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用） | 新版智能体中用于增强反思能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| | `ReAct 最大轮次`（1–50） | 单次会话中工具调用最大次数 | 新版智能体防止无限循环 |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下截断位置（从末尾） | 防止超上下文，见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 输入规模 | 平衡精度与 [Token](../concepts/token.md) 成本 |
| **会话控制** | `短期记忆轮数`（0–30） | 多轮对话中保留的历史轮数 | 新版智能体，0 表示禁用上下文 |
| | `historyList` 变量 | 工作流中预置的全局对话历史变量 | 工作流节点间共享上下文 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) |

## 使用方式

- **创建入口**：统一通过百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → **创建应用**，按类型选择入口。  
- **配置核心**：  
  - 智能体：在模型选择器中指定 `千问-Max` 等强工具调用模型；通过系统提示词定义角色与工具使用规则；在“规划”模块启用知识库、MCP、技能等能力 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：拖拽节点（大模型、意图分类、变量处理等）至画布，配置各节点的模型、提示词、输入/输出变量（如 `${sys.query}`、`大模型1/result`），并连线形成执行流 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 高代码：选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）、资源规格及环境变量；通过“工具”Tab 关联知识库/MCP，通过“网关”Tab 发布生产 API [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
- **发布与调用**：**所有应用必须发布后方可调用**。发布后可在“发布渠道”页签获取 API Endpoint 与鉴权方式（API Key 或网关 [Token](../concepts/token.md)），支持 HTTP POST 调用标准 JSON 接口。文件需通过 `file_list`（URL）或 `session_file_id`（上传 API 返回）传递，不可在请求体中直接嵌入二进制内容 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **模型兼容性**：`enable_thinking` 参数仅对支持思考模式的模型生效（如千问-Max 系列），非支持模型在配置界面中不可见；千问-VL 系列模型在关闭预解析时仍可直接解析图片/视频，但其他模型必须开启预解析才能处理非文本文件 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤ 10MB；聊天窗口上传的文件**仅在当前会话有效**，刷新即失效；生产环境推荐使用文件上传 API 获取 `session_file_id` 以支持更大文件与稳定传输 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **计费关键点**：  
  - 模型调用费用 = 输入 [Token](../concepts/token.md)（含知识库召回内容、文件解析文本、记忆体内容） + 输出 Token；  
  - 知识库检索本身不额外计费，但召回文本计入输入 Token；  
  - [长期记忆](../concepts/long-term-memory.md)存储免费，但其内容参与 Prompt 构建，**占用的 Token 暂不计费**（见文档 3）；  
  - MCP 工具调用费用由第三方或按模型调用计费，百炼不加收 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **权限与部署**：高代码应用部署需提前授权函数计算（FC）与 API 网关服务角色；工作流中“自定义缓存”记忆功能需在节点级显式启用；RAM 子账号发布应用前须确保拥有 `ram:CreateServiceLinkedRole` 权限 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


