# 应用调用方式对比：Application Call vs Bailian Application Calling

本文旨在帮助开发者清晰理解百炼平台中两种主流应用调用机制——`Application Call`（新版标准调用）与 `Bailian Application Calling`（旧版兼容调用）的核心差异，明确其设计定位、能力边界与适用约束，从而在实际集成中做出高效、合规的技术选型。随着百炼平台持续演进，`Application Call` 已成为推荐的统一调用范式，而 `Bailian Application Calling` 主要用于存量 Agent 1.0 应用的平滑迁移与兼容支持。

## 关键维度对比

| 维度 | Application Call | Bailian Application Calling |
|------|------------------|----------------------------|
| **定位与演进状态** | 百炼平台当前主推的**新一代标准化调用协议**，面向 Agent 2.0、旧版 Agent 及 Workflow 全面统一；持续迭代增强[多模态](../concepts/multi-modal.md)、流式、异步等能力 | **历史兼容层调用方式**，主要适配 Agent 1.0 和早期 Workflow 应用；功能收敛，不再新增特性，逐步向 `Application Call` 迁移 |
| **输入格式** | ✅ 支持双模式：<br>- 字符串 `prompt`（单轮）<br>- OpenAI Messages 数组（多轮），且 `user` 消息 `content` 可嵌套 `input_text`/`input_image`/`input_file` 结构<br>✅ 显式支持图像（需 VL 模型+应用配置）、文件（仅智能体） | ✅ 支持 `prompt`（单轮）或 `messages`（多轮）<br>❌ **不支持图像/文件等[多模态](../concepts/multi-modal.md)输入**；`messages` 中 `content` 仅为纯文本字符串，无结构化媒体字段 |
| **输出格式** | ✅ 同步调用支持结构化响应（含 `output.text`、`output.references`、`usage` 等）<br>✅ **支持 SSE [流式输出](../concepts/streaming-output.md)**（`stream=true`），适用于长文本生成、实时对话渲染<br>✅ 异步调用返回 `task_id`，后续 `retrieve` 获取完整结果 | ✅ 返回标准 JSON 响应（含 `output.text`）<br>❌ **不支持[流式输出](../concepts/streaming-output.md)（SSE）**<br>❌ **不支持异步调用**；所有请求均为同步阻塞式 |
| **支持的应用类型** | ✅ 新版智能体（Agent 2.0）<br>✅ 旧版智能体（Agent 1.0）<br>✅ 工作流（Workflow）应用<br>✅ 所有类型均统一使用同一 API 接口 | ✅ 智能体应用（Agent 1.0）<br>✅ 工作流应用（Workflow）<br>❌ **不支持 Agent 2.0**（新版智能体需使用 `Application Call`） |
| **API 端点** | ✅ 多地域支持：<br>- 华北2（北京）：`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>- 德国/新加坡/东京等：需构造带 `workspace_id` 的 Base URL（如 `https://dashscope.{region}.aliyuncs.com/...`）<br>✅ 同一端点复用同步/异步/流式能力 | ❌ **严格限定华北2（北京）地域**：<br>`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>❌ 其他地域调用将失败；无 `workspace_id` 机制，不支持跨地域子业务空间调用 |
| **计费方式** | ✅ 按实际调用消耗计费：<br>- 同步调用：按 token 用量（输入+输出）计费<br>- 异步调用：按任务执行时长 + token 用量计费<br>✅ 支持细粒度用量统计（`usage.input_tokens`/`output_tokens`） | ✅ 按 token 用量计费（仅同步）<br>❌ 无异步计费模型；用量统计字段较简略（如缺失 `input_tokens` 明确拆分） |
| **会话管理** | ✅ `session_id` 由服务端生成并返回，客户端需持久化传递<br>✅ 有效期：最后一次请求后 1 小时<br>✅ 无显式轮次上限（依赖应用自身配置） | ✅ 支持 `session_id`（云端管理）或 `messages`（客户端管理）<br>✅ `session_id` 有效期 1 小时，**硬性限制最多 50 轮对话**<br>✅ 若同时传 `messages`，则 `session_id` 被忽略（明确优先级） |
| **插件与自定义参数** | ✅ 通过 `biz_params` 透传任意键值对，与应用内定义的参数名严格匹配<br>✅ 支持多插件参数嵌套（如 `biz_params.plugin_xxx`）<br>✅ 参数校验由应用逻辑控制 | ✅ 仅支持插件专用透传路径：`biz_params.user_defined_params.{plugin_code}`<br>✅ 必须配合插件配置使用，非插件场景下 `biz_params` 无效<br>✅ 参数结构强约束，灵活性较低 |
| **SDK 封装** | ✅ `dashscope.Application.call()`（DashScope SDK）<br>✅ `openai.OpenAI().responses.create()`（OpenAI 兼容 Responses API）<br>✅ Java/Node.js/Go/C#/PHP 全语言 SDK 均提供原生封装 | ✅ `dashscope.Application.call()`（同名方法，但底层调用逻辑不同）<br>✅ 仅 Python/Java SDK 提供完整支持；其他语言文档示例较少<br>✅ Java SDK 要求 ≥2.12.0，Python ≥1.14.0（为 `biz_params` 兼容） |

