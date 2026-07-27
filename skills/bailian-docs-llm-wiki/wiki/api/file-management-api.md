# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 RESTful 接口完成，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

文件管理 API **不依赖特定大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列、以及 [文件解析增强型模型](../../raw/model-api-reference/file-parsing-enhanced-models.md)）提供统一的文件存储与引用能力。当前支持的功能包括：
- `POST /v1/files`：上传文件（支持 `.pdf`, `.txt`, `.docx`, `.xlsx`, `.csv`, `.pptx`, `.jpg`, `.png`, `.mp3`, `.wav` 等格式）
- `GET /v1/files/{file_id}`：获取单个文件元信息
- `GET /v1/files`：分页列举用户名下全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：部分旧版文档（如 [原始文档 v1.2](../../raw/model-api-reference/file-management-api.md)）中提及的 `PATCH /v1/files/{file_id}` 修改文件元数据功能已废弃，实际接口返回 `405 Method Not Allowed`，请以 [最新 API 参考](../../raw/model-api-reference/file-management-api.md) 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | `form-data` | binary | 是 | 待上传的文件二进制内容（仅 `POST /v1/files`） |
| `purpose` | `form-data` | string | 否 | 文件用途，取值 `assistants`（用于助手）、`batch`（批处理）、`fine-tune`（微调）；默认为 `assistants` |
| `file_id` | URL path | string | 是 | 文件唯一标识符（UUID 格式），由上传响应返回 |
| `limit` | query | integer | 否 | 列举时每页数量，默认 20，最大 100 |
| `after` | query | string | 否 | 分页游标，值为上一页最后一个 `file_id` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `size`, `created_at`, `status`（`uploaded` 表示就绪可用）。

2. **在其他 API 中引用文件**：  
   上传成功后，将返回的 `file_id` 填入对应模型请求体（如 `messages[].file_ids` 或 `input.files`），无需额外鉴权。具体字段位置详见 [模型输入规范](../../raw/model-api-reference/input-format.md)。

3. **删除前确认状态**：  
   删除前建议先 `GET /v1/files/{file_id}` 确认 `status === "uploaded"`，避免误删处理中或失败的文件。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（[文件管理 API](../../raw/model-api-reference/file-management-api.md) 明确规定）；
- 每个账户默认最多存储 **10,000 个文件**，超出后需主动清理（配额可通过控制台申请提升）；
- 文件保留期为 **永久**，但若连续 180 天未被任何模型请求引用，系统可能自动归档（归档后仍可访问，但响应延迟略高）；
- 上传时若 `purpose=assistants`，文件将自动触发 OCR（图片/PDF）或文本提取（Office 文档），结果异步生成，可通过 `GET /v1/files/{file_id}` 查看 `parsed_status` 字段；
- > **注意**：[文件管理 API](../../raw/model-api-reference/file-management-api.md) 中“支持 `.zip` 解压上传”描述为过时信息——当前版本不支持自动解压，`.zip` 文件将作为普通二进制文件存储，需自行解压后分别上传。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


