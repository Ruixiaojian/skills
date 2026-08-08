# memory library overview

百炼平台的 Memory Library 是一套面向[长期记忆](../concepts/long-term-memory.md)管理的基础设施，通过自动提取、结构化存储与语义检索能力，解决大模型跨会话上下文丢失问题。它支持记忆片段与用户画像两类核心数据形态，提供统一 API 接口和多语言 SDK，并可被 OpenClaw 等 Agent 框架原生集成。所有功能均基于 DashScope API 实现，开发者需配置 `DASHSCOPE_API_KEY` 后即可调用。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话历史中自动提炼关键事件（如“每天上午9点提醒喝水”），支持自定义内容写入、语义检索、分页列表、更新与删除。适用于通用[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、兴趣），支持字段级描述引导、初始值设置及异步获取。适用于需固定属性建模的业务。  
- **双模式适配**：既可通过 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 直接调用，也支持通过 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 实现零代码自动捕获与召回。  
- **多应用共享**：同一记忆库可被多个应用或 Agent 共享，通过 `user_id` 隔离不同用户空间。

> **注意**：文档 3 明确指出默认记忆库中预置的记忆片段规则“默认有效期 180 天”，而文档 1 声称“生成的记忆片段与用户画像暂无失效日期”。该矛盾源于规则级配置（文档 3）与实例级存储（文档 1）的粒度差异——实际过期行为由记忆规则中的 `memory expiration time` 决定，而非全局策略。请以控制台配置或 API 请求中显式指定的 `expiration` 参数为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 |
| `memory_library_id` | string | ❌ | 记忆库 ID；不填则使用默认记忆库（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)） |
| `project_id` | string | ❌ | 记忆片段规则 ID；不填则使用默认规则 |
| `profile_schema` | string | ❌ | 用户画像 Schema ID；传入后触发画像提取 |
| `top_k` | number | ❌（默认 5） | 检索返回的最大记忆条数，建议设为 3–10 平衡效果与性能 |
| `min_score` | number | ❌（默认 0） | 相似度阈值（0–100），低于此值的结果将被过滤 |
| `meta_data` | object | ❌ | 自定义元数据，用于分类管理（如 `"category": "reminder"`） |

## 使用方式

### 1. 基础 API 调用（推荐）
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话数组）或 `custom_content`（纯文本）。  
- **检索记忆**：调用 `SearchMemory`，传入 `messages` 或 `query` 字段进行语义检索。  
- **管理记忆**：使用 `ListMemory`（分页查询）、`UpdateMemory`（按 ID 更新）、`DeleteMemory`（按 ID 删除）。  
- **用户画像**：先 `CreateProfileSchema` 定义字段，再 `AddMemory` 时传 `profile_schema` 触发抽取，最后 `GetUserProfile` 获取结果。

### 2. OpenClaw 插件集成
安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件后，在 `~/.openclaw/openclaw.json` 中配置 `apiKey` 和 `userId` 即可启用自动捕获（`autoCapture`）与自动召回（`autoRecall`）。插件还暴露四个工具供 Agent 主动调用：`memory_search`、`memory_store`、`memory_list`、`memory_forget`。

### 3. 控制台快速验证
登录 [百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)，使用默认记忆库完成三步验证：  
① 调用 `AddMemory` 写入示例对话；  
② 在「记忆详情」页按 `user_id` 查看自动提取结果；  
③ 在「记忆检索」页输入自然语言查询（如“我需要做什么？”）测试召回效果。

## 限制和注意事项

- **速率限制（阿里云账号级别）**：  
  - 所有 API 总计 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  （详见 [长期记忆 API 限流说明](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）

- **延迟指标**：  
  - `SearchMemory` 端到端延迟：200–500ms  
  - `AddMemory` 延迟：500–1000ms；自动捕获为异步执行，不影响主流程响应速度  

- **计费提示**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）起正式商业化计费**，当前为限时免费阶段（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。

- **环境依赖**：必须配置 `DASHSCOPE_API_KEY` 环境变量，且确保调用进程可访问该变量（OpenClaw Gateway 需重启生效）。

- **Schema 设计建议**：用户画像字段名应语义唯一（避免同时定义“年龄”“年纪”“岁数”），描述需具体清晰，且不应期望单轮对话提取全部属性。

## 来源文档

- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)


