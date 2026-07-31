# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举已上传文件及删除文件。该 API 与模型调用解耦，适用于预处理阶段的文件准备（如知识库文档、图像输入等）。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

- **通用文件管理**：支持任意 MIME 类型文件（如 `text/plain`, `application/pdf`, `image/jpeg`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`）  
- **模型协同场景**：当前仅 [Qwen-VL](../../raw/model-api-reference/qwen-vl.md)、[Qwen2-Audio](../../raw/model-api-reference/qwen2-audio.md) 和部分 RAG 相关接口（如 `/v1/kb/files`）可直接引用通过本 API 上传的 `file_id`  
- 不支持直接用于 `chat/completions` 等纯文本模型的请求体中；若需在对话中使用文件，请先调用本 API 上传并获取 `file_id`，再按对应模型文档要求传入 —— 具体字段名和位置请参考 [原文标题](../../raw/model-api-reference/file-management-api.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | binary | 是 | 表单字段，原始文件二进制流（`multipart/form-data`） |
| `purpose` | string | 否 | 用途标识，目前仅支持 `"assistants"`（默认）或 `"vision"`；不同值影响后续模型调用时的兼容性，详见 [原文标题](../../raw/model-api-reference/file-management-api.md) |
| `filename` | string | 否 | 显式指定文件名（含扩展名），若未提供则从 `Content-Disposition` 中提取 |

> **注意**：`purpose=vision` 并非所有视觉模型都支持；例如 Qwen-VL 实际接受 `purpose=assistants` 或省略该字段，而部分新模型可能要求 `purpose=vision`。请以具体模型文档为准，避免硬编码。

## 使用方式

1. **上传文件**（`POST /v1/files`）  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/files \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `file_id`（如 `file-abc123`）和元数据。

2. **查询文件**（`GET /v1/files/{file_id}`）  
   获取状态（`uploaded`/`processed`/`error`）、大小、MIME 类型等。

3. **列举文件**（`GET /v1/files?limit=20&offset=0`）  
   分页返回文件列表，按上传时间倒序排列。

4. **删除文件**（`DELETE /v1/files/{file_id}`）  
   成功后该 `file_id` 不可再被任何模型接口引用。注意：删除不可逆，且不释放配额（配额按上传量实时扣减）—— 此行为与 [原文标题](../../raw/model-api-reference/file-management-api.md) 描述一致。

## 限制和注意事项

- 单文件最大 100 MB（免费版）或 500 MB（企业版），超出将返回 `413 Payload Too Large`  
- 每日上传总配额受账号等级限制，可在控制台查看实时用量  
- 已上传但未被任何模型引用的文件，系统不会自动清理；建议业务侧自行维护生命周期  
- 文件内容仅用于模型推理输入，百炼平台不提供长期存储服务或 CDN 下载地址；如需对外分发，请自行保存原始副本

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


