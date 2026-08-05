# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/long-term-memory.md)能力基础设施，通过自动提取、结构化存储与语义检索机制，突破上下文窗口限制，实现跨会话的用户偏好与历史信息持续感知。它既支持开箱即用的插件集成（如 OpenClaw），也提供标准化 API 供任意应用自主接入，核心能力覆盖记忆片段、用户画像两类持久化数据形态。

## 支持的模型/功能

- **记忆片段（Memory Fragments）**：从对话消息流中自动提炼关键事件与事实（如“用户每天上午9点需要喝水提醒”），支持自动去重、动态更新与元数据分类管理；也可通过 `custom_content` 字段直接写入结构化文本。详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、兴趣），支持字段级描述引导、初始值设定及多轮渐进式填充。该能力在 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中完整定义。
- **统一检索能力**：所有记忆均经向量化索引，支持自然语言查询（如“我需要做什么？”）的语义召回，返回带相似度分数的结果列表。

> **注意**：文档 2 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 2 的“配置记忆片段规则”章节明确说明可设置 7 天、30 天、180 天或永不过期；文档 3 未提及过期策略。以控制台实际配置为准，**默认有效期为 180 天**，非永久有效。

## 关键参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `apiKey` | string | 是 | — | DashScope API Key，以 `sk-xxx` 开头；不支持 Coding Plan Key（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)） |
| `userId` | string | 是 | — | 用户唯一标识，用于隔离记忆空间；不同 `userId` 完全隔离 |
| `memoryLibraryId` | string | 否 | 默认记忆库 ID | 记忆库 ID，可在控制台获取；不传则使用默认记忆库 |
| `projectId` | string | 否 | 默认项目 ID | 记忆片段规则 ID，决定提取逻辑；不传则使用默认规则 |
| `profileSchema` | string | 否 | — | 用户画像 Schema ID，用于触发结构化属性抽取 |
| `topK` | number | 否 | `5` | 每次 `SearchMemory` 返回的最大条数（范围 1–100） |
| `minScore` | number | 否 | `0` | 相似度阈值（0–100），低于此值的结果被过滤 |

## 使用方式

### 插件集成（OpenClaw）
适用于已部署 OpenClaw Gateway 的场景：
1. 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`
2. 配置 `~/.openclaw/openclaw.json`，启用插件并填入 `apiKey` 与 `userId`（[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）
3. 重启 Gateway：`openclaw gateway restart`
4. 自动启用 `autoCapture`（对话后写入）与 `autoRecall`（对话前注入），无需额外调用

### 直接 API 调用
适用于任意应用：
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（自定义文本），指定 `user_id` 和可选规则 ID
- **检索记忆**：调用 `SearchMemory`，传入自然语言 `query` 或 `messages`，指定 `user_id` 和 `top_k`
- **管理记忆**：使用 `ListMemory`、`UpdateMemory`、`DeleteMemory` 进行分页查看、内容更新与删除
- **用户画像**：先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema`，最后用 `GetUserProfile` 获取结果（[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）

## 限制和注意事项

- **配额限制**（阿里云账号级别）：
  - 总调用量：≤ 3000 QPM（每分钟请求总数）
  - `AddMemory`：≤ 120 QPM
  - `SearchMemory`：≤ 300 QPM
  - 端到端延迟：`SearchMemory` 200–500ms，`AddMemory` 500–1000ms（[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）
- **插件约束**：OpenClaw 插件为全局配置，所有 Agent 共享同一记忆空间，**不支持按 Agent 独立配置**（[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）
- **计费提示**：记忆库将于 2026 年 8 月 20 日起正式商业化计费，Pro 版本（含 Rerank）¥0.03/次，Lite 版本 ¥0.018/次（[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）
- **环境变量**：API 调用需确保 `DASHSCOPE_API_KEY` 环境变量已正确设置且进程可访问（[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


