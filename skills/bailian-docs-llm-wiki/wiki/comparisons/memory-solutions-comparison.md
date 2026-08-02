# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory vs Memory Library

为帮助开发者在百炼平台中合理选型[长期记忆](../concepts/long-term-memory.md)能力，本文对当前两类核心方案——**Long Term Memory（[长期记忆](../concepts/long-term-memory.md)，新）** 与 **Memory Library（记忆库）** 进行系统性对比分析。二者虽同属平台级长期记忆基础设施，但在设计定位、功能边界、集成方式及适用阶段上存在显著差异。本对比聚焦实际工程落地场景，旨在厘清技术选型的关键决策依据，避免因概念混淆导致架构冗余或能力缺失。

## 关键维度对比

| 维度 | Long Term Memory（新） | Memory Library（记忆库） |
|------|------------------------|---------------------------|
| **定位与目标** | 面向 Agent 构建的轻量级、低延迟结构化记忆管理服务，强调语义召回精度与实时交互体验 | 百炼平台统一的长期记忆底座，支持跨应用、跨框架（如 OpenClaw）的共享记忆能力，强调规则可配置性与生命周期治理 |
| **输入格式** | `messages`（最多50条对话消息，含 role/content）或 `custom_content`（≤512 字符纯文本），二者互斥必填 | 同样支持 `messages` 或 `custom_content`；额外支持 `project_id`（指定记忆片段规则）、`profile_schema_id`（指定画像模板）、`meta_data`（结构化元数据）等精细化控制字段 |
| **输出格式** | `SearchMemory` 返回 `memory_nodes` 数组，每项含 `content`、`score`、`source`、`created_at` 等字段；`GetUserProfile` 返回结构化 JSON 对象 | 输出结构一致，但 `SearchMemory` 在插件场景下默认注入上下文（如 OpenClaw 的 `autoRecall`），且支持按 `meta_data` 过滤后返回增强结果 |
| **支持模型/能力** | ✅ 基础 CRUD（Add/Search/List/Delete/Update）<br>✅ 用户画像（需显式调用 `CreateProfileSchema` + `GetUserProfile`）<br>✅ 多规则联合检索（`project_ids` 数组）<br>✅ 语义增强（rerank/judge/rewrite 可选开关） | ✅ 全套 CRUD 操作<br>✅ 用户画像（同上，但文档明确支持多轮渐进提取）<br>✅ **内置记忆过期策略**（7/30/180天或永不过期，可配置）<br>✅ **开箱即用的 Agent 插件**（如 `modelstudio-memory-for-openclaw`，含 `autoCapture`/`autoRecall`） |
| **API 端点** | `POST /api/v2/apps/memory/add`<br>`POST /api/v2/apps/memory/memory_nodes/search`<br>`GET /api/v2/apps/memory/profiles/{user_id}`（需 profile_schema_id） | 端点路径相同（兼容旧版 API），但 `memory_library_id` 和 `project_id` 为关键路由/参数扩展点；插件调用封装了底层 HTTP 请求 |
| **计费方式** | 按调用量计费（QPM 限流体现为账号级配额），无独立记忆存储费用；当前未区分“记忆片段”与“用户画像”计费粒度 | 同样基于 API 调用次数计费；**记忆存储本身不额外收费**，但高频率 `AddMemory`/`SearchMemory` 将消耗配额；默认库与自建库计费规则一致 |
| **典型场景** | • 实时对话 Agent 中的即时记忆写入与秒级语义检索<br>• 需要动态混合多个记忆规则（如“待办+偏好+设备信息”联合召回）<br>• 对 `min_score`/`top_k` 等参数强定制、需精细控制召回质量 | • 多会话、长周期用户状态维护（如客服机器人跨周服务）<br>• 需自动过期清理的临时记忆（如活动优惠券有效期）<br>• 使用 OpenClaw 等框架并希望零配置启用记忆能力<br>• 多应用共享同一记忆库实现用户画像统一 |
| **数据持久性与生命周期** | **无自动过期机制**；所有记忆片段与画像永久保留，需开发者主动调用 `DeleteMemory` 清理 | **支持可配置的自动过期**（7/30/180天或永不过期），由 `project_id` 关联的记忆片段规则决定；默认规则为 180 天 |
| **SDK 与工具链支持** | `agentscope-runtime>=1.1.5` 提供 `AddMemory`/`SearchMemory` 封装；`UpdateMemory` SDK 已支持（文档曾滞后，以实际版本为准） | 官方提供 `modelstudio-memory-for-openclaw` 插件（含自动捕获/召回钩子）；Python SDK 接口与 Long Term Memory 新版一致，但插件层抽象更厚 |

