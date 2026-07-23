# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型推理解耦，适用于预处理数据、知识库文档、提示词附件等场景。所有操作均需通过 `Authorization` 头携带 Bearer [Token](../concepts/token.md) 进行身份认证。

## 支持的模型/功能

文件管理 API 不依赖具体大模型，是平台级基础设施能力，所有接入百炼的模型（如 Qwen 系列、Baichuan、GLM 等）均可复用已上传文件的 `file_id`。支持的核心功能包括：
- `POST /v1/files`：上传文件（支持 `multipart/form-data`）
- `GET /v1/files/{file_id}`：获取单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（支持 `purpose` 过滤）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：部分旧版 SDK 文档中提及的 `purpose=assistants` 已废弃，实际仅支持 `purpose=vision`（用于[多模态](../concepts/multi-modal.md)输入）和 `purpose=embedding`（用于向量检索），详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传文件，最大 200 MB |
| `purpose` | form-data | string | 否 | 取值为 `vision` 或 `embedding`；默认为 `embedding`；[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 明确不支持其他值 |
| `file_id` | path | string | 是（除上传外） | 平台生成的唯一文件标识，格式为 `file_...` |
| `limit`, `after` | query | integer/string | 否 | 分页参数，`limit` 默认 20，最大 100 |

## 使用方式

1. **上传文件**（示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=embedding"
   ```
2. 响应返回 `file_id` 和 `status=uploaded`，后续调用模型时可直接在 `input.files` 或 `messages.content` 中引用；
3. 列举文件时建议按 `purpose` 过滤，避免混用不同用途的文件；详情参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 200 MB，超限将返回 `400 Bad Request`；
- 同一 `file_id` 仅在 7 天内有效（若未被任何任务引用），之后自动清理；
- 删除操作立即生效且不可撤销，生产环境建议先调用 `GET /v1/files/{file_id}` 确认状态；
- 文件内容不支持修改，如需更新请重新上传并使用新 `file_id`；
- `purpose=vision` 仅支持图片（JPEG/PNG/WebP）和 PDF（含图像页），非图像 PDF 将返回 `422 Unprocessable Entity`。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


