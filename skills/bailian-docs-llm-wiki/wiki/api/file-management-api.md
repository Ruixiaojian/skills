# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 RESTful 接口完成，需使用有效的 API Key 进行身份认证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）提供统一的文件托管能力。其核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/csv` 等格式）
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考文档 (raw/api-reference.md)](../../raw/api-reference.md) 的最新版本为准；若二者冲突，以后者为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | binary | 是 | 待上传的原始文件字节流 |
| `purpose` | form-data body | string | 否 | 文件用途，当前仅支持 `"assistants"`（用于助手场景），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（删除/查询时） | 平台分配的唯一文件标识符，长度为 24 位十六进制字符串 |
| `limit` / `offset` | query | integer | 否 | 列举时分页控制，默认 `limit=20`, `offset=0` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **获取文件列表**：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. 所有响应均为 JSON 格式，成功时 HTTP 状态码为 `200`（查询/列举）或 `201`（上传），失败时返回标准错误结构（含 `code` 和 `message` 字段）。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`
- 每个项目（project_id）下最多存储 **10,000 个文件**；达到上限后上传将失败
- 已删除文件无法恢复，且其 `file_id` 不可复用
- 文件内容在上传后**不自动解析或索引**，需显式调用对应模型接口（如 `qwen-vl` 或 `knowledge-retrieval`）触发处理
- 上传时若未指定 `purpose`，系统默认设为 `"assistants"`，但该字段暂无实际路由作用——此行为与 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 描述一致，但未来可能扩展用途，请勿硬编码依赖该值

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


