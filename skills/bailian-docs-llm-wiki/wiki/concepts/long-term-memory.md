# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户信息管理能力，用于突破大模型上下文窗口限制，实现跨会话的用户偏好理解、历史事件追溯与个性化上下文注入。它通过自动提取对话关键信息生成记忆片段，并支持结构化用户画像构建与语义检索，所有能力以统一 API 接口（`https://dashscope.aliyuncs.com/api/v2/apps/memory/`）开放。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）增强**：在 Managed Agents 的会话生命周期中，可通过 `autoCapture` / `autoRecall` 钩子自动完成“对话结束写入记忆”与“新会话开始前召回相关记忆”，无需修改 Agent 逻辑；召回结果可直接注入系统提示词或工具调用上下文，提升响应一致性与个性化水平。  
- **应用级记忆管理**：任意基于百炼 API 构建的应用（如客服机器人、个人助理），均可独立调用 `AddMemory` 和 `SearchMemory`，将用户指令（如“把下周会议设为静音”）、反馈（如“上次推荐的餐厅太贵”）转化为结构化记忆，支撑后续决策。  
- **用户画像驱动服务**：配合 `CreateProfileSchema` 定义强约束模板（如 `{ "age": "integer", "preferred_language": "string" }`），在 `AddMemory` 中传入 `profile_schema` 后，系统自动从对话中抽取并增量更新字段，最终通过 `GetUserProfile` 获取完整、可信的结构化画像，用于精准推荐或权限控制。  
- **RAG 场景补充**：区别于知识库（RAG）面向通用文档的检索，长期记忆聚焦于**单用户专属、高时效性、强意图性**的信息（如“用户张三过敏源：花生”），可与知识库检索结果协同注入 Prompt，形成“通用知识 + 个性上下文”的双层上下文增强。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 常用值/建议 |
|--------|------|------|------|-------------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有接口必需；同一 `user_id` 下的记忆与画像共享命名空间。 | `"u_123456"`，建议业务侧稳定生成（如登录 ID 或匿名设备 ID） |
| `memory_library_id` | string | 否 | 指定记忆库存储位置（≤32 字符）；不传则使用账号默认记忆库（不可删除）。 | 控制台 [记忆库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取 |
| `messages` / `custom_content` | array / string | 互斥（仅 `AddMemory`） | `messages`：最多 50 条对话记录（role/content 对），由系统自动提取关键事件；`custom_content`：≤512 字符纯文本，绕过提取，适合已结构化内容。 | 生产环境优先用 `messages`；调试或日志导入可用 `custom_content` |
| `profile_schema` | string | 否（仅 `AddMemory` 需画像时） | 用户画像模板 ID；传入后触发自动抽取与更新。 | 必须先调用 `CreateProfileSchema` 创建模板 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"category": "health", "source": "voice_input"}`），用于业务分类、溯源或条件过滤。 | 建议控制字段数 ≤10，单 value ≤256 字符 |
| `top_k`, `min_score`, `plan_version` | integer / double / string | 否（仅 `SearchMemory`） | `top_k`：返回最多条目数（1–100，推荐 3–5）；`min_score`：相似度阈值（0.0–1.0，推荐 ≥0.3）；`plan_version`：决定检索策略与计费（`pro` 启用 Rerank，精度高；`lite` 关闭 Rerank，成本低）。 | **必须显式指定 `plan_version`**（小写 `"pro"` 或 `"lite"`），避免计费歧义 |

> ⚠️ 注意：  
> - 记忆有效期由关联的 `MemoryProject` 的 `expired_in_days` 字段控制；未设置则永不过期，**需业务侧主动管理生命周期**（如定期 `DeleteMemory` 或通过 `UpdateMemory` 标记状态）。  
> - `plan_version` 在 `AddMemory` 中由所选 `MemoryProject` 决定，在 `SearchMemory` 中由请求参数独立控制，且优先级高于 `enable_rerank`。  
> - 所有 API 请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`。

## 面向开发者，简洁实用

- ✅ **首选 SDK**：安装 `agentscope-runtime>=1.1.5`，直接调用封装好的异步方法（如 `AddMemory().arun()`），自动处理重试、鉴权与错误码解析。  
- ✅ **最小可行集成**：  
  1. 对话结束后 → 调用 `AddMemory`（传 `user_id` + `messages`）；  
  2. 新会话开始前 → 调用 `SearchMemory`（传 `user_id` + `query="本次会话可能需要的上下文"` + `top_k=3` + `plan_version="lite"`）；  
  3. 将返回的 `memory_nodes[].content` 拼接至 Prompt 开头（例如：`"历史上下文：{content}\n\n当前问题：{user_input}"`）。  
- ✅ **调试技巧**：用 `ListMemory` 查看已存记忆，用 `cURL` 快速验证接口连通性（参考 [API 参考文档](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 示例）。  
- ❌ **避免踩坑**：  
  - 不要省略 `user_id` —— 否则数据混入默认用户空间；  
  - 不要依赖“自动过期”—— 当前无默认 TTL，需自行清理；  
  - 不要忽略 `plan_version` —— 未指定将按平台默认策略计费，可能导致成本不可控。  

> 💡 提示：2026 年 8 月 20 日起正式计费，Pro/Lite 版本调用单价差异显著（如 Search Pro ¥0.001/次 vs Lite ¥0.00002/次），请根据业务精度要求合理选型。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [application component api reference](../api/application-component-api-reference.md)


