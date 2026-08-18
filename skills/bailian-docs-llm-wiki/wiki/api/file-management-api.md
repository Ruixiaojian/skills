# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理输入文件等场景。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，所有接入百炼平台的模型（如 Qwen 系列、Yi 系列及自定义微调模型）均可复用已上传文件的 `file_id` 进行后续调用（例如在 `messages` 中引用 `{"file_id": "xxx"}`）。当前支持的功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：查询单个文件元信息
- `GET /v1/files`：分页列举用户全部文件
- `DELETE /v1/files/{file_id}`：删除指定文件

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考：文件上传](../../raw/model-api-reference/file-upload.md) 中的最新说明为准；后者新增了对 `.xlsx` 和 `.md` 的支持，但该扩展尚未在所有区域部署，建议上传前先调用 `HEAD /v1/files/supported-types` 探测。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流，字段名必须为 `file` |
| `purpose` | form-data | string | 否 | 用途标识，可选值：`assistants`（用于助手）、`batch`（用于批量任务）、`fine-tune`（用于微调）；默认为 `assistants` |
| `file_id` | path | string | 是（除上传外） | 文件唯一标识符，由平台生成并返回于上传响应中 |
| `limit` | query | integer | 否 | 列举时每页数量，默认 20，最大 100 |
| `after` | query | string | 否 | 分页游标，值为上一页响应中的 `last_id` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `{"id": "file-xxx", "filename": "document.pdf", "purpose": "assistants", ...}`。

2. **在模型请求中引用**：将返回的 `file_id` 嵌入 `messages` 的 `content` 字段，如：
   ```json
   { "role": "user", "content": [{"type": "file", "file_id": "file-xxx"}] }
   ```

3. **清理资源**：调用 `DELETE /v1/files/{file_id}` 后，该文件将不可再被任何 API 引用；已用于运行中的任务（如正在执行的 `batch` 作业）的文件，删除将失败并返回 `409 Conflict`。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`。
- 每个账户默认最多存储 **10,000 个文件**；达到限额后上传将失败，需先删除旧文件。
- 文件内容仅作存储与解析，**不自动触发向量化或索引**；如需检索，请配合 [知识库 API](../../raw/knowledge-base/kb-api.md) 显式创建知识库并导入。
- 删除操作不可逆，且不释放已关联到活跃任务中的文件——此行为与 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 描述一致，但 [批量任务指南](../../raw/batch/batch-jobs.md) 补充说明：若文件正被 `batch` 任务读取，删除请求会阻塞至任务完成，而非立即报错。
- 所有文件在平台内默认私有，仅创建者可访问；暂不支持跨账号共享或权限细粒度控制。该限制已在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中明确声明。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


