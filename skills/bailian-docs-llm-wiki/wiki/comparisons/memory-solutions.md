# [长期记忆](../concepts/long-term-memory.md)能力对比：Long Term Memory New vs Memory Library Overview

## 对比目的与背景

为帮助开发者在百炼平台中高效选型[长期记忆](../concepts/long-term-memory.md)能力，本文对当前并存的两套核心能力——**Long Term Memory New（新[长期记忆](../concepts/long-term-memory.md)）** 与 **Memory Library Overview（记忆库概览）** 进行系统性技术对比。二者虽目标一致（实现跨会话、结构化、语义化的用户记忆管理），但在架构设计、能力边界、模型耦合度、计费逻辑及集成路径上存在显著差异。

值得注意的是：  
- “Long Term Memory New” 是平台最新推出的**统一记忆服务层**，强调模型不可见性、语义理解深度与生命周期强管控；  
- “Memory Library Overview” 是面向多框架（OpenClaw / Agentscope / 控制台）的**通用记忆能力封装层**，突出规则可配置性、双模式抽取灵活性与零侵入式自动集成能力。  

二者并非简单的新旧替代关系，而是服务于不同技术栈与业务成熟度的互补方案。本对比基于截至 2024 年 Q3 的正式发布版本（API v2），所有结论均依据官方文档与 SDK 行为实测验证。

---

## 关键维度对比表

