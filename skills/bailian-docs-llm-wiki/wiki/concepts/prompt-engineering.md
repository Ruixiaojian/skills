# Prompt 工程

Prompt 工程是系统性设计、构建、优化和复用提示词（Prompt）的方法论与技术实践，旨在精准引导大语言模型完成特定任务、提升输出一致性、可控性与业务适配度。在百炼平台中，它不是简单的文本输入，而是可配置、可版本化、可集成的工程化组件，支撑从零代码应用到高代码系统的全链路 AI 行为编排。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：通过 `System Prompt` 定义角色、任务边界与工具调用规范；支持将 Prompt 模板直接绑定至智能体，实现角色指令与知识库/MCP 工具调度逻辑的解耦。例如，客服智能体可复用“多轮意图澄清 + 术语约束 + 格式化回复”模板，无需重复编写系统指令。

- **工作流（Workflow）应用**：在大模型节点中引用 Prompt 模板 ID 或内联变量化 Prompt（如 `${query}`、`${retrieved_knowledge}`），实现动态上下文注入；结合 `messages` 输入结构，使 Prompt 成为工作流状态传递与条件分支决策的关键媒介。

- **高代码应用**：通过 SDK 调用 `GetPromptTemplate` 获取结构化模板内容，再结合业务变量实时渲染，嵌入 Python 服务逻辑；支持将 Prompt 作为配置项与模型参数（`temperature`、`max_output_tokens`）统一管理，实现灰度发布与 A/B 测试。

- **RAG 增强场景**：Prompt 与知识库协同——模板中预留 `${retrieved_chunks}` 占位符，由检索结果自动填充；避免硬编码样例，转向以模板驱动的“检索→填充→生成”标准化流程（替代已停用的 Prompt 样例库）。

- **模型微调前奏**：利用反馈优化生成高质量 few-shot 示例集，作为监督微调（SFT）数据的种子样本，缩短人工标注周期。

> ⚠️ 注意：Prompt 样例库（few-shot 样例库）功能已正式停止维护，所有新项目请迁移至 RAG 表格库或通过反馈优化生成带样例的 Prompt，不得在生产环境中继续使用。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 相关 API 的必需路径参数 | 必须提前获取并持久化存储，不可硬编码；推荐从环境变量或配置中心加载。 |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 等接口 | 控制台模板卡片右上角「复制 ID」；API 调用时需确保该模板处于「已发布」状态。 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "tone"]`），由 `GetPromptTemplate` 接口返回 | **禁止手动构造**；应解析接口响应中的 `variables` 字段，按需填充，避免字段缺失导致渲染失败。 |
| `content` | 模板主体内容，支持 ICIO/CRISPE/RASCEF 等结构化框架 | 单模板最大 6144 字符；建议拆分复杂逻辑为多个轻量模板，通过工作流串联复用。 |
| `type` | 模板类型，取值 `text`（文本生成）或 `image`（图片生成） | 图片生成模板需额外提供 `positive_prompt` 和 `negative_prompt` 字段，二者均参与渲染控制。 |

- **地域强制约束**：所有 Prompt 功能（模板管理、自动优化、反馈优化）**仅支持华北2（北京）地域**，调用时必须使用 `bailian.cn-beijing.aliyuncs.com` 接入点，跨地域请求将返回 `InvalidRegionId` 错误。

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码 Prompt**：创建自定义模板后，在智能体/工作流中直接引用 `promptTemplateId`，便于统一维护与灰度切换。
- ✅ **变量命名语义化**：使用 `user_query`、`product_name` 等清晰名称，避免 `var1`、`input` 等模糊占位符，降低协作理解成本。
- ✅ **自动优化免费试用**：对新 Prompt 初稿，先调用 `/api/v1/prompt/optimize` 进行结构增强（角色注入、指令明确化），再人工校验，节省 30%+ 编写时间。
- ✅ **反馈优化需最小数据集**：提交 `CreatePromptFeedbackOptimizationTask` 时，确保样例 ≥5 条（覆盖典型 case）、评测数据 ≥20 条（含正负例），否则任务失败。
- ❌ **禁用已停用能力**：勿调用 `AddPromptCaseLibrary` 或 `RetrieveFromPromptCaseLibrary` 等样例库相关接口；历史项目请尽快迁移到 RAG 表格库或反馈优化流程。
- 📦 **注意 [Token](token.md) 开销**：启用反馈优化或在 Prompt 中内嵌长知识片段会显著增加输入 [Token](token.md)，建议监控 `usage.input_tokens` 并设置 `max_output_tokens` 防止超限。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [bailian application calling](../guides/bailian-application-calling.md)


