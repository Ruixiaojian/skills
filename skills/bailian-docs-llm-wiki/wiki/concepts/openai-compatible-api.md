# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 接口，严格遵循 OpenAI REST API 协议（v1.x），支持使用 `openai` 官方 SDK（Python/Node.js 等）零代码修改接入千问（Qwen）系列及第三方大模型。其核心目标是降低迁移成本——开发者无需重写调用逻辑，仅需替换 `base_url` 和 `api_key`，即可将原有 OpenAI 应用快速对接百炼服务。

## 在百炼平台的不同场景中如何使用

OpenAI 兼容接口不是单一接口，而是一套按能力分层、统一协议的接口族，覆盖主流 AI 开发场景：

- **通用对话（`/chat/completions`）**：最常用入口，支持 `qwen3.7-plus`、`qwen-max`、`qwen-vl-plus` 等全部文本与多模态模型；适用于标准 LLM 调用、Agent 编排基础层。
- **智能体原生响应（`/responses`）**：`chat/completions` 的增强演进，内置联网搜索、代码解释器、网页提取等工具链，自动维护上下文，通过 `previous_response_id` 实现轻量状态管理；适合复杂任务自动化（如 Research Agent）。
- **文本补全（`/completions`）**：专为代码续写、模板填充设计，当前仅支持 `qwen-coder-turbo`（北京地域），支持前缀生成与“前后缀”中间生成模式。
- **嵌入向量（`/embeddings`）**：兼容 OpenAI Embedding 协议，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型；注意：多模态嵌入（如 `qwen3-vl-embedding`）**不支持**该协议，需用专用接口。
- **批量推理（Batch）**：提供两种形态：
  - **文件输入式 Batch**（异步）：提交 JSONL 文件，享受 50% 成本优惠；
  - **同步式 Batch Chat**：单次请求含多条消息，阻塞返回全部结果。
- **应用调用（`/apps/{APP_ID}/compatible-mode/v1/responses`）**：用于调用已发布的智能体或工作流应用，输入统一使用 `input` 字段（支持字符串、消息数组、图像、文件），无需维护会话 ID，历史由完整 `messages` 显式传递。
- **文件管理（`/files`）**：上传文档供 Qwen-Long/Qwen-Doc-Turbo 使用，`purpose` 可设为 `file-extract`（文档问答）、`batch`（批量处理）或 `fine-tune`（微调数据）。

> ⚠️ 注意：部分专用模型（如 `qwen-deep-research`、`gui-plus-*`、`tongyi-intent-detect-v3`）虽支持 OpenAI 兼容调用，但需通过 `extra_body` 传入非标准参数（如 `translation_options`、`enable_thinking`）；而 `qwen-deep-research` 等模型在部分地域**不支持** OpenAI 兼容接口，必须使用 DashScope SDK。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `base_url` | string | 服务端点，**必须匹配 API Key 所属地域** | 是 | 推荐使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>旧域名（如 `dashscope.aliyuncs.com`）仍可用但即将停用。 |
| `api_key` | string | 百炼控制台生成的 API Key | 是 | 需配置为 `Authorization: Bearer <api_key>`；**按地域独立管理，不可跨地域复用**。 |
| `model` | string | 模型 ID（如 `qwen3.7-plus`、`text-embedding-v4`） | 是 | 必须与所选接口类型匹配（例如 `/completions` 仅支持 `qwen-coder-turbo`）。 |
| `messages` / `input` / `prompt` / `input` | array / string / string / mixed | 输入内容格式依接口而异 | 是 | • `chat/completions`：`messages` 数组<br>• `responses`：`input`（字符串或消息数组）<br>• `completions`：`prompt` 字符串<br>• `embeddings`：`input`（字符串或字符串数组）<br>• `applications`：`input`（同 `responses`） |
| `stream` | boolean | 是否启用流式响应 | 否 | 默认 `false`；设为 `true` 时，SDK 需按 chunk 迭代处理；`stream_options={"include_usage": true}` 可在流末尾返回 token 统计。 |
| `extra_body` | object | 传递非 OpenAI 标准字段（如 `vl_high_resolution_images`, `translation_options`, `enable_thinking`） | 否 | 用于启用模型特有功能，详见各模型 API 文档。 |

## 面向开发者：简洁实用指南

✅ **快速上手（3 步）**  
1. 控制台创建 API Key（确保地域正确）；  
2. 获取 WorkspaceId（北京/新加坡/东京/法兰克福地域必需）；  
3. 初始化 OpenAI Client：  
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

✅ **避坑要点**  
- ❌ 不要跨地域混用 API Key 与 `base_url`；  
- ❌ `tools` / `tool_choice` / `response_format`（JSON mode）/ `parallel_tool_calls` 在 OpenAI 兼容接口中**不支持或部分生效**，需用 DashScope 原生接口；  
- ❌ `qwen-deep-research`、`Qwen-Audio` 等模型**明确不支持** OpenAI 兼容协议；  
- ✅ 生产环境建议锁定模型版本号（如 `qwen3.7-plus-20250701`），避免别名（如 `qwen3.7-plus`）因升级导致行为漂移；  
- ✅ 流式响应中 `delta.content` 可能为空字符串，客户端需忽略并持续拼接。

✅ **调试建议**  
- 使用 `curl` 直接测试：  
```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"你是谁？"}]}'
```
- 查看百炼控制台「API 调用监控」，实时验证请求成功率、延迟与 Token 消耗。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


