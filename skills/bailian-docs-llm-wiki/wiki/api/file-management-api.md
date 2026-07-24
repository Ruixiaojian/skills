# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源。所有操作均通过 HTTP REST 接口完成，需携带有效的 `Authorization` 头。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列、以及百炼自研的 embedding 和 RAG 模型）提供统一文件支撑。其核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（支持 `limit` 和 `offset` 参数）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确列出支持的 MIME 类型，实际支持范围以 [API 参考文档 v2.3](../../raw/model-api-reference/api-reference-v2.3.md) 为准；后者补充了 `.xlsx` 和 `.md` 格式支持，但该扩展尚未在所有区域部署，建议首次使用前通过 `OPTIONS /v1/files` 验证。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | binary | 是 | 待上传的原始文件流（非 base64） |
| `purpose` | form-data body | string | 否 | 文件用途，可选值：`assistants`（默认）、`batch`、`fine-tune`；不同用途影响后续调用权限，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（删除/查询时） | 平台分配的唯一文件标识符，形如 `file_abc123xyz` |
| `limit`, `offset` | query | integer | 否 | 列举接口分页参数，默认 `limit=20`, `offset=0` |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/files \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `file_id` 和 `status: "uploaded"`。

2. **后续调用**：获得 `file_id` 后，可在 `messages` 或 `file_ids` 字段中直接引用（如用于 `chat/completions` 的 `file_ids` 参数），无需额外鉴权。

3. **错误处理**：常见错误码包括 `400 Bad Request`（格式不支持）、`401 Unauthorized`（token 无效）、`404 Not Found`（`file_id` 不存在），详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的「错误响应」章节。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（免费版）或 **2 GB**（企业版），超出将返回 `413 Payload Too Large`；
- 文件保留期默认为 **永久**，但若连续 90 天未被任何 API 调用引用（如未出现在 `messages` 或 `file_ids` 中），系统可能自动清理；
- 删除操作立即生效且不可逆，调用后 `file_id` 将无法再用于任何模型请求；
- `purpose=assistants` 的文件可被 `chat/completions` 直接引用；`purpose=fine-tune` 的文件仅限微调任务使用，混用将导致 `400` 错误。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


