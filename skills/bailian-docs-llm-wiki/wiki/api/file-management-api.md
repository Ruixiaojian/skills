# file management api

file management api 提供对百炼平台托管文件的全生命周期管理能力，支持上传、查询、列举和删除等核心操作。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源等场景。所有操作均需通过 HTTP 接口调用，并依赖有效的 API Key 认证。

## 支持的模型/功能

file management api **不绑定具体大模型**，而是作为独立的基础设施服务存在，所有接入百炼平台的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）均可复用已上传的文件 ID 进行后续调用（例如在 `messages` 中引用 `file_id`）。其功能严格限定为：  
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/csv` 等格式）  
- `GET /v1/files/{file_id}`：获取单个文件元信息  
- `GET /v1/files`：分页列举当前项目下的全部文件  
- `DELETE /v1/files/{file_id}`：删除指定文件  

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未说明文件上传后是否自动触发解析，但实际使用中，仅当文件被用于知识库或 RAG 场景时，才需额外调用 `/v1/knowledge_bases/{kb_id}/files` 接口触发切片与向量化；此行为不属于 file management api 职责范围。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的原始文件二进制流 |
| `purpose` | form-data | string | 否 | 取值为 `"assistants"`（默认）或 `"vision"`；影响后续模型调用时的兼容性，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（除列表外） | 文件唯一标识符，由平台生成并返回于上传响应中 |
| `limit` / `offset` | query | integer | 否 | 列举接口分页参数，默认 `limit=20`, `offset=0` |

## 使用方式

1. **上传文件**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `size`, `created_at` 等字段。

2. **引用文件**：  
   在调用 `/v1/chat/completions` 时，可在 `messages` 中以 `{"type": "file_id", "file_id": "file-xxx"}` 形式引用，无需重新上传。

3. **清理资源**：  
   删除前请确认该 `file_id` 未被任何知识库或运行中的任务引用，否则将返回 `409 Conflict` 错误。参考 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的错误码说明。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`  
- 每个项目（project_id）下最多存储 **10,000 个文件**；达到上限后上传请求将失败  
- 文件上传后**不自动持久化至长期存储**：若 7 天内未被任何 API（如知识库导入、chat 调用）引用，系统可能自动清理（具体策略以控制台公告为准）  
- `purpose=vision` 仅支持图片类格式（`image/jpeg`, `image/png`），且仅限于[多模态](../concepts/multi-modal.md)模型调用；混用会导致 `400 Bad Request`  
- 删除操作不可逆，且不释放已关联的 token 消耗配额（配额按上传时计费）

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


