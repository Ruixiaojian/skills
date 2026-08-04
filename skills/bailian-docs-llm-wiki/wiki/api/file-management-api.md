# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理输入文件等场景。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，是独立于模型推理的服务模块。它支持以下核心功能：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/json`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：按 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的所有文件（默认返回最近 20 个）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，但实际接口校验逻辑与 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 所述一致；建议以运行时 `415 Unsupported Media Type` 错误响应为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流（`multipart/form-data`） |
| `purpose` | form-data | string | 否 | 用途标识，当前仅支持 `"assistants"`（用于助手知识库），其他值将被忽略 |
| `file_id` | path | string | 是（查询/删除时） | 文件唯一 ID，由上传成功响应返回的 `id` 字段提供 |
| `limit` | query | integer | 否 | 列举时每页数量，默认 20，最大 100 |
| `after` | query | string | 否 | 分页游标，值为上一页响应中的 `last_id` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `size`, `created_at` 等字段。

2. **后续操作**：使用返回的 `id` 调用 `GET /v1/files/{file_id}` 或 `DELETE /v1/files/{file_id}`。

3. **批量管理**：通过 `GET /v1/files?limit=50` 获取文件列表后，可结合业务逻辑筛选或清理过期文件。

详细请求/响应结构请参考 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **100 MB**；超出将返回 `413 Payload Too Large`
- 每个项目（project）下最多存储 **10,000 个文件**；达到上限后上传将失败
- 已删除文件无法恢复，且其 `file_id` 不可复用
- `purpose` 参数暂不校验也不影响行为，未来可能启用，建议始终传 `"assistants"`
- 文件内容不会被自动解析或索引，需配合 `assistants` 或 `retrieval` 相关 API 显式触发处理

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