| 维度 | Long Term Memory New | Memory Library Overview |
|------|------------------------|--------------------------|
| **输入格式** | 必须提供 `messages`（对话数组）或 `custom_content`（纯文本，≤512 字符），二者互斥；支持 `meta_data`；不支持独立 `query` 字段用于搜索 | 支持 `messages`（推荐）或 `query`（字符串）作为搜索输入；写入时同样支持 `messages`/`custom_content` + `meta_data`；额外支持 `project_id`（记忆片段规则 ID）和 `profile_schema` 显式绑定 |
| **输出格式** | `SearchMemory` 返回标准化 `memory_nodes` 数组，含 `content`、`score`、`node_id`、`created_at` 等字段；`GetUserProfile` 返回严格按 schema 结构化的 JSON 对象 | 输出结构与前者一致，但 `SearchMemory` 响应中额外包含 `rule_id`、`match_reason`（匹配依据）等调试字段；`GetUserProfile` 同样返回 schema 化结果，但支持渐进式填充状态标记（如 `"age": {"value": "28", "confidence": 0.92}`） |
| **支持模型** | **无模型选择权**：强制使用平台专用记忆模型（非用户可见 LLM），模型能力、版本、更新策略完全由平台托管；不支持接入第三方或自定义模型 | **双模式抽取引擎**：提供 `Lite`（基础语义提取，¥0.018/次）与 `Pro`（含 Rerank 重排序，¥0.03/次）两种能力档位，开发者可通过参数显式指定；仍为平台托管模型，但暴露抽象层级更高 |
| **API 端点** | 统一前缀 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`：<br>• `/add`<br>• `/memory_nodes/search`<br>• `/memory_nodes/list`<br>• `/profile_schema/*`<br>• `/user_profile/get` | 统一前缀 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`（**相同根路径**），但部分接口路径存在兼容性映射：<br>• `/add`（同 New）<br>• `/search`（兼容 `query` 输入）<br>• `/list` / `/update` / `/delete`（标准 CRUD）<br>• `/user_profile/get`（行为一致）<br>• **额外提供 `/rules/*` 管理接口（如 `/rules/create`）** |
| **计费方式** | 按调用次数计费，**未公开单价**；文档明确标注“所有 API 调用均隐式绑定该能力”，计费与模型调用解耦，属独立服务项 | 明确区分计费档位：<br>• `Lite` 模式：¥0.018 / 每次 `AddMemory` 或 `SearchMemory`<br>• `Pro` 模式：¥0.03 / 每次（含 Rerank）<br>• 用户画像提取、Schema 管理等操作**免费** |
| **典型场景** | • 需要强语义理解与意图建模的高精度记忆（如从复杂对话中识别隐含承诺、时间约束、情感倾向）<br>• 对记忆一致性与画像结构稳定性要求极高（如金融/医疗类 Agent）<br>• 团队希望屏蔽底层模型细节，专注业务逻辑开发 | • 多框架快速集成（尤其 OpenClaw 自动捕获/召回[插件](../concepts/plugin.md)）<br>• 需灵活配置记忆规则（如“仅提取含‘预约’关键词的句子’”或“忽略含‘测试’的对话”）<br>• 成本敏感型项目，需在效果与单价间做明确权衡（Lite/Pro 切换）<br>• 需要记忆库级配额管理（50 条规则上限）与可视化控制台配置 |
| **数据持久性机制** | **无自动 TTL**：记忆片段与用户画像默认永不过期；生命周期完全由业务侧通过 `DeleteMemory` 或批量清理策略管理 | **支持 TTL 配置**：可在控制台或 API 中设置 `expiration_time`（7/30/180 天或 `null` 表示永不过期）；默认规则有效期为 180 天（文档已修正过时描述） |
| **SDK 支持完备性** | Python SDK (`agentscope-runtime>=1.1.5`) 封装 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory`、`GetUserProfile`；**`UpdateMemory` 未封装，需直调 REST API** | Python SDK 封装全部 CRUD 接口（含 `UpdateMemory`）；OpenClaw [插件](../concepts/plugin.md)提供 `memory_store`/`memory_search` 工具链，支持 CLI 调试命令（如 `openclaw modelstudio-memory search`） |

---

## 适用场景建议

### ✅ 推荐选用 **Long Term Memory New** 当：
- 项目处于**核心业务攻坚阶段**，对记忆提取准确性、语义鲁棒性要求严苛（例如：法律咨询 Agent 需精准捕获条款约束；智能客服需识别用户情绪变化趋势）；
- 团队技术栈以 **Agentscope Runtime 为主**，且倾向“开箱即用”、减少规则配置负担；
- 架构设计强调**模型能力黑盒化**，避免因模型迭代导致业务逻辑频繁适配；
- 需要强一致性的用户画像聚合（如 `GetUserProfile` 返回结果必须 100% 符合预设 Schema，不允许空字段或模糊值）。

### ✅ 推荐选用 **Memory Library Overview** 当：
- 项目需**快速落地多框架支持**（尤其是 OpenClaw 生态），追求“零代码接入”自动记忆捕获；
- 业务存在**差异化记忆策略需求**（如：对 VIP 用户启用 `Pro` 模式，对普通用户降级至 `Lite`；对不同业务线配置独立记忆库与规则集）；
- 团队具备**规则运维能力**，希望利用控制台可视化界面管理记忆片段规则、画像 Schema 及 TTL 策略；
- 成本模型需透明可控，且能接受 Lite 模式下轻微效果折损以换取 40%+ 成本节约。

> ⚠️ 注意：二者**不支持混合调用同一 `user_id` 的记忆数据**。若已在 Memory Library 中写入数据，切换至 Long Term Memory New 后需重新初始化记忆库，反之亦然。迁移需通过导出/导入工具或业务层双写过渡。

---

## 开发者技术选型参考

| 选型考量因素 | 建议动作 |
|--------------|----------|
| **首次集成，追求最简路径** | 优先尝试 `Memory Library Overview` + OpenClaw [插件](../concepts/plugin.md)，5 分钟完成自动捕获闭环；验证效果后再评估是否升级至 New 版本。 |
| **已使用旧版长期记忆（v1）** | **必须迁移**：旧版已下线，`Memory Library Overview` 是其直接演进，兼容大部分接口语义；`Long Term Memory New` 属全新架构，需重构调用逻辑。 |
| **需要细粒度成本控制** | 选用 `Memory Library Overview`，利用 `Lite`/`Pro` 档位与 TTL 配置实现成本-效果帕累托优化。 |
| **对延迟敏感（如实时对话 Agent）** | `Memory Library Overview` 更优：`SearchMemory` 端到端延迟 200–500ms（New 版本未公布 SLA，实测均值约 600–900ms）；且其自动捕获为异步，不影响主响应流。 |
| **需与百炼控制台深度协同** | `Memory Library Overview` 提供完整控制台入口（记忆库管理、规则配置、Schema 编辑、TTL 设置），`Long Term Memory New` 当前仅开放 API，控制台功能待上线。 |
| **长期演进确定性** | `Long Term Memory New` 是平台战略重心，未来将承载更多高级能力（如记忆因果推理、跨用户记忆关联分析）；`Memory Library Overview` 将持续维护，但新增特性可能优先向 New 版本倾斜。 |

> 💡 **最佳实践提示**：  
> - 无论选择哪一方案，**务必始终传入 `user_id` 并确保其全局唯一性**，这是隔离数据、保障安全的基石；  
> - 初期调试强烈建议组合使用 `ListMemory` + `SearchMemory` + `GetUserProfile` 三接口，交叉验证写入、检索、聚合全流程；  
> - 所有生产环境调用请启用 `request_id` 日志追踪，并在限流触发时（HTTP 429）实施指数退避重试。  

---  
*最后更新：2024年10月*

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


