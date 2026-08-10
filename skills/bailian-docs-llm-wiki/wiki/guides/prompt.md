# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化模板、自动优化、样例引导等多种机制，开发者可高效构建稳定、可复用、符合业务需求的提示词，显著降低 Prompt 工程门槛并提升模型输出质量。所有功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力，面向不同场景和成熟度需求：

- **Prompt 模板**：支持预置模板（开箱即用，覆盖营销文案、摘要抽取等通用场景）和自定义模板（支持文本生成与图片生成两类），通过变量插值实现动态内容填充。预置模板不可修改，自定义模板支持编辑、复制与删除 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强等重构，适用于快速提升模糊或低效 Prompt 的效果，且不计费 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（few-shot）与评测数据集，通过多轮评估与反思生成高适配性 Prompt，效果优于纯自动优化，尤其适合垂直领域任务 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 中描述的 *Prompt 样例库* 功能已明确标注“**已不再维护**”，官方推荐迁移到 RAG 表格库。因此该功能不应作为当前开发方案选用，避免技术路径过时。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需，需通过[获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`）或控制台关联 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts=true` | API 调用时启用样例检索调试模式，响应中返回 `thoughts` 字段含详细召回过程 | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 样例库关联应用时可配置，默认 5，上限 10；直接影响 [Token](../concepts/token.md) 消耗与效果平衡 | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 评测数据量 | Prompt 反馈优化要求至少 20 条评测数据，样例数据建议 5–10 条且覆盖全部类别 | [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) |

## 使用方式

### 控制台操作
- **模板管理**：进入「应用开发 > 组件管理 > 提示词」，可创建（文本/图片生成）、编辑、复制、删除自定义模板；预置模板仅支持查看、调用与复制副本。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可复制结果或「保存为模板」。
- **反馈优化**：在「提示词 > 反馈优化」页面配置推理模型、初始 Prompt、样例数据（上传或选样例库）、评测数据，启动优化任务。
- **样例库（已弃用）**：虽仍可见于控制台「样例库」入口，但文档明确要求迁移至 RAG 表格库，**不建议新建或依赖**。

### API 与 SDK
- 所有模板操作（创建、获取、更新）均通过 `bailian` OpenAPI 实现，核心接口包括 `CreatePromptTemplate`、`GetPromptTemplate`。
- 获取模板后，需将变量（如 `${topic}`）替换为实际值，再作为 `system` 或 `user` 消息发送至目标模型 API。
- 调试推荐使用 OpenAPI Explorer，在线填写 `workspaceId` 和 `promptTemplateId` 后直接发起调用，SDK 示例支持 Java/V2.0 等主流语言 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、自动优化、反馈优化）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **[Token](../concepts/token.md) 限制**：
  - 模板内容最大 6144 字符（控制台编辑框显示计数）；
  - Prompt 反馈优化中，单条样例或评测数据过长将导致优化失败；
  - 样例库启用后，召回样例会显著增加输入 [Token](../concepts/token.md)，需按公式 `总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token` 预估成本 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **容量限制**：
  - 单个样例库最多 300 条样例（已弃用，仅作历史参考）；
  - 单个智能体应用最多关联 5 个样例库（同上）；
  - 批量导入样例库 Excel 文件 ≤20MB，单次 ≤100 条。
- **安全与隐私**：提交至自动优化功能的 Prompt 数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **模型选择**：Prompt 反馈优化明确推荐使用 `qwen-max` 作为推理模型，以保障优化过程稳定性。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


