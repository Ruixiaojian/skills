# 异步任务

异步任务是百炼平台为处理耗时较长的模型推理任务（如图像生成、视频合成、3D建模、语音识别等）而设计的非阻塞调用模式：客户端提交请求后立即获得唯一 `task_id`，无需等待结果，后续通过轮询或事件通知方式获取执行状态与输出。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wanx2.1-t2i-turbo`、`wanx2.1-kf2v-plus` 等模型必须启用异步模式。需在请求头中显式设置 `X-DashScope-Async: enable`，否则调用失败；成功响应返回 `task_id`，用于后续结果查询或取消。
  
- **视频生成**：所有视频类 API（文生视频、图生视频、参考生视频等）**强制异步**。统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 接口，`task_id` 有效期为 24 小时，超时后无法查询状态。

- **3D生成**：Tripo 模型（如 `Tripo/Tripo-H3.1`）仅支持异步调用，且**严格限定华北2（北京）地域**。提交任务后必须轮询 `GET /api/v1/tasks/{task_id}`，建议间隔 ≥15 秒；下载 URL（如 `pbr_model_url`）仅有效 2 小时，需及时保存。

- **语音与多模态任务**：`paraformer-16k-1`（语音识别）、`qwen-vl-plus`（多模态理解）等长耗时模型，在输入含大文件（如长音频、高清图）时推荐转为异步调用，避免 HTTP 超时。

- **专业模型扩展能力**：部分 `more models` 中的垂直模型（如 GUI-Plus、Qwen-OCR 大图输入）虽默认同步，但在处理高分辨率图像或复杂交互流程时，可通过业务空间配置或 SDK 参数主动切换为异步工作流（需确认模型文档是否明确支持）。

> ✅ **关键区别**：同步调用适用于毫秒级响应场景（如文本生成、意图识别），直接返回结果；异步调用适用于秒级至分钟级任务，解耦请求与响应，保障服务稳定性与资源利用率。

## 关键参数和配置

| 参数/配置 | 说明 | 开发者须知 |
|-----------|------|------------|
| `X-DashScope-Async: enable` | **必需请求头**，标识本次调用为异步模式 | 缺失该 Header 将导致 400 错误；所有异步模型均强制校验 |
| `task_id` | 任务唯一标识符（UUID 格式字符串） | 返回后立即保存；用于轮询、批量查询、取消操作；有效期统一为 **24 小时** |
| `GET /api/v1/tasks/{task_id}` | 轮询接口 | QPS 限流 20，建议轮询间隔 ≥15 秒；状态包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED` |
| `POST /api/v1/tasks/{task_id}/cancel` | 取消接口 | 仅对 `PENDING` 状态任务生效；已运行或完成的任务不可取消 |
| 事件通知（EventBridge） | 替代轮询的推荐方案 | 配置监听 `dashscope:System:AsyncTaskFinish` 事件，推送至 HTTP 回调或 RocketMQ；降低延迟与客户端负载 |
| `expire_in_seconds`（临时 Key） | 临时凭证有效期 | 若使用临时 API Key 调用异步任务，需确保其 TTL ≥ 任务预期耗时（建议设为 300–1800 秒） |

## 面向开发者，简洁实用

- ✅ **必做三件事**：  
  1. 请求头加 `X-DashScope-Async: enable`；  
  2. 提交后立刻提取并持久化 `task_id`；  
  3. 优先配置 EventBridge 事件通知，避免轮询——这是生产环境最佳实践。

- ⚠️ **避坑提示**：  
  - 不要复用 `task_id` 发起多次查询（无害但浪费）；  
  - 不要在 `task_id` 过期（24h）后尝试查询，返回 `UNKNOWN`；  
  - 下载结果 URL（如 `pbr_model_url`、`rendered_image_url`）通常仅有效 2 小时，务必及时 GET 并落盘；  
  - 异步任务不支持流式响应（`stream: true` 无效），请勿混用。

- 🛠️ **调试建议**：  
  使用 `curl -H "X-DashScope-Async: enable" ...` 快速验证异步通路；  
  在控制台「任务中心」查看实时状态与日志（需开通对应 Workspace 权限）；  
  对于失败任务，检查 `output.error.code` 和 `output.error.message` 字段，常见错误如 `INPUT_INVALID`（OSS URL 解析失败，缺 `X-DashScope-OssResourceResolve: enable`）、`QUOTA_EXHAUSTED`（额度不足）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more models](../api/more-models.md)


