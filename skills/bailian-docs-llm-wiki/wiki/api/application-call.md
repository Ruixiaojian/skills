# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等），向其提交输入并获取模型或流程执行结果的核心交互方式。它支持同步与异步两种模式，适配单轮/多轮对话、文本/图像/文件等多模态输入，并可通过 DashScope 原生 API 或 OpenAI 兼容 API 两种协议发起。调用前需明确目标应用身份（APP ID）、运行环境（Workspace ID，如适用）及认证凭证（API Key）。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用协议**：
  - **DashScope 原生协议**：提供 `POST /api/v1/apps/{APP_ID}/completion` 接口，适用于对性能和控制力要求较高的场景。
  - **OpenAI 兼容协议（Responses API）**：提供 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` 接口，支持 `stream` [流式输出](../concepts/streaming-output.md)与 `background` 异步执行，便于复用现有 OpenAI 生态代码。
- **多模态能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型节点入参设为 `imageList`（工作流）。
  - 文件输入：仅智能体应用支持，需在应用内选择“全文引用”或“切片检索”文件处理方式。
- **会话管理**：DashScope 协议通过 `session_id` 维护上下文（有效期 1 小时）；OpenAI 协议则要求显式传递完整 `input` 消息数组（含 `system`/`user`/`assistant` 角色），暂不支持 `pre_response_id` 或 `conversation_id` 隐式上下文。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出 Workspace ID 在德国（法兰克福）、新加坡、日本（东京）等非北京地域也是必需的，且是 Base URL 的组成部分。这表明 DashScope 原生 API 的地域限制可能已过时或不完整，实际调用应以 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中的地域说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。 |
| `Workspace ID` | string | 条件必填 | 仅当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等特定地域时必需，是 Base URL 的一部分。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：用于单轮纯文本对话；<br>- 数组：用于多轮对话或含 `input_text`/`input_image`/`input_file` 的多模态输入。 |
| `stream` | boolean | 否（默认 false） | 仅 OpenAI 协议支持。设为 `true` 启用流式响应（需工作流应用在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关）。 |
| `background` | boolean | 否（默认 false） | 仅 OpenAI 协议支持。设为 `true` 切换为异步调用，立即返回任务 ID。 |
| `biz_params` | object | 否 | 仅 OpenAI 协议支持。用于向工作流或插件配置的应用传递自定义业务参数，参数名与应用内定义必须一致。 |
| `session_id` | string | 否（多轮必需） | 仅 DashScope 协议支持。首次调用不传，响应中返回；后续请求携带以延续会话。 |

## 使用方式

### 1. DashScope 原生 API（推荐用于高性能场景）
- **Endpoint**: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **认证**: Header `Authorization: Bearer {DASHSCOPE_API_KEY}`
- **示例（curl）**:
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/your-app-id/completion" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "input": {"prompt": "你是谁？"},
      "parameters": {},
      "debug": {}
    }'
  ```

### 2. OpenAI 兼容 API（推荐用于快速集成/流式/异步场景）
- **同步 Endpoint**: `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **异步 Endpoint**: 同上，但请求体中增加 `"background": true`
- **认证**: Header `Authorization: Bearer {DASHSCOPE_API_KEY}`，并设置 `base_url`（SDK）或直接拼接 URL（HTTP）
- **示例（Python SDK 同步流式）**:
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
  )
  stream = client.responses.create(input=[{"role":"user","content":"你好"}], stream=True)
  for chunk in stream:
      if hasattr(chunk, 'delta') and chunk.delta:
          print(chunk.delta, end='', flush=True)
  ```

### 3. 在线调试
所有应用均支持通过控制台 **应用卡片 → 发布 → API 调试** 进入可视化调试页，无需编码即可验证参数与响应。

## 限制和注意事项

- **地域限制**：DashScope 原生 API（v1）和 OpenAI 兼容 API（v2）当前均**仅支持华北2（北京）地域**，其他地域暂不可用。
- **Workspace ID 依赖**：若应用部署在德国（法兰克福）、新加坡、日本（东京）等非北京地域，或位于子业务空间，则必须提供 `Workspace ID`，否则调用失败。该 ID **只能通过控制台手动获取**，不支持 API 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **异步与流式互斥**：`background=true` 与 `stream=true` **不可同时设置**，异步调用不支持[流式输出](../concepts/streaming-output.md)。
- **多轮对话差异**：
  - DashScope 协议：依赖 `session_id` 管理状态，服务端维护上下文。
  - OpenAI 协议：必须在每次请求的 `input` 数组中**显式传入完整历史消息**（含 `assistant` 回复），服务端不维护会话状态。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


