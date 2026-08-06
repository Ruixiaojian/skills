# file management api

file management api 提供对百炼平台托管文件的全生命周期管理能力，支持上传、查询、列举和删除等核心操作。该 API 与模型推理解耦，适用于预处理数据、知识库文档管理及[多模态](../concepts/multimodal.md)输入准备等场景。所有操作均需通过 `Authorization` 头携带有效 API Key 进行身份验证。

## 支持的模型/功能

- **通用文件管理**：所有接入百炼平台的服务均可调用本 API 管理自有文件（不绑定特定模型）  
- **[多模态](../concepts/multimodal.md)前置支持**：为 `qwen-vl-plus`、`qwen2-audio` 等[多模态](../concepts/multimodal.md)模型提供文件引用基础能力（详见 [文件管理](../../raw/model-api-reference/file-management-api.md)）  
- **知识库集成**：上传后的文件可直接用于创建或更新知识库条目（参考 [文件管理](../../raw/model-api-reference/file-management-api.md) 中的 `file_id` 关联逻辑）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | binary | 是 | 文件二进制流（multipart/form-data） |
| `filename` | string | 是 | 原始文件名（含扩展名，如 `report.pdf`） |
| `purpose` | string | 否 | 用途标识，当前仅支持 `retrieval`（默认值），其他值将被忽略（见 [文件管理](../../raw/model-api-reference/file-management-api.md)） |
| `file_id` | string | — | 响应返回字段，全局唯一，后续操作必需 |

> **注意**：`purpose` 参数在部分旧版 SDK 文档中被误标为支持 `fine-tuning`，但实际后端仅识别 `retrieval`；该不一致已在最新 [文件管理](../../raw/model-api-reference/file-management-api.md) 中修正。

## 使用方式

1. **上传文件**：`POST /v1/files`，使用 `multipart/form-data` 提交  
2. **查询单个文件**：`GET /v1/files/{file_id}`  
3. **列举文件**：`GET /v1/files?limit=20&offset=0`（支持分页）  
4. **删除文件**：`DELETE /v1/files/{file_id}`（异步执行，成功即返回 204）

所有接口均遵循 RESTful 规范，响应体为 JSON 格式，错误码参照标准 HTTP 状态码（如 401、404、422）。

## 限制和注意事项

- 单文件大小上限：100 MB  
- 每日上传配额：免费版 100 次/日，企业版按合同约定（配额详情见控制台）  
- 已删除文件不可恢复，且 `file_id` 不可复用  
- 文件元数据（如 `filename`）仅在上传时生效，后续无法修改  
- 列举接口默认按 `created_at` 降序排列，不支持自定义排序字段  

> **注意**：若上传后立即调用 `GET /v1/files/{file_id}` 返回 `404`，通常因文件仍在异步处理队列中，建议等待 1–2 秒后重试——该行为在 [文件管理](../../raw/model-api-reference/file-management-api.md) 中有明确说明。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


