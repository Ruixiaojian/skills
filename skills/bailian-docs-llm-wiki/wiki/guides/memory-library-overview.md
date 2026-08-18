# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于解决大模型受上下文窗口限制、无法跨会话保留信息的问题。它通过自动从对话中提取关键事件（记忆片段）和结构化用户属性（用户画像），并持久化存储与语义检索，使智能体具备持续理解用户偏好与历史上下文的能力。该能力以开放 API 形式提供，支持任意应用接入及多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、智能去重、动态更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义模板（`ProfileSchema`）从对话中结构化抽取固定属性（如年龄、职业、爱好），支持字段级描述引导、初始值设定与增量更新。适用于需强 schema 约束的场景。  
- **双模态检索**：支持基于自然语言查询的语义检索（`SearchMemory`），并可选开启 Rerank 重排（Pro 版）以提升相关性；也支持分页列表（`ListMemory`）与 ID 精确查询。  
- **自动生命周期集成**：在 OpenClaw 等框架中可通过 `autoCapture` / `autoRecall` 钩子实现对话结束自动写入、对话开始前自动召回，无需手动干预 —— 详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 共享命名空间。 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传时默认使用账号下默认记忆库（不可删除）。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传时默认使用所选记忆库的默认规则。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需提取画像时必传，否则不触发画像抽取。 |
| `meta_data` | object | 否 | 自定义键值对，用于记忆分类、标签或业务上下文透传（如 `"location_name": "北京"`）。 |
| `plan_version` | string | 否（但强烈建议显式指定） | 控制策略版本：`pro`（启用 Rerank，质量高，¥0.03/次 Add，¥0.001/次 Search）或 `lite`（关闭 Rerank，成本低，¥0.018/次 Add，¥0.00002/次 Search）。注意：`AddMemory` 的 `plan_version` 由关联 `MemoryProject` 决定；而 `SearchMemory` 的 `plan_version` 由请求参数独立控制，优先级高于 `enable_rerank` —— 详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。 |

> **注意**：文档 1 中称“记忆片段默认有效期 180 天”，而文档 3 明确指出“生成的记忆片段与用户画像暂无失效日期”。实际行为以 API 运行时为准：**记忆过期时间由创建 MemoryProject 时配置的 `expired_in_days` 字段决定，若未设置则永不过期**。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 的 `CreateMemoryProject` 接口说明为准。

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：每轮对话结束后调用 `AddMemory`，传入 `messages` 数组（含 user/assistant 轮次）及 `user_id`；如需提取画像，必须同时传入 `profile_schema`。  
3. **检索记忆**：在新会话开始前或用户提问时调用 `SearchMemory`，传入 `user_id` 和自然语言 `query`（或 `messages`），推荐设置 `top_k=3~5` 并显式指定 `plan_version`。  
4. **注入上下文**：将 `SearchMemory` 返回的 `memory_nodes[].content` 拼接至 Prompt 开头或特定位置。  
5. **高级操作**：使用 `ListMemory` 浏览、`UpdateMemory` 编辑、`DeleteMemory` 删除单条记忆；通过 `CreateProfileSchema` 定义画像模板，再用 `GetUserProfile` 获取完整结构化画像 —— 所有 API 均可在 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中查到完整参数与示例。

## 限制和注意事项

- **速率限制**（阿里云账号级别）：  
  - `AddMemory`：120 次/分钟  
  - `SearchMemory`：300 次/分钟  
  - 所有记忆 API 合计：3000 次/分钟  
  （详情见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）  
- **商业化计费**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，Pro/Lite 版本按调用次数收费，详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **默认记忆库限制**：不可删除，但可编辑名称、描述及规则；其预置的“默认项目”规则不可删除，仅可编辑。  
- **用户画像字段设计**：应避免语义重复字段（如同时定义“姓名”“名字”“名称”），且单次对话通常无法提取全部画像字段，建议通过多轮交互渐进完善。  
- **延迟预期**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；OpenClaw 插件中 `autoCapture` 为异步执行，不影响主响应流。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


