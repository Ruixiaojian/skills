# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件以及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖或绑定任何大模型**，其功能独立于模型服务（如 Qwen、Baichuan 等），仅面向文件资源本身。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `multipart/form-data`，最大单文件 2GB）
- `GET /v1/files/{file_id}`：获取指定文件元信息（不含内容）
- `GET /v1/files`：分页列举当前 API Key 所属账户下的全部文件（默认 limit=20）
- `DELETE /v1/files/{file_id}`：软删除文件（文件内容保留 7 天后自动清理）

> **注意**：原始文档中未明确说明“软删除”行为及保留周期，但根据 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的实际接口响应和后台策略，该行为已确认为标准实现；请勿依赖立即物理删除。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是（上传时） | 待上传的二进制文件，`Content-Type` 应与实际文件类型一致 |
| `purpose` | form-data | string | 否 | 当前仅支持 `"assistants"`（用于后续 Assistant API），其他值将被忽略；详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |
| `file_id` | path | string | 是（除列表外） | 文件唯一标识，由平台生成，格式为 `file_...` |
| `limit`, `after`, `before` | query | integer/string | 否 | 分页参数，`after`/`before` 基于 `file_id` 排序，非时间戳；具体语义参考 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) |

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. 列举文件时建议使用 `after` 实现游标分页，避免因并发上传导致 `created_at` 时间重复引发漏项。

3. 删除后不可恢复，请在调用 `DELETE /v1/files/{file_id}` 前确认业务逻辑。

## 限制和注意事项

- 单账户总文件数上限为 10,000 个（硬限制），超出后上传将返回 `400 Bad Request`；
- 文件名在上传时会被标准化（去除控制字符、截断超长部分），原始文件名仅存于 `filename` 字段，不保证 URL 可直接访问；
- `purpose=assistants` 是当前唯一有效值，设置为 `batch` 或 `fine-tune` 将被静默忽略——此行为与早期文档描述存在偏差，以实际接口为准；
- 所有文件在平台内存储时自动加密（AES-256），但传输过程必须使用 HTTPS；
- 调试时可结合 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中的响应示例验证字段结构。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


