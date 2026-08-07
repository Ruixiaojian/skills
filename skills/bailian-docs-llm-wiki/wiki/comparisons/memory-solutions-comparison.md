# [长期记忆](../concepts/long-term-memory.md)与记忆库方案对比

为帮助开发者在百炼平台中准确选型，本文对当前两类主流[长期记忆](../concepts/long-term-memory.md)能力——**[长期记忆](../concepts/long-term-memory.md)（新）**（`long-term-memory-new`）与**记忆库**（`memory-library`）——进行系统性对比分析。二者虽均面向“跨会话用户状态持久化”这一核心目标，但在架构设计、能力边界、使用范式及运维模型上存在显著差异。本对比基于最新公开文档（2024年Q3），聚焦实际工程落地中的关键决策维度，旨在为智能体（Agent）、对话系统、个性化服务等场景提供清晰的技术选型依据。

## 关键维度对比

| 维度 | 长期记忆（新） | 记忆库 |
|------|----------------|---------|
| **定位与设计目标** | 一体化、开箱即用的结构化记忆管理服务，强调“零模型调用负担”与端到端语义理解闭环 | 灵活可插拔的记忆基础设施组件，强调多框架兼容性（尤其 OpenClaw）、规则可配置性与版本演进能力 |
| **输入格式** | `messages`（最多50条对话消息，含 role/content）或 `custom_content`（≤512 字符纯文本）；二者互斥必填 | 同样支持 `messages` 或 `custom_content`；但 `messages` 无明确条数硬限制（依赖后端处理能力），`custom_content` 长度未明文约束（实践中建议 ≤2KB） |
| **输出格式** | 返回结构化 `memory_nodes` 数组，每个节点含 `id`、`content`、`extracted_fields`（按 schema 提取的键值对）、`meta_data`、`created_at` 等标准化字段；所有字段语义统一、机器可解析 | 输出格式一致（`memory_nodes`），但 `extracted_fields` 结构更依赖所选 `project_id`（记忆片段规则）或 `profile_schema`（画像模板）；字段命名与类型由业务定义，灵活性更高 |
| **支持模型** | **不暴露模型 ID**：由平台统一托管专用记忆模型，开发者无需指定、切换或感知底层模型；所有提取、向量化、检索均由服务端完成 | 支持 **`Pro` 与 `Lite` 两种抽取版本**：<br>• `Pro`：启用 Rerank，精度高，¥0.03/次<br>• `Lite`：基础语义匹配，成本低，¥0.018/次<br>（通过 `version` 参数控制，默认 `Pro`） |
| **API 端点** | 统一前缀 `https://dashscope.aliyuncs.com/api/v2/apps/memory/{path}`<br>• `/add` / `/search` / `/list` / `/delete` / `/update`（RESTful） | 统一前缀 `https://dashscope.aliyuncs.com/api/v1/memory/{path}`<br>• `/add` / `/search` / `/list` / `/update` / `/delete`（RESTful）<br>• 额外支持 `/rules`（管理片段规则）、`/schemas`（管理画像模板）等元数据接口 |
| **计费方式** | 按 **调用次数计费**：<br>• `AddMemory`：¥0.02/次<br>• `SearchMemory`：¥0.015/次<br>• `ListMemory`/`DeleteMemory`/`UpdateMemory`：免费<br>（注：`ProfileSchema` 系列接口免费） | 按 **调用次数 + 版本因子计费**：<br>• `AddMemory`：¥0.02/次（与版本无关）<br>• `SearchMemory`：¥0.03/次（`Pro`） 或 ¥0.018/次（`Lite`）<br>• 其他管理类接口免费 |
| **记忆生命周期管理** | **无自动过期机制**：所有记忆片段与画像永久存储，需业务侧主动调用 `DeleteMemory` 清理 | **支持配置过期策略**：可在控制台或 API 中为记忆片段规则（`project_id`）设置有效期（7/30/180 天或永不过期），默认 180 天；过期后自动归档不可检索 |
| **用户画像能力** | 通过 `ProfileSchema` 接口显式管理模板，并在 `AddMemory` 时通过 `profile_schema` 参数触发结构化抽取；字段强约束，适合严格 Schema 场景 | 同样支持 `CreateProfileSchema`，但更强调与 `project_id` 规则解耦；同一 `user_id` 可同时关联多个画像模板，支持多维画像建模 |
| **SDK 封装完备性** | Python SDK (`agentscope-runtime>=1.1.5`) 覆盖 `Add`/`Search`/`List`/`Delete`；`UpdateMemory` **暂未封装**，需手动 HTTP PATCH | Python SDK（`dashscope` 官方包）及 OpenClaw 插件均完整封装全部 CRUD 接口；`UpdateMemory` 可直接调用 |
| **框架集成深度** | 原生适配 Agentscope 运行时，提供 `AddMemory` 等工具类；**无官方 OpenClaw 插件支持** | **深度集成 OpenClaw**：提供 `autoCapture`（自动写入）、`autoRecall`（自动注入）插件钩子，支持全局记忆共享；也兼容 Agentscope |
| **典型场景** | • 快速上线轻量级对话记忆（如客服机器人记录用户诉求）<br>• 对模型透明性要求高、拒绝自行管理向量/摘要的团队<br>• 需要强一致性 Schema 管理的用户画像系统 | • 需要精细化控制记忆时效性（如金融风控临时偏好）<br>• 多 Agent 共享记忆且需统一插件管理（OpenClaw 架构）<br>• 需要 A/B 测试不同抽取策略（`Pro` vs `Lite`）<br>• 已有复杂画像体系，需灵活扩展字段 |

