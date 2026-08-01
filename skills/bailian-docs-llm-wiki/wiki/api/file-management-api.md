# file management api

文件管理 API 提供对百炼平台托管文件的全生命周期操作能力，包括上传、查询、列举和删除。该 API 与模型调用解耦，适用于预处理数据、构建知识库或管理训练/推理输入资源等场景。所有操作均通过 HTTP REST 接口完成，需携带有效的 `Authorization` 请求头。

## 支持的模型/功能

文件管理 API **不依赖具体大模型**，而是作为平台级基础设施服务，为所有支持文件输入的模型（如 Qwen 系列、Baichuan 系列及自定义微调模型）提供统一的文件存储与引用能力。其核心功能包括：
- `POST /v1/files`：上传文件（支持 `text/plain`, `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等格式）
- `GET /v1/files/{file_id}`：根据 ID 查询单个文件元信息
- `GET /v1/files`：分页列举当前项目下的全部文件（默认按创建时间倒序）
- `DELETE /v1/files/{file_id}`：删除指定文件（不可恢复）

> **注意**：部分旧版 SDK 文档中提及的 `/v1/files/upload` 路径已废弃，应以 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中定义的 `/v1/files` 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 待上传的原始文件字节流 |
| `purpose` | form-data | string | 否 | 文件用途，取值为 `assistants`（用于助手）、`vision`（用于多模态推理）或 `batch`（用于批量任务），默认为 `assistants`；该字段影响后续模型调用时的兼容性 |
| `file_id` | path | string | 是（查询/删除时） | 文件唯一标识符，由平台生成并返回于上传响应中 |
| `limit` / `after` | query | integer / string | 否 | 分页参数，`limit` 默认为 20，`after` 为上一页最后一个 `file_id` |

上传成功后响应体包含 `id`, `filename`, `size`, `purpose`, `created_at` 等字段，详见 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md)。

## 使用方式

1. **上传文件**（示例 cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "purpose=assistants"
   ```

2. **引用文件**：上传成功后获得 `file_id`，可在后续模型请求中通过 `"file_id": "file-xxx"` 形式传入（如 `messages` 中的 `file_ids` 字段），具体用法参见各模型的 input schema 文档。

3. **清理资源**：建议在任务完成后主动调用 `DELETE /v1/files/{file_id}` 释放存储空间；未被任何模型调用引用的文件将在 30 天后自动清理。

## 限制和注意事项

- 单文件大小上限为 **512 MB**；超出将返回 `400 Bad Request`；
- 每个项目下最多保留 **10,000 个文件**；达到上限后上传将失败，需先清理；
- 文件内容仅作存储与传递，**平台不执行 OCR、文本提取或格式转换**；PDF/Word 等二进制文件需由下游模型自行解析；
- 删除操作立即生效且不可撤销，请确认无关联任务正在运行；  
- 上传时若未指定 `purpose`，默认设为 `assistants`，但部分视觉模型（如 Qwen-VL）要求显式设置 `purpose=vision`，否则调用会失败 —— 此行为已在 [文件管理 (raw/model-api-reference/file-management-api.md)](../../raw/model-api-reference/file-management-api.md) 中明确说明。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


