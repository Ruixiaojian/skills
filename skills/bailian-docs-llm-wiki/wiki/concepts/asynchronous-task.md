# 异步任务

异步任务是百炼平台中用于处理耗时较长模型推理的执行模式，调用方提交请求后立即获得唯一 `task_id` 并返回响应，实际计算在后台异步执行；结果需通过轮询或事件通知机制获取，避免阻塞客户端与连接超时。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是百炼平台对**高延迟、长耗时模型能力的标准承载方式**，适用于以下典型场景：

- **生成类任务**：图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wan2.7-t2v`、`kling-v3-video-generation`）、3D 模型生成（`Tripo/Tripo-H3.1`）、语音识别（`paraformer-16k-1`）等，通常需数秒至数分钟完成；
- **多模态[文件处理](file-processing.md)**：当输入为大尺寸图片、视频、音频或批量图像（如多图生3D）时，系统自动启用异步流程以保障稳定性；
- **专业工具类模型**：局部重绘（`wanx-x-painting`）、图像擦除补全、虚拟模特试穿等免费体验模型，默认采用异步模式；
- **地域强约束服务**：如 Tripo 3D 生成、部分视频编辑模型，仅支持华北2（北京）地域，且**强制异步**——缺失 `X-DashScope-Async: enable` 请求头将直接报错。

> ✅ **关键区别**：同步任务（如 `qwen-plus` 文本生成）返回快、无状态管理开销；异步任务则需开发者主动管理生命周期（查询、取消、结果下载），但能可靠支撑复杂计算。

## 关键参数和配置

| 参数/配置 | 说明 | 注意事项 |
|-----------|------|----------|
| `task_id` | 任务唯一标识（UUID 格式字符串） | **必须保存**，用于后续查询、取消或结果获取；有效期通常为 24 小时（具体以模型文档为准） |
| `X-DashScope-Async: enable` | 强制启用异步模式的 HTTP 请求头 | **所有异步接口必需显式设置**，否则返回 `400 Bad Request` 或“不支持同步调用”错误 |
| `X-DashScope-OssResourceResolve: enable` | 启用临时 OSS URL 解析（多模态场景） | 上传文件后获得的 `oss://` URL 必须配合此头才能被模型正确读取，否则调用失败 |
| 回调配置（可选） | 通过 `callback_url`（HTTP）或 `mq_topic`（消息队列）接收完成通知 | 可替代轮询，降低请求压力；但事件投递存在毫秒级延迟，**生产环境必须以 `/api/v1/tasks/{task_id}` 查询的 `task_status` 为准** |
| 轮询间隔 | 建议 ≥15 秒（视频/3D 类任务）或 ≥5 秒（图像类） | 避免高频轮询触发限流；`PENDING` 和 `RUNNING` 状态可继续轮询，`SUCCEEDED`/`FAILED` 后应停止 |

## 面向开发者，简洁实用

- ✅ **第一步：发起异步任务**  
  ```bash
  curl -X POST \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-Async: enable" \
    -H "X-DashScope-OssResourceResolve: enable" \  # 多模态必加
    -d '{"model":"wanx2.1-t2i-turbo","input":{"prompt":"一只柴犬在太空站"}}' \
    https://dashscope.aliyuncs.com/api/v1/services/aigc/text-to-image/generation
  ```
  → 响应含 `"task_id": "xxx"`，立即保存。

- ✅ **第二步：获取结果（推荐轮询）**  
  ```bash
  curl -H "Authorization: Bearer $API_KEY" \
    https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
  ```
  检查响应中的 `"task_status"` 字段：  
  - `"PENDING"` / `"RUNNING"` → 继续轮询  
  - `"SUCCEEDED"` → 从 `"output.results"` 提取 `url`（注意：结果 URL 通常有 2–24 小时有效期，需及时下载）  
  - `"FAILED"` → 查看 `"output.code"` 和 `"output.message"` 定位错误  

- ⚠️ **避坑提示**  
  - 不要依赖回调时间戳判断完成，务必校验 `task_status == "SUCCEEDED"`；  
  - `task_id` 过期后无法查询，24 小时内未轮询到结果即视为丢失；  
  - 临时文件 URL（`oss://`）仅 48 小时有效，生产环境请使用自有 OSS + STS 鉴权；  
  - 取消任务仅对 `PENDING` 状态生效，`RUNNING` 中的任务不可中断。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)


