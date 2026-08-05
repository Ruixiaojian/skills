# Prompt 工程

Prompt 工程是指在百炼平台上系统性设计、构建、验证与迭代提示词（Prompt）的方法论与实践体系，其目标是通过结构化指令、角色设定、上下文注入、约束定义和反馈优化等技术手段，显著提升大语言模型输出的准确性、一致性、可控性与业务适配度。它不是一次性文本输入，而是一套可复用、可版本化、可评测的工程化资产。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：Prompt 工程直接体现为 `System Prompt` 的精细化编写——需明确角色定位（如“阿里云手机导购专家”）、任务边界（“仅推荐百炼平台支持的机型”）、输出格式（JSON Schema 或 Markdown 表格）、安全约束（禁止虚构参数）及工具调用规范（如“必须先检索知识库再回答”）。Few-shot 样例已由 RAG 表格库承接，不建议在 System Prompt 中硬编码问答对。

- **工作流（Workflow）应用**：每个「大模型节点」均需独立配置 Prompt，支持变量插值（如 `${user_intent}`）与条件模板（通过上游节点输出动态选择 Prompt 片段）。Prompt 工程在此体现为模块化拆分——将意图识别、内容生成、格式校验等子任务分别封装为专用 Prompt 模板，提升可维护性与复用率。

- **高代码应用**：开发者可通过 SDK 动态构造 Prompt，例如基于用户画像实时注入个性化约束（`"请用${user_tone}语气回答，重点突出续航和AI拍照"`），或结合 MCP 工具返回结果生成带上下文的链式 Prompt。此时 Prompt 工程与业务逻辑深度耦合，强调运行时可编程性。

- **模型评测与应用评估**：Prompt 工程成果需被量化验证。在 `application evaluation` 中，优化后的 Prompt 应作为新版本应用发布，并通过同一评测集进行回归对比；在 `model evaluation` 中，可将不同 Prompt 设计（如 ICIO vs RASCEF）作为独立变量，接入相同模型与数据集，横向比对各维度得分差异，实现“Prompt 即实验变量”。

- **RAG 增强场景**：Prompt 工程与知识库协同演进。例如，在切片检索模式下，Prompt 需显式声明“仅依据以下 <context> 回答，禁止编造”，并配合 `recall_k=3` 与 `max_assemble_length=2048` 等参数，确保模型聚焦于高质量召回片段——此时 Prompt 是 RAG 流程的“指挥协议”，而非孤立文本。

> ⚠️ 注意：旧版「Prompt 样例库」功能已停用，所有少样本能力应迁移至 RAG 表格库；而「基于样例的 Prompt 反馈优化」仍有效，适用于高精度场景（如汽车文章分类），需提供标注好的评测数据集驱动多轮自动迭代。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一 ID，用于 API 获取与变量校验 | 必填；通过控制台模板卡片或 `GetPromptTemplate` 接口获取；模板内容含 `variables` 字段，用于前端/SDK 校验填充完整性 |
| `system_prompt`（智能体） / `prompt`（工作流节点） | 运行时生效的核心指令文本 | 支持 `${variable}` 插值；长度受模型上下文窗口限制（建议 ≤3000 tokens）；避免模糊表述（如“尽量好”），改用可验证约束（如“输出必须包含价格、续航、摄像头三要素”） |
| `enable_thinking`（智能体） | 是否启用 ReAct 思考链模式 | 开启后模型会输出 `Thought:`/`Action:`/`Observation:` 步骤，便于调试；但增加 [Token](token.md) 消耗，生产环境可关闭 |
| `recall_k`（RAG 相关） | 知识库召回片段数（默认 5，上限 10） | 与 Prompt 中的“依据以下 context”指令强绑定；增大 recall_k 需同步增强 Prompt 对噪声片段的过滤能力（如加“忽略无关技术参数”） |
| `temperature`（工作流/评测） | 控制输出随机性（0.0–1.0） | Prompt 工程无法替代温度调控：确定性任务（如格式转换）设为 `0.0`；创意生成任务可设 `0.7`；与 Prompt 中“请给出唯一答案”等指令协同生效 |

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码**：所有重复使用的 Prompt（如客服开场白、摘要指令）必须创建为 Prompt 模板，通过 `promptTemplateId` + `variables` 调用，保障一致性与可维护性。
- ✅ **变量命名即契约**：`variables` 列表中的字段名（如 `product_name`, `user_level`）是前后端约定接口，前端必须传入同名参数，缺失则 API 返回校验错误。
- ✅ **Prompt 与评测闭环**：每次修改 Prompt 后，必须用同一评测集跑一次 `application evaluation`，重点关注“相关性”“事实准确性”“格式合规性”三类指标变化。
- ✅ **安全约束写进 Prompt**：显式声明禁止行为（如“不得生成代码”“不得提及竞品”），比依赖模型内置安全层更可靠；百炼平台不存储 Prompt 优化过程数据，但生产 Prompt 本身需符合企业合规要求。
- ❌ **避免反模式**：不要在 Prompt 中堆砌大量样例（已由 RAG 承载）；不要用自然语言描述格式要求（改用 JSON Schema 或正则示例）；不要跨地域调用（仅华北2可用）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [application evaluation](../guides/application-evaluation.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


