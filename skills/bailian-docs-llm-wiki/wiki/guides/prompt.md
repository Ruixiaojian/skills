# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为单次调用的直接输入，也可通过模板化、样例增强、自动优化等方式进行工程化管理，从而提升输出质量、一致性与可维护性。所有 Prompt 相关能力均需在华北2（北京）地域下使用，且依赖业务空间（Workspace）上下文。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同成熟度和精度需求：

- **Prompt 模板**：支持结构化变量注入（如 `${topic}`），适用于通用场景快速复用或复杂业务定制。模板分为[预置Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)（开箱即用，效果稳定）和[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)（支持文本生成与图片生成双模式，含 ICIO/CRISPE/RASCEF 等工程框架）。  
- **Prompt 样例库**：基于少样本学习（Few-shot），将高质量问答对组织为可检索的样例库，供智能体应用在推理时动态注入上下文。> **注意**：该功能已停止维护，[原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)明确提示“推荐将样例库数据迁移到 RAG 表格库中”。  
- **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色注入与指令强化，适用于缺乏 Prompt 工程经验的开发者；而[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)则进一步引入用户提供的评测数据，实现场景驱动的闭环优化，效果更精准。

## 关键参数

| 参数 | 说明 | 取值/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作（创建、获取、关联）均需指定 | 必填，通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `promptTemplateId` | 模板唯一 ID，用于 API 调用 `GetPromptTemplate` | 必填，控制台模板卡片上可复制 |
| `has_thoughts` | 控制是否返回样例检索过程详情（仅限已停用的样例库功能） | `true`/`false`，API 调用时设置 |
| 召回片段数 | 样例库关联应用时可配置的注入样例数量 | 默认 5，上限 10（见[原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |
| 评测数据量 | Prompt 反馈优化效果的关键因子 | 建议 ≥20 条，且覆盖全部目标类别 |

## 使用方式

### 控制台操作
- **模板管理**：进入「应用开发 > 组件管理 > 提示词」，可创建、编辑、复制或删除模板；预置模板支持「复制模板」生成可编辑副本。  
- **样例库（已停用）**：原位于「组件管理 > 样例库」，现仅作迁移参考。  
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可复制结果或「保存为模板」。  
- **反馈优化**：在「提示词 > 反馈优化」页面上传初始 Prompt、样例数据（5–10 条）及评测数据（≥20 条），启动多轮评估优化。

### API/SDK 调用
- 获取模板：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `variables` 数组与 `content` 字符串。  
- 创建模板：调用 `CreatePromptTemplate`，支持文本生成与图片生成类型，后者需分别指定 `positive_prompt` 和 `negative_prompt` 字段。  
- 智能体应用关联：通过应用配置 API 启用样例库（历史功能）或在创建应用时直接绑定优化后的模板 ID。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、自动优化、反馈优化）仅支持华北2（北京）地域，跨地域调用将失败。  
- **容量限制**：  
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；  
  - 图片生成模板的正向/负向 Prompt 各有独立长度限制，超长将截断；  
  - 反馈优化任务中，单次上传的评测 Excel 文件 ≤20MB，且建议单文件数据量 ≤100 条以保障稳定性。  
- **安全与隐私**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。  
- **功能演进**：Prompt 样例库功能已下线，新项目请使用 RAG 表格库替代；旧有样例库仍可查看，但不可新增或关联新应用。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


