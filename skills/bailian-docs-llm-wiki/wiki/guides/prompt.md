# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它支持结构化模板、样例增强、自动优化等多种工程化手段，帮助开发者将业务逻辑与模型能力解耦，实现可复用、可维护、可评估的提示词管理。所有 Prompt 功能均需在华北2（北京）地域使用，且依赖业务空间（Workspace）上下文。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力：

- **Prompt 模板**：分为预置模板（如营销文案生成、摘要抽取）和自定义模板（支持文本生成与图片生成两类），通过变量插值（如 `${topic}`）实现动态内容注入 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：基于少样本学习（Few-shot），通过用户提供的问答对集合引导模型输出风格与结构一致性；但该功能已停止维护，官方明确建议迁移到 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化与反馈优化**：前者基于单次大模型重写（如结构重组、角色注入）；后者则依赖用户提供的输入-输出样例集（5–10 条样例 + ≥20 条评测数据），在推理模型（推荐千问-max）上进行多轮评估与迭代优化 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 明确声明“Prompt样例库功能已不再维护”，而文档 2 和文档 4 均未提及此弃用状态，存在明显矛盾。实际开发中应以文档 3 的弃用说明为准，避免依赖已下线能力。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作均需指定 | 必填，通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `promptTemplateId` | 预置或自定义模板的唯一 ID | 必填，可在控制台模板卡片中直接复制 |
| `variables` | 模板中声明的占位符列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，不可手动修改 |
| `has_thoughts` | API 调用时启用样例检索调试信息的开关 | 仅适用于已关联样例库的应用（但该功能已弃用） |
| 召回片段数 | 样例库检索时注入上下文的最大样例数 | 默认 5，上限 10（见 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **创建提示词** → 选择「文本生成」或「图片生成」→ 指定输入模式（自定义创建 / 基于Prompt工程创建）→ 输入内容 → 单击 **优化Prompt**（可选）→ **保存** [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **调用模板**：在智能体应用配置中点击 **使用prompt** → **创建应用**，模板变量（如 `${name}`）将自动填充至提示词编辑框，最大字符限制为 6144。

### API/SDK 调用
1. 调用 `GetPromptTemplate` 获取模板内容与变量列表；
2. 替换变量值生成最终 Prompt；
3. 将生成的 Prompt 作为 `system` 或 `user` 消息传入模型推理接口（如 `ChatCompletion`）。

示例响应中 `content` 字段即为含变量的模板字符串，`variables` 字段声明了所有待替换字段。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板创建、优化、样例库）仅支持华北2（北京）地域，跨地域调用将失败。
- **[Token](../concepts/token.md) 开销**：启用样例库会显著增加输入 [Token](../concepts/token.md)（用户查询 + 召回样例 + 系统指令），直接影响计费；即使样例库本身免费，其带来的额外 [Token](../concepts/token.md) 成本需自行评估 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **模板容量**：单个 Prompt 模板内容上限为 6144 字符；图片生成模板需分别填写正向与负向 Prompt，无独立长度限制说明。
- **弃用提醒**：Prompt 样例库功能已正式下线，迁移路径参见 [Prompt 样例库迁移到 RAG 表格库](https://help.aliyun.com/zh/model-studio/migrate-sample-library-prompt-to-rag-table-library)；新项目严禁使用该能力。
- **数据安全**：Prompt 自动优化过程不存储用户输入，亦不用于模型训练，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


