# 提示词工程

提示词工程（Prompt Engineering）是系统性设计、优化与管理大语言模型输入指令（Prompt）的技术实践，旨在通过结构化模板、角色设定、样例引导、约束注入等方法，稳定提升模型在特定任务上的准确性、一致性与可控性。它不是一次性调试技巧，而是贯穿模型应用全生命周期的工程能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：系统提示词（System Prompt）是智能体行为的“操作系统”，需明确角色、目标、[工具调用](tool-use.md)规范及失败回退逻辑；推荐使用预置模板（如「客服助手」「技术文档解析」）快速启动，或基于 CRISPE/RASCEF 框架自定义高鲁棒性模板，并绑定 `qwen-max` 等强[工具调用](tool-use.md)模型以保障执行稳定性。

- **工作流（Workflow）应用**：Prompt 作为节点级配置项嵌入流程，例如在「大模型节点」中填充动态模板（如 `${user_query} + ${retrieved_context}`），配合变量映射实现上下文精准注入；此时 Prompt 工程重点在于与 RAG 检索结果、历史会话变量的结构化拼接，避免信息冗余或语义冲突。

- **高代码应用开发**：通过 SDK 调用 `GetPromptTemplate` 获取模板内容与 `variables` 声明，程序化完成占位符填充（如 `content.replace('${topic}', topic)`），再将完整 Prompt 作为 `messages[0].content` 或 `system` 字段传入模型 API；适用于需批量生成、A/B 测试或多租户差异化提示的场景。

- **RAG 增强场景**：虽已弃用 Prompt 样例库，但提示词工程仍深度协同知识检索——在系统提示中显式声明“仅依据以下知识片段回答，禁止编造”，并设置边界指令（如“若知识中无答案，请回复‘暂未查到’”），可显著抑制幻觉；同时建议将 `retrieval_config.top_k` 与 Prompt 中的“参考上述 {k} 条信息”保持语义一致。

- **图片生成任务**：支持双模态 Prompt 模板（正向/负向），需遵循 `wan2.7-image-pro` 或 `qwen-image-2.0-pro` 的风格语法（如 `masterpiece, best quality, (1girl:1.3), detailed eyes`），负向 Prompt 应明确排除常见干扰项（如 `deformed, blurry, text, signature`）；模板变量可用于动态注入主体、风格、构图等要素。

> ⚠️ 注意：Prompt 样例库功能已正式弃用，所有新项目请迁移至 RAG 表格库或通过反馈优化替代；存量应用须在 2026 年底前完成迁移。

## 关键参数和配置

| 参数 | 说明 | 实用建议 |
|------|------|----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt API 必填 | 控制台右上角「账号中心」→「业务空间」查看；API 调用时需显式传入 |
| `promptTemplateId` | 模板唯一 ID，用于获取/更新模板 | 创建后控制台 URL 中 `templateId=` 后的字符串；SDK 示例中直接引用该 ID |
| `variables` | 模板中声明的动态占位符（如 `["product_name", "tone"]`） | 填充时确保键名完全匹配，值为字符串类型；空值建议设为 `""` 而非 `null` |
| `temperature` | 控制输出随机性（0.0–1.0） | 精确任务（如代码生成、格式转换）设为 `0.1`；创意任务（如文案扩写）设为 `0.7` |
| `enable_thinking` | 开启模型内部反思链（仅支持 `qwen-max`/`qwen3.7-plus` 等指定模型） | 需在智能体或模型 API 请求中显式启用，配合 ReAct 轮次限制使用效果更佳 |
| 模板长度上限 | 文本生成模板 ≤ 6144 字符；图片生成无单字段限制，但受模型上下文窗口约束 | 控制台编辑框右下角实时计数；超长逻辑建议拆分为多步骤 Prompt 或结合工作流编排 |

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台 → 「提示词」→ 「+ 创建提示词」→ 选「文本生成」→ 粘贴基础指令 → 点击「自动优化」一键增强结构与指令清晰度。
- ✅ **API 集成四步法**：① 调用 `GetPromptTemplate` 获取模板；② 解析 `variables` 列表；③ 将业务数据按 key 映射为字符串并替换 `${key}`；④ 将填充后 Prompt 作为 `system` 或首条 `messages.content` 发送。
- ✅ **避坑指南**：  
  - 所有 Prompt 功能**仅限华北2（北京）地域**，跨地域调用必失败；  
  - 自动优化不存储用户数据，但反馈优化需提供 5–10 条高质量样例 + ≥20 条评测数据；  
  - 图片生成负向 Prompt 建议固定复用通用黑名单（如 `lowres, bad anatomy, worst quality`），避免每次重写。  
- ✅ **性能权衡**：启用复杂 Prompt（如含 5 条样例或长角色设定）将显著增加输入 [Token](token.md)，直接推高调用成本——建议先用 `qwen-flash` 快速验证效果，再切至 `qwen-max` 生产部署。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)


