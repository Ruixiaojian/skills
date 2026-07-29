# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 RESTful 接口完成，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

文件管理 API **不依赖特定大模型**，而是作为平台级基础设施服务，为所有支持[文件输入](../concepts/file-input.md)的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）提供统一的文件存储与引用能力。上传后的文件可通过 `file_id` 在 `/v1/chat/completions` 或 `/v1/embeddings` 等接口中作为 `file` 参数传入。详细功能说明见 [文件管理](../../raw/model-api-reference/file-management-api.md)。

## 关键参数

- `file`: multipart/form-data 格式上传的二进制文件（必填，支持 `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.md`）
- `purpose`: 字符串，取值为 `"assistants"`（默认）、`"batch"` 或 `"fine-tune"`，影响后续调用上下文（[文件管理](../../raw/model-api-reference/file-management-api.md) 中明确列出该字段）
- `filename`: 可选，用于覆盖原始文件名（仅当 `file` 为流式上传时建议显式指定）

> **注意**：部分旧版 SDK 文档将 `purpose` 描述为可省略且无默认值，但实际 API 行为以 [文件管理](../../raw/model-api-reference/file-management-api.md) 为准——`purpose` 默认为 `"assistants"`，且不同取值影响文件元数据校验逻辑。

## 使用方式

1. **上传文件**：`POST /v1/files`，返回含 `id`, `filename`, `purpose`, `status` 的 JSON 响应  
2. **查询单个文件**：`GET /v1/files/{file_id}`  
3. **列举文件**：`GET /v1/files?purpose=assistants&limit=20`（支持分页）  
4. **删除文件**：`DELETE /v1/files/{file_id}`（仅限 `processed` 状态文件）

所有请求需使用 `Bearer <api_key>` 认证，且 `Content-Type` 需按 multipart 正确设置边界。完整请求示例参见 [文件管理](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 512 MB（PDF/DOCX 类文档建议 ≤ 100 MB 以保障解析稳定性）  
- 同一 `purpose` 下最多保留 10,000 个文件；超出后需主动清理  
- 已被模型调用引用的文件（如正在用于 RAG 检索）无法删除，需先解除关联  
- 文件上传后状态为 `uploaded`，经后台异步处理变为 `processed` 才可用于模型调用；查询接口返回 `status` 字段用于判断就绪状态

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


