# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心控制机制。它既可作为静态指令直接调用，也可通过模板化、样例增强、自动优化等方式实现结构化、可复用、可迭代的工程化管理。所有 Prompt 功能均面向华北2（北京）地域用户提供服务，跨地域调用需另行确认可用性。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力：**Prompt 模板**（含预置与自定义）、**Prompt 样例库**（已停用）、以及**多模式 Prompt 优化**（含自动优化与反馈优化）。

- **Prompt 模板**支持文本生成与图片生成两类基础类型，分别适配 LLM 和[多模态](../concepts/multi-modal.md)生成任务。文本生成模板支持变量插值（如 `${topic}`），并内置 ICIO、CRISPE、RASCEF 等 [Prompt 工程](../concepts/prompt-engineering.md)框架辅助结构化设计；图片生成模板则明确区分正向 Prompt（指定应包含内容）与负向 Prompt（指定应排除内容）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **Prompt 样例库**功能已正式下线，官方明确提示“**已不再维护**”，并要求用户将存量数据迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **Prompt 优化能力**分为两类：  
  - *自动优化*：基于单条原始 Prompt，由大模型进行结构重组、角色注入、指令增强等通用改写；  
  - *反馈优化*：依赖用户提供的输入输出样例（few-shot）及评测数据集，通过多轮评估-反思-生成闭环，产出高度贴合业务场景的定制化 Prompt [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

> **注意**：文档 2 明确声明 Prompt 样例库“已不再维护”，而文档 3 的“模板类型”表格中仍将其列为有效能力之一。此处以文档 2 的停用声明为准，开发者不应再依赖该功能。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取与调用 | 字符串，长度无公开限制 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作均需绑定此上下文 | 必填，需通过控制台或 API 获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| 召回片段数（样例库） | 单次请求注入上下文的样例数量 | 默认 5，上限 10（但该功能已停用） | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 样例数据量（反馈优化） | 用于优化训练的输入输出对数量 | 建议 5–10 条（样例集），≥20 条（评测集） | [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) |
| 模板内容长度 | 控制台编辑时最大字符数 | ≤ 6144 字符 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **创建提示词** → 选择“文本生成”或“图片生成” → 指定输入模式（自定义创建 / 基于 [Prompt 工程](../concepts/prompt-engineering.md)创建）→ 编辑内容 → 保存。  
- **使用模板**：在智能体应用配置中，点击 **使用prompt** > **创建应用**，模板内容将自动填充至提示词编辑框；变量（如 `${platform}`）需在运行时传入。  
- **优化 Prompt**：在 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt → 单击 **优化** → 复制结果或 **保存为模板**。  
- **反馈优化**：在 [提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 新增优化任务 → 选择推理模型（推荐千问-max）→ 输入初始 Prompt → 上传样例集与评测集 → 启动优化。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，返回含 `variables` 数组与 `content` 字符串的 JSON 响应。  
- **创建模板**：调用 `CreatePromptTemplate` 接口，需指定 `workspaceId`、`name`、`type`（`TEXT_GENERATION` 或 `IMAGE_GENERATION`）、`content` 等字段。  
- **优化调用**：当前无公开 API 支持自动优化或反馈优化，二者均为控制台专属功能。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含创建、管理、调用）仅在华北2（北京）地域可用，其他地域控制台可能不可见或报错 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **容量与规模**：  
  - 单个自定义 Prompt 模板内容 ≤ 6144 字符；  
  - 图片生成模板的正向/负向 Prompt 分别计长；  
  - 反馈优化任务中，评测数据集建议 ≥20 条，样例集建议 5–10 条且覆盖全部类别 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  
- **安全与合规**：  
  - 自动优化过程不存储用户 Prompt，亦不用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；  
  - 所有 Prompt 内容需符合阿里云内容安全策略，触发审核可能导致优化失败。  
- **成本影响**：  
  - Prompt 样例库虽本身免费，但会显著增加 [Token](../concepts/token.md) 消耗（用户查询 + 召回样例 + 系统指令）；  
  - 反馈优化生成的 Prompt 若包含大量 few-shot 示例，同样会推高单次调用 [Token](../concepts/token.md) 成本。  
- **版本与兼容性**：  
  - 预置 Prompt 模板不可修改，但可通过“复制模板”生成可编辑副本；  
  - 自定义模板支持编辑与删除，但被应用引用的模板需先解除关联方可删除 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


