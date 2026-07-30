# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖任何大模型**，其功能独立于模型服务，适用于所有开通百炼平台权限的账号。支持的核心功能包括：  
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/jsonl` 等格式）  
- `GET /v1/files/{file_id}`：获取单个文件元信息（不含内容）  
- `GET /v1/files`：分页列举当前账号下所有文件（默认按创建时间倒序）  
- `DELETE /v1/files/{file_id}`：永久删除文件及其关联元数据  

> **注意**：文档中提及“支持 `.docx` 格式”为过时描述；当前版本仅支持 [原文标题](../../raw/model-api-reference/file-management-api.md) 明确列出的 MIME 类型，`.docx` 尚未开放解析与索引能力。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流（`POST /v1/files`） |
| `purpose` | form-data | string | 否 | 当前仅支持 `"assistants"`（预留扩展字段，其他值将被忽略） |
| `file_id` | path | string | 是（除列表外） | 文件唯一标识符，由平台生成，长度为 24 位十六进制字符串 |
| `limit` | query | integer | 否 | 列举接口每页最大返回数，默认 20，上限 100 |
| `after` | query | string | 否 | 分页游标，值为上一页响应中的 `last_id` |

所有请求必须携带 `Content-Type: multipart/form-data`（上传）或 `application/json`（其余接口），且 `file` 字段名不可更改。详细字段约束见 [原文标题](../../raw/model-api-reference/file-management-api.md)。

## 使用方式

1. **上传文件**：构造 `multipart/form-data` 请求，`file` 字段传入二进制内容，可选传 `purpose`；成功返回 `file_id`, `filename`, `size`, `created_at` 等字段。  
2. **查询/列举/删除**：使用返回的 `file_id` 调用对应接口，注意 `DELETE` 为幂等操作，重复调用返回 204。  
3. **错误处理**：常见错误码包括 `400 Bad Request`（格式不支持）、`404 Not Found`（`file_id` 不存在）、`401 Unauthorized`（密钥无效）。完整错误定义参见 [原文标题](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`。  
- 每个账号最多存储 **10,000 个文件**；达到上限后上传将失败（`403 Forbidden`）。  
- 已删除文件不可恢复，且其 `file_id` 不再可查——即使重传同名文件，也会生成新 `file_id`。  
- 文件内容仅在上传时做基础校验（如 PDF 结构完整性），**不自动触发 OCR 或文本提取**；若需后续用于 RAG，请显式调用 `files.process`（该功能尚未公开，详见内部文档）。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


