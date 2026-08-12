# 应用调用方式对比：Application Call、Bailian Application Calling 与 Managed Agents

为帮助开发者在百炼平台中高效选型，本文系统对比三种核心应用调用机制：**Application Call**（通用应用调用）、**Bailian Application Calling**（百炼原生应用调用）与 **Managed Agents**（托管式智能体运行时）。三者定位不同：前两者面向已发布、配置完成的“成品应用”进行端到端调用；后者则面向需深度控制执行生命周期、多步工具协同、状态持久化的复杂智能体开发场景。理解其差异是构建稳定、可扩展 AI 服务的关键前提。

## 关键维度对比

| 维度 | Application Call | Bailian Application Calling | Managed Agents |
|------|------------------|-----------------------------|----------------|
| **本质定位** | 百炼平台统一的应用级 API 调用协议，覆盖新版/旧版智能体及工作流，强调协议兼容性与多模态支持 | 百炼早期标准化的智能体/工作流调用方式，聚焦轻量集成与[插件](../concepts/plugin.md)参数透传，是 Application Call 的子集与历史演进基础 | 全托管的智能体运行时环境，提供沙箱、会话状态、工具链、事件流等底层能力，面向“构建型”而非“调用型”场景 |
| **输入格式** | 支持 `input` 字符串或结构化 `messages` 数组（含 `input_text`/`input_image`/`input_file` 多模态字段）；支持 `biz_params` 传递自定义业务参数 | 仅支持 `prompt`（单轮）或 `messages`（OpenAI 风格数组）；`biz_params` 专用于[插件](../concepts/plugin.md)参数透传（结构为 `{ "user_defined_params": { "<plugin_code>": { ... } } }`） | 通过 `/sessions/{id}/events` 提交用户事件（`role: "user"` + `content`），支持文本、文件引用（挂载后路径）；无 `prompt`/`messages` 概念，所有交互均为事件驱动 |
| **输出格式** | 同步返回 JSON 响应（含 `output.text`、`usage` 等）；支持 `stream=true` 流式响应（需应用启用）；异步模式返回 `task_id` | 同步返回 JSON（含 `output.text`、`usage.models[].model_id`）；**不支持[流式输出](../concepts/streaming-output.md)**；**不支持异步模式** | SSE 流式事件推送（`text/event-stream`），包含 `message`（模型回复）、`tool_call`（工具调用）、`tool_output`（工具结果）、`session_status` 等多种事件类型；无传统“响应体”，需客户端持续消费事件流 |
| **支持模型** | 由被调用应用内部绑定，调用方无需指定；支持通义千问全系列（Qwen-VL 多模态、Qwen-Max/Plus 等）及工作流编排模型 | 同上，由应用绑定；但工作流应用在华北2（北京）外地域可能受限（文档明确提示“仅适用于华北2（北京）地域”） | 显式声明 `model.id`（如 `"qwen3-max"`），支持 Qwen3 系列大模型；模型选择直接影响工具决策与代码执行质量，且与 Agent 配置强绑定 |
| **API 端点** | • DashScope 协议：`POST /api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容 Responses API：`POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | 统一使用 `POST /api/v1/apps/{app_id}/completion`（即 DashScope 协议端点） | 分层端点：<br>• 创建 Agent：`POST /agents`<br>• 创建 Environment：`POST /environments`<br>• 创建 Session：`POST /sessions`<br>• 发送事件：`POST /sessions/{id}/events`<br>• 订阅流：`GET /sessions/{id}/events/stream` |
| **计费方式** | 按模型 token（输入+输出）计费；调用本身无额外费用；地域与 Workspace ID 不影响计费逻辑 | 同 Application Call，按实际消耗的模型 token 计费；[插件](../concepts/plugin.md)调用若涉及外部服务，费用另计 | **三重计费**：<br>• 会话运行时费（0.5 元/小时，`running` 状态计费）<br>• 模型 token 费（同上）<br>• 工具/MCP 调用费（如 `bash`、`download_file` 等）<br>• 免费额度（10 小时）仅抵扣运行时费 |
| **典型场景** | • 实时客服对话（流式响应）<br>• 文档问答（上传 PDF + 多轮追问）<br>• 图像理解（上传图片 + 自然语言提问）<br>• 长耗时报告生成（异步任务 + 轮询） | • 快速集成预置智能体（如政策解读机器人）<br>• 业务系统嵌入问答模块（单轮/多轮）<br>• 通过插件参数动态控制智能体行为（如传入用户ID触发个性化推荐） | • 自动化数据分析（读取 CSV → Pandas 处理 → 生成图表）<br>• 代码辅助开发（理解需求 → 编写/调试 Python 脚本）<br>• 多步骤文件处理（下载 → 解压 → 提取文本 → 总结）<br>• 需中断续接的长周期任务（如分阶段审核流程） |
| **状态管理** | 依赖 `session_id`（服务端维护，有效期 1 小时）或显式 `messages` 数组；应用自身决定上下文长度与存储策略 | `session_id` 模式：服务端存储，最多 50 轮，1 小时有效；`messages` 模式：完全由客户端管理上下文 | 平台全托管：会话状态（消息历史、工具状态、沙箱文件系统）全程持久化；支持任意时刻 `terminate` 后 `resume`；SSE 流天然支持断线重连与事件续订 |
| **扩展性与控制力** | 高封装性，开箱即用；但无法干预模型推理中间过程、工具调用逻辑或沙箱环境 | 控制力弱于 Application Call；插件参数透传能力有限，不支持自定义工具或沙箱 | **最高控制力**：可定制 Agent 提示词、启用/禁用特定内置工具、预装 `apt`/`pip` 包、配置网络策略（`restricted`/`unrestricted`）、挂载自定义资源 |

