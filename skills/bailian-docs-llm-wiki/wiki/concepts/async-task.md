# 异步任务

异步任务是百炼平台针对耗时较长的生成类请求所采用的调用模式。与同步调用不同，异步任务将请求拆分为"创建任务"和"查询结果"两个步骤，客户端提交请求后立即获得一个 `task_id`，随后通过该 ID 轮询或接收通知来获取最终结果。

## 适用场景

在百炼平台中，以下场景默认或推荐使用异步任务：

| 场景 | 典型耗时 | 说明 |
|------|---------|------|
| **视频生成** | 1–5 分钟 | 文生视频、图生视频、数字人等所有视频生成任务均强制异步 |
| **3D 模型生成** | 数十秒至数分钟 | Tripo 文生 3D、图生 3D 等任务强制异步 |
| **图像生成（旧版模型）** | 数秒至数十秒 | 万相 V1、图像编辑、背景生成等采用异步；较新模型（qwen-image-2.0、wan2.6-t2i 等）已支持同步调用 |
| **应用调用** | 视应用复杂度而定 | OpenAI 兼容 Responses API 通过 `background: true` 参数开启异步执行 |

## 调用流程

### 步骤 1：创建任务

向对应的模型接口发送 POST 请求，**必须**在请求头中包含 `X-DashScope-Async: enable`，否则将报错 `"current user api does not support synchronous calls"`。

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-t2v-2026-04-25",
    "input": {
        "prompt": "一只小猫在月光下奔跑"
    }
}'
```

成功后返回 `task_id`，有效期 **24 小时**，超时后查询将返回 `UNKNOWN` 状态。

### 步骤 2：查询结果

使用统一的任务查询接口轮询任务状态：

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

建议轮询间隔 **15 秒**，避免过于频繁触发限流。

## 任务状态

任务在生命周期中经历以下状态流转：

```
PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）
```

| 状态 | 说明 |
|------|------|
| `PENDING` | 任务已提交，等待调度执行。此状态下可取消任务 |
| `RUNNING` | 任务正在处理中 |
| `SUCCEEDED` | 任务成功完成，可从响应中获取生成结果 |
| `FAILED` | 任务执行失败，响应中包含错误信息 |
| `CANCELED` | 任务已被取消 |
| `UNKNOWN` | task_id 不存在或已过期 |

## 任务管理接口

| 操作 | 方法 | 路径 | 限流 |
|------|------|------|------|
| 查询单个任务 | `GET` | `/api/v1/tasks/{task_id}` | 20 QPS |
| 批量查询任务 | `GET` | `/api/v1/tasks/` | 20 QPS |
| 取消任务 | `POST` | `/api/v1/tasks/{task_id}/cancel` | 20 QPS |

> 批量查询支持按时间、模型、状态等条件筛选。查询接口可查询当前 API Key 所属主账号下的所有任务，但无法跨主账号查询。

## 任务完成通知

频繁轮询会造成资源浪费并可能触发限流。百炼支持通过事件总线（EventBridge）主动推送任务完成通知，收到通知后仅需一次查询即可获取结果。

| 接收方式 | 适用场景 |
|---------|---------|
| **HTTP 回调 URL** | 通用场景，需公网或 VPC 可达的 HTTP 接口 |
| **RocketMQ** | 对消息可靠性要求高的场景，支持失败重试 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`。

## 关键配置与注意事项

| 配置项 | 说明 |
|--------|------|
| `X-DashScope-Async: enable` | 创建异步任务时必须携带的请求头 |
| task_id 有效期 | 24 小时，超时后系统自动清理 |
| 结果下载链接有效期 | 因模型而异，通常为 2–24 小时，请及时下载保存 |
| 查询限流 | 20 QPS，建议使用回调通知替代高频轮询 |
| 避免重复创建 | 获取 task_id 后应通过轮询获取结果，请勿对同一请求重复提交任务 |

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)
- [music generation references](../api/music-generation-references.md)

