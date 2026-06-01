# 异步任务模式

异步任务模式是百炼平台针对耗时较长的 AI 生成任务所采用的调用机制。其核心流程为"**创建任务 → 获取 task_id → 轮询或回调获取结果**"，将任务提交与结果获取解耦，避免长时间阻塞连接。

## 适用场景

百炼平台中以下类型的 API 采用异步任务模式：

| 场景 | 典型模型 / 功能 | 任务耗时参考 |
|------|----------------|-------------|
| **视频生成** | 万相 2.7、可灵、爱诗 PixVerse、数字人等 | 1–5 分钟 |
| **3D 模型生成** | Tripo-H3.1、Tripo-P1.0 | 分钟级 |
| **图像生成与编辑** | 万相 V1、wanx2.1-imageedit、背景生成等旧版模型 | 秒级至分钟级 |
| **应用调用** | 智能体 / 工作流的异步执行（Responses API 中 `background=true`） | 视应用复杂度而定 |

> **说明**：较新的图像生成模型（如 qwen-image-2.0、wan2.6-t2i、z-image-turbo）已支持同步调用，无需使用异步模式。音乐生成（Fun-Music）同样支持同步及 SSE 流式调用，不依赖异步任务轮询。

## 调用流程

### 步骤 1：创建任务

向对应的模型接口发送 POST 请求，**必须**在请求头中包含 `X-DashScope-Async: enable`，否则会收到错误 `"current user api does not support synchronous calls"`。

```bash
curl -X POST '<模型对应的接口地址>' \
    -H 'X-DashScope-Async: enable' \
    -H 'Authorization: Bearer $DASHSCOPE_API_KEY' \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "<模型名称>",
        "input": { ... },
        "parameters": { ... }
    }'
```

成功后返回 `task_id`，有效期为 **24 小时**。

### 步骤 2：轮询查询结果

使用返回的 `task_id` 轮询任务状态：

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H 'Authorization: Bearer $DASHSCOPE_API_KEY'
```

建议轮询间隔 **15 秒**。任务完成后，响应体中包含生成结果（如文件下载 URL）。

### 步骤 3（可选）：接收完成通知代替轮询

频繁轮询会浪费资源并可能触发限流（默认 20 QPS）。百炼支持通过事件总线（EventBridge）主动推送任务完成通知，收到通知后只需一次查询即可获取结果。

| 通知方案 | 适用场景 | 特点 |
|---------|---------|------|
| HTTP 回调 URL | 通用场景 | 简单直接，需公网或 VPC 可达的 HTTP 接口 |
| RocketMQ | 对消息可靠性要求高的场景 | 支持消息无丢失和失败重试 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`。

## 任务状态

任务在生命周期内依次经历以下状态：

| 状态 | 含义 |
|------|------|
| `PENDING` | 排队中，等待调度 |
| `RUNNING` | 处理中 |
| `SUCCEEDED` | 任务成功，可获取结果 |
| `FAILED` | 任务失败，响应中包含错误信息 |
| `CANCELED` | 已取消（仅 `PENDING` 状态的任务可取消） |
| `UNKNOWN` | 任务不存在或已过期 |

## 任务管理接口

| 操作 | 方法 | 路径 | 限流 |
|------|------|------|------|
| 查询单个任务 | `GET` | `/api/v1/tasks/{task_id}` | 20 QPS |
| 批量查询任务 | `GET` | `/api/v1/tasks/` | 20 QPS |
| 取消任务 | `POST` | `/api/v1/tasks/{task_id}/cancel` | 20 QPS |

批量查询支持按时间、模型、状态等条件筛选。查询接口可查询当前 API Key 所属主账号下的所有任务，但无法跨主账号查询。

## 关键参数与配置

| 参数 / 请求头 | 必选 | 说明 |
|--------------|------|------|
| `X-DashScope-Async: enable` | 是 | 启用异步模式的请求头，缺失将报错 |
| `Authorization: Bearer <API Key>` | 是 | 鉴权，各地域 API Key 独立 |
| `Content-Type: application/json` | 是 | 固定值 |
| `X-DashScope-OssResourceResolve: enable` | 条件 | 当输入使用 `oss://` 临时 URL 时必须设置 |

## 注意事项

- **task_id 有效期**：24 小时，过期后查询返回 `UNKNOWN` 状态。
- **结果文件有效期**：因场景而异（如 3D 模型下载链接 2 小时、音频 URL 24 小时），请及时下载保存。
- **避免重复创建任务**：获取 `task_id` 后应通过轮询或回调等待结果，重复提交相同请求会产生额外计费。
- **地域隔离**：各地域的 API Key 与请求地址独立，不可混用，跨地域调用将导致鉴权失败。
- **轮询频率控制**：查询接口默认限流 20 QPS，高并发场景建议使用 EventBridge 回调通知方案。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [music generation references](../api/music-generation-references.md)
- [image generation](../api/image-generation.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)


