# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心指令载体。它既可作为静态文本直接调用，也可通过模板化、工程化、反馈优化等方式进行结构化管理与持续迭代。平台提供从零构建、自动优化、样例增强到模板复用的全链路支持，覆盖文本生成、图片生成等[多模态](../concepts/multi-modal.md)场景，适用于通用任务快速启动和复杂业务深度定制。

## 支持的模型/功能

- **基础模型支持**：所有百炼接入的大语言模型（如通义千问系列）均支持原始 Prompt 输入；图片生成类模型（如万相）支持正向/负向 Prompt 分离输入。  
- **核心功能**：  
  - **自定义Prompt模板**：支持文本生成与图片生成两类模板，提供“自定义创建”和“基于Prompt工程创建”两种模式，内置 ICIO、CRISPE、RASCEF 等结构化框架 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)；  
  - **预置Prompt模板**：开箱即用的场景化模板（如营销文案生成、摘要抽取），效果稳定，适用于无Prompt设计经验的用户 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)；  
  - **Prompt自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与边界约束，提升输出稳定性 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)；  
  - **Prompt反馈优化**：利用用户提供的输入-输出样例（few-shot）驱动多轮评估与迭代，显著提升特定任务准确率，推荐使用千问-max 作为推理模型 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)；  
  - **Prompt样例库**：已**停止维护**，官方明确建议迁移至 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。> **注意**：该功能虽仍可访问，但不再更新且不推荐新项目使用，详见文档末尾迁移指引。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 必填，需与 `workspaceId` 配对使用 |
| `workspaceId` | 业务空间 ID，是模板归属和权限控制的基础 | 必填，通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `variables` | 模板中声明的占位符列表（如 `${topic}`、`${num1}`），用于运行时动态填充 | 模板创建时自动解析，不可在 API 调用中新增 |
| `max_tokens`（上下文） | 单次请求总 [Token](../concepts/token.md) 上限（含 Prompt + 输入 + 输出） | 文本生成默认 ≤ 6144 字符（约 8K tokens），具体依模型而定；图片生成受分辨率与提示词长度双重限制 |

## 使用方式

### 控制台操作
- **创建模板**：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面 → 单击 **创建提示词** → 选择类型（文本/图片生成）→ 选择输入模式（自定义 or Prompt工程）→ 编辑并保存。  
- **调用模板**：在智能体应用配置中点击 **使用prompt** → **创建应用**，模板变量（如 `${name}`）将自动填充至提示词编辑框；调试时可直接输入测试问题验证效果。  
- **反馈优化**：在[提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimization)页面 → 新增优化任务 → 上传样例数据（5–10条）与评测数据（≥20条）→ 启动优化 → 保存为模板或直接创建应用。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中返回 `content`（含变量）及 `variables` 列表。  
- **生成最终 Prompt**：将业务数据替换模板中的 `${variable}` 占位符，再作为 `system` 或 `user` 消息发送至目标模型 API。  
- **优势**：实现逻辑与内容分离，支持控制台热更新 Prompt 而无需重发代码，保障多服务间一致性 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（包括创建、管理、优化）**仅支持华北2（北京）地域**，跨地域调用将失败。  
- **模板容量**：单个 Prompt 模板内容最大支持 6144 字符（控制台界面显示字符计数）；API 层面受模型最大上下文窗口限制。  
- **样例数据要求**：  
  - 反馈优化中，样例数据集建议 **5–10 条**，且覆盖全部类别；评测数据集建议 **≥20 条**，越多效果越优；  
  - 样例库功能虽保留，但已明确废弃，新项目请勿依赖 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **安全与隐私**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。  
- **图片生成特殊性**：正向 Prompt 定义期望内容，负向 Prompt 排除干扰元素；二者共同作用，需避免语义冲突（如正向写“高清”，负向写“模糊”）。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)


