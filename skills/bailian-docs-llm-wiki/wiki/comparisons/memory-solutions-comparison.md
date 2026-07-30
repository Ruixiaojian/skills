# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory 与 Memory Library

本页旨在为开发者提供清晰、客观的技术选型参考，对比百炼平台当前两类主流[长期记忆](../concepts/long-term-memory.md)能力：**Long Term Memory（新）**（即 `long-term-memory-new`）与 **Memory Library**（即记忆库体系）。二者虽在概念上同属“[长期记忆](../concepts/long-term-memory.md)”范畴，但在架构定位、能力边界、集成方式及适用阶段上存在实质性差异。本文基于官方文档、API 行为规范及实际工程实践，从关键维度展开横向对比，帮助团队根据业务目标、技术栈成熟度与智能体演进阶段做出合理决策。

> ⚠️ 重要说明：  
> - “Memory Library” 并非独立于 Long Term Memory 的全新系统，而是其**面向产品化、规模化落地的统一能力封装与运营界面**，底层共享同一套存储、索引与模型服务；  
> - “Long Term Memory（新）” 是底层 API 层的正式命名，强调模型驱动、结构化抽取与细粒度控制；  
> - 二者**不构成互斥替代关系，而体现“能力原子化”与“场景工程化”的协同演进路径**。下表将明确其分工边界。

## 关键维度对比

