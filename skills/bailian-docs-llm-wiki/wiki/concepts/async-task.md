# 异步任务模式

异步任务模式是百炼平台针对耗时较长的生成类任务所采用的调用模式，其核心流程为**"创建任务 → 获取 task_id → 轮询或接收通知获取结果"**。与同步调用不同，异步模式下客户端无需保持长连接等待，适用于处理时间从数十秒到数分钟不等的生成任务。

## 适用场景

在百炼平台中，以下场景采用异步任务模式：

| 场景 | 典型模型 | 任务耗时 |
|------|---------|---------|
| **视频生成** | 万相 2.7、可灵 Kling、爱诗 PixVerse、数字人等 | 1～5 分钟 |
| **3D 模型生成** | Tripo-H3.1、Tripo-P1.0 | 数十秒至数分钟 |
| **图像生成与编辑**（旧版模型） | wanx-v1、wanx2.1-imageedit、背景生成等 | 数秒至数十秒 |
| **应用调用** | 智能体/工作流（Responses API 的 `background` 模式） | 视应用复杂度而定 |

> **说明**：较新的图像生成模型（如 qwen-image-2.0、wan2.6-t2i、z-image-turbo）已支持同步调用，无需异步模式。音乐生成（Fun-Music）支持同步和流式两种方式，同样无需异步轮询。

## 调用流程

### 步骤 1：创建任务

向对应的服务端点发送 POST 请求，**必须**在请求头中包含 `X-DashScope-Async: enable`，否则将报错：

> "current user api does not support synchronous calls"

```bash
curl -X POST '<服务端点URL>' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "<模型名称>",
    "input": { ... },
    "parameters": { ... }
}'
```

请求成功后返回 `task_id`，用于后续查询。

### 步骤 2：轮询查询结果

使用 `task_id` 调用统一的任务查询接口：

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

建议轮询间隔为 **15 秒**，根据任务状态决定是否继续轮询。

## 任务状态流转

```
PENDING（排队中） → RUNNING（处理中） → SUCCEEDED（成功）/ FAILED（失败）
                                       ↘ CANCELED（已取消）
```

| 状态 | 说明 |
|------|------|
| `PENDING` | 任务已提交，等待调度执行 |
| `RUNNING` | 任务正在处理中 |
| `SUCCEEDED` | 任务完成，可从响应中获取结果 |
| `FAILED` | 任务失败，响应中包含错误信息 |
| `CANCELED` | 任务已被手动取消 |
| `UNKNOWN` | task_id 不存在或已过期 |

## 任务管理接口

| 操作 | 方法与路径 | 说明 |
|------|-----------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 根据 task_id 查询任务状态与结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 支持按时间、模型、状态等条件筛选 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持取消 `PENDING` 状态的任务 |

以上接口的限流均为 **20 QPS**。

## 关键参数与配置

### 必需请求头

| Header | 值 | 说明 |
|--------|---|------|
| `X-DashScope-Async` | `enable` | 启用异步模式，缺失将报错 |
| `Authorization` | `Bearer sk-xxxx` | 百炼 API Key |
| `Content-Type` | `application/json` | 固定值 |

### 重要约束

| 项目 | 说明 |
|------|------|
| **task_id 有效期** | 24 小时，超时后查询返回 `UNKNOWN` 状态 |
| **结果下载链接有效期** | 因场景而异，通常为 2～24 小时，请及时下载 |
| **查询 QPS 限制** | 默认 20 QPS，频繁轮询可能触发限流 |
| **避免重复创建** | 获取 task_id 后应轮询结果，不要重复提交相同任务 |
| **跨账号限制** | 查询接口仅能查询当前 API Key 所属主账号下的任务 |

## 替代轮询：任务完成通知

频繁轮询会浪费资源并可能触发限流。百炼支持通过事件总线（EventBridge）主动推送任务完成通知，收到通知后只需一次查询即可获取结果。

| 推送方式 | 适用场景 |
|---------|---------|
| **HTTP 回调 URL** | 通用场景，需提供公网或 VPC 可达的 HTTP 接口 |
| **RocketMQ** | 对消息可靠性要求高的场景，支持失败重试 |

- **事件源**：`acs.dashscope`
- **事件类型**：`dashscope:System:AsyncTaskFinish`

## 最佳实践

1. **合理设置轮询间隔**：视频生成等长任务建议 15 秒以上，避免触发限流。
2. **生产环境使用回调通知**：高并发场景下优先使用 EventBridge 回调替代轮询。
3. **及时下载结果文件**：生成的文件

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [music generation references](../api/music-generation-references.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)

