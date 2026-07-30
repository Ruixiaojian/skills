# 长期记忆

长期记忆是百炼平台提供的结构化用户记忆管理能力，用于跨会话、跨对话持久化存储和语义化检索用户关键信息（如偏好、待办、事件、画像属性），突破大模型上下文窗口限制，赋予智能体持续理解与个性化响应能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为核心上下文增强能力，替代仅限 0–30 轮的短期记忆。通过 `AddMemory` 自动从对话流中提取结构化记忆片段（如“每周三14:00健身”），再由 `SearchMemory` 在后续交互中动态召回，支撑长期意图建模与个性化决策。
- **用户画像构建**：配合 `profile_schema_id`，将对话中抽取的信息（如“职业=设计师”“偏好=暗色模式”）映射至预定义 Schema 字段，实现渐进式、可验证的结构化画像沉淀。
- **[多模态](multi-modal.md)场景适配**：支持含 `image_url` 的[多模态](multi-modal.md)消息输入（`messages.content` 为 array 类型），但当前仅对其中的文本内容进行语义解析与记忆提取。
- **OpenClaw 等插件集成**：可通过配置 `autoCapture` 和 `autoRecall` 实现全自动记忆捕获与检索，无需修改业务逻辑，开箱即用。
- **多应用共享**：同一记忆库可被多个智能体或工作流复用，通过 `user_id` 实现数据隔离，天然支持 SaaS 多租户或跨角色协同场景。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于严格隔离记忆空间；不同 `user_id` 数据完全不可见 | 业务侧稳定 ID（如 `uid_12345`） |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话（一问一答计为 2 条），用于自动抽取；`custom_content`：直接注入纯文本（≤512 字符） | 优先用 `messages` 实现上下文感知提取 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符）；不传则使用默认库（控制台可查） | 多租户/分业务线时建议显式指定 |
| `profile_schema_id` | string | 否 | 关联用户画像 Schema，触发结构化字段抽取（需提前创建 Schema） | 画像场景必填 |
| `top_k`（SearchMemory） | integer | 否 | 检索返回的最大条数 | 3–10（平衡精度与性能） |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 [0.0, 1.0]，低于此值的结果被过滤 | 0.5–0.7（避免噪声或漏召） |
| `enable_rerank` / `enable_judge` / `enable_rewrite`（SearchMemory） | boolean | 否 | 高级搜索开关，需显式启用以提升召回质量 | `enable_rerank=True` 建议开启 |

> ⚠️ 注意：  
> - `project_id`（记忆片段规则 ID）非必需参数，未传时系统自动选用默认规则；规则中设置的“过期时间”仅影响新写入记忆的生命周期策略，**底层存储无自动过期机制**，业务需自行清理。  
> - 所有接口均基于 DashScope 统一认证（`Authorization: Bearer $DASHSCOPE_API_KEY`），无需额外模型部署或密钥管理。

## 面向开发者，简洁实用

- ✅ **快速起步**：只需 `user_id` + `messages` 即可调用 `AddMemory`，5 分钟接入自动记忆提取。  
- ✅ **精准检索**：`SearchMemory` 支持自然语言查询（如“我上周订的咖啡”），无需构造关键词，语义匹配即用。  
- ✅ **SDK 封装完备**：Python 使用 `agentscope-runtime>=1.1.5`，`AddMemory`、`SearchMemory`、`ListMemory` 已封装为异步工具类；`DeleteMemory` 同样可用，`UpdateMemory` 建议直接调用 REST API（SDK 暂未封装）。  
- ✅ **生产就绪**：  
  - 全接口限流明确（`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM）；  
  - 所有失败响应含 `request_id`，便于问题定位；  
  - `meta_data` 支持自定义标签（如 `{"source": "chat", "priority": "high"}`），方便业务侧分类管理。  
- ❌ **避坑提示**：  
  - `custom_content` 和单条 `messages.content` 均严格限制 ≤512 字符，超长将截断；  
  - 时间戳参数（如 `UpdateMemory.timestamp`）为秒级 Unix 时间戳，毫秒输入会被向下取整；  
  - 记忆片段与用户画像**无默认过期策略**，务必在业务层实现定期清理或 TTL 控制。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


