# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理所需资源等场景。所有操作均需通过 `Authorization: Bearer <token>` 认证，并遵循统一的 RESTful 接口规范。

## 支持的模型/功能

文件管理 API **不依赖特定大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列、以及 [文件解析增强型模型](../../raw/model-api-reference/file-parsing-enhanced.md)）提供底层文件支撑。核心功能包括：
- `POST /v1/files`：上传文件（支持 `multipart/form-data` 或 base64 编码）
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（可选 `purpose` 过滤）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：部分旧版文档中提及的 `/v1/files/upload_url` 预签名上传接口已废弃，当前仅支持直接上传；请以 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中的最新路径为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | file | 是 | 待上传的二进制文件（最大 512 MB） |
| `purpose` | form-data body 或 query | string | 否 | 文件用途，取值 `fine-tune`、`assistants` 或 `batch`；未指定时默认为 `assistants` |
| `file_id` | path | string | 是（除 POST 外） | 平台生成的唯一文件标识符，格式如 `file_abc123xyz` |
| `limit` / `after` | query | integer / string | 否 | 分页参数，`limit` 默认 20，`after` 为上一页末尾的 `file_id` |

详细字段定义与响应结构见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 使用方式

1. **上传文件**（示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```

2. **获取文件列表**（带分页）：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?limit=10&after=file_xyz789" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```

3. 所有成功响应均为 JSON 格式，含 `id`、`filename`、`bytes`、`created_at`、`purpose` 等字段；错误响应遵循统一错误码体系（如 `401 Unauthorized`、`404 File not found`）。完整请求/响应示例参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `400 Bad Request`。
- 每个项目（project）下最多存储 **10,000 个文件**；达到上限后需先清理再上传。
- 已被模型引用的文件（如用于知识库或微调任务）**无法直接删除**，需先解除关联。
- 文件上传后立即可用，但异步解析（如 PDF 文本提取）可能延迟数秒至数分钟，具体取决于文件类型与大小。
- 删除操作不可逆，且不触发事件回调；建议业务侧自行记录关键操作日志。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


