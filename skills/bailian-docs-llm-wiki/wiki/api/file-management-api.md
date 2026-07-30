# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举已上传文件及删除文件。该 API 与模型调用解耦，不参与推理过程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <token>` 认证，并遵循平台统一的错误响应格式（详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）。

## 支持的模型/功能

- **当前仅支持通用文件管理功能**：上传（`POST /v1/files`）、查询单个文件（`GET /v1/files/{file_id}`）、列举文件列表（`GET /v1/files`）、删除文件（`DELETE /v1/files/{file_id}`）  
- 不绑定特定大模型，所有接入百炼平台的服务均可复用同一套文件 ID（`file_id`）在后续 API（如 `chat/completions` 中引用）  
- 文件类型限制见下文“限制和注意事项”，暂不支持直接调用模型进行文件解析或嵌入生成 —— 此类能力由 `embedding` 或 `document_parse` 等专用接口提供，而非本 API（参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `file` | `multipart/form-data` body | 是 | 待上传的二进制文件，`Content-Type` 应与实际文件类型一致 |
| `purpose` | form-data field | 否 | 取值为 `assistants`（默认）或 `vision`；影响后续在[多模态](../concepts/multi-modal.md)模型中的可用性，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | URL path（查询/删除时） | 是 | 由上传成功响应返回的唯一标识符，全局唯一且不可修改 |

> **注意**：`purpose=vision` 仅对支持图像输入的模型生效；若上传图像后指定 `purpose=assistants`，则无法在 `qwen-vl` 等视觉模型中直接引用，需重新上传并设为 `vision`。

## 使用方式

1. **上传文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，携带 `file` 和可选 `purpose` 字段  
2. **获取文件信息**：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}`  
3. **列举文件**：`GET https://dashscope.aliyuncs.com/api/v1/files?limit=20&offset=0`（支持分页）  
4. **删除文件**：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}`  
所有响应均为 JSON 格式，含 `id`、`filename`、`bytes`、`created_at`、`purpose` 等字段。错误码遵循 RFC 7807 规范（如 `404 Not Found` 表示 `file_id` 不存在）。

## 限制和注意事项

- 单文件大小上限：**512 MB**（超出将返回 `413 Payload Too Large`）  
- 支持格式：文本类（`.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`）、图像类（`.jpg`, `.png`, `.webp`），不支持 `.exe`, `.zip` 等可执行或压缩包格式  
- 文件保留策略：成功上传后默认**永久保留**，除非显式调用 DELETE；平台不自动清理闲置文件  
- `file_id` 一旦生成即固定，不可重用；重复上传同名文件会生成新 `file_id`  
- 删除操作**不可逆**，且删除后关联的模型调用（如已用于 `chat/completions` 的 `file_id`）将立即失效 —— 此行为与旧版文档中“软删除”描述矛盾，以当前接口实际行为为准（参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)




