# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型推理解耦，适用于预处理数据、缓存上下文或管理知识库附件等场景。所有操作均需通过 `Authorization: Bearer <token>` 认证，并遵循平台统一的错误码规范。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为独立服务存在，所有百炼用户（无论使用 Qwen、Baichuan 或第三方模型）均可调用。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：按 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按 `created_at` 降序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考文档](../../raw/model-api-reference/file-management-api.md) 的最新 `Accept` 头说明为准；部分旧版 SDK 文档误将 `.xlsx` 列为支持格式，但当前服务端暂不解析 Excel 表格结构，仅允许上传（不触发自动切片），请参考 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的“限制”章节确认兼容性。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流（`multipart/form-data`） |
| `purpose` | form-data | string | 否 | 用途标识，目前仅支持 `"assistants"`（用于助手上下文），其他值将被忽略 |
| `file_id` | path | string | 是（查询/删除时） | 文件唯一 ID，由平台生成，形如 `file_abc123xyz` |
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
   成功响应返回 `file_id`、`filename`、`bytes`、`created_at` 等字段。

2. **后续调用**：获取的 `file_id` 可直接用于 `ChatCompletion` 请求的 `messages[].file_ids` 字段（需模型支持文件引用），或传入 `/v1/files/{file_id}` 查询状态。

3. **错误处理**：常见错误码包括 `400 Bad Request`（文件过大或类型不支持）、`404 Not Found`（`file_id` 不存在）、`429 Too Many Requests`（超出配额）。详细定义见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（PDF/DOCX 等文本类文件建议 ≤ 100 MB 以保障解析稳定性）
- 每个项目最多存储 **10,000 个文件**，超出后需主动清理
- 删除操作立即生效且**不可撤销**，无回收站机制
- 文件上传后默认启用内容解析（如 PDF 文本提取），但解析结果**不对外暴露 API 接口**，仅用于内部向量检索；如需原始文本，请自行解析上传前的文件
- `purpose=assistants` 是当前唯一有效值，设置其他值（如 `"fine-tune"`）将被静默忽略 —— 此行为与部分旧版文档描述不一致，以 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 为准

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


