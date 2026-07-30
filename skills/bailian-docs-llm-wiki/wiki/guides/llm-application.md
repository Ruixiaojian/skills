# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建范式，用于突破大语言模型在私有知识访问、实时信息获取、多步任务规划和确定性流程执行等方面的原生局限。通过将 LLM 与知识库、MCP 工具、工作流及代码能力深度集成，开发者可零代码或低代码构建面向真实业务场景的智能应用，如客服助手、旅行规划、日程管理等。该能力体系包含智能体（Agent）、工作流（Workflow）和高代码应用三类形态，分别适配自主决策、流程编排与深度定制需求。

## 支持的模型/功能

- **模型支持**：智能体应用支持千问全系列模型（如 `qwen-max`、`qwen-plus-latest`、`qwen-vl-plus`），以及 DeepSeek 等第三方模型；其中 `qwen-max` 和 `qwen-vl` 系列因强工具调用与[多模态](../concepts/multi-modal.md)能力被明确推荐用于复杂规划与文件处理场景 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **核心功能**：
  - **知识库（RAG）**：作为智能体的一项可调度工具，支持标签过滤以提升检索精度 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - **MCP 工具接入**：所有外部工具（含官方 MCP 广场服务与自定义 MCP）均统一纳入智能体的自主规划调度体系，支持动态、非固定顺序调用。
  - **文件处理**：提供三种模式：**全文引用**（适合总结/翻译）、**切片检索**（RAG 驱动，适合长文档问答）、**自定义处理**（模型自主调用工具，如图片风格转换）[文件问答 (raw/application-user-guide/llm-application/file-q-a.md)](../../raw/application-user-guide/llm-application/file-q-a.md)。
  - **内置沙箱工具**：包括 `bash`、`write`、`read`、`edit`、`glob`、`grep`、`download_file`，全部默认关闭，按需启用。
  - **技能（Skill）与应用组件**：支持将已发布智能体或工作流作为工具嵌入，实现能力复用。

> **注意**：文档 3（`single-agent-application.md`）仍使用“插件”一词描述外部工具，而文档 1（`new-single-agent-application.md`）已全面升级为“MCP 协议”并强调统一调度；当前平台以 MCP 为标准范式，旧版“插件”概念已过时，应以 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 为准。

## 关键参数

- **模型级参数**：
  - `temperature`：控制生成随机性，取值范围通常为 0.0–1.0。
  - `max_tokens`（最长回复长度）：限制模型输出 token 数，不含提示词。
  - `enable_thinking`：开启后支持思考链（Chain-of-Thought）推理，仅对兼容模型生效。
- **智能体行为参数**：
  - **ReAct 最大轮次**：限制单次会话中工具调用总次数（1–50），超限则终止调用并生成最终回复。
  - **短期记忆轮数**：配置 0–30 轮上下文，0 表示不传递历史对话；[长期记忆](../concepts/long-term-memory.md)暂未开放。
- **文件处理参数**（仅在 `file-q-a.md` 中明确定义）：
  - **全文引用模式**：`单文件最大解析长度（token）`（从末尾截断）、`最大拼装长度（token）`（从最后文件末尾截断）。
  - **切片检索模式**：`召回片段数`、`最大拼装长度`（按相关性得分丢弃低分片段）。

## 使用方式

- **创建路径**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择 **智能体应用 > Agent 2.0**（推荐）[新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流：通过可视化节点编排（开始/大模型/意图分类/结束等），适用于固定流程自动化 [工作流应用 (raw/application-user-guide/llm-application/workflow-application.md)](../../raw/application-user-guide/llm-application/workflow-application.md)。
  - 高代码应用：基于 Python 项目结构部署，支持 Serverless Function 或 K8s，适合深度定制 [高代码应用 (raw/application-user-guide/llm-application/rich-code-application.md)](../../raw/application-user-guide/llm-application/rich-code-application.md)。
- **调用方式**：
  - 所有应用必须**先发布**才能调用（API/SDK/钉钉/微信等渠道）。
  - API 调用入口统一位于应用的 **发布渠道 > API调用** 页签。
  - 文件问答的 API 调用需遵循预设处理模式，**无法在请求时动态切换**（如全文引用模式下，API 仅接收 `file_list` URL 并自动解析文本）[文件问答 (raw/application-user-guide/llm-application/file-q-a.md)](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 基于不同架构，**不支持直接升级或降级**；需重新创建新版应用 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **文件限制**：
  - 单会话最多上传 10 个文件，单文件 ≤10MB；
  - 上传文件**仅在当前会话有效**，刷新或关闭页面即丢失；
  - 生产环境推荐使用 `session_file_id`（文件上传 API）方式，支持更大文件与更稳定传输。
- **计费要点**：
  - 模型调用费用取决于输入/输出 token 总量，其中 RAG 检索内容、文件解析文本、记忆体内容均计入输入 token（记忆体内容 token 暂不计费）；
  - 工具调用（如 MCP、插件）可能产生额外费用，部分由第三方收取；
  - 上下文缓存仅支持**隐式缓存**（自动生效，不可配置），暂不支持显式缓存。
- **调试与排查**：
  - 若工具未按预期调用，需检查四点：技能是否挂载成功、系统提示词是否清晰引导工具使用、用户意图是否明确指向该技能、是否达到 ReAct 轮次上限 [新版智能体应用 (raw/application-user-guide/llm-application/new-single-agent-application.md)](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


