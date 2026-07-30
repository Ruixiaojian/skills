# Prompt 工程

Prompt 工程是百炼平台上系统化设计、管理与优化提示词（Prompt）的方法论与技术实践，旨在通过结构化模板、变量注入、自动重写和反馈驱动迭代等手段，将业务逻辑稳定、可复用地映射到大语言模型的生成行为中，实现高质量、高一致性、可评估的 AI 输出。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用构建**：在 Agent 2.0 应用中，Prompt 工程作为核心输入控制层。开发者可通过「使用 Prompt」功能直接绑定预置或自定义模板，模板变量（如 `${user_query}`、`${product_name}`）由智能体运行时自动填充；系统级指令（如角色设定、输出格式约束）建议置于 `system` 消息中，避免与用户输入混杂。

- **工作流（Workflow）编排**：在「大模型节点」中，支持直接引用已发布的 Prompt 模板 ID（`promptTemplateId`），或手动编写带变量插值的 Prompt 字符串。推荐使用模板方式，便于统一维护与 A/B 测试。

- **高代码应用开发（Python/SDK）**：通过 `GetPromptTemplate` 接口获取模板内容与 `variables` 列表，完成变量替换后，将生成的完整 Prompt 作为 `messages` 数组中的 `system` 或 `user` 消息传入 `ChatCompletion` 等推理接口。不建议硬编码 Prompt 字符串，应依赖模板 API 实现动态解耦。

- **RAG 增强场景**：虽 Prompt 样例库已下线，但 Prompt 工程仍与 RAG 深度协同——例如，在知识检索后，将召回片段与业务模板组合（如 `"根据以下资料回答：{retrieved_chunks}。问题：{user_query}"`），形成上下文感知的最终 Prompt，交由模型生成答案。

- **[多模态](multi-modal.md)任务（图文/音视频）**：对支持[多模态](multi-modal.md)的模型（如 `qwen3.5-omni-plus`），Prompt 工程同样适用。需注意：图像/音频 URL 需作为 `input` 结构的一部分传入，而文本 Prompt（含变量）应置于 `messages` 的 `user` 内容中，不可混入 `input` 字段。

> ⚠️ 注意：所有 Prompt 工程能力（创建、调用、优化）仅支持华北2（北京）地域，跨地域请求将失败；且必须指定有效的 `workspaceId`。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作的必需上下文 | 必填，从控制台或 RAM 权限页获取，不可省略 |
| `promptTemplateId` | 模板唯一 ID（预置或自定义） | 控制台模板卡片右上角可一键复制；API 调用时用于 `GetPromptTemplate` |
| `variables` | 模板声明的占位符列表（如 `["topic", "tone"]`） | 由 `GetPromptTemplate` 返回，**不可手动增删**；需严格按名称与类型（string/number）传入值 |
| `temperature` / `max_tokens` | 控制生成随机性与输出长度 | 属模型级参数，与 Prompt 分离；应在调用 `ChatCompletion` 时传入，而非模板内 |
| `enable_thinking` | 启用思考链（Chain-of-Thought）推理 | 仅对 `qwen3.7-plus` 等支持模型生效，需在推理请求中显式设置，不影响 Prompt 本身 |
| `prompt_extend`（图片生成） | 是否启用大模型智能扩写正向提示词 | 仅适用于 `wan2.7-image-pro` 等视觉模型，属 `parameters` 字段，非 Prompt 模板参数 |

- **模板容量限制**：单个文本 Prompt 模板最大 6144 字符；图片生成模板需分别提供 `prompt`（正向）与 `negative_prompt`（反向），无明确字符上限，但过长将显著增加 [Token](token.md) 开销。
- **变量安全规则**：变量值需做基础转义（如去除 `\n`、`{`、`}` 等可能破坏 JSON 结构的字符），避免注入攻击或解析失败。
- **弃用项规避**：`has_thoughts`、`召回片段数` 等参数仅与已下线的 Prompt 样例库相关，**新项目严禁使用**；替代方案为 RAG 表格库 + 自定义 Prompt 组合。

## 面向开发者的实用建议

- ✅ **优先使用预置模板**：营销文案、摘要抽取等高频场景已有开箱即用模板，可快速验证效果，再基于其结构定制。
- ✅ **变量命名语义化**：用 `customer_name` 优于 `var1`，便于团队协作与后续调试；避免在模板中嵌套复杂逻辑（如条件判断），应由 SDK 层处理。
- ✅ **版本化管理**：每次 `UpdatePromptTemplate` 即生成新版本；通过 `ListPromptTemplates` 查看历史版本，关键业务模板建议打标签（如 `v2-production`）。
- ❌ **避免在 Prompt 中硬编码敏感信息**：如 API Key、内部路径等；应通过环境变量或安全凭证服务注入。
- ❌ **勿依赖样例库**：该功能已正式下线，迁移至 RAG 表格库后，应将样例转化为结构化知识条目，由检索模块动态注入 Prompt。
- 📈 **监控 [Token](token.md) 开销**：启用变量注入或长模板后，务必在测试阶段检查 `usage.total_tokens`，防止意外超限计费。

Prompt 工程不是“写好一句话”，而是构建可维护、可灰度、可度量的提示词交付流水线——从控制台创建 → API 获取 → 变量渲染 → 模型调用 → 效果评测 → 迭代优化，全程闭环。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [use cases](../guides/use-cases.md)
- [model experience](../guides/model-experience.md)


