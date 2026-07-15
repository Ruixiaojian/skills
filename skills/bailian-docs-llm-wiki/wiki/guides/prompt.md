# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化模板、自动优化、样例引导等多种机制，开发者可高效构建、复用和迭代高质量提示词，显著提升模型输出的准确性、一致性与可控性。所有 Prompt 相关能力均默认适用于华北2（北京）地域，跨地域使用需另行确认支持状态。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同开发阶段和精度要求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），实现逻辑与内容分离。预置模板效果稳定、开箱即用；自定义模板支持基于 ICIO、CRISPE、RASCEF 等工程框架结构化构建，适用于金融风控、医疗咨询等强约束场景 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。  
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强和安全边界补充，不计费且数据不用于训练 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。  
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（建议 5–10 条）和评测数据集（建议 ≥20 条），在推理模型（推荐千问-max）上多轮评估、反思并生成带 few-shot 示例的优化 Prompt，适配真实业务场景 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

> **注意**：Prompt 样例库功能已下线，官方明确要求迁移至 RAG 表格库，不再维护 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`） | 控制台模板卡片或 API 响应中获取 |
| `workspaceId` | 业务空间 ID，调用所有 Prompt 相关 API 的必需参数 | 需通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `variables` | 模板变量列表（如 `["platform", "topic"]`），用于运行时填充 | `GetPromptTemplate` 接口响应中返回 |
| `has_thoughts` | API 请求参数，设为 `true` 时返回样例检索详情（仅限历史样例库调试） | 已废弃，仅用于兼容旧调试流程 |
| 召回片段数 | 单次请求注入上下文的样例数量（默认 5，上限 10） | 仅适用于已停用的样例库功能 |

## 使用方式

### 控制台操作
- **模板管理**：进入「应用开发 > 组件管理 > 提示词」，可创建、编辑、复制或删除自定义模板；预置模板在「提示词 > [插件](../concepts/plugin.md)市场」查看，支持一键复制、创建应用或调用 API 示例。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可直接复制结果或「保存为模板」。
- **反馈优化**：在「提示词 > 反馈优化」页面配置推理模型、初始 Prompt、样例数据（上传或选自样例库）及评测数据集，启动优化任务。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段动态填充变量。
- **创建应用**：将生成的 Prompt 作为 `system_prompt` 或 `user_prompt` 参数提交至智能体应用 API。
- **调试验证**：在 OpenAPI 调试页选择 SDK V2.0（推荐），自动填充参数后运行示例代码 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）当前仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 自定义模板内容最大支持 6144 字符；
  - 图片生成模板正向/负向 Prompt 各有独立长度限制（未明确定义，建议 ≤2048 字符）；
  - 反馈优化评测数据集建议 ≥20 条，样例数据集建议 5–10 条且覆盖全部类别。
- **安全与合规**：
  - 自动优化过程不存储用户 Prompt，不用于模型训练；
  - 所有模板变量需符合 `${variableName}` 格式，非法变量名将导致填充失败；
  - 图片生成负向 Prompt 中禁止包含违法、违规或敏感词，否则触发内容审核拦截。
- **成本影响**：启用反馈优化或历史样例库会显著增加输入 [Token](../concepts/token.md) 消耗（公式：`总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token`），需纳入费用预估。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


