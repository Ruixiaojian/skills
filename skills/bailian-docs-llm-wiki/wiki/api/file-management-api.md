# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举用户文件列表及删除文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖任何大模型**，其功能独立于模型服务，适用于所有开通百炼平台权限的账号。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/json`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）  
- `GET /v1/files/{file_id}`：获取指定文件元信息  
- `GET /v1/files`：分页列举当前用户全部文件（默认按 `created_at` 降序）  
- `DELETE /v1/files/{file_id}`：删除文件（不可恢复）  

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，但实际接口校验逻辑与 [文件上传限制说明 (raw/platform-guides/file-upload-limits.md)](../../raw/platform-guides/file-upload-limits.md) 一致；后者为权威来源，建议以该文档为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流（仅 `POST /v1/files`） |
| `purpose` | form-data | string | 否 | 当前仅支持 `"assistants"`（预留扩展字段，其他值将被忽略） |
| `file_id` | path | string | 是 | 文件唯一标识（UUID 格式），由平台在上传成功后返回 |
| `limit` | query | integer | 否 | 列举时每页数量，默认 `20`，最大 `100` |
| `after` | query | string | 否 | 分页游标（上一页响应中的 `last_id` 值） |

## 使用方式

1. **上传文件**（示例 cURL）：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@./report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `bytes`, `created_at`, `status`（值为 `"uploaded"`）等字段。

2. **查询/列举/删除**：使用返回的 `file_id` 构造对应请求路径。  
   注意：所有文件操作均作用于当前 API Key 所属租户空间，跨账号不可见。

3. **错误处理**：常见状态码包括 `400`（格式/大小超限）、`404`（`file_id` 不存在）、`401`（鉴权失败）。详细错误结构见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（参见 [文件上传限制说明 (raw/platform-guides/file-upload-limits.md)](../../raw/platform-guides/file-upload-limits.md)）  
- 每个账号总存储配额默认 **10 GB**，超出后上传将失败（配额可联系商务提升）  
- 已删除文件无法恢复，且其 `file_id` 不可复用  
- 文件内容不被自动解析或索引，如需用于 RAG 场景，须另行调用向量化或知识库 API  
- `purpose` 字段当前无实际作用，未来可能用于策略路由，**请勿硬编码为其他值**

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