## 适用场景建议

| 场景需求 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **新项目开发 / 新建智能体（Agent 2.0）或工作流应用** | ✅ Application Call | Agent 2.0 仅支持此方式；统一接口、[多模态](../concepts/multi-modal.md)、流式、异步能力是现代 AI 应用刚需；未来功能演进全部集中于此路径。 |
| **需要实时流式响应（如聊天界面逐字渲染、代码生成实时反馈）** | ✅ Application Call | Bailian Application Calling 完全不支持流式，无法满足低延迟交互体验。 |
| **处理耗时任务（如报告生成、批量数据处理、多步骤工具链执行）** | ✅ Application Call（异步模式） | Bailian Application Calling 无异步能力，长任务易超时失败；`background=true` + 轮询机制保障稳定性与可观测性。 |
| **需调用部署在德国、新加坡、东京等国际地域的应用** | ✅ Application Call | Bailian Application Calling 仅限北京地域，跨地域调用必然失败；`Application Call` 通过 `workspace_id` + 地域化 endpoint 实现全球部署支持。 |
| **存量 Agent 1.0 应用快速集成，且无需新特性（无图像/文件/流式/异步需求）** | ⚠️ Bailian Application Calling（短期过渡） | 接口简单、文档成熟、迁移成本低；但需注意：该路径已停止增强，长期维护风险高，建议规划升级至 `Application Call`。 |
| **需深度定制插件参数透传，且插件逻辑复杂、参数结构动态变化** | ✅ Application Call | `biz_params` 为扁平键值对，支持任意命名与嵌套；Bailian 的 `user_defined_params.{plugin_code}` 结构僵化，难以应对灵活业务参数。 |
| **严格受限于旧版 SDK 版本（如 Java <2.12.0）且暂无法升级** | ⚠️ Bailian Application Calling（临时兼容） | Application Call 的 SDK 要求更高（如 Java ≥2.12.0）；若升级受阻，可暂用旧方式，但应尽快制定 SDK 升级计划。 |

## 技术选型参考（面向开发者）

- **首选 `Application Call`**：它是百炼平台当前及未来的**事实标准**。除非存在不可逾越的兼容性障碍（如强依赖旧 SDK 且无法升级、仅维护极简 Agent 1.0 应用），否则所有新开发、功能增强、架构升级均应基于此方案。
  
- **避免混合使用**：同一应用不应在部分模块用 `Application Call`、部分用 `Bailian Application Calling`。二者凭证体系、错误码、响应结构虽相似，但行为语义（如会话上限、地域规则、多模态支持）存在本质差异，混用易引发隐蔽缺陷。

- **迁移建议**：
  - 对 Agent 1.0 应用：可在控制台一键升级为 Agent 2.0，随后无缝切换至 `Application Call`；
  - 对 Workflow 应用：无需变更应用本身，仅需调整调用代码——将 `prompt`/`messages` 封装为 `input` 字段，启用 `stream` 或 `background` 参数即可获得新能力；
  - 注意检查 `workspace_id`：若应用位于子业务空间或国际地域，`Application Call` 必须传入，而旧方式不支持。

- **安全与运维提示**：
  - 始终通过环境变量注入 `DASHSCOPE_API_KEY`，禁止硬编码；
  - 生产环境务必捕获 `request_id` 并记录，便于问题排查与用量审计；
  - 对异步任务，实现健壮的轮询重试机制（指数退避 + 最大重试次数）；
  - 多模态调用前，务必验证应用所选模型是否支持 VL 能力，并确认前端已正确配置图像/文件处理逻辑。

> **总结**：`Application Call` 是面向未来的、能力完备的统一调用范式；`Bailian Application Calling` 是面向过去的、功能受限的兼容接口。技术决策应以长期可维护性、功能扩展性与平台演进方向为根本依据。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


