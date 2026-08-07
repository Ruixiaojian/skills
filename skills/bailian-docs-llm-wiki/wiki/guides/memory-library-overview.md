# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话状态保持。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），持久化存储并支持语义检索，使智能体能在后续交互中复用历史上下文。该能力以 API 形式开放，可集成至任意应用或 Agent 框架（如 OpenClaw），默认记忆库开箱即用。

## 支持的模型/功能

- **记忆片段**：从对话消息中自动提取事件性、意图性内容（如“每天上午9点提醒我喝水”），支持自定义规则、自动更新与去重。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、偏好），支持字段级描述引导与初始值设置。适用于需固定属性建模的场景。  
- **双模式提取**：支持 `Pro`（启用 Rerank，¥0.03/次）和 `Lite`（无 Rerank，¥0.018/次）两种记忆抽取版本，详见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **全生命周期管理**：提供 `AddMemory`、`SearchMemory`、`ListMemory`、`UpdateMemory`、`DeleteMemory`、`GetUserProfile` 等完整 API，覆盖写入、检索、浏览、更新、删除与画像获取。  
> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且可在控制台配置为 7/30/180 天或永不过期。实际行为以控制台配置为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 |
| `messages` | array | 否（与 `custom_content` 二选一） | 对话消息列表，用于自动提取记忆片段或用户画像 |
| `custom_content` | string | 否（与 `messages` 二选一） | 直接写入的原始文本内容，绕过自动提取 |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库（见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)） |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需提取画像时传入 |
| `meta_data` | object | 否 | 自定义元数据，用于分类管理（如 `"location_name": "北京"`） |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数，建议设为 3–10（见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)） |
| `minScore` | number | 否（默认 0） | `SearchMemory` 最小相似度阈值（0–100），用于过滤低相关结果 |

## 使用方式

### 1. 基础 API 集成
- **写入记忆**：调用 `AddMemory`，传入 `user_id` 和 `messages`（或 `custom_content`）。  
- **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（如 `"我需要做什么？"`）。  
- **管理记忆**：使用 `ListMemory` 分页查看、`UpdateMemory`/`DeleteMemory` 修改或删除指定记忆节点。  
- **用户画像**：先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema`，最后用 `GetUserProfile` 获取结构化结果（见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)示例）。

### 2. OpenClaw 插件集成
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`。  
- 配置 `openclaw.json`，设置 `apiKey`、`userId` 及可选 `memoryLibraryId`、`projectId` 等（见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- 插件自动启用 `autoCapture`（对话后写入）和 `autoRecall`（对话前检索），并注册 `memory_search`、`memory_store` 等工具供 Agent 主动调用。

### 3. 控制台调试
- 在[百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)中：  
  - 查看/编辑记忆库与规则；  
  - 在 **记忆详情** 标签页按 `user_id` 筛选并查看记忆实体；  
  - 在 **记忆检索** 标签页调试召回效果，调整 `topK` 和规则选择。

## 限制和注意事项

- **配额限制**：阿里云账号级别限流——全部接口合计 ≤ 3000 QPM；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM（见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)与[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **延迟特性**：`AddMemory` 端到端延迟 500–1000ms，`SearchMemory` 为 200–500ms；OpenClaw 中 `autoCapture` 异步执行，不影响响应速度。  
- **ID 隔离**：`user_id` 是记忆空间隔离的唯一依据，务必确保其全局唯一性；同一 `user_id` 下所有操作共享命名空间。  
- **画像提取时效性**：调用 `AddMemory` 写入含画像信息的对话后，需等待约 3 秒再调用 `GetUserProfile`，否则可能返回未更新结果（见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)示例）。  
- **API Key 要求**：必须使用 DashScope API Key（非 Coding Plan Key），且需配置环境变量 `DASHSCOPE_API_KEY` 或在请求头中显式传递（见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


