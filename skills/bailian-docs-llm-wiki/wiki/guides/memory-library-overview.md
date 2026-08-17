# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/long-term-memory.md)基础设施，通过自动提取、结构化存储与语义检索能力，解决大模型跨会话遗忘问题。它支持记忆片段（事件型记忆）与用户画像（结构化属性）两类数据形态，所有能力均通过统一 API 对接，可被 OpenClaw Agent、自定义应用或控制台直接调用。该能力已深度集成至百炼生态，无需额外部署即可快速启用。

## 支持的模型/功能

- **核心记忆类型**：  
  - **记忆片段**：从对话历史中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持动态更新与智能去重；  
  - **用户画像**：基于预定义 Schema 提取结构化属性（如年龄、职业、爱好），适用于需固定字段的场景。  
- **适用范围**：开放 API 接口，支持任意第三方应用接入，也支持多应用共享同一记忆库 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **模型无关性**：Memory Library 本身不依赖特定大模型，其提取与检索由百炼服务端统一处理；但记忆内容的生成质量受所选记忆规则策略版本（Pro/Lite）影响，详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 2 称“生成的记忆片段与用户画像暂无失效日期”，而文档 2 的“配置记忆片段规则”章节明确支持设置 7 天、30 天、180 天或永不过期；文档 3 亦提及 `expired_in_days` 参数。此处以控制台可配置的实际行为为准——**记忆默认有有效期，由关联的记忆片段规则决定，非永久有效**。

## 关键参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `apiKey` | string | 是 | — | DashScope API Key（以 `sk-xxx` 开头），用于身份认证 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `userId` | string | 是 | — | 用户标识符，用于隔离不同用户的记忆空间，同一 `userId` 共享命名空间 |
| `memoryLibraryId` | string | 否 | 默认记忆库 | 记忆库 ID，可在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面获取 |
| `projectId` | string | 否 | 默认项目 | 记忆片段规则 ID，决定记忆提取策略与有效期 |
| `profileSchema` | string | 否 | — | 用户画像 Schema ID，用于触发结构化属性提取 |
| `topK` | number | 否 | `5` | 每次 `SearchMemory` 或自动召回返回的最大记忆条数 |
| `minScore` | number | 否 | `0` | 相似度阈值（0–100），低于此值的记忆不返回 |
| `autoCapture` / `autoRecall` | boolean | 否 | `true` | 控制是否启用对话后自动写入 / 对话前自动检索 |
| `plan_version` | string | 否 | `"pro"` | 检索时显式指定策略版本（`pro` 或 `lite`），优先级高于规则默认值 |

> **注意**：`plan_version` 在 AddMemory 调用中由 `projectId` 所关联的记忆片段规则决定，不可在请求体中直接指定；但在 SearchMemory 中可独立传入，且优先级高于规则版本 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 使用方式

### 1. 基础接入（API 直连）
- 配置环境变量 `DASHSCOPE_API_KEY`；
- 调用标准 REST API：
  - `POST /api/v2/apps/memory/add` 写入记忆（支持对话消息或自定义内容）；
  - `POST /api/v2/apps/memory/memory_nodes/search` 语义检索；
  - `GET /api/v2/apps/memory/memory_nodes` 分页列出；
  - `PATCH /api/v2/apps/memory/memory_nodes/{id}` 更新；
  - `DELETE /api/v2/apps/memory/memory_nodes/{id}` 删除。

### 2. OpenClaw Agent 集成
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`；
- 配置 `~/.openclaw/openclaw.json`，在 `plugins.entries.modelstudio-memory-for-openclaw.config` 中填入 `apiKey` 和 `userId` 等必填项；
- 插件自动注册 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个工具，Agent 可在运行时按需调用；
- 自动捕获（`autoCapture`）与自动召回（`autoRecall`）默认启用，无需手动触发。

### 3. 控制台管理
- 登录百炼控制台 → 进入[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)；
- 创建/编辑记忆库、配置记忆片段规则与用户画像规则；
- 在“记忆详情”、“记忆检索”标签页中可视化查看、调试与验证效果。

## 限制和注意事项

- **配额限制**（阿里云账号级别）：  
  - 总调用量 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM；  
  - 超限将返回 `429 Too Many Requests`。
- **商业化时间**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，Pro/Lite 版本按调用次数收费 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **延迟指标**：  
  - `SearchMemory` 端到端延迟：200–500ms；  
  - `AddMemory` 延迟：500–1000ms；  
  - 自动捕获为异步执行，不影响主流程响应速度。
- **兼容性**：  
  - 不支持使用阿里云百炼 Coding Plan 的 API Key；  
  - 插件仅支持统一配置，所有 Agent 共享同一记忆空间，暂不支持 per-Agent 独立配置 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)；
  - `meta_data` 字段可用于对记忆进行分类管理（如 `{"category": "health"}`），便于后续精准过滤与检索。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