## 各方案适用场景建议

### ✅ 推荐选用 **Long Term Memory（新）** 当：
- 构建低延迟敏感型 Agent（如实时语音助手、游戏 NPC），要求 `SearchMemory` 平均响应 ≤300ms；
- 需要在单次请求中**跨多个业务规则联合检索**（例如同时查询用户“日程习惯”和“设备绑定状态”）；
- 已有成熟 Agent 框架，仅需轻量级记忆增删查能力，**无需自动过期或跨框架插件**；
- 强依赖语义重排序（rerank）、意图判别（judge）等高级召回优化能力。

### ✅ 推荐选用 **Memory Library（记忆库）** 当：
- 开发面向真实用户的长期服务型应用（如个人助理、企业客服），需**自动清理过期记忆**降低噪声；
- 使用 **OpenClaw、LangChain 等主流框架**，期望通过插件一键启用记忆能力，减少胶水代码；
- 多个业务线/应用需**共享同一套用户画像与记忆规则**（如电商 App 与小程序共用会员偏好）；
- 需要通过 `meta_data` 实现细粒度分类（如按 `{"channel": "wechat", "region": "shanghai"}` 过滤检索）；
- 团队缺乏记忆生命周期运维经验，需平台级规则托管（如设置“优惠信息 7 天过期”）。

### ⚠️ 不推荐混用或迁移的场景：
- **勿将 Memory Library 的过期规则能力嫁接到 Long Term Memory 新版**：后者无对应配置入口，强行模拟需自行维护定时任务，违背设计初衷；
- **勿在 OpenClaw 中弃用 memory-library 插件而改用手动调用 Long Term Memory API**：将丢失 `autoRecall` 上下文注入、异步 `autoCapture` 等关键体验保障；
- **新项目启动时，避免默认选择“长期记忆（新）”而忽略记忆库的规则治理能力**：尤其当业务涉及用户隐私合规（如 GDPR 数据自动清除）时，Memory Library 的过期策略是刚需。

## 技术选型参考指南（面向开发者）

1. **先确认架构层级**  
   - 若处于 **Agent 编排层**（如使用 Agentscope Runtime 自定义流程），优先评估 `Long Term Memory（新）` 的 SDK 集成便捷性；  
   - 若处于 **应用集成层**（对接 OpenClaw/LangChain/自有框架），直接采用 `Memory Library` 插件方案，省去重复造轮子。

2. **检查核心需求清单**  
   ```markdown
   - [ ] 是否需要自动过期？ → 必选 Memory Library  
   - [ ] 是否使用 OpenClaw？ → 必选 Memory Library（官方插件深度适配）  
   - [ ] 是否要求单次搜索融合 ≥2 类业务规则？ → Long Term Memory（新）更灵活  
   - [ ] 是否已部署大量自定义元数据过滤逻辑？ → Memory Library 的 `meta_data` 支持更完善  
   - [ ] 是否对 P99 延迟要求 <400ms？ → Long Term Memory（新）实测更优  
   ```

3. **生产环境注意事项**  
   - 两者共享同一套 **账号级 QPM 限流**（Add ≤120, Search ≤300），需统一规划配额；  
   - `user_id` 是隔离边界，**务必确保其全局唯一且稳定**（推荐使用业务侧 UID 而非会话 ID）；  
   - 默认记忆库不可删除，新业务应创建独立 `memory_library_id` 实现规则与权限隔离；  
   - 用户画像字段命名需严格唯一（如避免“age”与“user_age”并存），否则影响抽取准确率。

> **总结一句话选型原则**：  
> **追求极致性能与规则灵活性 → Long Term Memory（新）；  
> 追求开箱即用、生命周期自治与生态集成 → Memory Library。**  
> 二者并非替代关系，而是百炼平台针对不同抽象层级提供的互补能力——前者是“内存操作原语”，后者是“记忆操作系统”。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


