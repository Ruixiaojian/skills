# 提示工程

提示工程（Prompt Engineering）是百炼平台上系统化设计、构建与优化大语言模型输入指令（Prompt）的方法论与实践体系，其目标是通过结构化表达、上下文控制、样例引导和自动化迭代等手段，显著提升模型输出的准确性、稳定性、可控性与业务适配性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，提示工程不是一次性配置动作，而是贯穿应用全生命周期的核心能力，具体体现为以下四类标准化实践：

- **模板化构建**：通过「Prompt 模板」功能，将角色设定、任务指令、约束条件、输出格式等要素结构化封装（支持 ICIO/CRISPE/RASCEF 等框架），实现跨应用复用。例如，在智能体应用中，将 `system_prompt` 字段直接绑定一个预置模板 ID；在工作流节点中，通过变量注入（如 `${user_query}`）动态填充业务上下文。

- **少样本引导（Few-shot）**：虽原「Prompt 样例库」功能已停止维护，但其核心思想仍延续于 RAG 表格库与智能体工具调度中——开发者可将高质量 Query-Answer 对作为知识片段注入检索上下文，或在 MCP 工具调用时显式提供范例，用于强格式约束（如 JSON Schema 输出）、风格对齐（如法律文书语气）等场景。

- **自动增强与反馈优化**：  
  - **自动优化**：对模糊、口语化的原始 Prompt（如“帮我写个产品介绍”），平台基于大模型自动注入角色、补充安全边界、重组逻辑结构，适用于快速原型验证；  
  - **反馈优化**：上传 5–10 条覆盖典型类别的输入-输出样例 + ≥20 条评测数据，平台多轮迭代生成更鲁棒的 Prompt，特别适合高精度分类、规则校验等垂直任务，效果优于纯文本优化。

- **运行时动态编排**：在智能体（Agent 2.0）与工作流中，Prompt 不再是静态字符串，而是与工具调用、记忆管理、多模态输入深度耦合的执行单元。例如：当用户上传图片时，系统自动拼接图文 Prompt；当启用 `enable_thinking` 时，Prompt 需预留 ReAct 推理链路占位符；[长期记忆](long-term-memory.md)模块会将 `historyList` 动态注入 Prompt 上下文。

> ⚠️ 注意：所有 Prompt 相关能力（模板、优化、调试）**仅支持华北2（北京）地域**，跨地域调用将失败。

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 备注 |
|------|------|----------|------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作必需 | 所有 API（`CreatePromptTemplate`, `GetPromptTemplate`）、SDK 初始化、控制台模板管理 | 必须通过控制台或 `ListWorkspaces` 获取，不可硬编码 |
| `promptTemplateId` | 模板唯一 ID，用于引用与调用 | 智能体应用系统提示词字段、工作流节点配置、API 请求体 | 预置模板与自定义模板均分配此 ID |
| `variables` | 模板中声明的动态变量（如 `["topic", "tone"]`），调用时需传入对应值 | 控制台模板编辑器、API 请求体、SDK 调用参数 | 占位符格式为 `${variable_name}`，长度 ≤6144 字符 |
| `has_thoughts=true` | 启用调试模式，返回 `thoughts` 字段含 Prompt 解析与样例召回详情 | 智能体应用 API 调用时的 query 参数 | 仅限调试，生产环境请关闭 |
| `temperature` / `max_tokens` | 控制输出随机性与长度上限 | 智能体/工作流/高代码应用的模型配置项 | 与 Prompt 共同影响最终输出质量，需协同调优 |

## 面向开发者，简洁实用

- ✅ **起步建议**：新项目优先使用预置模板（如“文案生成”“摘要抽取”），复制后按业务微调；避免从零手写长 Prompt。
- ✅ **变量安全**：所有 `variables` 值需经业务层清洗（如过滤控制字符、截断超长文本），防止注入攻击或 [Token](token.md) 溢出。
- ✅ **调试闭环**：用控制台右侧调试面板实时验证 Prompt 效果 → 发现问题后，导出 query-answer 对 → 进入「反馈优化」页面提交优化任务 → 替换模板并重新发布。
- ✅ **性能意识**：单个 Prompt 模板最大 6144 字符；若需长上下文，请优先使用 RAG 表格库或知识库切片检索，而非堆砌文本到 Prompt 中。
- ✅ **版本管理**：模板无内置版本号，建议在模板名称中添加语义标记（如 `QA_Template_v2_202504`），并通过 Workspace 隔离测试/生产环境。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)


