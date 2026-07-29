# 异步任务

异步任务是百炼平台为处理长耗时模型推理（如文生图、文生视频、3D生成、语音识别等）而设计的核心执行机制：调用方发起请求后立即获得唯一 `task_id`，无需阻塞等待结果，后续通过轮询或事件通知方式获取最终输出。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wanx-v1`、`wanx-sketch-to-image-lite`、`shoemodel-v1` 等模型**必须**使用异步模式；即使支持同步的模型（如 `wan2.6-t2i`），在高分辨率或多图批量生成时也建议切至异步以提升稳定性。
- **视频生成**：所有 Video Generation API（包括万相2.7、Kling、PixVerse、Vidu、数字人等）**强制异步**，请求头必须携带 `X-DashScope-Async: enable`，否则返回明确错误。
- **3D生成**：Tripo 模型（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）**仅支持异步**，不提供同步接口，且地域强约束于华北2（北京）。
- **多模态大模型推理**：当调用 `qwen-vl-plus`、`qwen-audio-plus` 等支持文件输入的模型，且输入含大尺寸图像/音频/视频时，平台自动降级为异步任务（即使请求未显式声明），避免超时失败。
- **文件解析与知识库构建**：虽非模型推理本身，但大文件（如百页PDF）的文本结构化解析过程也以异步任务形式执行，可通过 `task_id` 查询解析进度与结果。

> ✅ **统一行为**：所有异步任务均遵循「创建 → 查询/监听 → 获取结果」三步流程，`task_id` 是贯穿全生命周期的唯一凭证。

## 关键参数和配置

| 参数/配置 | 说明 | 注意事项 |
|-----------|------|----------|
| `task_id` | 异步任务全局唯一标识符（UUID格式），由创建接口返回 | 必须妥善保存；用于轮询、取消、下载结果；有效期通常为 24 小时（3D/视频任务）或 48 小时（部分图像任务） |
| `X-DashScope-Async: enable` | **必需请求头**，显式声明启用异步模式 | 缺失将导致 `400 Bad Request` 或 `synchronous calls not supported` 错误；不可与同步端点混用 |
| 轮询间隔 | 建议 ≥15 秒（3D）、≥30 秒（视频）、≥5 秒（图像） | 频繁轮询易触发限流；生产环境应结合指数退避策略 |
| 事件通知（推荐） | 配置 HTTP 回调 URL 或 RocketMQ 主题接收 `dashscope:System:AsyncTaskFinish` 事件 | 替代轮询，降低延迟与请求压力；需自行实现幂等处理（同一 `task_id` 可能重复推送） |
| 结果有效期 | 图像 URL 通常 24 小时，3D/视频资源 URL 通常 2 小时 | 务必在有效期内完成下载或持久化；过期后需重新查询任务获取新链接 |

## 面向开发者，简洁实用

- **不要轮询，优先用事件**：在服务端部署 HTTP 回调或 RocketMQ 消费者，监听 `AsyncTaskFinish` 事件，这是最高效、最可靠的方式。
- **`task_id` 是你的主键**：所有异步操作（查询、取消、结果下载）都依赖它——请记录到数据库或日志，并设置 TTL 清理策略。
- **检查请求头**：务必确认 `X-DashScope-Async: enable` 已设置，且 `Content-Type: application/json` 正确；漏掉任一都会失败。
- **地域与模型严格匹配**：异步任务的 `task_id` 只能在创建时使用的地域（如 `cn-beijing`）和 Workspace ID 下查询；跨地域调用 `GET /api/v1/tasks/{task_id}` 返回 `UNKNOWN`。
- **错误处理要覆盖三种状态**：  
  - `status: "QUEUED"` / `"RUNNING"` → 继续等待；  
  - `status: "SUCCEEDED"` → 解析 `output` 字段（含图片/视频/GLB URL、预览图、元数据）；  
  - `status: "FAILED"` → 查看 `error.code` 和 `error.message`（如 `InvalidParameter`, `ResourceNotReady`, `QuotaExceeded`）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [file management api](../api/file-management-api.md)


