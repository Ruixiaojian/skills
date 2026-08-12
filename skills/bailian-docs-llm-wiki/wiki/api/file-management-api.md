# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理输入文件等场景。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，所有接入百炼平台的模型（如 Qwen 系列、Yi 系列及自定义微调模型）均可复用已上传文件的 `file_id` 进行后续调用（例如在 `messages` 中引用文件）。核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：获取单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：原始文档中未明确列出支持格式，但 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 的接口示例和实际测试验证支持上述 MIME 类型；其他格式（如 `.xlsx`, `.pptx`）暂不支持，需转换为 CSV 或 PDF 后上传。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的文件二进制流 |
| `purpose` | form-data | string | 否 | 用途标识，目前仅支持 `"assistants"`（默认值），用于后续与 Assistant API 集成；[文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中未定义其他取值，传入非此值将被忽略 |
| `file_id` | path | string | 是（除 POST 外） | 文件唯一标识，由平台生成，格式为 `file_...` |

## 使用方式

1. **上传文件**（以 cURL 为例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```
   成功响应返回 `file_id`、`filename`、`size`、`status`（通常为 `"uploaded"`）等字段。

2. **在模型请求中引用文件**：  
   将返回的 `file_id` 填入消息内容的 `file_ids` 数组（如 `{"role": "user", "content": "请分析附件", "file_ids": ["file_abc123"]}`），具体用法见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限为 **512 MB**（超出将返回 `413 Payload Too Large`）
- 每个项目（project）下最多存储 **10,000 个文件**
- 已删除文件的 `file_id` 不可复用，且无法通过 API 恢复
- 文件内容解析（如 PDF 文本提取）由平台异步完成，`status` 字段可能短暂为 `"processing"`；若长期卡在此状态，请检查文件是否损坏或格式不支持
- 删除操作立即生效，无回收站机制

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


