# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化记忆持久化与智能召回。它通过自动提取对话中的关键事件（记忆片段）和结构化用户属性（用户画像），支持开发者将相关记忆注入 Prompt，从而构建具备持续理解能力的智能体。该能力以开放 API 形式提供，可集成至任意应用或 Agent 框架。

## 支持的模型/功能

记忆库本身不依赖特定大模型，其提取、向量化、检索等能力由百炼平台统一服务提供。核心功能包括：

- **记忆片段（Memory Snippet）**：从对话 `messages` 中自动提炼关键事实（如“每天上午9点提醒我喝水”），支持自定义内容写入（`custom_content`）、元数据标注（`meta_data`）及自动去重更新。适用于绝大多数[长期记忆](../concepts/memory.md)场景。  
- **用户画像（User Profile）**：基于预定义的 `profile_schema` 从对话中抽取结构化属性（如年龄、职业、偏好）。需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中指定 `profile_schema` 参数触发抽取。详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **自动捕获与召回**：在 OpenClaw 等 Agent 框架中，可通过插件实现 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入），无需手动调用。配置细节见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 明确指出“生成的记忆片段与用户画像暂无失效日期”，而文档 1 中默认记忆片段规则默认有效期为 180 天。实际行为以控制台配置为准——若未显式设置过期时间，则永不过期；若在规则中设置了 `memory_expiration_time`（如 7/30/180 天），则按该值生效。此差异源于规则级配置与全局默认值的区分，非矛盾。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间。同一 `user_id` 下所有记忆共享命名空间。 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 目标记忆库 ID。不传时使用默认记忆库。可在控制台记忆库卡片上获取。 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID。不传时使用对应记忆库的默认规则。 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID。仅当需触发画像抽取时必填。 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `top_k` | number | 否 | 检索返回的最大记忆条数，默认 5（OpenClaw 插件）或 3–10（API 最佳实践）。 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否 | 相似度阈值，用于过滤低相关性结果。OpenClaw 插件单位为整数（0–100），API 接口单位为浮点（0.0–1.0）。 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 和 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

### 基础 API 调用（通用）
1. **准备**：设置环境变量 `DASHSCOPE_API_KEY`（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入**：调用 `AddMemory`，传入 `messages` 或 `custom_content` 及 `user_id`。支持指定 `memory_library_id`、`project_id`、`profile_schema` 和 `meta_data`。  
3. **检索**：调用 `SearchMemory`，传入 `user_id` 和自然语言 `query` 或 `messages`。推荐 `top_k` 设为 3–10。  
4. **管理**：使用 `ListMemory`、`UpdateMemory`、`DeleteMemory` 进行分页查询、内容更新或删除。  

### OpenClaw 集成（开箱即用）
1. 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`。  
2. 配置 `~/.openclaw/openclaw.json`，填入 `apiKey` 和 `userId`，启用 `autoCapture`/`autoRecall`。  
3. 重启 Gateway 后，Agent 即自动完成记忆捕获与召回。同时暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用。详情见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回限流错误（429）。  
- **延迟**：`SearchMemory` 端到端延迟约 200–500ms；`AddMemory` 约 500–1000ms。自动捕获为异步执行，不影响主流程响应速度。  
- **记忆覆盖**：开启 `auto_update`（默认开启）后，相同语义的记忆会被自动合并更新，避免冗余。  
- **用户隔离**：`user_id` 是硬隔离边界，不同 `user_id` 的记忆完全不可见、不可交叉检索。  
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条“默认项目”规则（有效期 180 天），但可编辑。新建记忆库需手动配置规则。  
- **画像提取时效性**：调用 `AddMemory` 写入含画像信息的对话后，需等待约 3 秒再调用 `GetUserProfile` 获取结果，因后台异步处理。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


