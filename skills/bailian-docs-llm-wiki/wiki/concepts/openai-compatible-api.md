# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI v1.x 协议规范（如 `/v1/chat/completions`），支持使用标准 OpenAI SDK（如 `openai>=1.0.0`）直接调用千问（Qwen）及第三方模型，无需修改业务逻辑代码，实现零改造快速迁移。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套覆盖[多模态](multimodal.md)、多任务、多部署形态的协议族，在以下核心场景中统一启用：

- **基础模型调用**：通过 `Chat Completions` 接口调用 `qwen-plus`、`qwen-vl-plus`、`text-embedding-v4` 等模型，适用于通用对话、视觉理解、向量检索等任务；
- **智能体（Agent）集成**：通过 `Responses API`（`/compatible-mode/v1/responses`）调用已发布的智能体应用，自动启用联网搜索、代码解释器等内置工具链，开发者无需解析 `tool_calls`，服务端完成全流程编排；
- **[多模态](multimodal.md)输入**：在 `messages` 中嵌入 `image_url`（支持 OSS 临时 URL 或公网可访问地址），兼容 OpenAI Vision 规范，适用于 Qwen-VL、QVQ 等视觉模型；
- **批量与异步处理**：  
  - *Batch File*：上传 JSONL 文件发起异步批量推理（支持 256K 上下文模型）；  
  - *Batch Chat*：同步批量请求，适用于数据标注等非实时场景；  
- **开发工具接入**：直接配置为 Cursor、Qwen Code、Cherry Studio、Cline 等 IDE/桌面工具的后端，仅需设置 `base_url` 和 `api_key` 即可启用；
- **文件与知识增强**：通过 `Files API` 上传文档供 Qwen-Long/Qwen-Doc-Turbo 模型问答，或作为微调/批量任务输入。

> ✅ **关键提示**：所有 OpenAI 兼容接口均要求 `base_url` 显式指向地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不推荐使用通用 `dashscope.aliyuncs.com` 域名用于生产环境。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | 必填。必须为地域+业务空间专属地址，格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 北京、新加坡、东京、弗吉尼亚、法兰克福等地域均支持；`{WorkspaceId}` 需从控制台获取；不同地域 Key 不互通 |
| `api_key` | string | 必填。须与 `base_url` 所属地域、计费方案（[Token](token.md) Plan / Coding Plan / 按量）严格匹配 | [Token](token.md) Plan 个人版/团队版 Key 仅限编程工具使用，禁止用于 Dify/n8n 等工作流平台 |
| `model` | string | 必填。必须使用百炼平台支持的模型 ID（如 `qwen3.7-plus`、`qwen-vl-plus`、`text-embedding-v4`），不可混用 OpenAI 原生模型名 | `qwen-coder-turbo` 仅支持 `completions` 接口；`Qwen-Audio` 不支持 OpenAI 兼容协议 |
| `messages` | array | 必填（Chat/Responses）。格式为 `[{ "role": "user/system/assistant", "content": "..." }]`；支持 `image_url` 字段传图 | `system` 消息在 Chat Completions 中有效；`Responses API` 自动管理历史，支持 `previous_response_id` 续接 |
| `stream` | boolean | 否。设为 `true` 启用 SSE 流式响应（返回 `data: {...}`） | `stream_options={"include_usage": true}` 可在流末尾返回 token 统计 |
| `max_tokens` | integer | 否。控制输出长度上限（截断式），不影响模型内部生成长度 | 实际最大值受模型上下文窗口限制（如 `qwen3.8-max` 为 32768 tokens） |
| `temperature` / `top_p` | number | 否。二选一设置采样策略，避免同时指定 | 范围：`temperature [0.0, 2.0]`，`top_p [0.0, 1.0]`；`repetition_penalty` 仅 DashScope 原生接口支持 |
| `seed` | integer | 否。设置后提升结果确定性，推荐用于测试与调试 | |
| `stop` | string or array | 否。支持字符串或 token ID 列表，用于主动终止生成 | |

## 面向开发者，简洁实用

- ✅ **三步上手**：  
  1. 控制台开通百炼 → 创建业务空间 → 获取 `WorkspaceId` 和对应地域的 `API Key`；  
  2. 安装最新 OpenAI SDK：`pip install -U openai`；  
  3. 初始化客户端并调用：  
     ```python
     from openai import OpenAI
     client = OpenAI(
         api_key="sk-xxx",
         base_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
     )
     # 文本对话
     resp = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
     # 智能体调用（Responses）
     resp = client.responses.create(input="分析这份财报", app_id="app-xxx")
     ```

- ⚠️ **避坑指南**：  
  - 错误 401：检查 `api_key` 是否与 `base_url` 地域/计费方案匹配；  
  - 错误 400：确认 `model` 名称拼写正确（如 `glm-5.2` 在部分工具中需转为 `glm-5-2`）；  
  - 工具调用失败：确保使用 `Responses API`（非 `chat.completions`），且应用已启用对应工具；  
  - 图像无法识别：上传图片前先调用 `/api/v1/files` 获取临时 OSS URL，并确保 `image_url` 可公开访问；  
  - 流式无响应：检查 HTTP 客户端是否正确解析 SSE（`data:` 前缀），推荐使用 `openai` SDK 自动处理。

- 📌 **生产建议**：  
  - 使用业务空间专属 `base_url`，保障 SLA 与独立配额；  
  - 对高并发场景，复用 `aiohttp.ClientSession` 或 `requests.Session`；  
  - 敏感业务务必显式设置 `temperature=0.0` 和 `seed` 保证稳定性；  
  - 异步任务（图像/视频生成）优先配置 HTTP 回调或 RocketMQ 事件总线，避免轮询。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


