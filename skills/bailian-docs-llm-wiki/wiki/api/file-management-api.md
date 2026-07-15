# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询详情、列举已上传文件及删除文件。该 API 与模型调用解耦，不参与推理过程，仅用于文件资源的元数据与二进制内容管理。所有操作均需通过 `Authorization: Bearer <api_key>` 认证，并遵循平台统一的错误响应格式（详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）。

## 支持的模型/功能

- **功能范围**：当前仅支持通用文件托管，**不绑定任何特定大模型**；上传后的文件可被 `qwen-vl-plus`、`qwen2-audio` 等多模态模型在请求中通过 `file_id` 引用（如 `messages[0].image.file_id`），但文件管理 API 本身不执行模型推理。
- **操作类型**：`POST /v1/files`（上传）、`GET /v1/files/{file_id}`（查询）、`GET /v1/files`（列举）、`DELETE /v1/files/{file_id}`（删除）。
- 注意：`qwen2-audio` 模型虽支持音频文件输入，但其文件上传必须经由本 API 完成，不可直传至 `/v1/chat/completions` —— 此限制在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中明确说明。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 文件二进制流，支持 `image/*`, `audio/*`, `text/plain`, `application/pdf` 等常见 MIME 类型 |
| `purpose` | form-data | string | 否 | 取值为 `"batch"` 或 `"vision"`（默认 `"batch"`）；`"vision"` 用于图像类多模态模型（如 `qwen-vl-plus`），影响后续 token 计费逻辑 |
| `file_id` | path | string | 是（查询/删除时） | 由平台生成的唯一文件标识符，长度为 24 位十六进制字符串 |

> **注意**：文档中曾提及 `purpose=embedding` 选项，但该值已在 v2.3.0 版本后废弃，实际调用将返回 `400 Bad Request`；请以 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 当前版本为准。

## 使用方式

1. **上传文件**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/image.jpg" \
     -F "purpose=vision"
   ```
   成功响应包含 `id`, `filename`, `size`, `purpose`, `status="uploaded"`。

2. **在模型请求中引用**：  
   将返回的 `file_id` 填入消息内容，例如：
   ```json
   {
     "model": "qwen-vl-plus",
     "messages": [{"role": "user", "content": [{"type": "image_url", "image_url": {"file_id": "xxx"}}]}]
   }
   ```

## 限制和注意事项

- 单文件大小上限为 **100 MB**（PDF/音频）或 **20 MB**（图像），超出将返回 `413 Payload Too Large`；
- 每个 API Key 默认最多存储 **10,000 个文件**，超限时需先删除旧文件；
- 已删除文件不可恢复，且 `file_id` 不会复用；
- 文件上传后立即可用，但元数据同步可能存在秒级延迟，建议上传后等待 `status="uploaded"` 再引用；
- 所有文件默认保留 **90 天**，无访问行为的文件可能被系统自动清理（具体策略参见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)）。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


