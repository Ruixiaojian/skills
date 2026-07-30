# 应用调用方式对比：Application Call vs Bailian Application Calling

本文旨在帮助开发者清晰理解百炼平台中两种主流应用调用机制——`Application Call`（官方 API 规范命名）与 `Bailian Application Calling`（用户侧通用术语/文档体系命名）——在技术实现、能力边界与工程实践上的异同。二者并非互斥方案，而是同一底层能力在**不同抽象层级与文档视角下的表述**：前者侧重协议标准化与多模式支持（同步/异步/流式），后者强调开箱即用的集成体验与业务场景适配（如插件透传、统一接口）。本对比基于当前（2024 Q3）百炼平台正式发布能力整理，适用于新应用开发与存量系统迁移的技术选型决策。

## 关键维度对比

| 维度 | Application Call | Bailian Application Calling |
|------|------------------|-----------------------------|
| **定义与定位** | 百炼平台官方定义的标准化应用调用协议，覆盖新版智能体、旧版智能体、工作流三类应用，强调协议兼容性（DashScope 原生 + OpenAI 兼容）与调用模式完整性（同步/异步/流式）。 | 百炼用户文档体系中对“调用百炼应用”这一行为的统称，聚焦于实际集成流程、参数语义与典型业务能力（如插件参数透传），以简化开发者认知为设计目标。 |
| **输入格式** | • 支持 `input` 字段为 `string`（单轮文本）或 `array`（多模态消息数组，含 `type: "input_image"` / `"input_file"`）<br>• 显式支持图像、文件等多模态输入（需应用配置匹配）<br>• `session_id` 用于云端会话管理 | • 支持 `prompt`（字符串）或 `messages`（消息数组）作为核心输入<br>• `messages` 优先级高于 `session_id`，支持精确上下文控制<br>• 通过 `biz_params.user_defined_params` 结构化透传插件参数（如 `{"plugin_abc123": {"query_id": 42}}`）<br>• **不显式声明图像/文件输入语法**（依赖应用内配置，未在调用层暴露 `input_image` 等类型字段） |
| **输出格式** | • 同步响应：完整 JSON 结果（含 `output.text`、`usage`、`session_id` 等）<br>• [流式输出](../concepts/streaming-output.md)：SSE 格式分块返回（`stream=true`，仅同步支持）<br>• 异步响应：立即返回 `{ "task_id": "xxx" }`，需轮询 `/tasks/{id}` 获取结果 | • 统一返回标准 JSON 响应结构（含 `output.text`、`usage.models[].model_id`、`request_id`）<br>• **明确不支持[流式输出](../concepts/streaming-output.md)**（文档未提及 `stream` 参数，所有示例均为同步阻塞式）<br>• **不提供原生异步模式**（无 `background=true` 参数，未描述任务轮询机制） |
| **支持模型/应用类型** | • 新版智能体（Agent 2.0）<br>• 旧版智能体<br>• 工作流应用<br>• 多模态模型（Qwen-VL 系列）需在应用中显式配置图像处理逻辑 | • 智能体应用（Single Agent）<br>• 工作流应用（Workflow）<br>• **隐式绑定模型**：由应用发布时选定的模型（如 `qwen-max`）决定，调用方无需指定；响应中可通过 `usage.models[].model_id` 查看实际调用模型<br>• **未提及多模态模型支持细节**（如图像/文件输入能力未在关键参数或示例中体现） |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（同步/异步共用同一路径） | • **统一端点**：仅使用 `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• **不提供 OpenAI 兼容路径**（所有文档示例均基于 DashScope 原生接口） |
| **计费方式** | • 按实际调用的模型 [Token](../concepts/token.md) 数量计费（输入 + 输出）<br>• 异步任务、[流式输出](../concepts/streaming-output.md)、多模态输入（图像/文件）均计入对应模型的 [Token](../concepts/token.md) 消耗<br>• 费用归属应用所属的 Workspace | • 同样按 [Token](../concepts/token.md) 计费（输入 + 输出）<br>• 插件调用产生的额外费用（如第三方 API 调用）由插件配置独立结算，不计入主应用 Token 费用<br>• 文档强调 `biz_params` 透传不影响基础计费模型 |
| **典型场景** | • 需要低延迟响应的实时对话（启用 `stream=true`）<br>• 执行耗时较长的复杂工作流（启用 `background=true`）<br>• 集成多模态能力（上传图片分析、解析 PDF 文件）<br>• 已有 OpenAI 生态代码需最小改动迁移 | • 快速集成标准问答/客服机器人（单轮/多轮文本）<br>• 需与自定义插件深度协同的业务流程（如订单查询、工单创建）<br>• 追求接口简洁、减少协议学习成本的内部系统对接<br>• 对流式/异步无强需求，以功能正确性与可维护性为优先 |

## 适用场景建议

- **选择 `Application Call` 当：**  
  ✅ 项目需要**流式响应**（如聊天界面逐字渲染、长文本生成实时反馈）；  
  ✅ 任务执行时间可能超过数秒（如复杂数据分析、多步骤工作流），需**异步解耦**避免请求超时；  
  ✅ 应用涉及**图像识别、文档解析等多模态能力**，且需在调用层直接控制输入格式；  
  ✅ 已有基于 OpenAI SDK 的代码库，希望**零改造复用**（利用兼容接口）；  
  ❌ 不推荐用于仅需简单文本交互且无性能敏感要求的轻量级集成。

- **选择 `Bailian Application Calling` 当：**  
  ✅ 开发目标是快速上线一个**带插件能力的业务智能体**（如“查物流+改地址+发通知”一体化流程）；  
  ✅ 团队偏好**单一、稳定、文档完备的接口**，不愿处理多种端点与参数组合；  
  ✅ 多轮对话需**精确控制上下文长度或隔离敏感信息**（显式 `messages` 数组更可控）；  
  ✅ 项目处于 PoC 或 MVP 阶段，优先保障功能交付而非极致性能优化；  
  ❌ 不适合对首字延迟（TTFB）或总响应时间有严苛 SLA 要求的场景。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **是否需要流式输出？** | `Application Call`（`stream=true`） | `Bailian Application Calling` 文档及示例中完全未涉及流式能力，非可用选项。 |
| **是否需异步执行长任务？** | `Application Call`（`background=true`） | `Bailian Application Calling` 无对应参数与轮询机制，无法原生支持。 |
| **是否需调用图像/文件处理能力？** | `Application Call`（`input` 中 `type: "input_image"`） | `Bailian Application Calling` 的 `prompt`/`messages` 输入模型未定义多模态类型字段，依赖应用内黑盒配置，调用层不可控。 |
| **是否需透传插件参数？** | `Bailian Application Calling`（`biz_params.user_defined_params`） | `Application Call` 文档未定义插件参数透传结构，虽可通过 `input` 自定义字段实现，但缺乏标准化约定与文档指引。 |
| **是否已使用 OpenAI SDK？** | `Application Call`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） | 可直接复用现有 `openai` 客户端，仅需修改 `base_url` 和 `api_key`，迁移成本趋近于零。 |
| **是否追求接口极简与文档一致性？** | `Bailian Application Calling`（统一 `/completion` 端点） | 无需记忆多套路径（`/responses` vs `/completion`）、多套参数规则（`input` vs `prompt/messages`），降低出错概率。 |
| **是否部署在非华北2地域？** | `Application Call`（明确支持 `workspace_id` + 地域 Base URL） | `Bailian Application Calling` 文档虽未禁止跨地域，但多处强调“仅适用于华北2”，实操风险更高；`Application Call` 提供明确的跨地域调用指南。 |

> **重要提示**：二者底层均调用百炼平台同一服务，**不存在功能鸿沟**。差异源于 API 设计哲学——`Application Call` 是“能力全集”的协议层封装，`Bailian Application Calling` 是“最佳实践”的用户层封装。在实际开发中，可混合使用：例如用 `Bailian Application Calling` 实现主业务流，对特定高要求节点（如实时绘图反馈）切换至 `Application Call` 的流式接口。始终以 [百炼官方 API 参考](https://help.aliyun.com/zh/model-studio/developer-reference) 为准，并关注各文档标注的**地域限制**与**权限要求**。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


