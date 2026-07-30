# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 HTTP REST 接口完成，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列、以及 [文件解析增强型模型](../../raw/model-api-reference/file-parsing-enhanced-models.md)）提供统一的文件存储与引用能力。当前支持的文件类型包括：`text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`（.docx）, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`（.xlsx）, `text/csv`。其他类型暂不支持，详见 [原文标题](../../raw/model-api-reference/file-management-api.md) 的 MIME 类型列表。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | binary | 是 | 待上传的文件二进制流（`multipart/form-data`） |
| `purpose` | string | 否 | 文件用途，取值为 `assistants`（用于助手）、`batch`（用于批量任务）或 `fine-tune`（用于微调），默认为 `assistants`；不同用途影响后续可调用范围，具体行为参见 [原文标题](../../raw/model-api-reference/file-management-api.md) |
| `filename` | string | 否 | 显式指定文件名（若未提供，将从 `Content-Disposition` 中提取） |

> **注意**：`purpose=finetune` 在部分 SDK 版本中已被弃用，实际应使用 `purpose=fine-tune`（含连字符），请以 [原文标题](../../raw/model-api-reference/file-management-api.md) 中的最新定义为准。

## 使用方式

1. **上传文件**：`POST /v1/files`，返回 `file_id` 和元信息  
2. **查询单个文件**：`GET /v1/files/{file_id}`  
3. **列举文件**：`GET /v1/files?purpose=assistants&limit=20`（支持分页）  
4. **删除文件**：`DELETE /v1/files/{file_id}`（仅限 `uploaded` 状态文件）

所有请求需使用 `Bearer <api_key>` 认证，并设置 `Content-Type: multipart/form-data`（上传）或 `application/json`（其余操作）。

## 限制和注意事项

- 单文件大小上限为 512 MB（PDF/DOCX/XLSX）或 100 MB（纯文本/CSV）  
- 每个账户最多保留 10,000 个已上传文件（`uploaded` 状态）  
- 已被模型引用的文件（如用于知识库的文件）无法直接删除，需先解除关联  
- 文件内容在上传后自动触发异步解析（如 OCR、表格提取等），解析状态可通过 `status` 字段查询；解析失败时 `status` 为 `error`，错误详情见 `error` 字段 —— 具体状态机定义请参考 [原文标题](../../raw/model-api-reference/file-management-api.md)

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


