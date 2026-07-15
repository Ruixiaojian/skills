# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。通过结构化设计、模板化管理、样例增强与自动优化等能力，开发者可系统性提升模型输出的准确性、一致性与可控性。所有 Prompt 相关功能均需在华北2（北京）地域使用，且依赖业务空间（Workspace）上下文。

## 支持的模型/功能

百炼平台提供多种 Prompt 相关能力，覆盖从基础指令构造到高级场景适配的全链路：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），后者可通过控制台或 API 创建，并支持 ICIO、CRISPE、RASCEF 等工程框架辅助构建 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本学习注入高质量问答对，引导模型输出风格与格式一致的结果；但该功能已停止维护，官方明确建议迁移到 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，不计费且数据不用于训练 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（query-answer pairs）进行多轮评估与迭代优化，推荐使用 `qwen-max` 作为推理模型，效果优于纯文本自动优化 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 2 明确声明“Prompt样例库功能已不再维护”，而文档 1 和 3 中仍存在大量关于其创建、关联与调试的操作说明。实际开发中应以文档 2 的迁移指引为准，避免依赖已下线能力。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作（模板获取、样例库关联、反馈优化）均需指定 | 必填，通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 接口拉取内容 | 预置模板 ID 在控制台卡片中可见；自定义模板 ID 创建后生成 |
| `has_thoughts=true` | API 调用时启用样例检索过程日志（仅限已关联样例库的应用） | 仅影响响应中 `thoughts` 字段，非必需 |
| 召回片段数 | 单次请求注入上下文的样例数量，默认 5，最大 10 | 应用配置页可调，影响 Token 消耗与效果平衡 |
| 评测数据量 | Prompt 反馈优化中用于评估的 query-answer 对数量，建议 ≥20 条 | 数据越充分，优化效果越稳定 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) |

## 使用方式

### 控制台操作
- **模板创建与管理**：进入「组件管理 > 提示词」页面，支持自定义创建或基于 Prompt 工程框架（如 ICIO）生成；图片生成模板需分别填写正向/负向 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可复制结果或「保存为模板」。
- **反馈优化**：在「提示词 > 反馈优化」页面配置初始 Prompt、样例集（5–10 条）、评测集（≥20 条），启动多轮优化任务。

### API 调用
- 获取模板：调用 `GetPromptTemplate`，传入 `workspaceId` 和 `promptTemplateId`，返回含 `variables` 和 `content` 的 JSON 响应。
- 创建模板：调用 `CreatePromptTemplate`，需指定 `name`、`type`（`text` 或 `image`）、`content`（文本模板）或 `positivePrompt`/`negativePrompt`（图片模板）。
- 应用调用：若已关联样例库，可在请求体中设置 `has_thoughts: true` 查看检索详情。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；
  - 单个样例库最多 300 条样例（已停用，仅作历史参考）；
  - 批量导入样例文件 ≤20MB，单次 ≤100 条。
- **Token 成本**：启用样例库或反馈优化会显著增加输入 Token（样例内容 + 用户 query），需纳入成本预估 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **变量语法**：模板中使用 `${variable}` 占位符，渲染时需确保变量名与 `GetPromptTemplate` 返回的 `variables` 数组严格匹配。
- **安全合规**：自动优化服务不存储用户 Prompt 数据，亦不用于模型训练，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


