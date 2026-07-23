# Prompt 工程

Prompt 工程是系统性设计、迭代与优化提示词（Prompt）的方法论与实践体系，旨在通过结构化框架、自动化增强和数据驱动反馈，显著提升大模型在特定任务上的准确性、稳定性与可控性。它不是一次性指令编写，而是覆盖定义、测试、评估、优化、部署与监控的全生命周期工程实践。

## 在百炼平台的不同场景中，这个概念如何使用

Prompt 工程在百炼平台中已深度产品化，贯穿智能体、工作流、高代码应用及知识库增强等核心场景：

- **智能体（Agent）应用**：作为角色定义与工具调用规则的载体。System Prompt 采用 ICIO 或 RASCEF 等结构化框架（如明确 Role、Action、Steps、Constraints），配合 `enable_thinking` 参数启用反思链路，使模型更可靠地规划并调用知识库、MCP 等工具。
  
- **工作流（Workflow）应用**：每个「大模型」节点均支持绑定 Prompt 模板。模板变量（如 `${sys.query}`、`${retrieved_content}`）可动态注入上下文、RAG 结果或前序节点输出，实现多步任务中提示词的精准定制与复用。

- **知识库增强问答**：Prompt 工程直接决定知识检索结果的利用效果。例如，通过负向约束（如“禁止编造未提及的信息”）+ 引用标注指令（如“所有结论必须标注来源片段编号”），可显著提升回答可信度与可追溯性。

- **图片/[多模态](multi-modal.md)生成**：支持正向 Prompt（描述目标内容）与负向 Prompt（排除干扰元素）双通道输入，需避免语义冲突（如正向写“高清”，负向写“模糊”），并通过 CRISPE 框架结构化控制风格、构图与细节层级。

- **应用评测与迭代闭环**：Prompt 反馈优化功能依赖评测集（≥20 条）与样例集（5–10 条）驱动多轮自动重写，推荐使用 `qwen-max` 作为优化引擎；优化结果可一键保存为新模板，无缝接入已有应用。

> ⚠️ 注意：Prompt 样例库功能已停止维护，新项目请统一使用 RAG 表格库或评测反馈机制替代。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `promptTemplateId` + `workspaceId` | 模板唯一标识对，用于 API 获取模板内容 | 必须成对使用；`workspaceId` 需通过控制台或 `ListWorkspace` 接口获取，且仅华北2（北京）地域有效 |
| `variables` | 模板中声明的占位符（如 `${topic}`、`${num1}`），运行时由业务逻辑填充 | 占位符名称应语义清晰；避免嵌套（如 `${${var}}`）；模板创建后不可新增变量，需提前规划 |
| `max_tokens`（上下文） | 单次请求总 [Token](token.md) 上限（Prompt + 输入 + 输出） | 文本生成默认 ≤ 6144 字符（约 8K tokens）；图片生成需同时满足分辨率与提示词长度限制，建议正向 Prompt ≤ 300 字、负向 ≤ 150 字 |
| `temperature` | 控制生成随机性（0.0–1.0），值越高越发散 | 对确定性任务（如格式化输出、代码生成）设为 `0.0–0.3`；创意类任务可设 `0.7–1.0`，但需配合 `top_p` 或 `stop` 参数约束边界 |

## 面向开发者，简洁实用

- ✅ **优先使用结构化模板**：新建 Prompt 时选择「基于 Prompt 工程创建」，内置 ICIO（Identity-Context-Instruction-Output）、CRISPE（Capacity-Role-Insight-Statement-Personality-Experiment）等框架，比纯自由文本更易调试与复用。
  
- ✅ **API 调用三步法**：
  1. 调用 `GetPromptTemplate` 获取模板内容与 `variables` 列表；
  2. 用业务数据替换 `${variable}` 占位符（推荐使用标准字符串模板引擎，如 Python 的 `string.Template`）；
  3. 将生成的完整 Prompt 作为 `system` 或 `user` 消息发送至模型 API（如 `qwen-max`）。

- ✅ **热更新不改代码**：Prompt 模板在控制台编辑保存后，所有绑定该模板的应用将自动生效，无需重新部署服务，适合 A/B 测试与灰度发布。

- ✅ **安全合规**：自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云隐私政策；敏感字段（如用户 ID）建议通过变量注入而非硬编码进 Prompt。

- ❌ **避坑提醒**：
  - 不跨地域调用 Prompt 相关 API（仅支持华北2）；
  - 单模板内容勿超 6144 字符（控制台有实时计数）；
  - 图片生成负向 Prompt 避免与正向逻辑矛盾；
  - 反馈优化任务中，样例数据需覆盖全部业务类别，评测数据越多效果越优。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application evaluation](../guides/application-evaluation.md)


