# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/memory.md)能力基础设施，通过自动提取、向量化存储与语义检索机制，突破上下文窗口限制，实现跨会话的用户偏好与历史信息持续感知。它以统一 API 服务为底座，支持 OpenClaw 等 Agent 框架[插件](../concepts/plugin.md)化集成，也允许开发者直接调用 RESTful 接口或 SDK 进行深度定制。核心设计兼顾开箱即用性与企业级可配置性。

## 支持的模型/功能

- **记忆类型双轨支持**：  
  - **记忆片段（Memory Fragments）**：从对话消息中自动提炼关键事件（如“每天上午9点提醒喝水”），支持动态更新、智能去重与元数据分类；  
  - **用户画像（Profile Schema）**：基于预定义结构化模板提取固定属性（如年龄、职业、爱好），适用于需强一致性字段的场景。  
  二者可独立使用，也可协同工作——例如在 `AddMemory` 请求中同时指定 `profile_schema` 和对话内容，系统将并行生成片段与更新画像。

- **自动化能力**：  
  [插件](../concepts/plugin.md)模式下默认启用 `autoCapture`（对话结束自动提炼写入）和 `autoRecall`（对话开始前自动检索注入），无需 Agent 主动调用工具；[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 文档详细说明了该机制在 OpenClaw Gateway 中的生命周期钩子实现。

- **工具集开放**：  
  [插件](../concepts/plugin.md)向 Agent 注册 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个标准工具，支持运行时按需调用；[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 文档提供了对应 CLI 命令与 Python SDK 示例，便于调试与集成。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 2 明确指出默认记忆片段规则有效期为 180 天，且控制台支持自定义 7/30/180 天或永不过期选项。实际行为以控制台配置及 API 参数 `expiration_time` 为准，建议显式设置避免歧义。

## 关键参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `apiKey` | string | ✅ | — | DashScope API Key，用于鉴权；仅支持百炼平台 API Key，不支持 Coding Plan Key（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 常见问题 #3） |
| `userId` | string | ✅ | — | 用户隔离标识符，同一 `userId` 下记忆共享，不同 `userId` 完全隔离 |
| `memoryLibraryId` | string | ❌ | 默认记忆库 | 记忆库 ID，可在控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list) 页面获取；未提供时使用默认库 |
| `projectId` | string | ❌ | 默认项目 | 记忆片段规则 ID，决定如何提取内容；未提供时使用默认规则 |
| `profileSchema` | string | ❌ | — | 用户画像模板 ID，用于结构化属性抽取；需先通过 `CreateProfileSchema` 创建（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)） |
| `topK` | number | ❌ | `5` | 每次 `SearchMemory` 或 `autoRecall` 返回的最大记忆条数；推荐值 3–10（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 最佳实践） |
| `minScore` / `similarity_threshold` | number | ❌ | `0`（插件） / `0.5–0.7`（控制台） | 相似度阈值（0–100 或 0.0–1.0），低于此值的结果被过滤；控制台调试页建议设为 0.5–0.7，插件默认宽松，生产环境应根据召回质量调整 |

## 使用方式

- **插件集成（OpenClaw）**：  
  通过 `npm install @modelstudio/modelstudio-memory-for-openclaw` 安装，配置 `openclaw.json` 的 `plugins.slots.memory` 与 `plugins.entries`，重启 Gateway 即可启用自动捕获/召回；验证命令为 `openclaw modelstudio-memory stats`。

- **直接 API 调用**：  
  所有操作均通过 HTTPS 请求百炼服务端：  
  - 写入：`POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add`（支持对话消息或 `custom_content`）  
  - 检索：`POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search`  
  - 管理：`GET /memory_nodes`（列表）、`PATCH /memory_nodes/{id}`（更新）、`DELETE /memory_nodes/{id}`（删除）  
  完整接口规范见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

- **SDK 集成**：  
  推荐使用 `agentscope-runtime`（`pip install agentscope-runtime`），封装了 `AddMemory`、`SearchMemory`、`CreateProfileSchema` 等异步工具类，降低错误处理复杂度。

## 限制和注意事项

- **配额限制（阿里云账号级别）**：  
  - 总请求量 ≤ 3000 QPM（每分钟请求数）  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  超限返回 `429 Too Many Requests`，需实现退避重试逻辑。

- **性能指标**：  
  - `SearchMemory` 端到端延迟：200–500ms  
  - `AddMemory` 延迟：500–1000ms  
  `autoCapture` 异步执行，不影响主响应流；但高并发写入需注意限流。

- **关键约束**：  
  - 插件模式下**所有 Agent 共享同一记忆空间**，不支持按 Agent 独立配置（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) “重要”提示）；  
  - `userId` 是唯一隔离维度，业务需自行保证其唯一性与稳定性（如映射到用户登录 ID，而非临时会话 ID）；  
  - 用户画像字段名称需语义唯一（避免“姓名”“名字”“名称”并存），否则影响抽取准确率（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 最佳实践）；  
  - 控制台创建的记忆库无法删除（含默认库），仅可编辑名称、描述及规则。

- **调试建议**：  
  利用控制台 [记忆检索](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list) 标签页测试查询改写、意图判别、重排等开关效果；日志排查优先检查 `openclaw-YYYY-MM-DD.log` 中 `modelstudio-memory` 关键字（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 常见问题 #4）。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


