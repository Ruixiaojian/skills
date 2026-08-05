# 应用调用相关 API 对比：Application Call vs Application Component API Reference vs Bailian Application Calling

## 背景与目的  
在百炼平台生态中，开发者常需通过 API 与平台能力集成。但当前存在三类名称相近、用途易混淆的调用接口体系：  
- **Application Call**：面向已发布应用（智能体/工作流）的**运行时推理调用**，核心是“执行应用逻辑并获取结果”；  
- **Application Component API Reference**：面向平台底层能力组件（知识库、[数据连接](../concepts/data-connection.md)、Prompt 模板）的**资源管理型 OpenAPI**，核心是“构建和维护应用依赖的数据与配置”；  
- **Bailian Application Calling**：面向智能体与工作流应用的**轻量级用户指南式调用规范**，强调快速上手与业务集成，是 `Application Call` 的简化实践子集。  

本对比旨在帮助开发者清晰区分三者定位、能力边界与技术选型依据，避免因概念混淆导致接入失败、功能误用或架构设计偏差。

---

## 关键维度对比表

| 维度 | Application Call | Application Component API Reference | Bailian Application Calling |
|------|------------------|-------------------------------------|-----------------------------|
| **核心定位** | 应用运行时推理调用（Runtime Inference） | 平台能力组件管理（Resource Management） | 应用调用最佳实践指南（Usage Guide） |
| **输入格式** | `input`（字符串或消息数组）、`biz_params`、`session_id`、`stream`/`background` 控制参数 | 标准 ROA 请求：路径参数（如 `WorkspaceId`, `IndexId`）、Query 参数（分页）、JSON Body（如 `AddFile` 的 `parser` 配置） | 简化版 `prompt` / `messages` + `biz_params`，兼容 SDK 与 HTTP 调用 |
| **输出格式** | 同步：结构化响应（含 `output`, `usage`, `session_id`）；异步：任务 ID（`id`）及状态元信息 | 标准 OpenAPI 响应：成功返回 `200` + 资源对象（如 `IndexId`, `FileId`）；失败返回 `4xx/5xx` + 错误码与 `request_id` | 与 `Application Call` 完全一致（本质是其子集），无额外封装 |
| **支持模型/应用类型** | ✅ 新版智能体（Agent 2.0）、旧版智能体、工作流<br>✅ 多模态（图像/文件输入，需模型与配置匹配）<br>❌ 不支持知识库/[数据连接](../concepts/data-connection.md)等组件本身 | ❌ 不调用任何模型或应用<br>✅ 知识库（Index）、[数据连接](../concepts/data-connection.md)（Category/File/Connector）、Prompt 模板三大组件的全生命周期管理 | ✅ 智能体应用（Agent 1.0）、工作流应用<br>❌ 不支持新版智能体（Agent 2.0）、不支持多模态输入（文档未提及图像/文件）<br>✅ 插件透传（`user_defined_params`） |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• Responses（OpenAI 兼容）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | 地域化 ROA 接口：<br>• `https://bailian.cn-beijing.aliyuncs.com/`（北京）<br>• `https://bailian.ap-southeast-1.aliyuncs.com/`（新加坡）等<br>路径示例：`POST /openapi/2023-12-29/indices` | 与 `Application Call` 完全复用同一端点（`/completion`），无独立 endpoint |
| **认证方式** | Bearer [Token](../concepts/token.md)（`Authorization: Bearer <API_KEY>`） | ROA 签名（AccessKey ID/Secret）为主；部分接口（如 `Retrieve`）支持 API Key | Bearer [Token](../concepts/token.md)（`Authorization: Bearer <API_KEY>`），与 `Application Call` 一致 |
| **计费方式** | 按调用次数 + 模型 token 用量计费（计入 DashScope 账单） | 按 API 调用次数计费（知识库构建、文件解析等操作单独计费） | 同 `Application Call`（因其调用即走 `Application Call` 接口） |
| **典型场景** | • 实时客服对话（同步+流式）<br>• 自动生成周报（异步+长任务）<br>• 多模态问答（图像理解+文本生成） | • 批量导入 PDF 构建知识库<br>• 动态更新 Prompt 模板版本<br>• 监控知识库切片质量与检索延迟 | • 快速将智能体嵌入企业微信机器人<br>• 工作流应用对接内部 OA 系统审批节点<br>• 小程序中调用插件处理用户上传文件 |
| **地域支持** | ✅ 多地域（北京、上海、杭州、新加坡、东京、法兰克福等），`workspace_id` 决定 Base URL | ✅ 多地域（按 `WorkspaceId` 所属地域选择对应 Endpoint） | ⚠️ **工作流应用仅限华北2（北京）**；智能体应用无限制 |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要实时响应用户提问，并支持流式返回答案**（如聊天界面） | ✅ `Application Call`（同步 + `stream=true`） | 唯一支持[流式输出](../concepts/streaming-output.md)的方案；`Bailian Application Calling` 文档虽未明确禁止，但其指南未覆盖流式配置，且实际能力依赖底层 `Application Call` 接口。 |
| **需批量构建/更新知识库，或动态管理数据源与 Prompt 模板** | ✅ `Application Component API Reference` | 此为唯一提供知识库 `CreateIndex`/`SubmitIndexJob`、数据连接 `AddFile`/`AddCategory`、Prompt `CreatePromptTemplate` 等管理能力的接口体系。`Application Call` 和 `Bailian Application Calling` 完全不涉及此类资源操作。 |
| **快速上线一个工作流应用供业务系统调用，要求最小学习成本** | ✅ `Bailian Application Calling` | 提供最简参数模板（`app_id` + `prompt`/`messages`）、完整 SDK 示例与调试开关（`debug`），规避了 `Application Call` 中 `workspace_id` 地域适配、`input` 结构复杂性等细节，适合非深度集成场景。 |
| **调用新版智能体（Agent 2.0）并使用图像输入能力** | ✅ `Application Call` | `Bailian Application Calling` 明确不支持新版智能体；`Application Component API Reference` 不涉及应用调用。仅 `Application Call` 文档详细定义了 `imageList` 输入、VL 模型配置等关键路径。 |
| **需异步执行耗时任务（如生成 50 页分析报告）并轮询结果** | ✅ `Application Call`（`background=true`） | `Bailian Application Calling` 未提及异步模式；`Application Component API Reference` 无应用执行能力。`Application Call` 是唯一提供 `retrieve` 任务查询机制的方案。 |
| **在生产环境严格管控权限，需最小化 API 密钥暴露面** | ✅ `Application Component API Reference`（使用 RAM AccessKey）<br>⚠️ `Application Call` / `Bailian Application Calling`（必须使用全局 API Key） | `Application Component API Reference` 支持基于 RAM 的细粒度权限策略（如 `AliyunBailianDataReadOnlyAccess`），而另两者强制使用高权限 API Key，安全风险更高。 |

