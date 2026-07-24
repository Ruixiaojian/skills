# 提示词工程

提示词工程（Prompt Engineering）是系统性设计、优化和管理大语言模型输入提示（Prompt）的方法论与实践体系，旨在通过结构化表达、上下文注入、迭代反馈等技术手段，提升模型输出的准确性、一致性、可控性与业务适配度。它不是一次性技巧，而是贯穿模型应用全生命周期的工程化能力。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，提示词工程已深度集成到多个核心能力模块，支撑从快速原型到生产级应用的演进：

- **智能体（Agent）应用**：系统提示词（System Prompt）是 Agent 的“角色设定”与“行为契约”，直接影响其意图理解、工具规划与反思能力。开发者需结合 Agent 2.0 的 ReAct 链路，设计支持多步推理与错误恢复的提示结构（如 CRISPE 或 RASCEF 框架），并配合知识库、MCP 工具等上下文动态增强提示效果。

- **工作流（Workflow）应用**：每个大模型节点均需独立配置提示词模板。可通过变量插值（如 `${user_query}`、`${product_info}`）实现业务数据动态注入，结合条件分支与变量处理节点，构建可复用、可测试的提示逻辑单元。

- **高代码应用**：开发者可在 Python 代码中程序化生成 Prompt——例如基于用户画像动态拼接角色指令、从 RAG 检索结果中提取关键片段注入上下文、或调用 `GetPromptTemplate` API 获取预置模板后进行运行时渲染。提示词成为可版本化、可 A/B 测试的代码资产。

- **Prompt 模板管理（核心载体）**：百炼将提示词工程落地为标准化组件。支持文本/图片双模态模板，内置 ICIO、CRISPE 等结构化框架；变量语法统一为 `${variableName}`，无需额外模板引擎；所有模板均归属业务空间（Workspace），支持创建、更新、列表、删除等全生命周期 API（`CreatePromptTemplate` 等），便于 CI/CD 集成。

> ⚠️ 注意：Prompt 样例库（Few-shot）功能已正式下线，官方明确要求迁移至 RAG 表格库。新项目不应依赖该能力，应优先使用知识库（RAG）实现上下文增强。

## 关键参数和配置

| 参数 | 说明 | 实际用途 |
|------|------|----------|
| `workspaceId` | 业务空间唯一标识 | 所有 Prompt 相关 API（如 `GetPromptTemplate`）的必需路径参数，用于资源隔离与权限校验 |
| `promptTemplateId` | 模板唯一 ID | 用于获取、更新、调用指定模板；控制台创建后自动生成，格式如 `cfec40c311f14f3e976403059d8f0116` |
| `variables` | 模板变量列表 | 由 `GetPromptTemplate` 接口返回（如 `["topic", "tone", "length"]`），指导运行时数据填充逻辑 |
| `content`（模板内容） | 带 `${variable}` 占位符的字符串 | 直接字符串替换即可渲染，非 Jinja2 等复杂语法，轻量可靠 |
| `has_thoughts`（仅限历史样例库场景） | 控制是否返回检索过程详情 | 已弃用，新项目请忽略；RAG 场景请使用 `Retrieve` 接口的 `retrieval_results` 字段替代 |

- **地域约束**：所有 Prompt 工程能力（模板管理、自动优化）仅支持 **华北2（北京）** 地域，跨地域调用将失败。
- **长度限制**：单个 Prompt 模板内容 ≤ 6144 字符（含占位符）；变量名仅支持 ASCII 字母、数字、下划线。
- **[Token](token.md) 成本提示**：启用复杂提示结构（如长样例、多轮上下文）会显著增加输入 [Token](token.md)，直接影响计费——建议在效果验证后精简冗余描述。

## 面向开发者，简洁实用

- ✅ **起步最快方式**：控制台 →「组件管理 > 提示词」→「创建提示词」→ 选择「基于 Prompt 工程创建」，使用预置模板（如“营销文案生成”）快速启动，再逐步替换变量与调整结构。
- ✅ **API 集成三步法**：
  1. 调用 `ListPromptTemplates` 获取可用模板 ID；
  2. 调用 `GetPromptTemplate` 获取 `content` 与 `variables`；
  3. 将业务数据填入 `${...}` 占位符，生成最终 Prompt 字符串，作为 `system` 或 `user` 消息提交至应用 API。
- ✅ **调试建议**：在智能体/工作流调试面板中开启「思考模式」（`enable_thinking=true`），直观观察模型如何解析提示、规划步骤、调用工具——这是验证提示有效性的最直接方式。
- ✅ **避坑提醒**：不要硬编码提示词；避免在代码中拼接长文本；禁止将敏感信息（如密钥、内部 URL）写入模板内容——应通过环境变量或 RAG 动态注入。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)


