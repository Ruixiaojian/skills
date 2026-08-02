# Prompt 工程

Prompt 工程是系统性设计、管理、优化和迭代提示词（Prompt）的技术实践，旨在通过结构化模板、高质量样例、自动化增强与反馈驱动的迭代，提升大语言模型输出的准确性、一致性、可控性与业务适配度。它不是一次性编写指令，而是贯穿模型调用全生命周期的工程化方法论。

## 在百炼平台的不同场景中如何使用

Prompt 工程能力深度集成于百炼核心应用层，按使用方式与目标可分为四类落地场景：

- **模板化驱动（推荐首选）**：在智能体（Agent 2.0）、工作流（Workflow）或高代码应用中，将 Prompt 封装为可复用、可变量注入的模板（如 `{{input}}`、`{{knowledge}}`）。预置模板覆盖营销文案、摘要抽取等通用任务；自定义模板支持 ICIO/CRISPE/RASCEF 等工程框架，适用于需强格式约束或角色设定的场景（如“作为金融合规专员，逐条核对合同条款”）。  
- **样例引导（谨慎使用）**：通过少样本（few-shot）样例库注入高质量问答对，辅助模型理解输出风格与结构。**注意：该功能已标记为“不再维护”，仅限历史存量应用；新项目请统一迁移到 RAG 表格[知识库](knowledge-base.md)替代**——RAG 提供更稳定、可检索、易更新的上下文注入机制。  
- **自动优化（快速启动）**：对原始 Prompt（如“帮我写一封辞职信”）一键触发大模型重写，自动注入角色设定、明确输出约束、强化安全边界，并生成可直接部署的优化版本。适合无 Prompt 工程经验的开发者快速获得可用基线。  
- **反馈优化（垂直精调）**：基于真实业务数据（5–10 条初始样例 + ≥20 条评测数据），在推理模型上多轮反思与迭代生成 Prompt。效果显著优于纯文本优化，特别适用于汽车维修话术、医疗术语解释等强领域约束任务。

> ✅ 最佳实践：**优先使用模板 + RAG 替代样例库；新项目避免依赖样例库；复杂任务优先启用反馈优化验证模板效果。**

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 注意事项 |
|------|------|----------|----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需 | 所有 API（`CreatePromptTemplate` 等）、控制台操作上下文 | 必须通过控制台获取，不可猜测；地域隔离（当前仅华北2可用） |
| `promptTemplateId` | 模板唯一标识符 | API 调用（如 `GetPromptTemplate`）、智能体/工作流配置中引用 | 预置模板 ID 在控制台可见；自定义模板创建后生成；**不支持文生图类模板** |
| `has_thoughts: true` | 启用样例检索调试模式 | 智能体 API 请求头或 Query 参数 | 响应中返回 `thoughts` 字段含召回详情；仅对已关联样例库的应用生效（不推荐新用） |
| 召回片段数 | 单次请求注入的样例数量 | 智能体应用配置页（“样例库”设置） | 默认 5，上限 10；影响上下文长度与 Token 消耗 |
| `temperature` / `max_output_tokens` | 控制输出随机性与长度 | 智能体/工作流/高代码应用的模型配置项 | 属模型级参数，非 Prompt 专属，但直接影响 Prompt 效果稳定性 |

## 面向开发者：简洁实用指南

- **起步**：控制台 → [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → “复制模板”选用预置模板，再编辑变量占位符（如 `{{product_name}}`），立即用于智能体系统提示词。  
- **进阶**：在 [反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) 页面上传 5 条典型输入+理想输出（如用户咨询+标准回复），搭配 20+ 条测试问题，启动优化任务，导出结果后保存为新模板。  
- **API 集成**：调用 `CreatePromptTemplate` 创建模板，再在智能体 API 的 `input` 中通过 `{"prompt_template_id": "xxx", "variables": {"input": "xxx"}}` 注入动态内容。  
- **避坑提醒**：  
  - 不要手动拼接长 Prompt —— 使用模板变量；  
  - 不要为新项目启用样例库 —— 改用 RAG 表格[知识库](knowledge-base.md)；  
  - 文生图任务勿尝试创建 Prompt 模板 —— 当前 API 明确不支持；  
  - 所有 Prompt 操作必须指定 `workspaceId`，否则报错 `InvalidParameter.WorkspaceIdMissing`。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [model experience](../guides/model-experience.md)
- [application evaluation](../guides/application-evaluation.md)