| 维度 | Long Term Memory（新） | Memory Library |
|------|------------------------|----------------|
| **定位与角色** | 底层能力 API 套件，聚焦**高可控性、可编程性与模型能力暴露**；面向需要深度定制记忆提取逻辑、规则策略或与自研 Agent 框架深度集成的开发者。 | 上层工程化抽象，聚焦**开箱即用、[多模态](../concepts/multi-modal.md)接入、跨应用复用与低代码配置**；面向希望快速构建具备持续记忆能力的智能体、且重视交付效率与运维一致性的业务/产品团队。 |
| **输入格式** | 支持两种互斥模式：<br>• `messages`: 最多 50 条对话消息（role/content 结构），支持[多模态](../concepts/multi-modal.md) `content` 数组（但仅文本参与解析）；<br>• `custom_content`: 纯文本字符串（≤512 字符）。 | 兼容相同输入格式（`messages` / `custom_content`），并**额外支持 OpenClaw 插件的 `autoCapture` 自动捕获模式**——无需显式调用 API，由插件监听对话流自动触发记忆写入。 |
| **输出格式** | 返回结构化记忆片段（JSON 对象），含 `id`, `content`, `timestamp`, `meta_data`, `score`（检索时）等字段；支持 `profile_schema_id` 映射后生成带 schema 标签的画像属性。 | 输出格式完全一致；**额外提供 `GetUserProfile` 接口，返回完整、归一化的用户画像 JSON 对象**（如 `{ "age": 28, "occupation": "engineer", "preference": ["python", "open-source"] }`），屏蔽碎片化片段聚合逻辑。 |
| **支持模型与能力** | • 专用抽取模型（隐式调用，无需指定）<br>• 强语义理解：支持事件、提醒、偏好等意图识别<br>• 高级搜索开关：`enable_rerank` / `enable_judge` / `enable_rewrite`（需显式启用）<br>• 严格遵循 `profile_schema_id` 进行结构化约束 | • 底层模型完全相同<br>• **预置“默认项目”规则**（含 180 天过期策略模板，但实际存储无强制过期）<br>• 提供图形化控制台管理记忆库、规则、画像 Schema<br>• **OpenClaw 插件原生支持 `autoRecall`**：在 LLM 提示词中自动注入相关记忆，无需手动拼接上下文 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add`<br>`POST https://dashscope.aliyuncs.com/api/v2/apps/memory/search`<br>（统一 Base URL，路径区分操作） | **完全相同的 API 端点与协议**。<br>Memory Library 文档中引用的 `AddMemory` / `SearchMemory` 即指向上述 Long Term Memory（新）接口。二者为同一套后端服务。 |
| **计费方式** | 按调用量计费（QPM 限流 + 请求次数）：<br>• 所有接口合计 ≤3000 QPM（账号级）<br>• `AddMemory` ≤120 QPM<br>• `SearchMemory` ≤300 QPM<br>• 具体单价见 [百炼定价页](https://help.aliyun.com/zh/model-studio/pricing) | **计费模型完全一致**。Memory Library 的所有操作（包括 OpenClaw 插件触发的自动调用）均计入同一账号的 Long Term Memory 调用量配额。 |
| **典型场景** | • 构建需精细控制记忆生命周期的金融/医疗类 Agent（如：动态更新患者用药记录并校验时效性）<br>• 在自研 Agent 框架（如 LangChain、LlamaIndex）中嵌入定制化记忆模块<br>• 实验性验证不同抽取规则对业务指标的影响<br>• 需要 `UpdateMemory` 或 `DeleteMemory` 频繁操作的强状态管理场景 | • 快速上线客服/导购类智能体，要求“开箱即用”记忆能力<br>• 多个 Agent 应用（如销售助手、售后机器人）共享同一用户记忆库<br>• 使用 OpenClaw 框架，追求零侵入式记忆增强（`autoCapture` + `autoRecall`）<br>• 需要通过控制台统一管理记忆规则、画像 Schema 及审计日志 |

## 各方案的适用场景建议

### ✅ 推荐选择 **Long Term Memory（新）** 当：
- 你正在开发高度定制化的 Agent，需要直接控制记忆提取的触发时机、输入内容粒度（如仅传入特定轮次对话）或后处理逻辑；
- 你需要利用 `enable_rerank`、`enable_judge` 等高级搜索能力进行精准召回，并愿意在请求中显式配置开关；
- 你的技术栈已集成 `agentscope-runtime` 或其他 SDK，且能接受部分操作（如 `UpdateMemory`）需直调 HTTP API；
- 你处于 POC 或算法验证阶段，需频繁调整 `profile_schema_id` 或测试不同 `min_score` 阈值对召回质量的影响；
- 你对数据主权要求极高，需确保所有记忆操作均有明确 trace（`request_id`）且符合内部安全审计规范。

### ✅ 推荐选择 **Memory Library** 当：
- 你使用 OpenClaw 作为核心框架，希望以声明式配置（`autoCapture: true`）实现记忆能力“零代码接入”；
- 你需要在一个控制台内统一管理多个应用的记忆库、画像 Schema 和规则策略，降低跨团队协作成本；
- 你的业务场景强调“用户一致性”，例如同一用户在售前、售中、售后多个 Bot 中的行为记忆需全局共享；
- 你更关注最终效果而非实现细节，例如直接调用 `GetUserProfile` 获取结构化画像，而非自行聚合多个记忆片段；
- 你处于 MVP 快速迭代期，优先保障功能交付，后续再逐步下沉至 Long Term Memory（新）进行精细化优化。

## 面向开发者的选型参考

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| **“我只想让我的 Bot 记住用户说过的话，并在下次聊天时自动想起来”** | ✅ Memory Library + OpenClaw 插件 | `autoRecall` 自动注入上下文，无需修改提示词工程；`autoCapture` 免去手动调用 `AddMemory` 的负担。 |
| **“我需要把用户说的‘下周三下午三点开会’解析成结构化待办，并关联到日历系统”** | ✅ Long Term Memory（新） | 可通过 `profile_schema_id` 定义 `meeting_time: datetime` 字段，确保抽取结果可被下游系统直接消费；`custom_content` 模式也支持直接注入结构化文本。 |
| **“我的 Agent 框架是自研的，不兼容 OpenClaw，但需要稳定可靠的长期记忆”** | ✅ Long Term Memory（新） | 提供标准 REST API 与 Python SDK 封装（`AddMemory`, `SearchMemory`），可无缝集成至任意框架；`user_id` 隔离机制保障多租户安全。 |
| **“我们有 5 个不同的智能体应用，希望它们共享同一套用户偏好记忆”** | ✅ Memory Library | 通过指定相同 `memory_library_id`（或共用默认库）+ 不同 `user_id`，天然支持跨应用共享；控制台可集中查看所有应用的调用统计与错误日志。 |
| **“我需要定期清理 6 个月前的会议记录，但保留用户的长期偏好”** | ⚠️ 两者均需业务侧实现 | 二者均**不提供自动过期删除能力**。Long Term Memory（新）需定时调用 `ListMemory` + `DeleteMemory`；Memory Library 可借助控制台“批量删除”功能或通过 OpenClaw 插件扩展钩子函数实现。 |

> 💡 **终极建议**：  
> **不要将二者视为二选一，而应视作同一能力栈的“底层 API”与“上层平台”**。  
> - 初期推荐从 **Memory Library + OpenClaw** 入手，快速验证业务价值；  
> - 当遇到性能瓶颈、定制需求或需要深度可观测性时，平滑切换至 **Long Term Memory（新）** 的细粒度 API；  
> - 所有 `memory_library_id`、`profile_schema_id`、`user_id` 等标识符在两套方案中完全通用，迁移成本极低。  

如需进一步了解具体接口调用示例、错误码详解或配额扩容流程，请参阅对应 API 参考文档。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


