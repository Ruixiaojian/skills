# Prompt 工程

Prompt 工程是系统性设计、优化与管理大语言模型输入提示（Prompt）的方法论与实践体系，旨在通过结构化模板、自动化增强和反馈驱动迭代等手段，显著提升模型输出的准确性、一致性、可控性与业务适配度。它不是一次性编写指令，而是覆盖开发、测试、部署与持续演进全生命周期的工程化能力。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）与工作流应用**：将 Prompt 模板作为系统提示词（system [prompt](../guides/prompt.md)）注入，通过变量（如 `${user_intent}`、`${knowledge_snippet}`）动态拼接上下文、知识库召回结果或工具调用反馈，实现角色设定、任务约束与格式控制。推荐使用 `千问-Max` 等支持思考模式的模型，并配合 `enable_thinking: true` 以增强推理链可解释性。

- **高代码应用与 API 集成**：通过 `GetPromptTemplate` 接口拉取模板内容，在 SDK 或 HTTP 请求中填充 `variables` 字段后，作为 `messages[0].content` 提交至 `/v1/applications/{app_id}/invoke`。适用于需精细控制请求体、支持多轮状态管理或与自有前端深度集成的场景。

- **Managed Agents 托管运行时**：在创建 Agent 时，直接将优化后的 Prompt 字符串赋值给 `system`（控制台）或 `instructions`（SDK）字段。该 Prompt 将作为沙箱内模型的全局行为锚点，协同内置工具（如 `read`/`write`）完成文件解析、代码执行等复杂操作——此时 Prompt 需明确声明工具能力边界与调用规范（例如“仅当用户要求生成图表时才调用 `plot` 工具”）。

- **Skill 能力封装**：虽 Skill 本身不依赖显式 Prompt 调用，但其触发完全由 `SKILL.md` 中的 `description` 字段驱动。该描述本质是面向模型的轻量级 Prompt，需遵循 Prompt 工程原则：清晰定义输入类型、支持动作、典型触发词及排除场景，避免模糊表述（如“处理数据”应改为“从上传的 CSV 文件中提取销售额前 5 的城市并生成 Markdown 表格”）。

- **RAG 增强场景**：Prompt 工程与知识库深度协同。在模板中预留 `${retrieved_chunks}` 占位符，由平台自动注入检索结果；同时通过 Prompt 明确指令模型“仅基于以下内容回答，禁止编造”，并指定引用格式（如 `[1]`），确保事实准确性与可追溯性。

> ⚠️ 注意：所有 Prompt 功能（模板、自动优化、反馈优化）**仅支持华北2（北京）地域**，跨地域调用将失败。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 相关 API（如 `GetPromptTemplate`）必需 | 控制台首页左上角点击业务空间图标获取；建议存为环境变量，避免硬编码 |
| `promptTemplateId` | 模板唯一 ID，用于引用或复用 | 自定义模板 ID 可重命名，但不可变更；预置模板 ID 固定，可在控制台模板卡片上一键复制 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "tone"]`），运行时需传入对应值 | 变量名须为合法字符串，**不支持嵌套语法**（如 `${user.profile.name}`）；填充前务必对输入值做 XSS/注入过滤 |
| `temperature` / `max_tokens` | 模型生成参数，影响输出多样性与长度 | 在智能体或工作流配置中统一设置；`temperature=0.3` 适合确定性任务，`0.7` 适合创意生成；`max_tokens` 建议设为 2048 以内以控成本 |
| `enable_thinking` | 开启模型内部规划-反思链路（仅限 `千问-Max` 等支持模型） | 对复杂任务（如多步骤分析、工具编排）强烈推荐启用，便于调试与审计 |

## 面向开发者的关键实践建议

- **优先使用模板而非硬编码 Prompt**：将结构（指令、角色、格式）与变量（业务数据、上下文）分离，提升复用性与协作效率。控制台支持 ICIO/CRISPE/RASCEF 等主流框架一键生成模板。

- **快速启动用自动优化**：粘贴模糊原始 Prompt（如“帮我写个文案”），点击「自动优化」获得结构化版本，再人工微调——该功能免费、不计费、不用于训练。

- **高精度任务用反馈优化**：当分类、JSON 输出等任务准确率不足时，准备 5–10 条高质量输入-输出样例 + ≥20 条评测数据，调用 `/prompt/feedback-optimize` 接口，让大模型自我反思迭代。

- **弃用样例库，迁移到 RAG 表格库**：`has_thoughts` 等旧参数已失效；知识增强请统一使用结构化表格知识库，通过 `${table_data}` 插值 + 显式指令控制。

- **图片生成需专用模板**：仅支持「图片生成」类型模板，必须分别定义正向 Prompt（期望内容）与负向 Prompt（排除元素），且**不支持变量插值**，需静态填写。

- **安全第一**：所有变量填充必须自行过滤恶意内容；模板内容最大 6144 字符，超长 Prompt 可能导致截断或优化失败。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [skill](../guides/skill.md)


