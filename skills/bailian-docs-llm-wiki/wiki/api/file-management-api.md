# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型推理解耦，适用于预处理数据、知识库文档管理等场景。所有操作均需通过 `Authorization` 头携带有效 API Key 进行身份验证。

## 支持的模型/功能

文件管理 API 不依赖具体大模型，为平台级基础设施能力，所有接入百炼的模型（如 Qwen 系列、Baichuan 系列等）均可复用已上传文件的 `file_id`。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `multipart/form-data`）
- `GET /v1/files/{file_id}`：查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下所有文件
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确说明删除操作是否触发关联知识库的自动同步更新；实际行为以 [知识库文档管理规范](../../raw/kb/document-sync-policy.md) 为准，建议在删除前手动解除知识库绑定。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 是 | 上传文件二进制内容（`multipart/form-data` 中的 `file` 字段） |
| `purpose` | string | 否 | 文件用途，目前仅支持 `"assistants"`（默认值），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | string | 是（路径参数） | 文件唯一标识符，由平台生成，格式为 `file_abc123xyz` |
| `limit`, `after`, `before` | integer/string | 否 | 列举接口分页参数，`limit` 默认为 20，最大 100 |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **获取文件 ID 后用于其他服务**：返回 JSON 中的 `id` 字段可直接传入知识库创建或模型调用的 `file_ids` 数组中，例如：
   ```json
   { "id": "file_abc123xyz", "filename": "report.pdf", "status": "processed" }
   ```

3. **错误处理**：常见状态码包括 `400`（文件过大或类型不支持）、`404`（`file_id` 不存在）、`401`（认证失败）。详细错误码见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 512 MB；超出将返回 `400 Bad Request`
- 支持格式：`.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.md`（其他格式可能解析失败）
- 文件上传后状态为 `"uploaded"`，经后台异步处理后变为 `"processed"`；仅当状态为 `"processed"` 时方可用于模型或知识库
- 删除文件后，其 `file_id` 将立即失效，所有引用该 ID 的请求返回 `404`；但平台保留元数据 7 天用于审计（不可恢复）

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


