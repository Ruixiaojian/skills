# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 RESTful 接口完成，需使用有效的 API Key 进行身份验证。

## 支持的模型/功能

文件管理 API **不依赖特定大模型**，而是作为独立服务存在，所有百炼平台用户（无论是否开通模型调用权限）均可使用。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/csv`, `application/json` 等格式）
- `GET /v1/files/{file_id}`：按 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考手册](../../raw/model-api-reference/file-management-api.md) 的最新版本为准；部分旧文档提及 `image/*` 格式，但当前版本**不支持图像文件上传**，该描述已过时。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制内容（仅 `POST /v1/files`） |
| `purpose` | form-data | string | 否 | 文件用途，当前仅支持 `"assistants"`（默认值），其他值将被忽略 |
| `file_id` | path | string | 是（除列表外） | 文件唯一标识符，由平台生成，长度为 24 位十六进制字符串 |
| `limit` | query | integer | 否 | 列举时每页最大数量（1–100，默认 20） |
| `after` | query | string | 否 | 分页游标，值为上一页响应中的 `last_file_id` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **获取文件列表**（带分页）：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?limit=50&after=fil_abc123..." \
     -H "Authorization: Bearer $API_KEY"
   ```

3. **删除文件**：
   ```bash
   curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/fil_def456..." \
     -H "Authorization: Bearer $API_KEY"
   ```

详细请求/响应结构及错误码请参阅 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`
- 每个项目（project_id）最多存储 **10,000 个文件**；达到上限后上传将失败（`400 Bad Request`）
- 文件上传后**立即可用**，无需额外激活步骤；但若用于知识库或助手，需在对应服务中显式引用 `file_id`
- 删除操作**不可撤销**，且会同步清除所有关联引用（如已绑定至知识库的文件被删，知识库将无法访问该文件）
- 所有接口均遵循百炼平台通用限流策略：**100 QPS / 项目**，突发请求可能触发 `429 Too Many Requests`

更多细节与变更日志，请查阅 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


