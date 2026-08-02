# file management api

file management api 提供对百炼平台托管文件的全生命周期管理能力，支持上传、查询、列举和删除等核心操作。该 API 与模型调用解耦，适用于预处理数据、构建[知识库](../concepts/knowledge-base.md)或管理训练/推理所需资源。所有操作均需通过 `Authorization` 头携带有效的 API Key 进行身份验证。

## 支持的模型/功能

file management api **不绑定具体大模型**，而是作为独立的基础设施服务存在，所有接入百炼平台的模型（如 Qwen 系列、Baichuan、GLM 等）均可复用已上传的文件 ID（如 `file-xxx`）在请求中引用。当前支持的功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/csv` 等格式）
- `GET /v1/files/{file_id}`：获取单个文件元信息
- `GET /v1/files`：分页列举用户全部文件（默认按 `created_at` 降序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考：文件上传](../../raw/model-api-reference/file-upload.md) 中的最新说明为准；后者补充了 `.xlsx` 和 `.md` 的支持，但需注意 `.xlsx` 解析可能因内容复杂度导致结构化失败。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的原始文件二进制流（仅 `POST /v1/files`） |
| `purpose` | form-data | string | 否 | 用途标识，目前仅接受 `"assistants"`（用于助手场景），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（除列表接口外） | 文件唯一标识符，由平台生成，格式为 `file-` 开头的 24 位字符串 |
| `limit` | query | integer | 否 | 列表接口每页数量，默认 20，最大 100 |
| `after` | query | string | 否 | 分页游标，值为上一页返回的 `last_file_id` 或 `file_id` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `size`, `status`（`uploaded` 表示就绪）等字段。

2. **引用文件**：在调用 `/v1/chat/completions` 或 `/v1/agents/run` 时，通过 `file_ids: ["file-abc123"]` 字段传入，无需额外鉴权。

3. **删除前确认**：删除操作立即生效且不可逆，建议先通过 `GET /v1/files/{file_id}` 验证文件状态（`status` 必须为 `uploaded`）。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超过将返回 `400 Bad Request`。
- 每个账户默认配额为 **100 GB 总存储空间**，超出后上传失败（错误码 `429 Too Many Requests`）。
- 文件上传后默认保留 **90 天**，若 90 天内无任何 API 引用（如未在 chat 或 agent 请求中使用），系统自动清理；该策略在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未说明，实际行为以控制台配额页面公示为准。
- PDF 文件若含扫描图像（非文本层），将无法被后续模型解析——需预先 OCR 处理；此限制未在原始文档中体现，属平台底层能力约束。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


