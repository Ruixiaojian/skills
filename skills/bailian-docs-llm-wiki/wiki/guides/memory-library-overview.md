# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并基于语义检索在后续交互中召回相关记忆，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，支持直接集成或通过插件（如 OpenClaw）自动接入。

## 支持的模型/功能

- **记忆片段**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、更新与删除。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与完整画像获取。适用于需固定字段的业务场景。  
- **自动捕获与召回**：在 OpenClaw 等框架中可启用 `autoCapture` 和 `autoRecall` 钩子，实现对话结束自动写入、对话开始前自动检索注入，无需手动干预。详情见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **元数据支持**：`AddMemory` 支持传入 `meta_data` 字段（如 `{"location_name": "北京"}`），用于分类管理与精细化过滤。  

> **注意**：文档 1 称记忆片段默认有效期为 180 天，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。该矛盾以文档 3 为准——**记忆本身无内置过期机制**；过期时间仅由记忆规则配置控制（如默认规则设为 180 天），属可选策略而非强制约束。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 | 来源参考 |
|------|------|----------|------|----------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间。同一 `user_id` 共享命名空间。 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 目标记忆库 ID；不填则使用默认记忆库。可在控制台记忆库卡片上获取。 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用指定记忆库的默认规则。 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID；用于触发画像提取。 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `top_k` | number | 否（默认 5） | 检索返回的最大记忆条数，建议设为 3–10 平衡效果与性能。 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（默认 0） | 相似度阈值，用于过滤低相关性结果；文档 1 推荐设为 0.5–0.7。 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接内容）及 `user_id`。支持指定 `memory_library_id`、`project_id`、`profile_schema` 和 `meta_data`。  
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（`query` 或 `messages`），可选 `top_k` 和 `similarity_threshold`。  
4. **管理记忆**：使用 `ListMemory` 分页查看、`UpdateMemory` 修改内容、`DeleteMemory` 删除条目。  
5. **用户画像工作流**：先调用 `CreateProfileSchema` 定义字段 → `AddMemory` 时传入 `profile_schema` → 等待提取后调用 `GetUserProfile` 获取结果。  
6. **插件集成（OpenClaw）**：安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId` 即可启用自动捕获与召回，同时暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用。详细步骤见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计不超过 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回限流错误。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；自动捕获为异步执行，不影响主流程响应速度。  
- **默认记忆库不可删除**：但可编辑名称、描述及添加/修改规则；预置的“默认项目”规则不可删除，仅可编辑。  
- **画像字段设计**：避免语义重叠的字段名（如同时定义“年龄”“岁数”），否则影响抽取准确率；单次对话通常无法提取全部画像字段，需多轮积累。  
- **API Key 要求**：仅支持百炼平台生成的 DashScope API Key，**不支持 Coding Plan 的 API Key**。  
- **调试建议**：使用控制台“记忆检索”标签页调试召回效果，开启“改写”和“排序”（gte-rerank-v2）可提升口语化查询的准确性。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


