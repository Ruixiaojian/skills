# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源管理。所有操作均需通过 HTTP REST 接口调用，并使用标准的 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖任何大模型**，也不关联特定模型版本；其功能独立于 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 所述的底层存储服务。当前支持四项核心功能：  
- `POST /v1/files`：上传文件（支持 `text/plain`、`application/json`、`application/pdf`、`.csv`、`.xlsx` 等格式）  
- `GET /v1/files/{file_id}`：查询单个文件元信息（含状态、大小、上传时间等）  
- `GET /v1/files`：分页列举当前 API Key 所属账户下的全部文件  
- `DELETE /v1/files/{file_id}`：永久删除指定文件（不可恢复）

> **注意**：部分旧版文档中提及“文件可绑定至特定模型实例”，该描述已过时；实际文件为全局账户级资源，与模型实例无绑定关系，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | `multipart/form-data` body | File | 是 | 待上传的二进制文件对象（`POST /v1/files` 专用） |
| `purpose` | `multipart/form-data` body | string | 否 | 当前仅支持 `"assistants"`（用于后续与助手功能集成），其他值将被忽略 |
| `file_id` | URL path | string | 是（`GET/DELETE /v1/files/{file_id}`） | 文件唯一标识符，由平台生成并返回于上传响应中 |
| `limit` | query | integer | 否 | 列举时每页最大条目数，默认 20，上限 100 |
| `after` | query | string | 否 | 分页游标，值为上一页响应中的 `last_file_id` |

## 使用方式

1. **上传文件**（示例 cURL）：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `200 OK` 及包含 `id`、`filename`、`status`（通常为 `"uploaded"`）的 JSON 对象。

2. **查询与列举**：直接构造 GET 请求，无需额外 body；响应中 `status` 字段可能为 `"uploaded"`、`"processing"` 或 `"error"`，仅 `uploaded` 状态文件可用于后续功能（如知识库构建）。  
   > **注意**：`processing` 状态表示文件正在解析（如 PDF 文本提取），此过程异步完成，轮询间隔建议 ≥2s；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

3. **删除文件**：发送 DELETE 请求后，文件立即从列表中移除且无法恢复，但后台清理可能延迟数秒。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`  
- 每个账户最多保留 **10,000 个文件**；达到上限后上传新文件将失败（`400 Bad Request`）  
- 文件名中禁止包含 `/`, `\`, `..` 等路径遍历字符，否则返回 `400`  
- 已删除文件的 `file_id` 不可复用，且无法通过 API 恢复  
- 所有文件默认保留 **90 天**（自最后访问或操作时间起），超期后自动清理（此策略可能调整，以实际平台公告为准）

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


