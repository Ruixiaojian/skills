# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，通过智能体（Agent）、工作流（Workflow）和高代码应用三类模式，突破大模型在私有知识接入、实时信息获取、流程控制与复杂任务规划等方面的原生局限。开发者可根据任务开放性、流程确定性及定制深度，选择零代码、低代码或专业编码方式快速交付可生产部署的 AI 服务。

## 支持的模型/功能

- **模型支持**：所有 LLM Application 类型均支持千问系列主流模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`、`qwen-long`、`qwen-vl-max` 等），以及部分 DeepSeek 和开源模型；具体可用模型以控制台实时列表为准（参见 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)）。  
- **核心能力统一抽象为工具**：新版智能体（Agent 2.0）将知识库、MCP 服务、数据连接器、应用组件、内置技能（Skill）等全部纳入统一工具调度体系，由模型自主规划调用顺序与时机；而旧版智能体（Agent 1.0）则采用分阶段调用逻辑（先 RAG 后 MCP），过程不可追溯 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **[多模态](../concepts/multi-modal.md)文件处理**：支持文档、图片、音视频等 10+ 格式（单文件 ≤10MB），提供三种处理模式：**全文引用**（适用于短文档总结）、**切片检索（RAG）**（适用于长文档精准问答）、**自定义处理**（依赖配置的 MCP/插件执行编辑、转换等操作）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **工作流节点能力**：包含大模型、意图分类、变量处理、智能体群组等标准化节点，支持多路分支、状态传递与会话变量全局共享，适用于固定流程自动化场景（如客服分流、报告生成、日程管理）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码扩展能力**：支持基于 Python 的 Serverless Function 或 K8s 部署，可一站式接入 MCP 工具、自定义前端 WebUI（基于 Spark Design 框架），并集成企业级可观测性与 API 网关 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 2（智能体应用）与文档 3（新版智能体应用）存在关键架构差异：Agent 1.0 不支持“规划-执行-反思”全过程展示，且知识库与 MCP 调用逻辑分离；Agent 2.0 将二者统一为工具并支持动态调度。两者不兼容，无法升级，需重新创建应用。

## 关键参数

| 参数类别 | 参数名 | 说明 | 适用场景 |
|----------|--------|------|----------|
| **模型参数** | `temperature` | 控制输出随机性，取值 0–2，推荐 0.3–0.7 用于确定性任务 | 所有应用类型 |
| | `enable_thinking` | 是否开启思考模式（仅支持模型可用），影响 ReAct 链路中“Thinking”步骤是否展示 | 新版智能体（Agent 2.0） |
| | `max_react_rounds` | 单次会话中[工具调用](../concepts/tool-use.md)最大轮次（1–50），超限后强制生成最终回复 | 新版智能体 |
| **文件处理** | `single_file_max_tokens` | 全文引用模式下，单文件解析 token 上限（从末尾截断） | 文件问答 |
| | `retrieval_top_k` | 切片检索模式下，召回片段数上限 | 文件问答 |
| **记忆与上下文** | `short_term_memory_rounds` | 新版智能体短期记忆轮数（0–30），0 表示禁用多轮上下文 | 新版智能体 |
| | `historyList` / `imageList` | 工作流中预置会话变量，用于跨节点传递对话历史与图片列表 | 工作流应用 |
| **安全与鉴权** | 环境变量（`ENV`） | 在智能体/高代码应用中配置密钥、API Key 等敏感信息，避免硬编码 | 新版智能体、高代码应用 |

## 使用方式

- **创建与配置**：  
  - 智能体：控制台 → 应用中心 → 创建应用 → 选择 **智能体应用（Agent 2.0）**（推荐）或 **智能体应用（Agent 1.0）**；配置模型、系统提示词、知识库、MCP 工具等 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：拖拽节点（开始、大模型、意图分类、结束等）→ 连接执行路径 → 配置各节点模型、提示词、变量映射 → 测试 → 发布 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 高代码：控制台创建空白应用 → 选择部署方式（Serverless/K8s）→ 提交代码包（`.whl`）或使用模板 → 配置网关与前端 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

- **发布与调用**：  
  - **必须发布后方可调用**：所有应用类型均需在控制台单击“发布”按钮完成上线（含版本变更确认）[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
  - **API 调用**：发布后，在“发布渠道”页签查看 API 文档与 endpoint；智能体支持 `POST /v1/agents/{agent_id}/chat`，工作流支持 `POST /v1/workflows/{workflow_id}/run`，高代码应用接口由部署时自动生成 [新版智能体应用 API](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference)。  
  - **文件上传**：调试界面直接上传（仅当前会话有效）；生产环境推荐调用独立的 [文件上传 API](https://help.aliyun.com/zh/model-studio/call-single-agent-application/#30619780ddy93) 获取 `session_file_id` 后传入对话请求。

## 限制和注意事项

- **文件限制**：单次会话最多上传 10 个文件，单文件 ≤10MB；通过 URL（`file_list`/`image_list`）方式调用时，需确保公网可访问且非临时签名链接 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **调用限频**：每个智能体应用默认限流 **100 次/分钟**，该配额被所有 API 请求共享（含文件问答、普通对话等）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **模型能力约束**：  
  - 千问-VL 系列模型可直接解析图片/视频，无需开启预解析；其他文本模型处理非图像文件时，必须开启预解析才能提取内容 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 自定义插件超时限制为 **5 秒**，超时将中断调用 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **计费要点**：  
  - 仅调用产生费用，创建/配置不收费；  
  - 知识库检索内容计入模型输入 [Token](../concepts/token.md)，增加推理费用；  
  - MCP 工具按调用次数或第三方 API 规则计费，百炼不额外加收；  
  - [长期记忆](../concepts/long-term-memory.md)存储免费，但其内容注入 Prompt 会增加 [Token](../concepts/token.md) 消耗（暂不计费）[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **版本与兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，无法迁移；高代码应用暂不支持显式上下文缓存（仅隐式缓存生效）[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)


