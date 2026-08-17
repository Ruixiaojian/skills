# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话用户状态持久化能力，用于解决大模型原生“无状态”导致的上下文遗忘问题。它通过自动语义提取、向量化存储与智能检索，将对话中的关键事件（如提醒、偏好、承诺）和用户属性（如职业、兴趣）转化为可管理、可复用的记忆资产。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为核心状态层，支持 `autoCapture`（对话后自动提取）与 `autoRecall`（对话前自动检索），使 Agent 能记住用户历史指令（如“我讨厌咖啡因”）、持续跟踪任务进展（如“上次说要分析Q3销售数据”）。OpenClaw Agent 可通过插件一键集成，无需修改业务逻辑。
  
- **工作流（Workflow）与高代码应用**：通过调用 `SearchMemory` 接口在任意节点注入用户记忆，实现个性化流程分支（例如：若用户画像中 `is_vip == true`，则跳过付费确认步骤）；也可在 `AddMemory` 中写入工作流执行结果（如“订单ID: ORD-789 已创建”），供后续会话复用。

- **记忆库（Memory Library）统一管理**：所有应用共享同一套记忆基础设施。开发者可在控制台创建多个记忆库，按业务域隔离（如 `user_memory`、`support_ticket_memory`），并为每个库独立配置提取规则（有效期、字段映射、Pro/Lite 策略），实现多应用协同记忆。

- **与用户画像深度耦合**：当传入 `profile_schema` 时，系统在 `AddMemory` 过程中同步解析并更新结构化画像（如从“我今年35岁，在杭州做设计师”中提取 `age=35`, `city="杭州"`, `occupation="设计师"`），画像字段可直接用于条件判断或模板填充。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 场景 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作均以此隔离数据空间。**必须与业务系统用户 ID 对齐**。 | 全场景通用 |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符）；不传则使用默认库。建议生产环境显式指定，便于权限与配额管理。 | 全场景通用 |
| `projectId` | string | 否 | 记忆片段规则 ID（控制提取策略、有效期、是否启用 Rerank）。**决定 `AddMemory` 行为**，不可在请求体中覆盖。 | AddMemory / 自动捕获 |
| `top_k` / `min_score` | integer / number | 否 | `SearchMemory` 专用：最多返回 `top_k` 条（1–100，默认 10）；仅返回相似度 ≥ `min_score`（0–100，默认 0）的结果。 | SearchMemory |
| `plan_version` | string | 否 | `SearchMemory` 显式指定检索策略：`pro`（开启 Rerank，精度高，¥0.001/次）或 `lite`（基础向量检索，¥0.00002/次）。**优先级高于 `projectId` 关联的默认策略**。 | SearchMemory |
| `autoCapture` / `autoRecall` | boolean | 否 | 默认 `true`。控制是否在智能体对话生命周期中自动触发写入/召回。设为 `false` 时需手动调用 API。 | OpenClaw / 新版智能体 |
| `meta_data` | object | 否 | 键值对（如 `{"source": "web_app", "session_id": "sess_abc"}`），透传至 `AddMemory`/`UpdateMemory`，并在 `ListMemory` 中返回，用于业务追踪与审计。 | AddMemory / UpdateMemory |

> ⚠️ 注意：  
> - `messages`（对话数组）与 `custom_content`（纯文本）互斥，后者优先级更高；`messages` 中单条 `content` 支持字符串或含图片 base64 的数组。  
> - 记忆默认**非永久有效**：有效期由 `projectId` 所绑定的记忆片段规则决定（支持 7/30/180 天或永不过期），非 API 参数控制。  
> - 所有接口均基于 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，认证方式为 `Authorization: Bearer $DASHSCOPE_API_KEY`。

## 面向开发者，简洁实用

- ✅ **快速上手**：安装 `agentscope-runtime>=1.1.5`，直接使用封装类：
  ```python
  from agentscope.runtime import AddMemory, SearchMemory
  await AddMemory(user_id="u123", messages=[{"role":"user","content":"明天下午3点开会"}]).arun()
  result = await SearchMemory(user_id="u123", query="会议时间", top_k=3).arun()
  ```

- ✅ **调试建议**：  
  - 先在[控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)创建测试库与规则，再调用 API；  
  - 使用 `ListMemory` 查看实际存储的片段结构，验证提取效果；  
  - `SearchMemory` 返回的 `score` 字段即向量相似度（0–1），低于 `min_score` 的结果已被过滤。

- ⚠️ **避坑指南**：  
  - 不要依赖 `UpdateMemory.timestamp` 实现过期逻辑——记忆有效期由规则控制，`timestamp` 仅用于排序；  
  - `plan_version` 仅影响 `SearchMemory`，`AddMemory` 的提取质量由 `projectId` 决定；  
  - QPM 限流按阿里云账号全局计数（总 3000 QPM），高频调用需做好本地缓存或批量聚合。

- 💡 **最佳实践**：  
  - 对敏感信息（如手机号、身份证号），在 `meta_data` 中标记 `"pii": true`，后续可结合 DLP 策略处理；  
  - 将 `user_id` 与业务主键强绑定，避免因登录态切换导致记忆断裂；  
  - 生产环境务必设置 `memory_library_id` 和 `projectId`，确保行为可预期、可审计。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


