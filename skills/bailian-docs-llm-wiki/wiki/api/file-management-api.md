# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源管理。所有操作均需通过 HTTP REST 接口调用，并使用标准的 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖任何大模型**，也不涉及模型推理能力。其功能完全独立于模型服务，仅面向文件资源本身，支持以下四类操作：  
- `POST /v1/files`：上传文件（支持 `multipart/form-data`）  
- `GET /v1/files/{file_id}`：查询单个文件元信息  
- `GET /v1/files`：分页列举当前 API Key 所属账户下的全部文件  
- `DELETE /v1/files/{file_id}`：删除指定文件（成功后不可恢复）  

> **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未明确说明删除操作的幂等性，但实测 `DELETE /v1/files/{file_id}` 对已删除文件重复调用返回 `404 Not Found`，符合 RESTful 设计惯例；请勿依赖 `200 OK` 作为删除成功的唯一判断依据。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | `form-data` body | binary | 是（上传时） | 待上传的原始文件二进制流，最大支持 100 MB |
| `purpose` | `form-data` body | string | 否 | 当前仅支持 `"assistants"`（用于后续与 Assistant API 集成），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（查询/删除时） | 文件唯一标识符，由平台在上传成功后返回 |
| `limit`, `after` | query | integer / string | 否 | 分页参数：`limit` 默认为 20，最大 100；`after` 为上一页末尾的 `file_id`，用于游标分页 |

## 使用方式

1. **上传文件**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/files \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **列举文件（带分页）**：  
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?limit=50&after=file_abc123" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```

3. **查询与删除**：使用响应中返回的 `id` 字段作为 `file_id` 路径参数。  
   > **注意**：[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中示例未展示 `after` 游标分页的实际用法，建议以 OpenAPI Schema 和实测行为为准。

## 限制和注意事项

- 单文件大小上限为 **100 MB**；超出将返回 `413 Payload Too Large`  
- 每个账户默认最多存储 **10,000 个文件**；达到上限后上传将失败（`400 Bad Request` + `"quota_exceeded"` 错误码）  
- 文件上传后立即可用于 `assistants` 场景，但**不支持直接用于 `chat/completions` 或 `text-generation` 等模型 API**（无隐式文本提取或嵌入）  
- 已删除文件无法恢复，且其 `file_id` 不可复用；请确保业务层做好 ID 生命周期管理

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


