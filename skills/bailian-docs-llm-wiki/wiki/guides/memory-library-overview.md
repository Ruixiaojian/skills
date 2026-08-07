# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并支持语义检索与注入，使智能体具备持续性理解能力。该能力以开放 API 形式提供，可集成至任意应用，也支持多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段**：从对话中自动提取关键事件（如“每天上午9点提醒我喝水”），适用于大多数[长期记忆](../concepts/long-term-memory.md)场景；也支持直接写入自定义内容（`custom_content` 字段）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、爱好），适用于需固定字段的场景 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过插件生命周期钩子（`agent_end`/`before_agent_start`）实现全自动记忆写入与检索 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明记忆片段规则支持配置过期时间（7/30/180 天或永不过期），且默认规则有效期为 180 天。实际行为以控制台配置及 API 参数 `expiration_time` 为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则 |
| `profile_schema` | string | 否 | 用户画像模板 ID；用于触发画像提取 |
| `meta_data` | object | 否 | 自定义元数据，用于分类管理（如 `{"location_name": "北京"}`） |
| `top_k` | number | 否（默认 5） | 检索返回的最大记忆条数（OpenClaw 插件默认为 5，API 默认值需查文档） |
| `min_score` | number | 否（默认 0） | 相似度阈值（0–100），低于此值的结果将被过滤 |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量，获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. **写入记忆**：
   - 调用 `AddMemory` 接口传入 `messages`（对话历史）或 `custom_content`（直接内容），指定 `user_id`；
   - OpenClaw 插件启用 `autoCapture: true` 后，对话结束自动执行此操作 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
3. **检索记忆**：
   - 调用 `SearchMemory` 接口传入自然语言查询（如 `"我需要做什么？"`）；
   - OpenClaw 插件启用 `autoRecall: true` 后，对话开始前自动注入相关记忆 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
4. **管理记忆**：支持 `ListMemory`（分页列出）、`UpdateMemory`（PATCH 更新）、`DeleteMemory`（DELETE 删除）等操作 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
- **延迟指标**：`SearchMemory` 端到端延迟 200–500ms，`AddMemory` 延迟 500–1000ms；自动捕获为异步执行，不影响主响应流 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
- **版本差异**：记忆抽取支持 `Pro`（开启 Rerank，¥0.03/次）与 `Lite`（关闭 Rerank，¥0.018/次）两种版本，不传时默认 `Pro` [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **插件约束**：OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
- **画像字段设计**：画像属性名称应语义唯一（避免同时使用“年龄”“年纪”“岁数”），且描述需清晰具体；单轮对话通常无法提取全部字段，建议通过多轮交互逐步完善 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


