# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建范式，通过智能体（Agent）、工作流（Workflow）和高代码应用三种模式，将大语言模型与知识库、外部工具、数据源及定制逻辑深度集成，突破模型原生能力边界，支撑私有知识问答、实时信息获取、多步任务规划与复杂流程自动化等真实业务需求。

## 支持的模型/功能

百炼 LLM Application 支持三类核心构建模式，各自适配不同开发范式与业务复杂度：

- **智能体（Agent）应用**：以提示词驱动，支持自主意图理解、动态任务规划与工具调用。新版智能体（Agent 2.0）统一将知识库、MCP 服务等作为可调度工具，支持完整的“思考-执行-反思”链路回溯，显著提升复杂任务处理能力与过程可解释性 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）应用**：基于可视化节点编排，严格按预定义顺序执行大模型推理、API 调用、条件判断等步骤，适用于固定流程自动化，如诈骗识别、智能导购、日程管理等场景 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，支持完整 Python 项目部署为 Serverless 或 K8s 后端服务，提供 MCP 工具一站式接入、自定义前端（Spark Design）、可观测性与企业级运维能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有模式均支持文件问答能力，包含全文引用、切片检索（RAG）和自定义处理三种模式，适配文档、图片、音视频等多模态输入 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 4（旧版智能体）与文档 2（新版智能体）存在明确架构不兼容声明：“旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级”。开发者应优先选用 Agent 2.0，并通过新建应用而非迁移方式启用。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用模式 |
|----------|--------|------|----------|
| **模型配置** | `temperature` | 控制生成随机性，值越高输出越多样；默认建议 0.1–0.7 | 智能体、工作流、高代码 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型），影响规划链路展示完整性 | 智能体（Agent 2.0） |
| | `ReAct 最大轮次` | 限制单次会话中工具调用次数（1–50），防无限循环 | 智能体（Agent 2.0） |
| **文件处理** | `单文件最大解析长度（token）` | 全文引用模式下截断位置（从文件末尾起） | 智能体（文件问答） |
| | `召回片段数` / `最大拼装长度` | 切片检索模式下控制 RAG 输入规模 | 智能体（文件问答） |
| **会话控制** | 短期记忆轮数（0–30） | 多轮对话上下文保留轮数，0 表示无历史传递 | 智能体（Agent 2.0） |
| | `historyList` 变量 | 工作流中全局会话变量，供支持记忆的节点（如大模型、意图分类）引用 | 工作流 |
| **部署配置** | 实例规格 / 并发度 / 最小实例数 | 影响高代码应用性能与冷启动延迟，时延敏感业务建议最小实例数 ≥ 1 | 高代码 |

## 使用方式

- **创建与配置**：  
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用” → **Agent 2.0**（推荐）→ 配置模型、系统提示词、知识库、MCP 工具等 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：拖拽节点（开始、大模型、意图分类、结束等）→ 连接执行路径 → 在各节点中配置模型、提示词、用户提示词（如 `${sys.query}`）及记忆策略 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 高代码：控制台选择模板或上传 `.whl` 包 → 配置部署方式（Serverless/K8s）、资源规格 → 一键部署 → 通过 API 测试或文本对话调试 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

- **发布与调用**：  
  所有应用**必须发布后方可被调用**。发布后：  
  - 智能体/工作流：在“发布渠道”页签获取 API Endpoint 与鉴权方式，支持标准 HTTP POST 请求（需携带 `Authorization: Bearer <API Key>`）。  
  - 高代码：除测试面板外，建议开通云原生 API 网关，配置路由与 [Token](../concepts/token.md) 鉴权，实现生产环境稳定访问 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
  - 文件问答：API 调用时需按模式选择参数——`image_list`/`file_list`（URL 方式）或 `session_file_id`（上传 API 返回 ID），且**无法在 API 调用时动态切换处理模式** [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **模型与文件兼容性**：  
  - 千问-VL 系列模型具备原生多模态能力，即使关闭“预解析文件”，也可直接解析图片/视频；其他文本模型则严格依赖预解析开关状态 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 文件上传限单次会话最多 10 个、单文件 ≤10MB；超限场景必须使用文件上传 API 获取 `session_file_id` [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  

- **计费关键点**：  
  - 模型调用费用按输入/输出 [Token](../concepts/token.md) 计费，**知识库检索内容计入输入 [Token](../concepts/token.md)**，切片检索模式通常比全文引用更节省成本 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
  - MCP 工具费用分两类：阿里云官方 MCP 按模型调用计费；第三方 MCP 调用产生的费用由第三方收取，百炼不代收 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - [长期记忆](../concepts/long-term-memory.md)存储免费，但其内容注入 Prompt 后增加的 Token **暂不计费**（仅短期记忆 Token 计费） [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  

- **行为约束**：  
  - 自定义[插件](../concepts/plugin.md)超时限制为 5 秒，超时将中断调用 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
  - 工作流中“意图分类”节点的缓存策略需明确选择“自定义缓存”以实现跨节点上下文共享，否则仅限当前节点内有效 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 智能体未按预期调用工具时，需排查四方面：技能是否挂载成功、系统提示词是否清晰描述工具能力与触发条件、用户意图是否明确指向该技能、是否达到 `ReAct 最大轮次` 限制 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


