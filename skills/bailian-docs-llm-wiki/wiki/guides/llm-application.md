# llm application

`llm application` 是阿里云百炼平台面向开发者提供的大语言模型应用构建能力集合，支持通过零代码、低代码或高代码方式，将 LLM 与知识库、外部工具（MCP/插件）、多模态文件处理等能力深度集成，以突破模型原生能力边界，构建可解决真实业务问题的 AI 应用。核心形态包括智能体（Agent）、工作流（Workflow）和高代码应用三类，分别适用于动态规划、固定流程编排和深度定制场景。

## 支持的模型与功能

- **模型支持**：  
  智能体应用支持千问系列（如 `千问-Max`、`千问-Plus-Latest`、`千问-VL-Max`）、DeepSeek 及开源模型等；其中 `千问-VL` 系列具备多模态能力，可直接解析图片/视频，无需预解析 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  > **注意**：文档 3 中提及“插件”作为独立能力，而文档 1 明确指出新版智能体已统一采用 MCP 协议接入所有外部工具（含原插件），旧版插件机制已逐步迁移。实际开发中应优先使用 MCP [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **核心功能**：  
  - **知识库（RAG）**：支持切片检索与全文引用两种模式，可与上传文件混合检索 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)；新版智能体将知识库作为自主规划调用的工具之一，支持标签过滤提升精度。  
  - **工具调用**：内置沙箱工具（`bash`、`read`、`write` 等）及 MCP 服务（官方 MCP 广场或自定义服务），支持多步 ReAct 规划。  
  - **文件处理**：提供三种模式——**全文引用**（适合总结/翻译）、**切片检索**（适合长文档问答）、**自定义处理**（需配置 MCP/插件，适合图像风格转换等复杂操作）。  
  - **记忆**：支持 0–30 轮短期记忆；[长期记忆](../concepts/long-term-memory.md)暂未开放。  
  - **技能（Skill）**：可复用的能力包，自动识别任务并调用，无需编码。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 备注 |
|------|------|----------------|------|
| `enable_thinking` | 是否开启思考模式（仅支持模型） | `true` / `false` | 开启后可展示“规划-执行-反思”链路，仅限支持该能力的模型（如 `千问-Max`）；不支持时参数不可见 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| `ReAct 最大轮次` | 单次会话中工具调用最大次数 | 1–50 | 超限后强制退出工具链并生成最终回复 |
| `最长回复长度` | 模型生成内容的 token 上限（不含提示词） | 正整数 | 影响输出完整性，需结合模型上下文窗口设置 |
| `温度系数` | 控制输出随机性与多样性 | 0.0–2.0 | 数值越高越随机，建议问答场景设为 0.1–0.6 |
| `单文件最大解析长度`（全文引用） | 单个文件提取的 token 数上限 | 正整数 | 超出部分从文件末尾截断 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md) |
| `召回片段数`（切片检索） | 每次问答最多引用的知识片段数 | 正整数 | 配合 `最大拼装长度` 控制输入 token 消耗 |

## 使用方式

1. **创建与配置**：  
   - 访问百炼控制台 → 应用管理 → 创建应用 → 选择类型（推荐 `智能体应用（Agent 2.0）`）。  
   - 在模型选择器中选定模型（如 `千问-Plus-Latest`），通过参数配置器调整关键参数。  
   - 配置系统提示词（定义角色、约束、工具引导）、知识库、MCP 工具、文件处理模式等。

2. **调试与测试**：  
   - 在右侧对话框输入问题（如 `你是谁？`），支持文本输入与文件上传（单会话 ≤10 个文件，单文件 ≤10MB）。  
   - 新版智能体以卡片流形式展示“思考”与“工具调用”步骤，便于过程分析。

3. **发布与调用**：  
   - **必须发布**后方可调用：点击右上角“发布”，确认变更后生效。  
   - API 调用：在“发布渠道”页签 → “API调用” → 查看接口文档与鉴权方式；文件需通过 `file_list`（URL）或 `session_file_id`（上传 API）传递 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)。  
   - 高代码应用支持 Serverless Function 或 K8s 部署，可通过网关暴露生产 API。

## 限制和注意事项

- **版本兼容性**：Agent 1.0 与 Agent 2.0 架构不兼容，无法升级或降级，需重新创建应用 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件有效期**：聊天窗口上传的文件仅在当前会话有效；通过 `session_file_id` 上传的有效期为 24 小时；URL 方式依赖源地址可用性。  
- **计费逻辑**：  
  - 模型调用费用按输入/输出 token 计费，**知识库召回内容计入输入 token**；  
  - 全文引用模式 token 消耗显著高于切片检索；  
  - MCP 工具可能产生额外费用（第三方 API 费用由服务商收取）。  
- **工具超时**：自定义 MCP 超时限制为 5 秒，超时将中断调用 [原文标题](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **缓存支持**：仅支持隐式缓存（自动生效，不可配置），暂不支持显式缓存。  
- **地域限制**：文件问答功能当前仅支持中国大陆版（北京地域）。

## 来源文档

- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


