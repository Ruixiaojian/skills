# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI v1 REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等路径），支持使用标准 OpenAI SDK（`openai>=1.0.0`）直接调用千问（Qwen）及第三方模型，无需修改业务代码逻辑，仅需替换 `base_url` 和 `api_key` 即可完成快速迁移。

## 在百炼平台的不同场景中如何使用

- **模型推理**：通过 `/v1/chat/completions` 调用 Qwen 文本模型（如 `qwen3.7-plus`）、多模态模型（`qwen3-vl-plus`）或第三方模型（DeepSeek、Kimi 等）；通过 `/v1/embeddings` 调用文本向量模型（`text-embedding-v4`）；通过 `/v1/rerank`（非官方 OpenAI 路径，但兼容其请求结构）调用排序模型（`qwen3-rerank`）。  
- **智能体与应用调用**：使用 `/v1/responses` 接口调用已发布的智能体（Agent）或工作流应用，自动管理对话历史、内置工具链（联网搜索、代码解释器等），并支持 `previous_response_id` 实现上下文延续。  
- **批量与文件处理**：通过 `/v1/batch`（文件输入模式）或 `/v1/chat/completions`（同步批量模式）发起异步/同步批量推理；通过 `/v1/files` 管理文档分析、切片检索等文件相关能力。  
- **会话状态管理**：使用 `/v1/conversations` 系列接口（`POST /conversations`, `GET /conversations/{id}/messages`）创建、查询和维护跨设备持久化对话会话。  
- **[多模态输入](multimodal-input.md)**：在 `messages.content` 中按 OpenAI 标准格式混合传入 `text` 与 `image_url`（支持 Data URL 或公网可访问 URL），适用于 `qwen3-vl-plus`、`QVQ` 等视觉模型（注意：`QVQ` 强制要求 `stream=true`）。

> ⚠️ 注意：并非所有百炼能力均支持 OpenAI 兼容协议。例如：Qwen-Audio、多模态 Embedding 模型（`qwen3-vl-embedding`）、`fine-tune` 微调任务、原生 DashScope 工具调用（`tool_calls` 显式解析）等，仅支持 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 | 备注 |
|------|------|------|------|------|
| `base_url` | string | **必须配置**，指向百炼兼容模式服务端点：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（推荐生产环境）<br>或 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京地域存量迁移） | ✅ | 各地域 host 不同（如 `cn-beijing`、`ap-southeast-1`），不可混用；旧域名 `dashscope.aliyuncs.com/v1` 已不推荐 |
| `api_key` | string | 阿里云 AccessKey（建议 RAM 子账号 + 最小权限策略），通过 `Authorization: Bearer <api_key>` 传递 | ✅ | 必须与 `base_url` 所属地域、计费方案（[Token](token.md) Plan / Coding Plan / 按量）匹配，否则返回 `401` |
| `model` | string | 模型 ID，大小写敏感，如 `"qwen3.7-plus"`、`"qwen3-vl-plus"`、`"text-embedding-v4"` | ✅ | 需严格匹配[支持列表](https://help.aliyun.com/zh/model-studio/developer-reference/openai-compatibility)；视觉模型不可用于纯文本接口 |
| `messages` | array | 对话消息数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`（字符串或含 `type`/`text`/`image_url` 的对象） | ✅（除 `completions`） | `system` 消息在 Chat Completions 中有效；`Responses` 接口自动处理历史，无需手动拼接 |
| `stream` | boolean | 是否启用流式响应 | ❌（默认 `false`） | `true` 时返回 SSE 格式（`data: {...}`）；`QVQ` 等流式专用模型强制要求 `true` |
| `stream_options` | object | 流式增强选项 | ❌ | 设置 `{"include_usage": true}` 可在最后一 chunk 返回 token 统计 |
| `dimensions` | integer | 向量维度（仅部分 embedding 模型支持） | ❌ | 如 `text-embedding-v4` 支持 `512`/`1024`/`2048`；`v1`/`v2` 不支持该参数 |
| `previous_response_id` | string | 上一轮 Responses 响应的 `id`（UUID 格式） | ❌（多轮必需） | 用于 `Responses` 接口自动续写，**非 `output.msg_xxx` 字段** |
| `input` | string/array | 应用调用时的核心输入 | ✅ | 字符串（单轮文本）或消息数组（多轮/多模态）；文件需先上传获取 URL 再传入 |

## 面向开发者：简洁实用提示

- ✅ **快速上手**：复制控制台生成的 `WorkspaceId` 和 `API Key`，5 行 Python 即可调用：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key="sk-xxx")
  resp = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
  print(resp.choices[0].message.content)
  ```

- ✅ **调试优先**：所有 OpenAI 兼容接口均支持控制台「API 调试」页面实时测试，无需编码验证参数与响应结构。

- ⚠️ **避坑指南**：
  - `tools` 字段在 `Responses` 接口下由服务端自动触发并注入结果，**不返回 `tool_calls`，也不需要你手动调用工具函数**；
  - 流式响应解析需适配 SSE（`data:` 前缀），而非 JSON Lines；
  - 地域隔离严格：北京地域的 Key 不能用于新加坡 endpoint，反之亦然；
  - 模型限流按主账号合并计算，快照版模型（如 `qwen-plus-2025-07-28`）额度显著低于稳定版（如 `qwen3.7-plus`）。

- 📦 **SDK 选择**：优先使用 `openai>=1.0.0` 官方 SDK（兼容性最佳）；若需高级功能（如文件上传、批量任务管理），可搭配 `dashscope` SDK 混合使用。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


