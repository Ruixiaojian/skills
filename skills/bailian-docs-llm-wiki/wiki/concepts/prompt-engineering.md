# Prompt 工程

Prompt 工程是指系统性设计、迭代与优化大语言模型输入指令（Prompt）的方法论与实践技术，目标是提升模型输出的准确性、稳定性、可控性与业务适配性。它不是简单的“写提示词”，而是融合结构化框架（如 CRISPE、RASCEF）、变量注入、样例引导、安全约束与自动评估的工程化过程。

## 在百炼平台的不同场景中，这个概念如何使用

- **模板化构建**：在「组件管理 > 提示词」中创建文本或图片生成类 Prompt 模板，支持基于 ICIO/CRISPE/RASCEF 等框架结构化组织角色、任务、约束与示例；图片生成需分别配置正向 Prompt 与负向 Prompt。
- **智能体应用集成**：在 Agent 2.0 应用中，系统提示词（System Prompt）即为 Prompt 工程的核心载体，支持嵌入变量（如 `/user_name`）、调用知识库片段（RAG）、注入工具描述，并可通过 `enable_thinking=true` 观察模型推理链路。
- **自动化优化**：通过控制台「提示词 > 自动优化」或 API `CreatePromptFeedbackOptimizationTask`，将原始 Prompt + 样例数据集提交给大模型（推荐 `qwen-max`），自动生成含角色设定、指令强化、边界说明与 few-shot 示例的高精度版本。
- **RAG 协同增强**：Prompt 工程与 RAG 表格库深度协同——不再依赖已下线的样例库，而是将高质量问答对沉淀为结构化表格知识，由 Prompt 显式引导模型按格式检索并引用，实现确定性任务（如分类、JSON 输出）的稳定交付。

> ⚠️ 注意：所有 Prompt 工程相关能力（模板、优化、RAG 表格关联）**仅支持华北2（北京）地域**；跨地域调用将返回错误。

## 关键参数和配置

| 参数 | 说明 | 使用场景 | 备注 |
|------|------|----------|------|
| `promptTemplateId` | Prompt 模板唯一标识符 | API 调用 `GetPromptTemplate` 获取模板内容后渲染使用 | 控制台创建后即生成，不可修改 |
| `workspaceId` | 业务空间 ID | 所有 Prompt 相关 API（如 `CreatePromptTemplate`, `GetPromptTemplate`）必传 | 是资源隔离与权限作用域基础，需提前获取 |
| `variables` | 模板中预声明的变量名数组（如 `["topic", "tone"]`） | 渲染模板时动态填充，如 `content.replace("{topic}", topicValue)` | 变量名由模板定义决定，运行时不可新增或删减 |
| `has_thoughts` | 请求头或参数，设为 `true` 时返回 `thoughts` 字段 | 智能体应用调试阶段查看 RAG 检索过程、样例匹配逻辑 | 仅对已启用知识库且支持思考模式的模型（如 `qwen-max`）生效 |
| `temperature` | 控制输出随机性（0.0–2.0） | 在智能体应用或直接调用模型 API 时设置 | Prompt 工程效果需配合合理 temperature：问答类建议 0.1–0.6，创意生成可设 0.7–1.2 |

- **长度限制**：单个 Prompt 模板内容 ≤ 6144 字符（控制台实时计数）；RAG 注入片段默认 5 条，上限 10 条，影响 [Token](token.md) 成本与精度平衡。
- **模型兼容性**：
  - 文本生成类 Prompt 模板适配 `qwen3.7-plus`、`qwen3.7-flash` 等主流文本模型；
  - 图片生成类 Prompt 模板仅适配 `wan2.7-image-pro` 等图像模型，不兼容文本模型；
  - 反馈优化任务推荐使用 `qwen-max` 作为推理模型以获得最佳效果。

## 面向开发者，简洁实用

- ✅ **起步建议**：从预置模板开始（如“营销文案生成”），复制后修改变量与约束，再逐步迁移到自定义 CRISPE 结构。
- ✅ **调试技巧**：启用 `has_thoughts=true` 查看 RAG 检索片段，验证 Prompt 是否有效引导模型关注关键上下文。
- ✅ **生产规范**：避免在 Prompt 中硬编码敏感信息；变量命名统一小写+下划线（如 `user_query`）；所有模板必须绑定 `workspaceId` 并发布后方可 API 调用。
- ❌ **避坑提醒**：Prompt 样例库功能已下线，请勿新建或依赖；新项目务必使用 RAG 表格库替代；文生图 Prompt 暂不支持通过 API 创建（仅控制台支持）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)


