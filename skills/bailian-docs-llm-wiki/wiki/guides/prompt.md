# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心指令载体。它既可作为静态文本直接调用模型，也可通过模板化、工程化、样例增强等方式实现结构化设计与动态生成。合理使用 Prompt 能显著提升输出质量、一致性与可控性，是构建稳定可靠大语言模型应用的关键环节。

## 支持的模型/功能

百炼平台提供多种 Prompt 相关能力，覆盖从基础指令到高级优化的全链路：

- **预置 Prompt 模板**：由阿里云官方维护，适用于通用场景（如营销文案、摘要抽取、风格改写），效果稳定且开箱即用，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **自定义 Prompt 模板**：支持文本生成与图片生成两类，可通过控制台或 API 创建；文本类支持「自定义创建」与「基于Prompt工程创建」两种模式，后者内置 ICIO、CRISPE、RASCEF 等结构化框架，适用于复杂任务；图片类支持正向/负向 Prompt 分离控制。> **注意**：所有模板功能当前仅适用于华北2（北京）地域，该限制在 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 和 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中均明确标注。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，不计费且数据不用于训练，详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（few-shot）和评测数据集，通过多轮评估与反思生成更贴合业务目标的 Prompt，推荐使用千问-max 作为推理模型，详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **Prompt 样例库**：已**停止维护**，官方明确建议迁移至 RAG 表格库，参见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 的说明部分。

## 关键参数

- `promptTemplateId`：模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`）。
- `workspaceId`：业务空间 ID，所有 Prompt 操作均需指定，获取方式见 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。
- `variables`：模板中声明的变量列表（如 `${platform}`、`${topic}`），用于运行时动态填充。
- `has_thoughts`：API 请求参数，设为 `true` 时可在响应 `thoughts` 字段中查看样例检索过程（仅适用于已停用的样例库功能）。
- 召回片段数：样例库关联应用时可配置，默认 5，上限 10（影响 [Token](../concepts/token.md) 消耗与效果平衡）。

## 使用方式

### 控制台操作
- **创建模板**：进入「应用开发 > 组件管理 > 提示词」，点击「创建提示词」，选择类型（文本/图片）与输入模式（自定义/工程化），填写内容后保存。
- **优化 Prompt**：在「提示词」页面右上角进入「自动优化」，粘贴原始 Prompt，点击「优化」后可复制或「保存为模板」。
- **使用模板**：在预置或自定义模板卡片中点击「使用prompt > 创建应用」，模板内容自动填充至智能体应用提示词区，变量（如 `${name}`）可直接编辑。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，返回含 `content` 与 `variables` 的 JSON 响应。
- **生成最终 Prompt**：将业务数据代入模板变量（如 `content.replace('${topic}', 'AI伦理')`），再将拼接后的完整 Prompt 作为 `system` 或 `user` 消息发送给目标模型。
- **反馈优化任务**：通过「提示词 > 反馈优化」页面提交初始 Prompt、样例数据（5–10 条）与评测数据（≥20 条），系统自动完成多轮迭代并输出优化结果。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（包括创建、管理、调用）目前仅支持华北2（北京）地域，跨地域调用将失败。
- **模板长度**：控制台编辑框最大支持 6144 字符；API 层面受模型上下文窗口限制（如通义千问-Plus-La[test 1](test-1.md)28K），需自行校验总 [Token](../concepts/token.md) 数。
- **样例库状态**：Prompt 样例库功能已下线，[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 文档明确指出“已不再维护”，新项目请勿依赖。
- **[Token](../concepts/token.md) 成本**：启用反馈优化或样例库（历史遗留）会显著增加输入 Token，成本公式为：`总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token`。
- **数据安全**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


