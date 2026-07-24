# file management api

文件管理 API 用于在百炼平台中对用户上传的文件进行生命周期管理，支持上传、查询、列举和删除等核心操作。所有文件需先通过该 API 上传后，方可被其他模型（如大模型推理、RAG 等）引用。API 设计为 RESTful 风格，基于 HTTP + JSON 协议，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

- **上传文件**：支持 `multipart/form-data` 方式上传单个文件（最大 2GB），返回唯一 `file_id`；  
- **查询文件详情**：根据 `file_id` 获取文件元信息（名称、大小、状态、上传时间等）；  
- **列举文件列表**：分页获取当前项目下所有已上传文件（默认按创建时间倒序）；  
- **删除文件**：永久移除指定 `file_id` 的文件（不可恢复）。  
> **注意**：该 API 不直接支持模型推理或内容解析，仅提供文件托管能力；如需文本提取，请配合 [文档解析 API](../../raw/model-api-reference/document-parsing-api.md) 使用。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | binary | 是（上传时） | 原始文件二进制流，`Content-Type` 应与文件实际类型一致 |
| `file_id` | string | 是（查询/删除时） | 由上传接口返回的唯一标识符，格式为 `file-xxx` |
| `limit` / `offset` | integer | 否（列举时） | 分页参数，默认 `limit=20`, `offset=0` |
| `project_id` | string | 否 | 指定项目 ID；若未传，则使用请求凭证绑定的默认项目 |

详细字段定义与响应结构请参见 [文件管理](../../raw/model-api-reference/file-management-api.md) 文档。

## 使用方式

1. **上传**：`POST /v1/files`，`Content-Type: multipart/form-data`；  
2. **查询**：`GET /v1/files/{file_id}`；  
3. **列举**：`GET /v1/files?limit=10&offset=0`；  
4. **删除**：`DELETE /v1/files/{file_id}`。  
所有请求需在 `Authorization` 头中携带 Bearer [Token](../concepts/token.md)（格式：`Bearer <api_key>`）。完整调用示例可参考 [文件管理](../../raw/model-api-reference/file-management-api.md) 中的「请求示例」章节。

## 限制和注意事项

- 单文件上限为 **2 GB**，超出将返回 `400 Bad Request`；  
- 文件保留期默认为 **永久**，但平台可能因合规要求清理超 365 天未访问的冷数据（具体策略以 [文件管理](../../raw/model-api-reference/file-management-api.md) 公告为准）；  
- 删除操作立即生效且不可撤销，建议业务层做好二次确认；  
- `file_id` 仅在当前 `project_id` 下有效，跨项目不可复用。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


