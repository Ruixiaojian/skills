# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理输入资源等场景。所有操作均通过 HTTP REST 接口完成，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）提供统一的文件存储与引用能力。其核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：部分旧版文档中提及的 `/v1/files/upload` 路径已废弃，实际应使用 `/v1/files`（见 [文件管理](../../raw/model-api-reference/file-management-api.md)），请以该文档为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | binary | 是 | 待上传的文件二进制流（`multipart/form-data`） |
| `purpose` | form-data body | string | 否 | 用途标识，目前仅支持 `"assistants"`（用于助手场景），其他值将被忽略（详见 [文件管理](../../raw/model-api-reference/file-management-api.md)） |
| `file_id` | URL path | string | 是（除列举外） | 文件唯一 ID，由平台生成并返回于上传响应中 |
| `limit`, `after` | query | integer / string | 否 | 列举时的分页参数（`after` 为上一页最后一个 `file_id`） |

## 使用方式

1. **上传文件**（示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer <api_key>" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `{"id": "file-xxx", "filename": "report.pdf", "size": 123456, ...}`。

2. **引用文件**：上传后获得的 `file_id` 可直接用于后续模型请求（如 `messages` 中的 `file_id` 字段），无需额外转换。

3. **删除前确认**：删除操作无二次确认，且删除后关联的模型调用（如已用于知识库 chunking）可能失效，请谨慎操作。更多细节参见 [文件管理](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **200 MB**；超出将返回 `413 Payload Too Large`
- 每个项目（`project_id`）最多存储 **10,000 个文件**；达到上限后上传将失败
- 文件保留期为 **永久**，除非显式删除；平台不自动清理闲置文件
- 上传时若 `purpose` 非 `"assistants"`，请求仍成功但字段被忽略——此行为与早期 SDK 文档描述存在差异，以 [文件管理](../../raw/model-api-reference/file-management-api.md) 实际实现为准
- 文件内容不支持直接读取或下载（仅可通过 `file_id` 在模型上下文中引用），如需原始内容，请在上传前自行保存副本

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


