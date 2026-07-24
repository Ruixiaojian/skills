# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入，是连接业务逻辑与模型能力的关键接口。通过结构化模板、样例引导、自动优化等机制，开发者可系统性地管理提示词生命周期，提升输出一致性、可控性与效果稳定性。所有 Prompt 相关功能当前仅支持华北2（北京）地域。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同精度与工程化需求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板，适用于文本生成与图片生成两类任务。文本生成模板支持 ICIO、CRISPE、RASCEF 等结构化框架；图片生成模板支持正向/负向 Prompt 分离配置。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型复现特定解释风格或格式（如术语解释+类比）。**注意**：该功能已停止维护，官方明确建议迁移到 RAG 表格库，参见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的迁移说明。

- **Prompt 自动优化与反馈优化**：
  - *自动优化*：基于单条原始 Prompt，由大模型重写以增强指令清晰度、角色设定与安全边界；
  - *反馈优化*：基于用户提供的输入输出样例（query-answer pairs）和评测数据集，进行多轮评估-反思-迭代，生成更贴合实际场景的 Prompt。后者要求推理模型推荐使用 `qwen-max`，且评测数据建议 ≥20 条。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识 | 必填，需通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `promptTemplateId` | 模板唯一 ID | 必填，可在控制台模板卡片或 API 响应中获取（如 `cfec40c311f14f3e976403059d8f0116`） |
| `variables` | 模板变量列表 | 由 `GetPromptTemplate` 接口返回，用于运行时填充（如 `["platform", "topic"]`） |
| `has_thoughts` | 控制是否返回样例检索过程 | API 调用时设为 `true`，响应中 `thoughts` 字段含召回详情（仅限样例库关联应用） |
| 召回片段数 | 注入上下文的样例数量 | 应用配置中可调，默认 5，上限 10（见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |

## 使用方式

### 控制台操作
- **模板创建**：进入「组件管理 > 提示词」，选择「创建提示词」，按类型（文本/图片生成）和输入模式（自定义创建 / 基于 Prompt 工程创建）配置；
- **样例库关联**：在智能体应用「配置」页开启「样例库」开关，最多绑定 5 个库，系统自动多路召回；
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可复制或「保存为模板」；
- **反馈优化**：在「提示词 > 反馈优化」页面上传样例数据（建议 5–10 条）与评测数据（建议 ≥20 条），启动优化任务。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables`；
- **渲染 Prompt**：将业务数据代入模板变量（如 `${platform}` → `"小红书"`），生成最终 Prompt 字符串；
- **调用应用**：将渲染后的 Prompt 作为 `system` 或 `user` 消息提交至应用 API；若启用样例库，需设置 `has_thoughts=true` 查看检索细节。

> **注意**：`GetPromptTemplate` 接口返回的 `content` 字段即为待填充的模板字符串，其变量语法为 `${variableName}`，非 Jinja2 或其他模板引擎语法，直接字符串替换即可。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）均仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；
  - 单个样例库最多 300 条样例；单个智能体应用最多关联 5 个样例库；单次请求最多注入 10 个召回样例；
  - 批量导入样例库仅支持 ≤20MB Excel 文件，单次最多 100 条。
- **功能弃用**：Prompt 样例库功能已下线维护，[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 文档明确要求迁移至 RAG 表格库，新项目不应依赖该能力。
- **[Token](../concepts/token.md) 成本**：启用样例库或反馈优化会显著增加输入 [Token](../concepts/token.md)（含样例内容），直接影响计费，需在效果与成本间权衡。
- **数据安全**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合百炼数据隐私政策（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)）。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


