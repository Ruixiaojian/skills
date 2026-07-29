# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它支持结构化模板、样例增强、自动优化等多种工程化手段，帮助开发者将业务逻辑与模型能力解耦，实现可复用、可迭代、可评估的提示词管理。所有功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力：**Prompt 模板**（含预置与自定义）、**Prompt 样例库**（已停用）、以及**Prompt 自动优化**与**反馈优化**。

- **Prompt 模板**分为两类：[预置Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)由阿里云提供，覆盖营销文案、摘要抽取等通用场景；[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)支持文本生成与图片生成两种类型，允许用户通过控制台或 API 创建、编辑和复用，适用于金融风控、医疗咨询等强定制需求场景。  
- **Prompt 样例库**功能已下线，官方明确说明“**已不再维护**”，推荐迁移至 RAG 表格库（参见[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)）。> **注意**：文档 3 中描述的样例库创建、关联与调试流程已失效，不可用于新项目开发。  
- **Prompt 自动优化**基于大模型对原始 Prompt 进行结构重组、角色注入与指令增强，不计费且不用于模型训练；而**Prompt 反馈优化**则依赖用户提供的输入-输出样例（5–10 条训练样例 + ≥20 条评测样例），通过多轮评估与反思生成更贴合实际业务效果的 Prompt，推荐使用千问-max 作为推理模型。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`） | 必填，从控制台模板卡片获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `variables` | 模板中声明的变量列表（如 `${topic}`、`${num1}`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，最大支持 6144 字符总长 |
| `recall_k` | 样例库召回片段数（仅历史有效） | 默认 5，上限 10 —— 但该参数已随样例库功能停用而失效 |
| `has_thoughts` | API 调用时启用样例检索过程日志（仅历史有效） | 仅在样例库生效期间可用，当前无实际作用 |

> **注意**：文档 3 中关于 `recall_k`、多路召回及 `has_thoughts` 的说明已过时，不应作为当前开发依据。

## 使用方式

### 控制台操作
- **创建模板**：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面 → 单击 **创建提示词** → 选择“文本生成”或“图片生成” → 按需选用“自定义创建”或“基于Prompt工程创建”（如 ICIO、CRISPE 框架）→ 输入内容 → 单击 **优化Prompt**（可选）→ **保存**。  
- **调用模板**：在智能体应用配置中单击 **使用prompt** → **创建应用**，模板变量（如 `${platform}`）将自动填充至提示词编辑框；右侧测试区输入问题即可调试。  
- **自动优化**：访问[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)页面 → 粘贴原始 Prompt → 单击 **优化** → 可直接复制或单击 **保存为模板**。  
- **反馈优化**：进入[提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → 新增优化任务 → 选择推理模型 → 输入初始 Prompt → 上传样例数据（建议 5–10 条）与评测数据（≥20 条）→ 启动优化 → 保存结果为模板或直接创建应用。

### API/SDK 集成
- 使用 `GetPromptTemplate` 接口拉取模板内容，解析 `variables` 字段后动态填充业务数据，再构造完整 Prompt 发送给目标模型。  
- 模板调用无需修改代码即可更新内容，实现逻辑与提示词分离（参见[使用Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)中“常见问题”说明）。  
- 所有 API 均需配置 `RegionId=cn-beijing`，且仅支持华北2（北京）地域。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、反馈优化）**仅限华北2（北京）地域**，跨地域调用将失败。  
- **模板容量**：单个 Prompt 模板内容最大支持 6144 字符；图片生成模板需分别填写正向与负向 Prompt。  
- **反馈优化数据要求**：样例数据应覆盖全部目标类别（每类至少 1 条），评测数据建议 ≥20 条以保障优化质量；数据不足将导致效果下降。  
- **安全与隐私**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**（参见[文档 4](../../raw/application-user-guide/prompt/optimize-prompt.md)）。  
- **废弃功能警示**：Prompt 样例库功能已正式下线，现有应用应尽快迁移至 RAG 表格库；继续依赖该功能可能导致服务中断或调试失败。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


