# llm application

`llm application` 是阿里云百炼平台面向业务场景构建 AI 应用的核心抽象，旨在突破大语言模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限。通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，开发者可按需选择零代码、低代码或专业编码方式，集成知识库、MCP 工具、记忆、[数据连接](../concepts/data-connection.md)器等能力，快速交付稳定、可控、可复现的生产级 AI 服务。

## 支持的模型/功能

百炼 `llm application` 支持三类核心构建模式，各自适配不同能力边界与开发范式：

- **智能体（Agent）应用**：以提示词驱动，由大模型自主理解意图、规划步骤、动态调用知识库、MCP 工具、内置沙箱（如 `bash`/`read`/`edit`）等能力完成开放式任务。新版智能体（Agent 2.0）将知识库与 MCP 统一为可规划工具，支持完整“思考-执行-反思”链路回溯，显著优于旧版固定调度逻辑 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：通过可视化节点编排（如大模型、意图分类、变量处理、智能体群组等）定义确定性执行路径，适用于多步骤自动化场景（如电商客服分流、诈骗识别、日程管理）。节点间通过会话变量（`query`/`historyList`/`imageList`）共享上下文，支持自定义缓存与全局记忆 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，基于 Python 项目结构（支持 `.whl` 包或命令行部署），提供 Serverless Function 或 K8s 两种部署方式，并原生集成 MCP 工具接入、API 网关、可观测性及 Spark Design 前端框架 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

文件处理能力统一内置于智能体中，支持三种模式：**全文引用**（整文件入上下文，适合短文档总结）、**切片检索**（RAG，长文档精准问答）、**自定义处理**（模型自主调用 MCP/插件处理文件，如图片风格转换）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 3（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先选用 Agent 2.0，旧版仅用于存量维护。

## 关键参数

各模式关键配置参数如下：

- **智能体**：  
  - `enable_thinking`：是否开启思考模式（仅支持模型可用），影响决策过程透明度；  
  - `ReAct 最大轮次`（1–50）：限制单次会话中工具调用总次数；  
  - `短期记忆轮数`（0–30）：控制多轮对话上下文长度；  
  - 文件处理参数：`单文件最大解析长度`（token）、`最大拼装长度`（全文引用）；`召回片段数`、`最大拼装长度`（切片检索）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  

- **工作流**：  
  - 节点级参数：大模型节点的 `温度系数`、`最长回复长度`；意图分类节点的 `自定义缓存` 开关；  
  - 全局会话变量：`query`（用户输入）、`historyList`（对话历史）、`imageList`（上传图片列表）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  

- **高代码应用**：  
  - 部署参数：`vCPU`/`内存`/`最小实例数`/`单实例并发度`；  
  - 环境变量：用于注入 MCP 工具鉴权密钥等敏感信息；  
  - 网关参数：自定义域名、[Token](../concepts/token.md) 鉴权路由 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 使用方式

- **创建与配置**：  
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → 指定 Agent 2.0 → 配置模型、系统提示词、知识库、MCP、文件处理模式；  
  - 工作流：拖拽节点（开始/大模型/意图分类/结束等）→ 连接连线 → 配置各节点参数（如提示词、模型、变量引用）→ 测试 → 发布；  
  - 高代码：控制台创建空白应用 → 选择模板或上传 `.whl` 包 → 配置部署资源 → 部署 → 在“工具”Tab 关联知识库/MCP → 在“网关”Tab 启用生产路由 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

- **调用与集成**：  
  - 所有应用**必须先发布**才能被调用；  
  - API 调用统一通过“发布渠道”页签的“查看API”获取 endpoint 与鉴权方式；  
  - 文件问答 API 中，`file_list`（通用文件 URL）与 `image_list`（图片 URL）参数用于传递文件，`session_file_id`（通过文件上传 API 获取）推荐用于生产环境大文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；  
  - 工作流支持将已发布的智能体/工作流作为“智能体群组”节点嵌入，实现跨应用能力复用 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

## 限制和注意事项

- **通用限制**：  
  - 单次智能体会话 `ReAct 轮次` 上限为 50；  
  - 文件上传：单会话最多 10 个文件，单文件 ≤10MB；上传文件仅在当前会话有效，刷新即失效；  
  - API 调用频率：默认 100 次/分钟/应用，所有 API 请求共享此配额 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  

- **模型与能力限制**：  
  - `enable_thinking` 参数仅对支持思考模式的模型（如千问-Max）生效；  
  - 千问-VL 系列模型可直接解析图片/视频，无需开启预解析；其他模型必须显式开启预解析才能处理非文本文件 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；  
  - 自定义插件超时限制为 5 秒 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  

- **计费说明**：  
  - 仅调用产生费用，创建应用不收费；  
  - 费用主体为模型调用（按输入/输出 [Token](../concepts/token.md) 计费）、知识库（按量付费 + 召回内容增加 [Token](../concepts/token.md)）、MCP（按调用或第三方计费）；  
  - “[长期记忆](../concepts/long-term-memory.md)”存储免费，但其内容注入 Prompt 产生的 Token 暂不计费 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)；  
  - 高代码应用部署后即开始计费（函数计算、API 网关、模型调用等）[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

> **注意**：文档 3 提到“[长期记忆](../concepts/long-term-memory.md)的数据存储不收费”，而文档 2 明确说明“[长期记忆](../concepts/long-term-memory.md)：该功能计划在未来的迭代中支持”。二者存在事实矛盾——当前（Agent 2.0）**不支持长期记忆功能**，文档 3 的描述已过时，应以文档 2 为准。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


