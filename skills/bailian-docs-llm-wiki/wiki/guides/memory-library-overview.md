# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并基于语义检索在后续交互中动态召回，使智能体具备持续性理解能力。该能力以开放 API 形式提供，支持任意应用集成，也支持多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段**：从对话消息流中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、更新与删除；适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与最终聚合查询；适用于需固定字段的用户建模场景。  
- **双模式提取**：支持 `Pro`（启用 Rerank，精度高，¥0.03/次）和 `Lite`（无 Rerank，成本低，¥0.018–¥0.025/次）两种记忆抽取版本，详见[配置记忆规则](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **自动捕获与召回**：在 OpenClaw 等框架中可通过插件实现 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入），无需手动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明默认记忆片段规则有效期为 180 天，且可在控制台配置为 7/30/180 天或永不过期。此处以文档 1 的可配置行为为准，实际过期策略由记忆规则决定。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离。 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传则使用默认记忆库（见[创建记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅在提取画像时需传入。 |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与条件过滤。 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数，建议设为 3–10（见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。 |
| `minScore` | number | 否（默认 0） | 相似度阈值（0–100），低于此值的记忆不返回。 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（获取方式见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory`，传入 `messages`（对话数组）或 `custom_content`（直接写入文本），指定 `user_id` 及可选参数。  
3. **检索记忆**：调用 `SearchMemory`，传入自然语言查询（如 `"我需要做什么？"`）或 `messages`，系统返回语义最相关记忆列表。  
4. **注入上下文**：将检索结果拼接至 Prompt，驱动个性化响应。  
5. **高级操作**：使用 `ListMemory` / `UpdateMemory` / `DeleteMemory` 进行管理；通过 `CreateProfileSchema` + `GetUserProfile` 构建和读取用户画像。  

OpenClaw 用户可直接安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `openclaw.json` 配置 `apiKey` 和 `userId` 即可启用全自动捕获与召回，详见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **速率限制**（阿里云账号级别）：  
  - 所有 API 合计 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  （详见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)与[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）  
- **延迟参考**：`SearchMemory` 端到端延迟 200–500ms；`AddMemory` 延迟 500–1000ms；自动捕获为异步执行，不影响主流程响应速度。  
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条有效期 180 天的“默认项目”规则，可编辑但不可删。  
- **用户画像提取延迟**：调用 `AddMemory` 写入带 `profile_schema` 的对话后，需等待约 3 秒再调用 `GetUserProfile`，否则可能返回空值（见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)示例）。  
- **API Key 兼容性**：仅支持百炼平台标准 API Key；不支持 Coding Plan 的 API Key（见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


