# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于解决大模型跨会话上下文丢失问题。它通过自动从对话中提取关键信息并结构化存储为“记忆片段”和“用户画像”，支持语义检索与跨会话上下文注入，使智能体具备持续理解用户偏好与历史的能力。该能力以开放 API 形式提供，适用于自研应用、OpenClaw Agent 等各类集成场景。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：自动从 `messages` 中提炼事件性、意图性内容（如“每天上午9点提醒我喝水”），支持手动写入 `custom_content`；适用于通用[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义的 `profile_schema` 从对话中抽取结构化属性（如年龄、职业、兴趣），需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` ID 触发抽取。  
- **双模式接入**：既可通过直接调用 [长期记忆 API (新)](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 实现细粒度控制，也支持通过 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 实现零代码自动捕获与召回。  
- **多应用共享**：同一 `memory_library_id` 可被多个应用共用，`user_id` 作为隔离维度保障数据边界。

> **注意**：文档 3 提到默认记忆库中“默认项目”规则“默认有效期 180 天”，而文档 1 明确说明“生成的记忆片段与用户画像暂无失效日期”。该矛盾源于规则配置项（`memory_expiration_time`）与实际存储行为的差异——**记忆本身永不过期，但规则可配置过期策略，且仅对新写入生效；已存在的记忆不受影响**。详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 中“配置记忆片段规则”部分。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 数据完全隔离 |
| `memory_library_id` | string | ❌ | 记忆库 ID；不填则使用默认记忆库（每个账号自带一个） |
| `project_id` | string | ❌ | 记忆片段规则 ID；不填则使用默认规则或记忆库内首个可用规则 |
| `profile_schema` | string | ❌ | 用户画像规则 ID；仅当需触发画像抽取时传入 |
| `top_k` | number | ❌（默认 5） | 检索返回的最大记忆条数；OpenClaw 插件默认为 `5`，API 推荐设为 `3–10` 平衡效果与性能 |
| `min_score` | number | ❌（默认 0） | 相似度阈值（0–100），低于此值的结果将被过滤；OpenClaw 插件单位为百分制，API 返回分数范围为 `[0,1]`，需注意单位转换 |

## 使用方式

### 1. 基础 API 调用（推荐用于自研应用）
- **写入记忆**：调用 `POST /api/v2/apps/memory/add`，传入 `messages` 或 `custom_content` + `user_id`。  
- **检索记忆**：调用 `POST /api/v2/apps/memory/memory_nodes/search`（推荐）或 `/api/v2/apps/memory/search`（旧路径，功能一致），传入 `user_id` 和 `messages` 或 `query`。  
- **管理记忆**：支持 `GET /memory_nodes`（分页列表）、`PATCH /memory_nodes/{id}`（更新）、`DELETE /memory_nodes/{id}`（删除）。  
- **用户画像流程**：`CreateProfileSchema` → `AddMemory`（含 `profile_schema`）→ `GetUserProfile`（需等待约 3 秒后查询）。

### 2. OpenClaw 插件集成（推荐用于 OpenClaw Agent）
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`  
- 配置 `~/.openclaw/openclaw.json`，设置 `apiKey` 和 `userId`，启用 `autoCapture`/`autoRecall`（默认开启）  
- 插件自动注册工具：`memory_search`、`memory_store`、`memory_list`、`memory_forget`，Agent 可在运行时动态调用  

### 3. 控制台操作（调试与验证）
- 在 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 页面查看/编辑记忆库、配置规则、调试检索效果  
- “记忆详情”页按 `user_id` 查看记忆实体，“记忆检索”页模拟语义查询并调整 `改写`、`排序`、`相似度阈值` 等参数优化召回质量  

## 限制和注意事项

- **配额限制**（阿里云账号级别）：  
  - 所有 API 合计 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  （详见 [长期记忆 API (新)](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）

- **延迟表现**：  
  - `SearchMemory` 端到端延迟：200–500ms  
  - `AddMemory` 延迟：500–1000ms；OpenClaw 插件中 `autoCapture` 为异步执行，不影响主响应流  

- **元数据与分类**：建议在 `AddMemory` 的 `meta_data` 字段中添加业务标签（如 `"category": "reminder"`），便于后续 `ListMemory` 过滤与管理  

- **用户画像最佳实践**：  
  - 字段名需语义唯一（避免同时定义“年龄”“年纪”“岁数”）  
  - 不应期望单轮对话提取全部画像字段，需通过多轮交互逐步完善  

- **环境依赖**：所有方式均需配置 `DASHSCOPE_API_KEY` 环境变量或显式传入 `apiKey`，且 Key 必须为百炼平台生成的有效密钥（**不支持 Coding Plan 的 API Key**）

## 来源文档

- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)


