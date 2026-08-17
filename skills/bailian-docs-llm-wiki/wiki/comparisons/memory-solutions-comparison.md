# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory 与 Memory Library

> **对比目的与背景**  
> 为帮助开发者清晰理解百炼平台当前提供的两类[长期记忆](../concepts/long-term-memory.md)能力——`Long Term Memory（新）`（文档标识为 `long-term-memory-new`）与 `Memory Library`（文档标识为 `memory-library-overview`）——本文从技术实现、接口设计、能力边界和商业化策略等维度进行系统性对比。需特别说明：**二者并非互斥的“两个产品”，而是同一底层能力在不同演进阶段的对外呈现形式**。`Memory Library` 是当前官方主推的统一抽象层，而 `Long Term Memory（新）` 是其早期命名及部分 SDK 封装的遗留表述。本次对比旨在消除命名混淆，明确技术选型依据，避免因文档版本差异导致集成偏差。

---

## 关键维度对比表

| 维度 | Long Term Memory（新） | Memory Library |
|------|------------------------|----------------|
| **定位与演进关系** | 早期 API 封装形态，强调“自动提取+语义搜索”基础能力；部分文档/SDK 中仍沿用此名称 | 当前统一能力品牌，是平台级[长期记忆](../concepts/long-term-memory.md)能力的正式命名与功能集合，覆盖记忆片段、用户画像、规则管理、插件集成等全链路 |
| **输入格式** | 支持 `messages`（最多 50 条对话消息，一问一答计为 2 条）或 `custom_content`（≤512 字符纯文本），二者互斥；`custom_content` 优先级更高 | 同上，完全兼容；额外支持 `meta_data`（任意 JSON 对象）用于分类标注（如 `"category": "health_reminder"`），支持后续条件过滤检索 |
| **输出格式** | `SearchMemory` 返回结构化 `memory_nodes` 数组，含 `id`, `content`, `score`, `timestamp`, `meta_data` 等字段；无原生分页元信息（需依赖 `ListMemory` 分页） | 输出结构一致；`SearchMemory` 响应中显式包含 `pagination` 字段（含 `total`, `page`, `page_size`），语义更清晰；`GetUserProfile` 返回完整结构化画像对象（含字段值、置信度、填充轮次等） |
| **支持模型** | 不直接绑定特定大模型；所有能力由百炼平台后端统一处理（底层调用自研记忆理解与重排模型） | 同上；但明确支持与 OpenClaw 等框架深度集成，可通过插件实现“对话结束自动写入 + 对话开始前自动检索注入”，无需业务代码手动调用 |
| **API 端点（Base URL）** | `https://dashscope.aliyuncs.com/api/v2/apps/memory/` | 完全相同，使用同一 Base URL；所有接口路径（如 `/add`, `/memory_nodes/search`）一致 |
| **核心接口能力** | 提供 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`, `UpdateMemory`, `CreateProfileSchema`, `GetUserProfile` 等 | 接口集完全一致；额外强调 `project_id` 参数（记忆片段规则 ID），支持多规则并存（如“健康提醒规则”、“电商偏好规则”），实现场景化隔离与策略定制 |
| **用户画像管理** | 支持 `CreateProfileSchema` 等模板操作，但文档未明确说明是否支持动态创建后立即用于 `AddMemory`；`profile_schema` 参数为可选，且未说明默认行为 | 明确支持“模板即用”：创建并发布 `ProfileSchema` 后，可在 `AddMemory` 中直接传入 `profile_schema` ID 触发抽取；支持渐进式填充（单轮未填全字段，后续对话持续补全） |
| **策略版本控制（pro / lite）** | `SearchMemory` 支持 `plan_version` 参数（`pro`/`lite`），**优先级高于 `enable_rerank`**；`AddMemory` 无显式策略参数，策略由关联的 `memory_library_id` 或默认库隐式决定 | `plan_version` 同样支持且语义一致；关键增强：`SearchMemory` 的 `plan_version` **与 `project_id` 所属规则的策略完全解耦**——即使项目配置为 `lite`，请求中传 `plan_version: "pro"` 仍按 Pro 计费并启用 Rerank，提供更灵活的按次质量调控能力 |
| **计费方式** | 自 2026 年 8 月 20 日起正式计费；按 `pro`/`lite` 版本区分单价；`Add` 与 `Search` 独立计费 | 计费模型完全一致；官方文档明确将 `Memory Library` 定义为计费主体，`Long Term Memory（新）` 的调用即计入 `Memory Library` 账单 |
| **数据生命周期管理** | 文档声明“暂无自动失效机制”，需业务侧自行管理；未提供 `expired_in_days` 等过期参数 | 支持在创建记忆片段规则（`project_id`）时显式配置 `expired_in_days`（如 30/90/180 天），到期自动归档；若未设置，则永不过期（与实际运行行为一致，消除了早期文档矛盾） |
| **典型场景** | 快速接入基础记忆能力的 MVP 应用；对画像结构要求简单、规则复用需求低的轻量级智能体 | 多场景共存的生产级应用（如客服+健康助手+电商导购共用一个记忆库）；需精细化规则治理、画像渐进填充、自动捕获/注入、跨应用共享记忆的中大型项目 |

---

## 适用场景建议

| 场景特征 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **快速验证概念（PoC）、单功能智能体（如会议纪要助手）** | ✅ Long Term Memory（新） | SDK 封装成熟（`agentscope-runtime>=1.1.5`），示例代码丰富，5 分钟即可完成 `Add` + `Search` 基础闭环，适合技术预研与原型开发 |
| **需多规则隔离、多画像模板并行、跨会话强一致性保障的生产系统** | ✅ Memory Library | 支持 `project_id` 规则粒度管控、`meta_data` 标签过滤、显式过期策略、OpenClaw 插件自动注入，大幅降低运维复杂度，符合企业级 SLA 要求 |
| **已有 `agentscope-runtime` 集成，但需升级至最新能力（如自动过期、渐进画像）** | ⚠️ 迁移至 Memory Library | 接口完全兼容，仅需升级 SDK 至最新版（`agentscope-runtime>=1.2.0`），并在调用中增加 `project_id` 和 `meta_data` 参数，即可启用全部增强特性 |
| **需与 OpenClaw 框架深度集成，实现“零代码”记忆管理** | ✅ Memory Library | 唯一支持官方 `modelstudio-memory` 插件的方案，自动完成写入/检索/上下文注入全流程，彻底解放业务逻辑 |

---

## 技术选型参考（面向开发者）

- **不要选择 “Long Term Memory（新）” 作为独立技术栈**：它不是独立产品，而是 `Memory Library` 的历史别名与早期 SDK 封装。所有新项目应直接基于 `Memory Library` 文档与 API 开发。
- **优先使用 `project_id` 而非 `memory_library_id`**：`project_id`（记忆片段规则）是能力组织的核心单元，支持独立配置提取策略、过期时间、Rerank 开关；`memory_library_id` 仅用于库级隔离（如多租户），日常开发中通常使用默认库，无需显式传参。
- **必填 `user_id`，慎用全局共享**：`user_id` 是记忆空间的硬隔离边界，务必确保其唯一性与稳定性（推荐使用业务侧用户 UID）。切勿在不同用户间复用同一 `user_id`，否则导致记忆污染。
- **善用 `meta_data` 提升检索精度**：在 `AddMemory` 时添加 `"source": "chat_app_v2"`, `"priority": "high"` 等标签，后续 `SearchMemory` 可结合 `filter` 参数（如 `{"priority": "high"}`）精准召回，避免语义漂移。
- **生产环境必须设置 `plan_version`**：不传 `plan_version` 时行为未定义（可能降级为 `lite` 或报错）。明确指定 `pro`（高精度）或 `lite`（低成本）以保障预期效果与预算可控。
- **画像字段设计遵循“最小完备”原则**：每个 `ProfileSchema` 字段应有明确业务用途，避免冗余；利用 `description` 字段提供抽取提示（如 `"职业：请提取用户明确提及的职业名称，如'医生''教师'，勿猜测"`），提升抽取准确率。

> **最后提醒**：两套文档描述的是同一套服务。当遇到接口行为差异时，请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)（`Memory Library` 主文档）为准。`Long Term Memory（新）` 相关文档将逐步归档，其 SDK 封装已平滑迁移至 `Memory Library` 兼容层。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


