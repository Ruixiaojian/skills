# Prompt 工程

Prompt 工程是百炼平台上系统性设计、迭代与管理提示词（Prompt）的技术实践，旨在通过结构化模板、自动化优化、反馈驱动调优等手段，稳定提升大语言模型在具体业务场景下的输出准确性、一致性与可控性。它不是一次性指令编写，而是覆盖设计、测试、评估、部署与持续演进的闭环工程方法。

## 在百炼平台的不同场景中如何使用

Prompt 工程能力深度融入百炼三大应用构建范式，按需选用：

- **智能体（Agent）应用**：系统提示词（System Prompt）是智能体行为的“操作系统”，需结合 CRISPE 或 RASCEF 等框架明确角色、目标、步骤与约束；可直接绑定已优化的 Prompt 模板，并通过 `enable_thinking` 参数增强推理过程的可观测性。
- **工作流（Workflow）应用**：每个「大模型」节点均可独立配置 Prompt 模板（支持变量插值），实现多步骤任务中不同环节的精准语义控制（如“提取关键信息”→“生成摘要”→“转为客服话术”）。
- **高代码应用**：开发者可通过 SDK 调用 `GetPromptTemplate` 动态获取模板内容与变量定义，在 Python 服务中完成运行时渲染与组合，支撑复杂业务逻辑下的 Prompt 动态组装。
- **RAG 场景协同**：Prompt 工程与知识库（Index）协同——高质量 Prompt 明确指示模型如何利用检索片段（如“仅基于以下文档回答，不可编造”），而评测结果又能反向指导 Prompt 重写（例如发现“幻觉率高”，则强化“严格依据上下文”约束）。

> ⚠️ 注意：已下线的「Prompt 样例库」（Few-shot 样例库）功能不再推荐使用，所有少样本引导需求应迁移至「RAG 表格库」或通过「反馈优化」注入样例数据。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `workspaceId` | 所有 Prompt 操作的必需上下文标识，所有模板、优化任务均归属于此空间 | 从控制台或 API 获取后硬编码于配置文件，避免跨 workspace 错误 |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 等接口精准读取 | 建议在 CI/CD 流程中将模板 ID 与版本号绑定，实现 Prompt 可追溯 |
| `variables` | 模板中声明的动态变量列表（如 `["topic", "tone"]`），由 `GetPromptTemplate` 接口返回 | 客户端必须校验变量存在性并提供默认值，防止渲染失败 |
| `temperature` / `max_output_tokens` | 控制生成随机性与长度上限（属 LLM 应用层参数，非 Prompt 专属但强相关） | 对确定性任务（如格式化输出）设 `temperature=0.1`；对长文本生成需预留足够 `max_output_tokens` 并监控 [Token](token.md) 消耗 |
| `top_k`（RAG 场景） | 影响召回片段数，间接决定 Prompt 中注入的上下文量级 | 默认 5，建议根据业务精度要求在 3–8 间调整；过高易引入噪声，过低导致信息缺失 |
| 评测数据集规模 | 反馈优化要求至少 20 条评测样本，样例数据建议 5–10 条且覆盖全部业务类别 | 使用 `application evaluation` 自动生成评测集，确保样本分布真实反映线上流量 |

## 面向开发者的实用建议

- ✅ **优先使用自动优化**：粘贴原始 Prompt 后一键生成结构更清晰、指令更明确的版本（免费、不训练模型、无数据留存），适合快速验证基础效果。
- ✅ **反馈优化是生产首选**：当自动优化无法满足业务指标时，用真实 query-answer 对 + 评测集启动反馈优化，它能基于千问-max 进行多轮评估迭代，产出可量化提升的 Prompt。
- ✅ **模板即代码**：将 Prompt 模板视为基础设施代码——用 `CreatePromptTemplate` / `UpdatePromptTemplate` API 管理，纳入 Git 版本控制，配合 CI 自动部署。
- ❌ **避免手动拼接字符串**：禁止在代码中硬编码 `${variable}` 替换逻辑；务必调用 `GetPromptTemplate` 获取标准变量列表，再用安全模板引擎（如 Jinja2）渲染。
- ⚠️ **注意地域限制**：Prompt 模板功能仅支持华北2（北京）地域，跨地域调用会失败，请确认 `workspaceId` 所属 Region。
- ⚠️ **严控 [Token](token.md) 成本**：含样例或长知识片段的 Prompt 会显著增加输入 [Token](token.md)，建议在调试阶段开启 `enable_thinking` 查看完整输入，上线前做 Token 预估与压测。

> 提示：图片生成类 Prompt 需同时配置 `prompt`（正向）与 `negative_prompt`（负向），二者共同约束输出；文本生成推荐按任务复杂度选用 ICIO（简单）、CRISPE（角色交互）、RASCEF（多步流程）框架，而非自由发挥。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application evaluation](../guides/application-evaluation.md)
- [use cases](../guides/use-cases.md)


