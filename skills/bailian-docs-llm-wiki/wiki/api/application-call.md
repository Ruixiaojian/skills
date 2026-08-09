# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 进行集成，支持文本、图像、文件等[多模态](../concepts/multimodal.md)输入及多轮对话上下文管理。所有调用均需提供有效的 APP ID 和 API Key，并在特定地域（如华北2）下生效。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，API 阻塞等待结果返回；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但工作流应用需在结束节点启用流式开关并重新发布。
  - **异步调用**：适用于耗时任务（如长报告生成），设置 `background=true` 后立即返回任务 ID，后续通过 `retrieve` 查询状态；**异步模式不支持[流式输出](../concepts/streaming-output.md)**，此限制明确记载于 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **[多模态](../concepts/multimodal.md)输入**：
  - 图像输入：需选用通义千问 VL 系列模型，并在智能体中配置“自定义处理”，或在工作流中将模型入参设为 `imageList`；相关配置说明见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件输入：**仅智能体应用支持**，且需在应用内选择“全文引用”或“切片检索”文件处理方式。
- **会话管理**：DashScope API 通过 `session_id` 维护多轮对话（有效期 1 小时）；Responses API 则要求显式传递完整消息历史数组，当前不支持基于 `pre_response_id` 或 `conversation_id` 的隐式上下文延续。

> **注意**：文档 2（[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)）声明“仅适用于华北2（北京）地域”，而文档 4（[应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)）同样标注相同地域限制，但文档 3 和 5 的 Responses API 文档也重复强调该限制。这并非矛盾，而是全量 API 当前均限定于华北2 地域，属统一约束而非冲突信息。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制获取；若应用位于子业务空间或德国/北京/新加坡/东京地域，还需传入 `workspace_id`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。 |
| `input` | string / array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及[多模态](../concepts/multimodal.md)（`input_text`/`input_image`/`input_file`），其中 `input_file` 仅智能体应用可用。 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）；**异步调用时不可设为 `true`**。 |
| `background` | boolean | 否 | 是否启用异步模式（默认 `false`）；设为 `true` 时返回任务 ID，需另行查询结果。 |
| `biz_params` | object | 否 | 用于向工作流或智能体传递自定义参数（如 `{"city": "北京"}`），参数名与应用内定义必须严格一致。 |

## 使用方式

- **API Endpoint**：
  - DashScope 原生接口：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - Responses API（OpenAI 兼容）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **认证方式**：HTTP Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，API Key 需通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取并配置至环境变量。
- **SDK 调用**：
  - DashScope SDK（Python/Java 等）：直接调用 `Application.call()`，传入 `app_id`、`prompt` 等参数。
  - OpenAI SDK：初始化客户端时指定 `base_url`（含 `APP_ID`），再调用 `client.responses.create()`。
- **调试入口**：控制台中进入目标应用卡片 → “发布” → “API 调试”，可在线填写参数并执行测试。

## 限制和注意事项

- **地域限制**：所有 `application call` 接口当前**仅支持华北2（北京）地域**，其他地域暂不可用。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询能力（来源：[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **会话与上下文**：DashScope API 的 `session_id` 机制与 Responses API 的消息数组机制互不兼容，不可混用；后者要求每次请求携带完整历史，无隐式状态管理。
- **异步任务生命周期**：异步任务创建后，需主动轮询 `retrieve` 接口直至状态变为 `completed`/`failed`/`cancelled`；任务结果不会自动推送，超时未查询将导致结果丢失。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


