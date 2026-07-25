# file management api

file management api 提供对百炼平台托管文件的全生命周期管理能力，支持上传、查询、列举和删除等核心操作。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均需通过 HTTP 接口调用，并依赖有效的 API Key 和权限配置。

## 支持的模型/功能

file management api **不绑定特定大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）提供统一的文件存储与引用能力。其功能覆盖：  
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）  
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息  
- `GET /v1/files`：分页列举当前项目下的全部文件  
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）  

> **注意**：部分旧版文档中提及的 `multipart/form-data` 必须包含 `purpose=assistants` 字段，但该限制已在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中明确移除；实际请求中 `purpose` 为可选字段，仅在用于 Assistants API 场景时建议设置。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | binary | 是 | 待上传的文件二进制内容（`multipart/form-data` 中的 `file` 字段） |
| `purpose` | string | 否 | 文件用途，可选值：`assistants`、`batch`、`fine-tune`；默认为 `assistants`，不影响基础文件管理功能 |
| `file_id` | string | 是（查询/删除） | 文件唯一标识符，由上传成功响应返回的 `id` 字段提供 |
| `limit` / `after` | integer / string | 否（列举） | 分页参数，`limit` 默认为 20，最大支持 100；`after` 为上一页最后一个 `file_id` |

上传成功响应体中必含 `id`、`filename`、`bytes`、`created_at` 和 `status` 字段，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/files \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **引用文件**：上传后返回的 `file_id` 可直接用于后续模型调用（如 `messages` 中的 `file_ids` 数组），无需额外转换。

3. **错误处理**：常见状态码包括 `400`（文件格式/大小不合规）、`401`（认证失败）、`403`（权限不足）、`404`（`file_id` 不存在）。具体错误详情见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（PDF/DOCX 等二进制格式）或 **100 MB**（纯文本）；超出将返回 `400 Bad Request`  
- 每个项目（`project_id`）下最多存储 **10,000 个文件**；达到上限后需先清理再上传  
- 已删除文件无法恢复，且其 `file_id` 不会复用  
- 文件内容不会被平台自动解析或索引，如需向量化或切片，请调用 `vectorize` 或 `chunking` 相关 API 配合使用  
- `purpose=assistants` 的文件可被 `assistant` 对象直接引用，但 `purpose=batch` 或 `purpose=fine-tune` 的文件**不可用于聊天类 API**，此行为差异未在早期文档中明确说明，需以最新 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 为准

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


