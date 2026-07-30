# Prompt 工程

Prompt 工程是指在百炼平台上，通过系统化设计、结构化表达与迭代优化提示词（Prompt），以精准引导大语言模型行为、提升输出稳定性、可控性与业务适配性的技术实践。它不是简单的“写指令”，而是融合角色设定、任务分解、约束注入、样例引导与效果验证的工程化方法论。

## 在百炼平台的不同场景中如何使用

Prompt 工程能力深度集成于百炼三大核心层，开发者可根据需求选择对应路径：

- **模板化开发（推荐用于标准化任务）**  
  使用「Prompt 模板」功能，在控制台或通过 `CreatePromptTemplate` API 创建可复用的提示词资产。支持基于 ICIO、CRISPE、RASCEF 等成熟框架结构化编写（如明确 Role/Task/Format/Constraint），适用于营销文案生成、摘要抽取、JSON 结构化输出等确定性任务。文本与图片生成模板需分别配置（后者需正向/负向 Prompt 分离）。

- **智能体应用（Agent）中的动态编排**  
  在 Agent 2.0 应用中，Prompt 工程体现为**系统提示词（System Prompt）的精细化配置**：支持嵌入变量（如 `/user_name`）、绑定知识库检索结果、注入工具调用上下文，并可通过 `enable_thinking=true` 观察模型推理链路。此时 Prompt 是 Agent 的“大脑指令集”，直接影响规划、工具选择与响应质量。

- **自动化优化（适合无 Prompt 经验或快速验证）**  
  利用「Prompt 自动优化」服务，输入原始自然语言指令（如“帮我写一封道歉邮件”），平台自动注入角色、明确格式、强化边界（如“不使用感叹号”）、增强安全性，输出更鲁棒的版本；或使用「Prompt 反馈优化」，上传 query-answer 样例对，由 `qwen-max` 等强模型驱动多轮评估，生成带 few-shot 示例和显式约束的高精度 Prompt，特别适用于分类、表格生成等结构化任务。

> ⚠️ 注意：Prompt 样例库功能已下线，新项目请统一迁移至 RAG 表格库实现上下文增强；所有 Prompt 相关能力（模板、优化、关联）**仅支持华北2（北京）地域**。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符 | 调用 `GetPromptTemplate` 获取内容后，必须按 `variables` 字段声明的变量名（如 `["topic", "tone"]`）填充值，不可动态增删变量。 |
| `workspaceId` | 业务空间 ID | 所有 Prompt API（模板、优化、应用调用）均需显式传入，是资源隔离与权限控制的基础。 |
| `has_thoughts` | 是否返回样例召回详情 | 仅在已关联 RAG 表格库的智能体应用中有效；设为 `true` 时，响应中 `thoughts` 字段可查看实际注入的上下文片段，用于调试检索效果。 |
| `temperature`（全局） | 输出随机性控制 | 建议 Prompt 驱动的确定性任务（如结构化提取）设为 `0.1–0.3`；创意类任务可放宽至 `0.6–0.8`。该参数作用于模型层，与 Prompt 内容协同生效。 |
| 召回片段数（RAG 场景） | 单次注入的上下文片段数量 | 默认 `5`，上限 `10`；增加可提升信息覆盖，但显著增加 [Token](token.md) 成本与延迟，需在控制台或 API 中权衡设置。 |

## 面向开发者的实用建议

- **优先模板化**：将高频、稳定 Prompt 封装为模板（而非硬编码在代码中），便于版本管理、A/B 测试与跨应用复用。
- **变量即契约**：模板中 `variables` 是运行时契约——前端/SDK 必须提供完整且类型匹配的值，缺失或错位将导致渲染失败。
- **优化≠替代**：自动优化是起点，非终点；产出的 Prompt 应人工校验逻辑完整性与业务合规性，尤其关注安全边界是否被弱化。
- **[Token](token.md) 敏感性**：Prompt 内容 + 变量填充后总长度 ≤ 6144 字符；RAG 注入片段数 × 平均片段长度 + Prompt 本身，需严格控制在模型上下文窗口内（如 `qwen3.7-plus` 支持 1M token，但实际应预留 20% 给输出）。
- **地域强约束**：若应用部署在其他地域（如华东1），必须将 Prompt 相关逻辑（模板获取、优化调用）路由至 `cn-beijing` 接入点，否则直接报错。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)


