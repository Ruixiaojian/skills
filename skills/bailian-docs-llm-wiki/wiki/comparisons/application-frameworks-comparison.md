# 应用构建框架对比：Managed Agents vs Application Component API vs Frameworks

## 对比目的与背景

在百炼平台生态中，开发者面临多种技术路径来构建 AI 原生应用：从全托管的智能体运行时（Managed Agents），到细粒度的数据与知识能力组合（Application Component API），再到面向主流开发范式的框架级集成（Frameworks）。三者定位不同、抽象层级各异、适用边界清晰。本对比旨在为开发者提供客观、可操作的技术选型参考，帮助其根据**应用形态、控制粒度、团队能力与交付节奏**等核心因素，快速判断最适合的构建路径，避免过度工程化或能力缺失风险。

---

## 关键维度对比表

| 维度 | Managed Agents API | Application Component API | Frameworks（LlamaIndex / Spring AI Alibaba） |
|------|---------------------|----------------------------|-----------------------------------------------|
| **定位与角色** | 智能体（Agent）全生命周期托管运行时，聚焦“会话驱动型”交互式应用 | 底层能力组件化服务，提供数据连接、知识库、Prompt 管理等原子能力，供自主编排 | 主流开源框架的百炼适配层，降低 RAG/智能体/知识检索类应用的接入门槛 |
| **输入格式** | ChatML 格式 message 数组（含 `role`, `type`, `content`），支持[多模态](../concepts/multi-modal.md)文本块；事件驱动模型 | RESTful 请求体（JSON），按接口语义定义（如 `AddFileRequest`, `RetrieveRequest`）；文件上传需先申请租约（Lease） | 框架原生对象（如 LlamaIndex 的 `Document`/`QueryEngine`，Spring AI 的 `Prompt`/`ChatClient`），由 SDK 自动序列化为百炼协议 |
| **输出格式** | SSE 流式事件（`message`, `tool_call`, `session_status` 等）或分页事件历史；结构化程度高，含 `thoughts`、`docReferences` 等语义字段 | JSON 响应体，严格遵循 OpenAPI Schema（如 `ListFilesResponse`, `RetrieveResponse`）；返回字段明确，但无统一语义层封装 | 框架标准返回类型（如 `Response`、`StreamingResponse`、`List<Document>`），经适配器映射为百炼能力，部分字段（如 `docReferences`）需显式启用 |
| **支持模型** | 仅限百炼托管模型（如 `qwen-plus`），`model.id` 必须为字符串且严格匹配平台列表；**不支持自定义/外部模型** | **不直接调用大模型**；所有模型能力通过下游组件（如知识库检索、Prompt 渲染）间接使用；知识库检索默认用 `qwen-max`，但不可在 Component API 层切换 | 支持指定生成模型（`qwen-max`, `qwen-plus`）及重排模型（`gte-rerank`）；模型名通过框架配置项传入，**仍受限于百炼公开模型池** |
| **API 端点** | 地域化 MAAS Endpoint（如 `https://<ws_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio`）；强绑定 workspace + region | ROA 风格通用 Endpoint（如 `bailian.cn-beijing.aliyuncs.com`）；按资源类型路由（`/data-connection`, `/knowledge-base`, `/prompt`） | **无独立端点**；复用 DashScope 统一 API（`dashscope.aliyuncs.com`）；框架内部完成鉴权、路由与协议转换 |
| **计费方式** | 按实际调用计费：Session 运行时长（秒）、工具执行次数、文件存储（GB/天）、事件流传输量；**会话空闲期不计费** | 按调用频次（QPS）与资源用量计费：文件解析/索引构建（按页/小时）、知识库检索（次）、Prompt 执行（次）、OSS 数据同步（流量） | **框架本身免费**；所有底层调用（模型推理、知识库检索、重排、文档解析）均按百炼对应计费项单独计费，与直接调用 API 一致 |
| **典型场景** | 客服对话机器人、多步骤任务助手（如订机票+查天气+发邮件）、需沙箱隔离与状态持久化的复杂工作流 | 构建企业级知识中枢（对接 ERP/CRM 文件）、管理 Prompt 版本库、自动化数据导入与索引构建、定制化检索增强流程 | 快速验证 RAG 效果、将现有 LlamaIndex/Spring Boot 应用迁移至百炼、需要框架生态（插件、可观测性、Spring 生态集成）的中大型项目 |
| **状态管理** | 内置完整状态机（`idle → running → terminated`）；Session 自动管理上下文、工具状态、中断恢复；支持 `archive`/`delete` 终态控制 | **无会话状态**；纯无状态 CRUD 接口；状态需由调用方自行维护（如缓存检索上下文、轮询任务状态） | 依赖框架自身状态管理（如 LlamaIndex 的 `Index` 实例、Spring AI 的 `ChatClient` Bean）；百炼侧不维护跨请求状态 |
| **安全与隔离** | 工作空间级资源隔离；沙箱环境（`cloud` 类型）提供网络/依赖隔离；Skill/File 需安全扫描后激活 | RAM 子账号 + 最小权限策略；文件/知识库/Category 均归属 Workspace；OSS 授权需主账号显式配置 | 继承框架运行时安全模型（如 Spring Security）；百炼侧仅校验 `DASHSCOPE_API_KEY`，不感知框架内权限体系 |

