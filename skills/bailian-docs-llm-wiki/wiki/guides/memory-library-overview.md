# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化记忆持久化与智能召回。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），并基于向量检索技术在后续交互中精准注入上下文，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，可集成至任意应用，也支持多应用共享同一记忆空间。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话消息中自动提炼关键事件与事实（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、动态更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化用户属性（如年龄、职业、偏好），支持字段级描述引导、初始值设定与多轮增量更新。适用于需固定属性建模的场景。  
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过插件生命周期钩子实现 `autoCapture`（对话结束自动写入）与 `autoRecall`（对话开始前自动检索注入），无需手动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **多规则支持**：每个记忆库最多支持 50 条记忆片段规则和 50 条用户画像规则，支持按业务场景隔离配置 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明默认记忆片段规则“默认有效期 180 天”，且控制台界面支持设置 7/30/180 天或永不过期。实际行为以控制台配置及 API 中 `expiration_days` 参数为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 | 来源 |
|------|------|----------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 目标记忆库 ID；不填则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发画像提取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义键值对，用于记忆分类、标签或业务上下文关联 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否（默认 5） | 检索返回最大条数，建议设为 3–10 平衡效果与性能 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（默认 0 / 0.5） | 相似度阈值；过低易引入噪声，过高可能漏召 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接内容），指定 `user_id` 及可选规则参数。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入自然语言查询（如 `"我需要做什么？"`）或 `messages`，系统执行语义检索并返回高相关性记忆节点。  
4. **集成到应用**：将检索结果拼接进 Prompt，或通过 OpenClaw 插件自动完成 `autoRecall` 注入；也可调用 `ListMemory`、`UpdateMemory`、`DeleteMemory` 进行管理。  
5. **用户画像工作流**：先调用 `CreateProfileSchema` 定义字段，再在 `AddMemory` 中传入 `profile_schema`，最后用 `GetUserProfile` 获取完整画像 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **延迟特性**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；自动捕获为异步执行，不影响主流程响应速度。  
- **规则覆盖**：默认记忆库不可删除，但可编辑；预置的“默认项目”规则不可删除，仅可编辑 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **画像字段设计**：避免语义重叠字段（如同时定义“姓名”“名字”“名称”），单次对话难以提取全部属性，应通过多轮对话逐步完善 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **OpenClaw 插件约束**：记忆插件为全局统一配置，所有 Agent 共享同一记忆空间，暂不支持 per-Agent 独立配置 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


