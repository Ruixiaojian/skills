# Prompt 工程

Prompt 工程是指在百炼平台上系统性设计、优化与管理提示词（Prompt）的方法论与实践体系，旨在通过结构化框架、动态变量、样例增强和自动化反馈等手段，提升大模型输出的准确性、一致性、可控性与业务适配度。它不是一次性指令编写，而是覆盖设计、测试、迭代、部署与监控的全生命周期工程活动。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：System Prompt 是智能体行为的“大脑”，需明确定义角色、任务边界、工具调用规范及安全约束；支持嵌入 Few-shot 样例（如“用户问：… → 你答：…”）提升任务理解，但需注意样例会增加输入 [Token](token.md) 消耗。
- **工作流（Workflow）应用**：每个大模型节点均可独立配置 Prompt 模板，支持变量注入（如 `${query}`、`${historyList}`）实现上下文感知生成；可结合意图分类节点，为不同意图分支绑定专用 Prompt，实现精细化控制。
- **高代码应用**：开发者可通过 SDK 调用 `GetPromptTemplate` 获取模板内容，运行时动态填充变量后，作为 `system` 或 `user` 消息传入模型 API；适合需强逻辑校验、多步骤组装或与外部服务联动的复杂场景。
- **模板中心统一管理**：所有 Prompt 均以模板形式组织，支持「预置模板」开箱即用、「自定义模板」按需创建（含 ICIO/CRISPE/RASCEF 等结构化框架），并可在控制台一键复用于多个应用。
- **自动优化与反馈优化**：对原始 Prompt 可直接启用「自动优化」获得角色注入与指令强化版本；若已有高质量输入-输出样例（5–10 条）和评测集（≥20 条），推荐使用「反馈优化」，由千问-max 多轮反思生成业务定制化 Prompt。

## 关键参数和配置

- `promptTemplateId`：模板唯一 ID，API 调用必需，用于 `GetPromptTemplate` 等接口。
- `workspaceId`：所有 Prompt 操作的上下文标识，必须显式传入，获取方式见 [获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。
- `variables`：模板中声明的占位符（如 `${topic}`、`${platform}`），需在运行时用实际值替换，建议使用字符串安全替换（如 `content.replace(/\$\{([^}]+)\}/g, (match, key) => data[key] || '')`）。
- `temperature` / `top_p`：虽非 Prompt 专属参数，但在调用时与 Prompt 协同影响输出稳定性——Prompt 工程效果在低 `temperature=0.1–0.4` 下更易收敛。
- 地域限制：所有 Prompt 模板功能（创建、管理、调用）仅支持华北2（北京）地域，跨地域请求将失败，请确保 SDK 或 API 请求 endpoint 与 workspace 所在地域一致。

## 面向开发者的实用建议

- ✅ **优先使用结构化框架**：新建文本类 Prompt 模板时，选择「基于 Prompt 工程创建」模式，ICIO（Identity-Context-Instruction-Output）适合通用任务，CRISPE（Capacity-Role-Insight-Statement-Personality-Experiment）适合角色驱动型应用。
- ✅ **变量命名清晰且唯一**：避免 `${id}` 与 `${ID}` 混用；生产环境建议在模板中添加注释说明变量用途（如 `<!-- ${product_name}: 用户咨询的具体商品名称 -->`），便于协作维护。
- ✅ **[Token](token.md) 成本前置校验**：模板长度 + 变量填充后总字符数 ≤ 模型上下文窗口（如 qwen-plus-latest 支持 128K），建议用 `bailian-sdk` 提供的 `countTokens()` 方法预估，避免超限报错。
- ❌ **勿依赖已下线功能**：Prompt 样例库已停止维护，新项目请迁移至 RAG 表格库或使用反馈优化替代。
- ❌ **避免硬编码敏感逻辑**：如身份验证规则、业务风控策略等，应通过 MCP 工具或后端服务实现，而非写死在 Prompt 中——既不安全，也难迭代。

> 提示：所有 Prompt 优化过程均不存储用户数据，符合阿里云隐私政策；调试阶段建议开启 `stream=True` 实时观察生成过程，快速定位 Prompt 设计缺陷。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [start using](../guides/start-using.md)
- [application support](../guides/application-support.md)