## 各方案适用场景建议

- **选择 Application Call 当**：  
  ✅ 你需要调用已在百炼平台**正式发布**的各类应用（新版智能体、旧版智能体、工作流），且要求**多模态支持（图文/文件）、流式响应、异步任务或跨地域部署**；  
  ✅ 你的前端或服务已适配 OpenAI 接口，希望最小改造接入百炼；  
  ❌ 不适合需要深度定制工具链、控制执行沙箱或实现复杂状态流转的场景。

- **选择 Bailian Application Calling 当**：  
  ✅ 你正在维护或集成**基于百炼早期版本构建的智能体/工作流应用**，且业务逻辑简单、无需流式或异步；  
  ✅ 你依赖**插件参数透传**（如根据用户角色动态切换知识库）且不涉及图像/文件输入；  
  ✅ 你追求最简 SDK 调用（`Application.call(app_id, prompt)`）并接受华北2（北京）为工作流首选地域；  
  ❌ 不推荐用于新项目——它已被 Application Call 全面兼容和增强，功能更少、灵活性更低。

- **选择 Managed Agents 当**：  
  ✅ 你的任务本质是**多步骤、有状态、需工具协同**（如“分析用户上传的销售数据 → 生成可视化图表 → 输出 PPT”）；  
  ✅ 你需要**完全掌控执行环境**（安装特定包、限制网络、挂载私有文件）；  
  ✅ 你要求**会话可中断、可续接、可审计**（所有事件持久化，支持回溯与调试）；  
  ✅ 你愿意承担稍高的运维认知成本（管理 Agent/Environment/Session 生命周期）以换取最大灵活性；  
  ❌ 不适合简单问答、单次文本生成等低复杂度场景——过度设计且成本更高。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|----------|------|
| “我有一个现成的百炼智能体，想在网页聊天框里实时显示回答” | **Application Call**（启用 `stream=true`） | 直接复用应用，流式响应体验最佳，SDK 调用简洁 |
| “我要把百炼的合同审查机器人嵌入 ERP 系统，每次传入合同文本和客户ID” | **Application Call** 或 **Bailian Application Calling** | 两者均可；优先 Application Call（兼容性更好，未来保障更强）；`biz_params` 传递客户ID即可 |
| “我需要让 AI 读取用户上传的 Excel，用 Pandas 清洗数据，再画出趋势图” | **Managed Agents** | 唯一支持 `bash`/`pip install pandas`/`read`/`write` 全链路的方案；Application Call 无法执行代码或安装依赖 |
| “我的应用需在德国法兰克福地域运行，且要支持用户上传图片提问” | **Application Call** | 明确支持德/京/新/东京四地；多模态输入（`input_image`）为 Application Call 特性，Bailian Calling 未提及 |
| “我正在开发一个需长期运行、支持暂停恢复的 AI 助手（如论文写作助手）” | **Managed Agents** | 会话状态全托管 + `terminate`/`resume` + 事件持久化，是此类场景的基础设施级解决方案 |
| “我只想快速测试一个智能体效果，不关心部署细节” | **Application Call**（同步模式） | 最低门槛：获取 `app_id` + `DASHSCOPE_API_KEY`，一行代码调用，即时获得结果 |

> **重要提醒**：  
> - **Bailian Application Calling 是 Application Call 的历史形态与子集**，新项目请直接使用 Application Call；存量系统迁移成本极低（多数参数与端点兼容）。  
> - **Managed Agents 不替代 Application Call**，而是互补：前者构建“智能体引擎”，后者调用“智能体应用”。你完全可以将 Managed Agents 构建的复杂 Agent 发布为一个标准应用，再通过 Application Call 对外提供服务。  
> - 所有方案均**严禁硬编码 API Key**，务必通过环境变量或密钥管理服务注入，并遵循最小权限原则。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [managed agents](../guides/managed-agents.md)