---

## 技术选型参考（面向开发者）

### 选择 `Application Call` 当：
- 你正在开发**高定制化 AI 应用网关**，需精细控制同步/异步、流式、会话、多模态等行为；
- 你使用的是**新版智能体（Agent 2.0）或需文件/图像输入**；
- 你需要**跨地域部署应用**（如新加坡业务空间调用工作流），并自行管理 `workspace_id` 与 Base URL；
- 你已熟悉 DashScope SDK 或 OpenAI 兼容协议，追求最大灵活性。

### 选择 `Application Component API Reference` 当：
- 你的核心需求是**自动化运维平台能力组件**，例如：CI/CD 流程中自动创建知识库、定时刷新数据源、灰度发布 Prompt 模板；
- 你需要**强权限隔离**（如数据团队仅能操作知识库，不能调用任何应用）；
- 你正在构建**RAG 基础设施层**，需直接调用 `Retrieve` 接口实现自定义检索逻辑，而非依赖智能体内置 RAG。

### 选择 `Bailian Application Calling` 当：
- 你是**业务线前端/后端工程师**，目标是“让这个工作流尽快跑起来”，而非深入平台机制；
- 你调用的应用**确定为旧版智能体或工作流**，且无需多模态、异步、流式等高级特性；
- 你希望获得**最简代码示例、调试支持（`debug` 开关）和明确的错误排查指引**（其文档聚焦用户常见问题）；
- 你接受**地域限制**（工作流必须在北京），且项目周期紧张，无法投入时间适配多地域 `workspace_id`。

> 💡 **终极建议**：  
> - **不要将三者视为互斥选项**——典型生产架构中，三者常协同使用：  
>   `Application Component API Reference` → 构建知识库与数据源 →  
>   `Application Call` → 发布并调用新版智能体（支持图像）→  
>   `Bailian Application Calling` → 为内部运营系统提供轻量 SDK 集成。  
> - **始终以控制台为准**：文档中关于地域、参数必填性的描述可能存在滞后，务必通过 [百炼控制台](https://bailian.console.aliyun.com) 查看当前地域可用服务与最新参数说明。  
> - **SDK 优先**：无论选用哪种方案，均推荐使用官方 DashScope SDK（Python/Java/TypeScript），它已统一处理签名、重试、错误解析与地域路由，大幅降低接入风险。

## 被对比主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)


