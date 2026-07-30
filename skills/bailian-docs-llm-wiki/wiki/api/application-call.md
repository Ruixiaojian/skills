# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等）的核心能力。开发者使用 APP ID（及必要时的 Workspace ID）和 API Key，向统一 endpoint 发起 HTTP 请求或调用 SDK，即可触发应用逻辑并获取结构化响应。该机制支持同步与异步两种模式，覆盖单轮/多轮对话、文本/图像/文件[多模态](../concepts/multi-modal.md)输入及[流式输出](../concepts/streaming-output.md)等典型场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用；其中[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)明确限定仅适用于华北2（北京）地域。
- **[多模态](../concepts/multi-modal.md)能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型节点入参变量设为 `imageList`（工作流）；
  - 文件输入：**仅智能体应用支持**，且需在应用内选择“全文引用”或“切片检索”[文件处理](../concepts/file-processing.md)方式；
- **交互模式**：
  - 同步调用：适用于实时交互，即时返回结果，支持[流式输出](../concepts/streaming-output.md)（`stream=true`）；
  - 异步调用：适用于耗时任务（如复杂报告生成），通过 `background=true` 触发，返回任务 ID 后轮询状态；> **注意**：异步调用**不支持[流式输出](../concepts/streaming-output.md)**，此限制在[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)中明确说明，与同步调用形成互补。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制；若应用位于子业务空间或特定地域（如德国法兰克福），还需提供 `workspace_id` —— 获取方式详见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string 或 array | 是 | 核心输入内容：<br>- 字符串：用于单轮纯文本对话；<br>- 消息数组：用于多轮对话或含图片/文件的[多模态](../concepts/multi-modal.md)输入，格式需符合 OpenAI 兼容规范（`role`, `content` 等）。 |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)。仅同步调用有效；异步调用中设置 `true` 将被忽略。 |
| `background` | boolean | 否（默认 `false`） | 是否启用异步模式。设为 `true` 时立即返回任务 ID，后续需调用 `retrieve` 查询结果。 |
| `biz_params` | object | 否 | 传递应用内定义的**自定义参数**（如城市名、索引值等），参数名与类型须与应用配置严格一致；该参数仅在 OpenAI 兼容模式（Responses API）中生效。 |

## 使用方式

### 1. 基础调用路径
- **DashScope 原生 API**（推荐用于高性能、全功能场景）：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  支持 Python/Java/Go 等 SDK 及 curl 直接调用，请求体为 `{"input": {"prompt": "..."}}` 格式。
- **OpenAI 兼容 Responses API**（推荐用于快速迁移或复用 OpenAI 生态）：  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上 endpoint，但请求体中增加 `"background": true`。

### 2. 多轮对话实现
- **DashScope API**：通过 `session_id` 维护上下文。首次请求不传，响应中返回 `session_id`；后续请求在参数中显式传入该 ID 即可延续会话（有效期 1 小时）。
- **Responses API**：**不依赖 `session_id`**，而是要求在每次请求的 `input` 数组中**完整传递历史消息**（含 `user`/`assistant` 角色消息）。文档明确说明：“基于 `pre_response_id` 或 `conversation_id` 的上下文功能将在后续支持”。

### 3. 开发者工具链
- **凭证配置**：API Key 建议通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码；
- **调试入口**：控制台中进入 **应用卡片 → 发布 → API 调试**，可免代码验证参数与逻辑；
- **SDK 选型**：
  - DashScope SDK：适配原生 API，功能最全；
  - OpenAI Python SDK（v1.0+）：适配 Responses API，兼容 `openai>=1.0.0` 接口。

## 限制和注意事项

- **地域限制**：所有文档均强调当前 API 仅支持**华北2（北京）地域**，其他地域（如德国法兰克福、新加坡）虽需 `workspace_id`，但未明确其 API endpoint 是否可用，实际调用前需确认地域兼容性。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口，详见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询全部业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- > **注意**：文档 2 与文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 提到“德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下的模型时，API 请求中才必须包含 `Workspace ID`”。此处存在隐含矛盾——文档 1 暗示这些地域的 API 是可用的，而文档 2/3 未覆盖；开发者应以控制台实际可用 endpoint 和错误提示为准，优先验证北京地域，再扩展至其他地域。
- **异步任务管理**：异步调用后必须主动轮询 `retrieve` 接口获取结果，平台不提供 Webhook 回调；任务状态终态为 `completed`/`failed`/`cancelled`，需在代码中完整处理这三种情况。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)




