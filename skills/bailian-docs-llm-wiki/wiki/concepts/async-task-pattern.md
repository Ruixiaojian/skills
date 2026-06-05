# 异步任务轮询模式

异步任务轮询模式是百炼平台为处理长耗时生成类请求（视频、3D、音乐、语音转写、模型调优、模型部署等）统一采用的调用范式：客户端先 `POST` 提交任务获取 `task_id` / `job_id`，再周期性 `GET` 查询任务状态，直到进入 `SUCCEEDED` 或 `FAILED` 终态后取走结果 URL 或下游标识。

## 适用场景

百炼平台中，下列场景一律走异步任务流程（同步立即返回会被显式拒绝）：

- **视频生成**：通义万相、爱诗 Pixverse、可灵 Kling、Vidu、数字人 / 特效模型。客户端拿到 `task_id`，轮询完成后下载视频，下载链接默认 24 小时有效。
- **3D 模型生成**：Tripo-H3.1 / Tripo-P1.0 的文生 3D、单图生 3D、多图生 3D。结果含 `pbr_model_url` / `base_model_url`，下载链接 2 小时有效。
- **录音文件识别（ASR）**：Qwen-ASR-Filetrans、Paraformer-v2、Fun-ASR 等模型对长音频的离线转写。
- **音乐生成**：Fun-Music 在非流式模式下返回音频 OSS URL（24 小时有效）。
- **模型调优 / 微调**：上传训练文件 → 创建调优任务 → 轮询 `job_id` 至成功后拿到 `finetuned_output` 模型 ID。
- **模型导入 / 模型部署**：把 OSS 权重注册到百炼，或把基础模型 / 微调模型拉起为专属推理服务。

实时识别 / SSE 流式音乐 / OpenAI 兼容同步接口走 WebSocket 或流式协议，不在本模式范围内。

## 标准调用流程

无论具体业务，异步任务都遵循同一条三段式主线：

1. **提交任务**：`POST` 业务端点，请求头必须带 `X-DashScope-Async: enable`（否则报 "current user api does not [support](../guides/support.md) synchronous calls"），鉴权统一用 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，响应返回 `task_id` 或 `job_id`。
2. **轮询查询**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（视频 / 3D / ASR / 音乐），或 `GET /api/v1/fine-tunes/{job_id}`（模型调优）、`GET /api/v1/custom_models/import/{job_id}`（模型导入）。建议轮询间隔 15 秒。
3. **拿结果**：终态为 `SUCCEEDED` 时从 `output` / `results` 中取下载 URL 或下游模型标识；`FAILED` 时根据 `error_code` / `message` 排查。

### 通用任务状态机

| 业务类型 | 状态枚举 |
| --- | --- |
| 视频 / 3D / ASR / 音乐 | `PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED` |
| 模型调优 | `PENDING` / `QUEUING` / `RUNNING` / `CANCELING` / `SUCCEEDED` / `FAILED` / `CANCELED` |
| 模型导入 | `PENDING` → `RUNNING` → `SUCCESSED` / `FAILED`（注意拼写为 `SUCCESSED`） |

任务超过有效期后部分接口会返回 `UNKNOWN` 状态，需视为不可恢复。

## 关键参数与请求头

### 必备请求头

| 头字段 | 值 | 说明 |
| --- | --- | --- |
| `X-DashScope-Async` | `enable` | 异步提交必填，缺失即被同步路径拒绝 |
| `Authorization` | `Bearer ${DASHSCOPE_API_KEY}` | 北京 / 新加坡 API Key 不通用，需按地域分别获取 |
| `Content-Type` | `application/json` | 标准 JSON 提交 |

### 服务端点地域

- **中国内地（北京）**：`https://dashscope.aliyuncs.com/...`
- **国际（新加坡）**：`https://dashscope-intl.aliyuncs.com/...` 或新版多租域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`

3D 生成、模型调优、模型导入 / 部署等部分能力**仅在北京地域可用**，使用前需确认 API Key 归属地域，否则返回鉴权或路由错误。

### 标识与有效期

| 标识 | 来源 | 有效期 |
| --- | --- | --- |
| `task_id` | 视频 / 3D / ASR / 音乐异步提交响应 | 通常 24 小时；超时查询返回 `UNKNOWN` |
| `job_id` | 模型调优 / 模型导入 / 模型压缩响应 | 任务终态前持续有效 |
| 结果下载 URL | `output.audio.url` / `results[*].url` / `pbr_model_url` 等 | 视频 / 音乐 24 小时；3D 模型 2 小时 |
| `deployed_model` | 模型部署响应 | 持续有效，作为后续推理调用的 `model` id |

务必在有效期内将结果文件**转存至自有存储**，过期后链接不可恢复。

## 工程实践建议

- **不要重复创建任务**：拿到 `task_id` / `job_id` 后只走查询接口；重复提交会重复计费（特别是模型部署，`POST` 成功即开始计费，无论是否调用模型）。
- **控制轮询频率**：查询接口有 RPS 限制（如 3D 默认 20 RPS）。生产环境建议 15 秒一次，超出频率请改用**异步任务回调**（部分接口支持）。
- **并发约束**：模型调优**同一用户同时只允许一个训练任务执行**，其余任务进入 `QUEUING`，调度时需按串行规划。
- **完整状态覆盖**：轮询逻辑必须覆盖所有终态（`SUCCEEDED` / `FAILED` / `CANCELED` / `UNKNOWN`），并对失败响应中的 `code` / `error_code` / `message` 做差错处理（常见：`InvalidParameter`、`NotFound`、`OperationDenied`、`InvalidApiKey`、`InternalError`）。
- **批量任务排查**：批量提交场景（如文件上传）需检查响应中 `data.failed_uploads` 等部分失败字段，不要假定整批成功。
- **结果落地**：所有下载 URL 都是 OSS 临时签名链接，业务系统应在轮询成功的同一调用链中完成转存，避免延后处理导致链接失效。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [model training](../api/model-training.md)
- [deploy dedicated services](../api/deploy-dedicated-services.md)


