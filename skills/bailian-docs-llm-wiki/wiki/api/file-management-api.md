# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为独立的基础设施服务存在，所有接入百炼平台的模型（如 Qwen 系列、Baichuan 系列等）均可复用已上传的文件 ID。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.md` 等格式）
- `GET /v1/files/{file_id}`：获取单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[原文标题](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持格式，但实际接口校验逻辑与 [原文标题](../../raw/model-api-reference/file-management-api.md) 的 `/v1/files` 响应示例一致，确认支持上述扩展名；若上传不支持格式，将返回 `400 Bad Request` 及 `unsupported_file_type` 错误码。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的原始文件二进制流 |
| `purpose` | form-data | string | 否 | 用途标识，取值为 `assistants`（默认）、`batch` 或 `fine-tune`；不同用途影响后续调用上下文可见性，详见 [原文标题](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（除 POST 外） | 文件唯一标识符，由平台生成并返回于上传响应中 |

## 使用方式

1. **上传文件**（以 cURL 示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `id`, `filename`, `bytes`, `created_at`, `purpose` 字段。

2. **引用文件**：在调用 `/v1/chat/completions` 或 `/v1/assistants/runs` 时，通过 `file_ids: ["file-xxx"]` 传入已上传文件 ID，无需重复上传。

3. **清理资源**：建议定期调用 `DELETE /v1/files/{file_id}` 清理不再使用的文件，避免配额占用。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（超过将返回 `413 Payload Too Large`）
- 每个项目默认配额为 **100 GB 总存储空间**，超出后上传失败
- 删除文件后，其 `file_id` 在 24 小时内仍可能被缓存，期间关联的 assistant run 或 batch job 仍可访问（行为与 [原文标题](../../raw/model-api-reference/file-management-api.md) 描述一致）
- `purpose=assistants` 的文件仅对同一 project 下的 assistants 可见；`purpose=batch` 文件仅限 batch inference 使用，跨 purpose 不互通

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


