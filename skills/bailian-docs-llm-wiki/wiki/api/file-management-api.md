# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举账户下所有文件以及删除指定文件。该 API 与模型调用解耦，不参与推理流程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖或绑定任何大模型**，其功能独立于 `qwen-max`、`qwen-plus` 等推理模型。它面向所有开通百炼服务的用户开放，适用于 RAG 场景中知识库文件预处理、[多模态](../concepts/multi-modal.md)输入文件准备等通用文件托管需求。具体支持的操作详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 关键参数

- `file`: `multipart/form-data` 格式上传的二进制文件（必填，单文件 ≤ 100 MB）  
- `purpose`: 字符串，当前仅支持 `"file-extract"`（用于后续文本提取）或 `"assistants"`（用于助手[工具调用](../concepts/tool-use.md)），其他值将被拒绝  
- `filename`: 可选，显式指定文件名（若未提供，将从 `file` 的 `Content-Disposition` 中解析）  
- `id`: 文件唯一标识符（UUID v4 格式），由平台在上传成功后返回，后续 `GET /files/{id}` 和 `DELETE /files/{id}` 均需此 ID  

> **注意**：原始文档 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 未明确说明 `purpose` 的取值约束，但实际接口校验严格限定为上述两个值；生产环境请以 API 返回的 `400 Bad Request` 错误提示为准。

## 使用方式

1. **上传文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，携带 `file` 和 `purpose`  
2. **查询文件详情**：`GET https://dashscope.aliyuncs.com/api/v1/files/{id}`  
3. **列举文件**：`GET https://dashscope.aliyuncs.com/api/v1/files?limit=20&offset=0`（支持分页）  
4. **删除文件**：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{id}`  

所有响应均为 JSON 格式，含 `id`、`filename`、`purpose`、`status`（`uploaded`/`processed`/`error`）、`created_at` 等字段。完整请求示例和响应结构参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 100 MB；超过将返回 `413 Payload Too Large`  
- 同一账户下最多保留 10,000 个 `uploaded` 或 `processed` 状态的文件；超出后上传将失败  
- 已关联至活跃知识库或助手的文件无法直接删除，需先解除关联  
- `purpose=assistants` 的文件在 7 天无引用后自动清理（`status` 变为 `expired`），此行为未在原始文档中说明，属平台隐式策略

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