## 适用场景建议

- **选择「长期记忆（新）」当**：
  - 团队希望 **最小化技术栈复杂度**，避免模型选型、向量库维护、Rerank 配置等运维负担；
  - 业务对 **Schema 一致性要求极高**（如医疗问诊必须提取“过敏史”“用药史”等固定字段），且能接受统一模板管理；
  - 主要使用 **Agentscope 框架**，且无需 OpenClaw 生态支持；
  - 成本敏感度中等，优先保障开发效率与交付速度。

- **选择「记忆库」当**：
  - 应用已基于 **OpenClaw 构建**，需利用其 `autoCapture`/`autoRecall` 实现零侵入记忆闭环；
  - 业务存在 **明确的时效性需求**（如活动期间临时偏好、短期订单上下文），需依赖平台级过期策略；
  - 需要 **灵活的成本调控能力**（例如非核心场景降级至 `Lite` 版本）；
  - 用户画像维度丰富、动态演进（如电商场景需同时维护“购物偏好”“售后倾向”“内容兴趣”多套 Schema），需解耦管理；
  - 已有成熟向量检索经验，希望保留对底层能力（如 Rerank 开关、相似度阈值粒度）的精细控制。

## 技术选型参考（面向开发者）

| 决策问题 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我只想让对话机器人记住用户说过的关键信息，不想碰模型和向量” | ✅ 长期记忆（新） | 全托管语义理解，`messages` 输入即得结构化结果，无额外配置成本 |
| “我的系统用 OpenClaw，且所有 Agent 必须共享同一份用户记忆” | ✅ 记忆库 | 唯一提供 OpenClaw 官方插件支持，`autoRecall` 可自动注入上下文，避免重复编码 |
| “我需要给用户画像设置 30 天自动过期，防止信息陈旧” | ✅ 记忆库 | `project_id` 规则支持配置 `expiration_time`，长期记忆（新）无此能力 |
| “我正在做 A/B 测试，想对比高精度检索（Pro）和低成本检索（Lite）的效果” | ✅ 记忆库 | `version` 参数可动态切换，长期记忆（新）无版本概念 |
| “我用 Agentscope，且只需要基础 CRUD，不关心 OpenClaw” | ⚖️ 两者均可，推荐长期记忆（新） | SDK 封装更轻量，API 设计更简洁，错误码与文档一致性更高 |
| “我需要更新记忆的某个字段（如修正用户电话），且不希望覆盖其他元数据” | ⚖️ 两者均可，但注意细节：<br>• 长期记忆（新）：`UpdateMemory` 为**增量更新**（已有字段保留）<br>• 记忆库：`UpdateMemory` 默认为**全量替换**（需传入完整 `meta_data`） | 务必查阅对应 API 文档的 `PATCH` 行为说明，避免数据丢失 |

> **重要提醒**：  
> - 两个方案**不互斥**，可共存于同一应用（例如：用「长期记忆（新）」管理用户基础档案，用「记忆库」管理会话级临时偏好）；  
> - 所有生产环境部署前，请务必验证 **限流策略**（账号级 QPM 总配额 3000）是否满足峰值需求；  
> - `user_id` 是隔离核心，确保其全局唯一性与稳定性（建议使用业务主键而非临时 token）；  
> - 无论选择哪种方案，**`meta_data` 字段均为分类与审计关键**，建议约定命名规范（如 `{"source": "app_x", "version": "v2"}`）。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


