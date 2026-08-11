# 应用全生命周期能力对比：Application Call vs Managed Agents API vs Application Publishing and Sharing

本文旨在帮助开发者清晰理解百炼平台三大核心能力在**应用全生命周期支持维度上的定位差异与协同关系**。随着智能体应用从开发、调试、集成到规模化交付的演进，不同阶段对灵活性、可控性、工程化程度和终端交付形态提出差异化要求。`Application Call` 侧重**已发布应用的标准化调用**，`Managed Agents API` 聚焦**智能体运行时的细粒度管控与动态编排**，而 `Application Publishing and Sharing` 则面向**面向终端用户的多渠道交付与业务集成**。三者并非互斥替代，而是覆盖“调用—托管—分发”闭环的关键环节。本对比将从技术实现、适用边界与选型建议出发，为架构设计与技术决策提供依据。

## 关键能力维度对比

| 维度 | Application Call | Managed Agents API | Application Publishing and Sharing |
|------|------------------|---------------------|-------------------------------------|
| **核心定位** | 已发布应用（Agent/Workflow）的**生产级同步/异步调用接口** | 智能体（Agent）的**全生命周期托管运行时服务**（含沙箱、会话、事件、技能等资源建模） | 已发布应用（仅限 Agent 1.0 + Workflow）的**多渠道终端交付与复用封装能力**（UI/钉钉/微信/组件/音视频） |
| **输入格式** | - 纯文本字符串<br>- 多轮消息数组（`messages`），支持 `text`/`image_url`/`file_id`<br>- `biz_params` 传递自定义参数 | - 事件驱动：`POST /sessions/{id}/events`，`input` 为 role-content 结构数组<br>- 支持 `text`/`image_url`/`file_id`<br>- 文件需预先上传并获取 `file_id` | - UI：可视化表单映射至 `query`/`imageList` 等预设参数<br>- 钉钉/微信：通过平台回调注入用户消息（文本/图片）<br>- 组件：上游节点显式传参（JSON 对象）<br>- 音视频：H5/SDK 触发语音/文本输入 |
| **输出格式** | - 同步：完整响应（含 `output.text`/`output.files`）或流式 chunk<br>- 异步：任务 ID（`task_id`），后续轮询获取结果<br>- 无原生 SSE 流 | - 同步事件响应（确认接收）<br>- **原生 SSE 流式事件流**（`GET /sessions/{id}/events/stream`），含 `session_status`、`tool_calls`、`message`、`error` 等细粒度事件 | - UI：渲染后的 HTML 页面（含交互逻辑）<br>- 钉钉/微信：卡片消息（Markdown/富文本/按钮）<br>- 组件：返回结构化 JSON 输出（由下游节点解析）<br>- 音视频：实时语音转文本+AI 回复+合成语音流（H5/SDK 封装） |
| **支持模型** | - 通义千问全系列（Qwen-VL、Qwen-Max、Qwen-Plus 等）<br>- 支持工作流中配置的任意模型（含自定义模型） | - **仅百炼托管 Qwen 系列模型**（如 `qwen-plus`）<br>- 模型 ID 必须通过 `model.id` 显式指定，**不支持自定义模型部署** | - 依赖底层应用所用模型<br>- **仅 Agent 1.0 和 Workflow 应用支持发布**；Agent 2.0 **完全不可发布**（UI/钉钉/微信/组件/音视频均不支持） |
| **API 端点** | - DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>- OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | - RESTful 资源端点：<br> `POST /agents` / `POST /environments` / `POST /sessions` / `POST /sessions/{id}/events`<br>- Endpoint 格式：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio` | - **无标准 REST API**，全部通过百炼控制台操作或 SDK 封装调用<br>- UI/钉钉/微信等渠道依赖三方平台回调机制<br>- 组件调用通过工作流节点或智能体技能方式触发（内部 RPC） |
| **会话管理** | - DashScope API：`session_id`（1 小时有效期）<br>- Responses API：**必须每次传递完整消息历史**（无服务端状态维护） | - **Session 资源显式生命周期管理**（`idle` → `running` → `terminated`）<br>- 会话绑定 Agent 版本快照与 Environment，状态可查询、可中断 | - UI：会话由前端页面维持，后端无状态<br>- 钉钉/微信：平台会话 ID 透传，百炼侧按需重建上下文<br>- 组件：无独立会话概念，调用即执行，结果即时返回 |
| **计费方式** | - 按**调用次数 + 模型 token 消耗**计费<br>- 同步/异步调用统一计费模型<br>- 费用归属：调用方 API Key 所属账号 | - 按**Session 运行时长 + 模型 token 消耗**计费<br>- 文件存储（≤100 GB）、Skill 扫描、Environment 依赖安装等附加资源单独计费 | - **所有渠道产生的模型调用费用均由应用创建者 UID 账号承担**<br>- UI 生产环境需订阅团队版及以上套餐<br>- 钉钉/微信/音视频无额外通道费，但模型调用费照常收取 |
| **地域限制** | - **仅华北2（北京）地域可用**<br>- 子业务空间或特定地域（德/新/日）需额外 `workspace_id` | - **仅华北2（北京）地域可用**<br>- Endpoint 中 `region` 固定为 `cn-beijing` | - 发布功能本身无地域限制<br>- 但所依赖的底层应用（Agent/Workflow）必须已发布且位于支持地域（通常同属北京） |
| **典型场景** | - 客服系统对接（Web/App 后端调用）<br>- 自动化报告生成（异步批量处理）<br>- [多模态](../concepts/multi-modal.md)内容分析（图文混合输入）<br>- OpenAI 生态迁移项目 | - 需要工具调用链路可观测的智能体（如代码生成+执行+验证）<br>- 动态沙箱环境需求（如安装 pandas 处理 Excel）<br>- 实时事件追踪与干预（如人工接管、步骤回滚）<br>- 多版本 Agent A/B 测试 | - 内部员工自助服务门户（UI 应用）<br>- 客户服务入口（钉钉机器人/微信公众号）<br>- 复用能力沉淀（将通用问答封装为组件供多个工作流调用）<br>- 实时音视频客服（H5 扫码快速接入） |

## 适用场景建议

### ✅ 推荐使用 `Application Call`
- 你的应用已完成开发并**正式发布**，需要稳定、高性能地被业务系统调用；
- 场景以**实时交互（聊天）或批处理（报告生成）为主**，无需深度干预执行过程；
- 已有 OpenAI 兼容 SDK 或希望最小化改造成本；
- 输入输出格式简单明确，**不需要细粒度事件监听或沙箱环境控制**；
- [多模态](../concepts/multi-modal.md)（图像/文件）是刚需，且需兼容多种模型。

### ✅ 推荐使用 `Managed Agents API`
- 你需要**完全掌控智能体运行时行为**：监控每一步工具调用、捕获中间错误、动态中断或注入指令；
- 应用逻辑复杂，**依赖外部工具（如数据库查询、代码执行）且需隔离运行环境**（Cloud Environment）；
- 需要**长期会话状态管理**（如多步骤表单填写、跨 session 上下文继承）；
- 开发流程强调**可复现性与版本化**（Agent/Environment/Skill 均支持版本快照）；
- 对安全性要求高，需文件扫描、Skill 安全审核等平台级保障。

### ✅ 推荐使用 `Application Publishing and Sharing`
- 你的目标用户是**非技术人员**（如客服、销售、普通员工），需要开箱即用的界面或聊天入口；
- 需要将能力**快速嵌入现有办公生态**（钉钉/微信）或客户触点（H5 页面、小程序）；
- 希望将某个高频能力**抽象为可复用组件**，供其他智能体或工作流直接调用，避免重复开发；
- 业务场景适合**轻量级实时互动**（如语音问答、视频客服引导），且接受百炼提供的标准化音视频 SDK；
- ⚠️ 注意：**仅限 Agent 1.0 和 Workflow 应用**；若已升级至 Agent 2.0，请改用 `Application Call` 集成。

## 技术选型参考（面向开发者）

| 选型考量点 | Application Call | Managed Agents API | Application Publishing and Sharing |
|------------|------------------|---------------------|-------------------------------------|
| **开发成熟度** | ★★★★☆（文档完善、SDK 全面、OpenAI 兼容） | ★★★☆☆（概念抽象度高，需理解 Session/Event/Environment 模型） | ★★★★☆（控制台向导式操作，低代码，但定制化能力弱） |
| **运维复杂度** | 低（无状态调用，依赖少） | 中高（需管理 Session 生命周期、文件/技能状态、沙箱依赖） | 低（平台托管 UI/渠道，但需维护三方平台凭证与权限） |
| **扩展性** | 中（支持[多模态](../concepts/multi-modal.md)、异步、流式，但无法干预执行） | 高（可编程事件处理、自定义 Skill、动态 Environment） | 低（发布形态固定，UI/钉钉/微信配置项有限，不支持自定义渲染） |
| **安全合规** | 依赖 API Key 权限控制，文件上传需鉴权 | 提供 Skill 安全扫描、文件状态机（`checking`→`available`）、沙箱隔离 | 依赖业务空间隔离，UI 可配置匿名访问权限组，但链接无内置鉴权 |
| **与 Agent 2.0 兼容性** | ✅ 完全支持（推荐 Agent 2.0 的首选调用方式） | ✅ 支持（Agent 2.0 可作为托管 Agent 创建） | ❌ **完全不支持**（仅限 Agent 1.0） |
| **推荐组合模式** | - Agent 2.0 应用 → `Application Call` + 自研前端<br>- Agent 1.0 应用 → `Application Call`（API 集成）或 `Publishing`（终端交付） | - 复杂工具链智能体 → `Managed Agents API` + 自研调度器<br>- 需要沙箱计算的分析任务 → `Managed Agents API` + Cloud Environment | - 内部提效工具 → `Publishing` → UI 应用<br>- 客户服务触点 → `Publishing` → 钉钉/微信<br>- 能力复用 → `Publishing` → 组件 |

> **关键结论**：  
> - **不要用 `Publishing` 对接 Agent 2.0** —— 这是常见误用，会导致发布失败；  
> - **不要用 `Application Call` 替代 `Managed Agents API` 的事件监控需求** —— 后者提供不可替代的执行过程可见性；  
> - **`Application Call` 与 `Publishing` 并非二选一**：一个用于后台系统集成，一个用于前端终端交付，常共存于同一应用（如：UI 应用后端调用 `Application Call` 接口）。  
>   
> 最终选型应基于 **“谁在用”、“怎么用”、“需要看到什么”** 三重判断：面向开发者？面向终端用户？是否需要干预执行？是否需要沙箱？是否需要多渠道分发？答案将自然指向最匹配的能力组合。

## 被对比主题页

- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)
- [application publishing and sharing](../guides/application-publishing-and-sharing.md)


