# 长期记忆

长期记忆是百炼平台提供的结构化用户状态与对话历史持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨应用的用户偏好、关键事实与画像信息的自动提取、安全存储与语义召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为上下文增强的核心组件，长期记忆支持在新会话启动前自动检索（`autoRecall`）并注入相关记忆片段（如“用户讨厌咖啡因”），使智能体无需依赖历史对话轮次即可提供个性化响应；也可在对话结束后自动捕获（`autoCapture`）关键意图（如待办提醒、偏好变更）。
- **工作流（Workflow）应用**：通过显式调用 `SearchMemory` 工具节点，在流程关键步骤（如“生成个性化推荐”前）动态加载用户画像或历史行为，实现状态驱动的分支决策。
- **高代码应用与 Managed Agents**：开发者可直接集成 `agentscope-runtime` SDK 中的 `AddMemory`/`SearchMemory` 工具类，在自定义 Python 逻辑中精确控制记忆写入时机与检索条件（例如仅检索带 `meta_data: {"source": "survey"}` 的片段）。
- **OpenClaw 等框架集成**：通过官方插件 `@modelstudio/modelstudio-memory-for-openclaw`，零代码启用自动捕获与召回，同时暴露 `memory_search`/`memory_store` 等工具供 Agent 主动调用。
- **记忆库统一管理**：所有记忆均归属至逻辑隔离的「记忆库」（Memory Library），支持多应用共享同一库，也支持为不同业务创建独立库并配置差异化规则（如过期策略、Rerank 版本、默认画像模板）。

## 关键参数和配置

| 参数 | 说明 | 必填 | 默认值 | 注意事项 |
|------|------|------|--------|----------|
| `user_id` | 用户唯一标识符，最大 64 字符，所有操作以此实现多租户数据隔离 | 是 | — | 建议使用业务系统中的稳定 ID（如 `uid_12345`），避免使用临时 token |
| `messages` / `custom_content` | 二选一：传入对话数组（最多 50 条，一问一答计为 2 条）或纯文本内容（≤512 字符） | 是（互斥） | — | `custom_content` 优先级更高；若需写入非对话类信息（如注册表单、API 响应摘要），优先用此字段 |
| `memory_library_id` | 目标记忆库 ID（32 字符内） | 否 | 默认记忆库 | 可在控制台「记忆库列表」获取；生产环境建议显式指定，避免误用默认库 |
| `project_id` | 记忆片段规则 ID（影响提取逻辑、过期时间等） | 否 | 默认规则 | 规则中可配置 `expired_in_days`（如 `0` 表示永不过期）、`auto_refresh` 等，需提前在控制台创建 |
| `profile_schema` | 用户画像模板 ID | 否 | — | 需先调用 `CreateProfileSchema` 创建；用于触发结构化属性抽取（如从“我今年35岁，做设计师”中提取 `age=35`, `occupation="designer"`） |
| `plan_version`（仅 `SearchMemory`） | 检索策略版本：`"pro"`（启用 Rerank，精度高、成本高）或 `"lite"`（基础向量检索，成本低） | 否 | `"pro"` | **关键计费参数**：`pro` ¥0.001/次，`lite` ¥0.00002/次；该参数优先级高于 `enable_rerank`，显式传入即生效 |
| `top_k`（仅 `SearchMemory`） | 最大召回数量 | 否 | `10`（API） / `5`（OpenClaw 插件） | 范围 `1–100`；建议根据下游模型上下文长度合理设置（如 Qwen-Max 输入上限 32K token，`top_k=10` 通常足够） |
| `min_score`（仅 `SearchMemory`） | 相似度阈值 | 否 | `0.3` | 值域 `[0,1]`；设为 `0.6` 可显著提升结果相关性，但可能降低召回率 |

> ⚠️ 注意：记忆片段默认有效期由 `project_id` 对应规则中的 `expired_in_days` 决定（未配置时按默认项目值，如 180 天）；**长期记忆本身无全局过期机制，过期行为完全由规则控制**。

## 面向开发者，简洁实用

- **快速上手**：只需 `user_id` + `messages` 或 `custom_content` 即可调用 `AddMemory`；搜索时传 `user_id` + 查询消息，`plan_version` 按成本敏感度选择。
- **SDK 优先**：使用 `agentscope-runtime>=1.1.5`，封装了连接复用、重试、错误分类（如 `MemoryQuotaExceededError`），比裸 API 更健壮。
- **避免常见坑**：
  - 不要省略 `user_id`——缺失将导致 400 错误；
  - `messages` 中角色必须为 `"user"` 或 `"assistant"`，其他值（如 `"system"`）会被忽略；
  - `SearchMemory` 返回的是 `memory_nodes` 列表，每个节点含 `content`（原始文本）、`score`（相似度）、`meta_data`（自定义元信息），直接取 `node.content` 即可注入 [prompt](../guides/prompt.md)；
  - 若需强一致性更新（如修正错误偏好），先 `ListMemory` 定位 `node_id`，再 `UpdateMemory`，而非重复 `AddMemory`（后者会新增冗余节点）。
- **调试技巧**：使用 `ListMemory` 查看已存片段；在控制台「记忆库 → 详情页」开启「调试模式」，可实时查看自动提取的日志与结构化结果。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


