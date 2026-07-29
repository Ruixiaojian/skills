# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等[多模态输入](../concepts/multi-modal-input.md)，并可维护会话上下文。所有调用均需提供有效的 APP ID 及认证凭据。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但功能支持存在差异：
  - 图像输入仅在选用通义千问 VL 系列模型且完成对应配置（如智能体设为“自定义处理”，工作流模型节点入参填 `imageList`）后生效 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 文件输入**仅限智能体应用**，且需在应用内选择“全文引用”或“切片检索”文件处理方式 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 多轮对话在 DashScope API 中通过 `session_id` 实现（有效期 1 小时），而 Responses API 当前**不支持 `pre_response_id` 或 `conversation_id`**，需显式传递完整历史消息 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

- **调用模式**：
  - **同步调用**：适用于实时交互场景，API 阻塞等待结果返回；
  - **异步调用**：适用于耗时较长任务（如报告生成），立即返回任务 ID，后续通过 `retrieve` 查询状态；**异步模式不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：文档 4（新版智能体应用 API 参考）与文档 5（应用 DashScope API 参考）均描述 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 明确限定为“新版智能体应用”，而文档 5 未作此限定且标题为“智能体、工作流”，二者适用范围存在矛盾。实际生产中应以应用创建时的类型为准，并优先参考 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 的通用说明。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。若应用位于子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域，还需传入 `workspace_id`。 |
| `input` | string / array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及多模态（`input_text`/`input_image`/`input_file`）。`input_file` 仅智能体支持。 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)（默认 `false`）。启用需在工作流应用的结束节点开启“[流式输出](../concepts/streaming-output.md)”开关并重新发布 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。 |
| `background` | boolean | 否 | 是否异步执行（默认 `false`）。设为 `true` 即触发异步流程，返回任务 ID [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |
| `biz_params` | object | 否 | 用于向工作流或智能体传递自定义参数（如城市名、索引值），参数名与应用内配置必须一致 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |

## 使用方式

- **Responses API（OpenAI 兼容）**：
  - **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - **SDK 初始化**：`base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'`
  - 支持 Python/Java SDK 及 curl，兼容 OpenAI `client.responses.create()` 调用风格。

- **DashScope API（原生）**：
  - **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - **SDK 初始化**：使用 `dashscope.Application.call()`（Python）或 `ApplicationParam.builder()`（Java）
  - 支持 Python/Java/PHP/Node.js/C#/Go 多语言示例，`input.prompt` 为必填字段。

- **在线调试**：所有应用均支持通过控制台 **应用卡片 → 发布 → API 调试** 进行快速验证。

## 限制和注意事项

- **地域限制**：Responses API（同步/异步）及新版智能体 API 文档均明确标注**仅适用于华北2（北京）地域**；其他地域调用需确认 Workspace ID 是否已正确嵌入 Base URL [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询全部 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **流式与异步互斥**：`stream=true` 与 `background=true` 不可同时设置，否则请求将失败 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **会话管理**：DashScope API 的 `session_id` 机制与 Responses API 的全量消息传递是两种独立方案，不可混用。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


