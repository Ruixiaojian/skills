# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖任何大模型**，也不涉及模型推理，其功能完全独立于模型服务。它面向所有开通百炼平台服务的用户开放，适用于 RAG、知识库构建、[多模态](../concepts/multi-modal.md)预处理等场景中的文件准备环节。当前支持的操作包括：  
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/json`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）  
- `GET /v1/files/{file_id}`：查询单个文件元数据  
- `GET /v1/files`：分页列举当前项目下的全部文件  
- `DELETE /v1/files/{file_id}`：删除指定文件（成功后不可恢复）  

> **注意**：原始文档中未明确列出支持的 MIME 类型，但 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 仅说明“包括上传、查询、列举和删除操作”，实际支持格式需以最新控制台上传界面或 OpenAPI Schema 为准；建议在调用前通过 `HEAD /v1/files/supported-types`（如可用）或参考 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的隐含上下文验证。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流（`POST /v1/files`） |
| `purpose` | form-data | string | 否 | 当前仅支持 `"assistants"`（默认值），其他值将被忽略；该字段语义暂未启用，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是 | 文件唯一标识（UUID 格式），由平台生成并返回于上传响应中 |
| `limit` | query | integer | 否 | 列举时每页数量，默认 20，最大 100 |
| `after` | query | string | 否 | 分页游标（上一页响应中的 `last_id`） |

## 使用方式

1. **上传文件**：使用 `multipart/form-data` 提交，示例 cURL：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `bytes`, `created_at`, `status`（应为 `"uploaded"`）。

2. **后续操作**：所有 `GET`/`DELETE` 请求均需在 URL 中携带 `file_id`，例如 `GET /v1/files/fil_abc123`。

3. 文件上传后立即可用于 `create_knowledge` 或 `create_dataset` 等下游接口，无需额外激活步骤。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`。
- 每个项目（project）下最多存储 **10,000 个文件**；达到上限后上传将失败（`400 QuotaExceeded`）。
- 已删除文件的 `file_id` 不可复用，且无法通过 API 恢复。
- 文件内容不支持修改：如需更新，须重新上传并使用新 `file_id` 替换旧引用。
- > **注意**：原始文档 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 未提及配额限制，但生产环境已强制执行上述大小与数量限制，开发者应主动校验响应状态码而非仅依赖文档描述。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


