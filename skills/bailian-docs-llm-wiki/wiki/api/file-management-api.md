# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举已上传文件及删除文件。该 API 与模型调用解耦，不参与推理过程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证，并遵循平台统一的错误响应格式（详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）。

## 支持的模型/功能

- **功能范围**：当前仅支持通用文件托管，**不绑定任何特定大模型**；上传后的文件可被 `qwen-vl-plus`、`qwen2-audio` 等[多模态](../concepts/multimodal.md)模型在请求中通过 `file_id` 引用（参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中“使用场景”说明）。
- **不支持的功能**：文件内容解析、格式转换、OCR 或向量化等预处理操作——这些需由客户端自行完成或调用独立的处理 API。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | binary | 是 | multipart/form-data 中的文件字段，支持格式见下文限制 |
| `purpose` | string | 否 | 取值为 `"assistants"`（默认）或 `"batch"`；影响后续模型调用时的兼容性，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `filename` | string | 否 | 建议显式指定，否则从 `Content-Disposition` 中提取；长度 ≤ 256 字符，仅允许 ASCII 字母、数字、下划线、短横线、点 |

> **注意**：原始文档中未明确 `purpose=batch` 的实际生效条件，实测发现仅当调用 `/v1/batch` 接口提交任务时才有效；若误设为 `batch` 后用于 `assistants` 场景，可能导致模型返回 `file_not_found` 错误。

## 使用方式

1. **上传文件**：`POST /v1/files`，`Content-Type: multipart/form-data`
2. **查询单个文件**：`GET /v1/files/{file_id}`
3. **列举文件**：`GET /v1/files?limit=20&after=file_abc123`
4. **删除文件**：`DELETE /v1/files/{file_id}`（成功后不可恢复）

所有响应体均为 JSON，含 `id`、`filename`、`bytes`、`created_at`、`status`（`uploaded` / `error`）等字段。上传失败时 `status` 为 `error`，且 `error.message` 提供具体原因。

## 限制和注意事项

- **文件大小**：单文件 ≤ 512 MB（超过将返回 `413 Payload Too Large`）
- **支持格式**：文本类（`.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`）、图像（`.jpg`, `.png`, `.webp`, `.gif`）、音频（`.mp3`, `.wav`, `.flac`）、视频（`.mp4`, `.mov`，仅支持元数据提取，不解析帧）  
- **保留周期**：未被任何活跃资源（如 assistant、thread、batch job）引用的文件，将在 30 天后自动清理
- **并发限制**：同一 API Key 每分钟最多发起 10 次上传请求，超出将返回 `429 Too Many Requests`

> **注意**：原始文档未提及视频文件的实际处理能力边界；根据最新平台行为，`.mp4` 文件上传成功后仅能被 `qwen-vl-plus` 作为整体输入（不支持时间戳切片），此行为与文档中“支持视频”表述存在隐含歧义，建议以实际调用结果为准。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


