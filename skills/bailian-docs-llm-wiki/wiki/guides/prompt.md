# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于明确任务目标、设定角色、约束输出格式并注入上下文。通过模板化、样例增强、自动优化等机制，开发者可系统性提升 Prompt 的可维护性、复用性和效果稳定性，避免硬编码与重复调试。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同开发阶段和精度要求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），实现结构与变量分离，便于集中管理与跨应用复用。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型输出风格与结构一致的结果，适用于智能客服、术语解释等需强一致性场景。> **注意**：该功能已停止维护，[文档 2](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确提示“推荐将样例库数据迁移到 RAG 表格库中”，新项目不应依赖此能力。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入与指令增强；另提供**反馈式优化**（Prompt Feedback Optimization），利用用户提供的输入-输出样例集，在推理模型（推荐 `qwen-max`）上多轮评估迭代，生成更贴合实际业务效果的 Prompt。后者需至少 5 条样例（覆盖全部类别）和 20 条评测数据，效果优于单次自动优化。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值/限制 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 控制台模板卡片或 API 返回中获取，长度固定 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作均需指定 | 通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `variables` | 模板中声明的动态变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，用于填充时校验 |
| `has_thoughts` | API 调用时启用样例检索过程日志（仅限已废弃的样例库功能） | 布尔值，设为 `true` 时响应含 `thoughts` 字段 |
| 召回片段数 | （样例库功能）单次请求注入上下文的样例数量 | 默认 5，可在应用配置中调整，上限 10 |
| 图片生成模板参数 | 区分 `positive_prompt`（正向提示）与 `negative_prompt`（负向提示） | 分别控制生成内容应含/应排除的元素 |

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 点击 **+ 创建提示词** → 选择类型（文本/图片生成）及输入模式（自定义创建 / 基于 Prompt 工程框架如 ICIO、CRISPE）。框架详情见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **样例库（已弃用）**：访问 [样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case) → 创建并关联至智能体应用 → 在应用配置中开启样例库开关。
- **自动优化**：在 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面右上角点击 **自动优化** → 输入原始 Prompt → 执行优化 → 可直接复制或保存为模板。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 与 `variables` 后填充变量生成最终 Prompt。
- **反馈优化**：调用 Prompt 反馈优化任务接口（路径 `/prompt/feedback-optimize`），上传样例数据（Excel，≤20MB，≤100条）与评测数据（建议 ≥20 条），启动异步优化任务，完成后下载优化结果。
- **模型调用**：将生成的 Prompt 作为 `messages` 中的 `system` 或 `user` 内容，按标准 OpenAI 兼容格式发送至目标模型 API（如 `qwen-plus`）。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、自动优化、图片模板）仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板最大长度为 **6144 字符**（控制台编辑框右下角实时计数）；
  - 图片生成模板中正向/负向 Prompt 各有独立长度限制，总和计入模型输入 [Token](../concepts/token.md)；
  - （已弃用）样例库：单库最多 300 条样例，单应用最多关联 5 个库，单次召回最多 10 条。
- **安全与隐私**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。
- **计费影响**：
  - Prompt 模板与自动优化本身不额外计费；
  - 使用样例库或反馈优化会显著增加输入 [Token](../concepts/token.md)（样例内容 + 评测数据注入），直接影响模型调用费用；
  - 图片生成模板中负向 Prompt 过长可能导致生成质量下降，需权衡描述精度与 [Token](../concepts/token.md) 消耗。
- > **注意**：文档间存在关键矛盾——[文档 2](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确声明 Prompt 样例库“已不再维护”，而[文档 4](../../raw/application-user-guide/prompt/prompt-custom-template.md) 的“相关文档”链接仍指向该功能。开发者应以文档 2 的停用声明为准，新项目必须迁移至 RAG 表格库方案。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