---

## 各方案适用场景建议

### ✅ 选择 **Managed Agents API** 当：
- 应用核心是**多轮、有状态、带工具调用的对话体验**（如销售顾问、IT 支持助手）；
- 需要开箱即用的**沙箱执行环境**（运行 Python 工具脚本、访问内部 API）；
- 要求**会话级状态自动管理**（上下文延续、中断恢复、超时清理）；
- 团队希望**最小化运维负担**，专注 Agent 设计与 Skill 编排，而非底层基础设施；
- 对模型选择无定制需求，接受百炼托管模型能力边界。

### ✅ 选择 **Application Component API** 当：
- 构建**后台数据中枢或知识平台**，需精细控制文件解析、知识库构建、Prompt 版本发布等环节；
- 需要**与现有系统深度集成**（如定时同步数据库表、监听 OSS 事件触发知识更新）；
- 要求**完全自主的状态与流程编排**（例如：自定义重排逻辑、混合检索策略、多知识库路由）；
- 团队具备较强后端开发能力，熟悉 RESTful 设计与幂等性处理；
- 需要规避框架锁定，保持未来技术栈演进灵活性（如迁移到自研调度引擎）。

### ✅ 选择 **Frameworks** 当：
- 项目已基于 **LlamaIndex 或 Spring Boot 技术栈**，追求**零改造迁移**至百炼；
- 目标是**快速原型验证或 MVP 上线**，优先保障开发效率而非极致控制；
- 需要利用框架生态能力（如 LlamaIndex 的 Node Postprocessor、Spring AI 的 `Advisor` 机制、Actuator 健康检查）；
- 应用形态明确为 **RAG 检索问答、智能体调用、或知识库增强聊天**，无需沙箱或复杂状态机；
- 团队熟悉对应框架，且接受其抽象带来的约束（如 LlamaIndex 不支持自定义切分器）。

---

## 技术选型决策指南（面向开发者）

| 决策维度 | 推荐方案 | 关键判断依据 |
|----------|----------|--------------|
| **应用是否需要“会话”概念？** | Managed Agents API | 若用户交互天然具有上下文依赖（如“上一条说的XX，现在帮我查下相关文档”），且需自动维持状态，则 Agents 是唯一选择。Component API 和 Frameworks 均需自行实现会话管理。 |
| **是否必须运行任意代码（Python/Shell）？** | Managed Agents API | 只有 Managed Agents 提供沙箱环境（`Environment`）支持工具脚本执行；Component API 仅提供数据能力，Frameworks 仅调用百炼已有服务。 |
| **是否已有成熟框架代码基？** | Frameworks | 若已有 LlamaIndex 构建的 RAG 应用或 Spring Boot 项目，直接集成 Frameworks 可节省 80%+ 接入成本；反之，为新项目强行引入框架可能增加学习曲线。 |
| **是否需对接非百炼数据源（如 MySQL、SharePoint）？** | Application Component API | Component API 的 `Connector` 和 `AddFilesFromAuthorizedOss` 支持标准化对接；Frameworks 仅支持百炼知识库；Managed Agents 需将对接逻辑封装为 Skill（开发成本高）。 |
| **是否要求模型完全可控（微调/私有部署）？** | ❌ 三者均不支持 | 百炼当前所有路径均**仅支持平台托管模型**；若需私有模型，请评估百炼 Model Studio 或阿里云 PAI 平台。 |
| **团队是否缺乏全栈 AI 工程经验？** | Managed Agents API 或 Frameworks | Agents 提供最高抽象（拖拽式 Agent 配置 + SDK 调用）；Frameworks 利用社区惯用范式降低认知负荷；Component API 要求理解 ROA、租约、幂等性等细节，适合资深后端。 |

> **重要提醒**：三者并非互斥。生产实践中常见**组合使用**——例如：用 Application Component API 构建和维护知识库，再通过 Managed Agents API 创建调用该知识库的智能体；或用 Frameworks 快速搭建前端 Demo，后端核心流程用 Component API 实现高可靠性调度。选型应以**端到端交付价值**为最终目标，而非单一技术指标。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)


