# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 独立于模型推理调用，专用于文件资源管理，适用于预处理数据集、上传知识库文档或临时工件等场景。所有操作均需通过 `Authorization` 请求头携带有效 API Key 进行身份验证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是平台级基础设施能力，所有接入百炼的项目均可使用（无论是否启用模型服务）。当前支持以下核心功能：  
- `POST /v1/files`：上传文件（支持 `multipart/form-data` 和 base64 编码两种方式）  
- `GET /v1/files/{file_id}`：按 ID 查询单个文件元信息  
- `GET /v1/files`：分页列举当前项目下所有文件（支持 `limit` 和 `offset`）  
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）  

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确说明删除操作的幂等性，但实测多次删除同一 `file_id` 返回 `404`，建议业务层自行处理重试逻辑。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data body | binary | 是（上传时） | 文件原始二进制内容，最大支持 512 MB |
| `purpose` | form-data body | string | 否 | 取值为 `assistants`（默认）、`vision` 或 `batch`；影响后续在对应场景中的可用性，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（查询/删除） | 由平台生成的唯一文件标识符，格式如 `file-abc123xyz` |
| `limit`, `offset` | query | integer | 否（列举时） | 默认 `limit=20`, `offset=0`；`offset` 超过总数量返回空列表 |

## 使用方式

1. **上传文件**（示例 cURL）：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **获取文件列表并解析 `file_id`**：  
   响应中 `data[].id` 即为 `file_id`，可用于后续查询或删除。注意 `data` 为数组，即使仅一个文件也需索引访问。

3. **在其他 API 中引用文件**：  
   上传后获得的 `file_id` 可直接用于 `assistants` 或 `batch` 相关接口（如创建 assistant 时传入 `file_ids: ["file-xxx"]`），无需额外转换。具体字段映射规则参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `413 Payload Too Large`  
- 每个项目默认配额为 **100 GB 总存储空间**，超限后上传失败（错误码 `403 Forbidden`）  
- 文件上传后立即可读，但异步处理（如 OCR、文本切片）可能延迟数秒至数分钟，查询 `status` 字段为 `"processed"` 方可安全使用  
- 已删除文件无法恢复，且其 `file_id` 不会复用；重复上传相同文件将生成新 `file_id`  
- `purpose=vision` 的文件仅限视觉模型调用，`purpose=assistants` 的文件不可用于 `batch` 推理任务——此约束未在原始文档中显式强调，需开发者自行校验用途一致性

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


