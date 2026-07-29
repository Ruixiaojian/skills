# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件以及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖或绑定任何大模型**，其功能独立于模型服务（如 Qwen、Baichuan 等），仅面向文件资源本身。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `multipart/form-data`，最大单文件 2GB）
- `GET /v1/files/{file_id}`：获取指定文件元信息（不含内容）
- `GET /v1/files`：分页列举当前 API Key 所属账户下的全部文件（默认 limit=20）
- `DELETE /v1/files/{file_id}`：软删除文件（文件内容保留 7 天后自动清理）

> **注意**：原始文档中未说明软删除策略，但 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 明确指出“删除操作为逻辑删除”，而其他旧版文档曾误述为立即物理清除；请以该文档为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是（上传时） | 待上传的二进制文件流 |
| `purpose` | form-data | string | 否 | 当前仅支持 `"assistants"`（用于后续 Assistant API），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（除列表外） | 平台返回的全局唯一文件 ID，格式为 `file_...` |
| `limit`, `after` | query | integer/string | 否 | 分页参数，`after` 为上一页末尾的 `file_id`，用于游标分页 |

## 使用方式

1. **上传文件**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/files \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **查询与列举**：  
   列举全部文件后，取响应中 `data[].id` 作为 `file_id` 调用详情接口；注意响应字段 `status` 可能为 `"uploaded"` 或 `"error"`，需主动检查。

3. **删除文件**：  
   删除后无法恢复，且关联的 Assistant 或 RAG 应用将因文件不可用而报错；建议先确认无活跃引用。该行为在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中有明确警示。

## 限制和注意事项

- 单账户最多保留 **10,000 个文件**（按 `file_id` 计数），超出后上传将返回 `400 TooManyFiles`；
- 文件名在上传时会被标准化（去除控制字符、截断超长部分），原始文件名仅存于 `filename` 字段，不保证路径语义；
- 不支持断点续传、分片上传或并行上传同一文件；重复上传相同内容会生成新 `file_id`；
- `purpose=assistants` 是当前唯一有效值，设置为 `batch` 或 `fine-tune` 将静默忽略——此行为与早期文档描述不一致，以最新 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 为准。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


