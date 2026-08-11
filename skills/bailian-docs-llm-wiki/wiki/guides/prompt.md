# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于明确任务目标、设定角色、约束输出格式并注入领域知识。通过结构化模板、样例引导与自动优化等机制，开发者可系统性地提升模型输出的准确性、一致性与可控性，降低人工调优成本。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

- **模板化支持**：提供预置 Prompt 模板（覆盖营销文案、摘要抽取、风格改写等通用场景）和自定义 Prompt 模板（支持文本生成与图片生成两类），均通过统一 ID 管理，便于复用与协作 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **样例增强**：支持少样本学习（Few-shot）机制，可通过 Prompt 样例库将高质量问答对注入上下文，显著提升特定领域（如术语解释、客服应答）的输出稳定性与风格一致性。
- **自动优化**：提供两种优化路径：
  - 基于大模型重写的**Prompt 自动优化**（适用于单点指令提效）；
  - 基于输入输出样例的**Prompt 反馈优化**（需提供标注数据集，效果更贴近业务真实分布）[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- > **注意**：Prompt 样例库功能已**停止维护**，官方明确推荐迁移到 RAG 表格库实现类似能力 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填；仅限华北2（北京）地域有效 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填；需通过控制台或 API 获取 |
| `variables` | 模板中声明的变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 |
| `has_thoughts` | API 调用时启用样例检索调试模式的开关 | 仅限智能体应用 API；设为 `true` 时响应含 `thoughts` 字段 |
| 召回片段数 | 单次请求注入上下文的样例数量 | 默认 5，最大 10；在应用配置中调整 |

## 使用方式

### 控制台流程
1. **创建**：在[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面，选择「创建提示词」→ 指定类型（文本/图片生成）→ 选择输入模式（自定义创建 / 基于 Prompt 工程框架）→ 保存；
2. **优化**：在「自动优化」页面粘贴原始 Prompt，一键生成结构化版本；或在「反馈优化」页面上传样例与评测数据集，启动多轮迭代优化；
3. **使用**：在智能体应用配置中关联模板或样例库，或直接点击模板卡片的「创建应用」填充至提示词编辑框。

### API 流程
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 与 `variables`；
- **填充变量**：将业务数据代入 `${variable}` 占位符，生成最终 Prompt；
- **调用模型**：将生成的 Prompt 作为 `system` 或 `user` 消息发送至目标模型 API（如 `qwen-plus`）；
- **样例库调试**：调用智能体应用 API 时设置 `has_thoughts=true`，检查 `thoughts` 字段验证样例召回逻辑。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）仅支持华北2（北京）地域，跨地域调用将失败；
- **模板长度**：控制台提示词编辑框最大支持 6144 字符，超长模板需拆分或精简；
- **样例库容量**：单个样例库最多 300 条样例；每个智能体应用最多关联 5 个样例库；单次召回上限 10 条 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)；
- **数据安全**：Prompt 自动优化过程不存储用户输入，且**绝不用于模型训练**；
- > **注意**：文档中提及的「Prompt 样例库」与「RAG 表格库」功能存在事实性替代关系，当前新项目应优先采用 RAG 表格库实现样例增强，避免依赖已下线能力。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


