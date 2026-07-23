# 多模态

多模态（Multimodal）指模型能够同时理解、生成或处理多种类型数据（如文本、图像、音频、视频、3D几何、动作序列等）的能力，其核心在于跨模态语义对齐与联合建模。在百炼平台中，“多模态”不是单一模型属性，而是贯穿能力设计、API协议与开发者调用范式的横切架构原则——同一服务接口可灵活适配不同输入模态组合，并统一输出结构化结果。

## 在百炼平台的不同场景中，这个概念如何使用

- **统一输入抽象**：所有支持多模态的模型均通过 `input` 字段声明输入类型，而非固定字段名。例如：
  - 文本+图像理解：`{"text": "描述这张图", "image": "https://..."}`（`qwen3.7-plus`）
  - 图生视频：`{"media": [{"type": "image_url", "url": "..."}], "prompt": "生成10秒动画"}`（`wan2.7-i2v`）
  - 单图/多图/文三选一生3D：`input.image`、`input.images` 或 `input.prompt`（`Tripo/Tripo-P1.0`），互斥且由模型自动路由
  - 实时音视频交互：`append_audio()` + `append_video()` 双流注入（`qwen3.5-omni-realtime`）

- **能力分层复用**：
  - **基础多模态理解**：`qwen3.7-plus`、`qwen3.5-omni-plus` 等通用大模型支持图文、音视频、OCR混合输入，无需切换模型即可处理跨模态指令（如“对比这两张发票金额并生成表格”）。
  - **专用多模态生成**：图像（T2I/I2I）、视频（T2V/I2V/R2V）、3D（T23D/I23D/MultiI23D）等能力由垂直模型实现，但共享统一的 `model` + `input` + `parameters` 调用范式。
  - **端到端实时多模态**：`Omni Realtime API` 将 ASR、LLM、TTS、VAD 全链路封装为单 WebSocket 连接，开发者只需传入原始音视频流，即可获得同步的文本响应与合成语音，无需自行编排模态转换流程。

- **异步/同步模式解耦**：  
  - 同步适用低延迟、小体积模态（文本、短语音、小图理解）；  
  - 异步强制用于高计算负载模态（视频生成、3D重建、长视频理解），通过 `X-DashScope-Async: enable` 头统一标识，任务状态与结果通过 `task_id` 标准化获取。

## 关键参数和配置

| 参数 | 类型 | 说明 | 开发者须知 |
|------|------|------|------------|
| `model` | string | 必填。精确指定模型ID，决定支持的模态组合与能力边界（如 `qwen3.7-plus` 支持图文+视频，`wan2.7-image-pro` 仅支持图像生成） | ❗不可跨模态混用（如用 `qwen3.7-plus` 调用视频生成 endpoint 会失败） |
| `input` | object | 必填。结构化输入容器，**字段名由模型能力动态决定**：<br>- 文本：`{"text": "..."}`<br>- 图像：`{"image": "url"}` 或 `{"images": ["url1","url2"]}`<br>- 音频/视频：`{"audio_url": "..."}` / `{"video": "..."}`<br>- 混合：`{"text": "...", "image": "...", "audio_url": "..."}`（部分模型支持） | ✅ 始终检查目标模型文档中 `input` 的合法字段组合；❌ 不要硬编码字段名（如 `prompt` 在新模型中已弃用，改用 `messages` 或 `input.text`） |
| `parameters` | object | 可选。控制生成行为的键值对，**模态专属参数需显式声明**：<br>- 图像：`{"size": "1024*1024", "negative_prompt": "模糊"}`<br>- 视频：`{"duration": 5, "aspect_ratio": "16:9"}`<br>- 3D：`{"geometry_quality": "ultra", "texture": false}`<br>- Omni Realtime：`{"turn_detection_type": "semantic_vad", "enable_search": true}` | ⚠️ 参数有效性严格依赖 `model` —— 同一参数名在不同模型中含义可能不同（如 `size` 在图像中是分辨率，在视频中是 `720P`） |
| `X-DashScope-Async` | header | string | 异步任务必需头，值必须为 `"enable"`；同步调用时**不得携带该头** | ❗遗漏将导致 400 错误（如 Tripo 3D、视频生成）；✅ 同步模型（如 `qwen3.7-plus`）携带该头将被拒绝 |

## 面向开发者，简洁实用

- **第一步：确认模态需求 → 选模型 → 查文档**  
  不要先写代码，先查 [模型能力矩阵](https://help.aliyun.com/zh/model-studio/model-capabilities-matrix)：明确你要处理的是「文本+图像理解」还是「图像→视频生成」，再锁定对应模型（如 `qwen3.7-plus` vs `wan2.7-i2v`），最后精读该模型的 [API参考文档](https://help.aliyun.com/zh/model-studio/model-api-reference) —— 输入结构、参数约束、地域限制均以模型为准。

- **第二步：用 `input` 组织数据，不用 `prompt`**  
  百炼统一范式是 `input.{modality}`，而非旧式 `prompt` 字段。正确示例：  
  ```json
  {
    "model": "qwen3.7-plus",
    "input": {
      "text": "分析这张图中的商品价格和折扣信息",
      "image": "https://example.com/receipt.jpg"
    }
  }
  ```
  错误示例（旧协议残留）：`{"prompt": "分析...", "image_url": "..."}`。

- **第三步：异步任务必带头、必轮询、必及时下载**  
  对视频、3D、批量图像等异步任务：  
  - 请求头必须含 `X-DashScope-Async: enable`；  
  - 响应中提取 `task_id`，用 `GET /api/v1/tasks/{id}` 轮询（间隔 ≥15 秒）；  
  - `SUCCEEDED` 状态下立即下载 `output.results[0].xxx_url`（链接有效期通常为 2 小时）。

- **第四步：调试优先用业务空间域名**  
  始终使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如北京：`https://xxx.cn-beijing.maas.aliyuncs.com`），而非公共 endpoint —— 它提供更高稳定性、更低延迟，并确保模态能力与额度归属一致。

- **避坑提示**：  
  - 🚫 不要跨模型复用参数（`aspect_ratio` 在 Kling 视频有效，在 Tripo 3D 中无效）；  
  - 🚫 不要混用协议版本（`wan2.7` 模型必须用新版 endpoint，`wan2.6` 用旧版）；  
  - ✅ 所有多模态能力均支持 `DASHSCOPE_API_KEY` 统一认证，无需额外密钥。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)


