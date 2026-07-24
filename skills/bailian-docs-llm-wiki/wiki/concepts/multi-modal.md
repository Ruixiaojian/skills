# 多模态

多模态（Multimodal）指模型能够同时理解、生成或协同处理两种及以上类型的数据模态（如文本、图像、音频、视频、3D几何、语音信号等），并建立跨模态语义关联的能力。在百炼平台中，多模态不是单一模型特性，而是贯穿模型选型、API设计、输入输出协议与应用编排的系统级能力范式。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用层面**：多模态体现为统一 `input` 字段的结构化承载能力。例如：
  - 文本+图像联合理解：`{"prompt": "描述这张图", "image": "https://..."}`（`qwen3.7-plus`）；
  - 多图参考编辑：`{"images": [{"file_token": "img_1"}, {"file_token": "img_2"}], "prompt": "将第二张图风格迁移至第一张"}`；
  - 音视频混合输入：`{"audio_url": "https://...", "video_url": "https://..."}`（部分 `qwen3.5-omni` 变体）；
  - 3D生成输入：支持 `input.prompt`（文生3D）、`input.image`（图生3D）或 `input.images`（多视角重建），由字段名显式声明模态意图。

- **实时交互层面**：`omni realtime api` 将多模态固化为协议能力——通过 `modalities: ["text", "audio"]` 显式声明输出组合，并强制要求 `input_audio_format` 和 `output_audio_format` 统一为 `pcm`，确保音视频流与文本流在 WebSocket/ AOQ/WebRTC 协议栈中同步传输、对齐时序。

- **应用编排层面**：`application call` 支持多模态输入混合提交。智能体或工作流应用可接收 `Messages` 数组，其中单条消息 `content` 可含 `input_text`、`input_image` 或 `input_file` 类型；文件类输入（如 PDF、PPT）在后台自动解析为文本+图像混合表示，交由 VL 模型处理。

- **向量与检索层面**：`qwen3-vl-rerank` 等模型直接支持“文本+图像”混合排序，输入为 `{"query": "红色跑车", "documents": [{"text": "...", "image": "https://..."}, ...]}`，实现跨模态相关性打分，无需人工对齐特征空间。

- **第三方模型集成**：通过 [OpenAI 兼容接口](openai-compatible-api.md)调用 `kimi/kimi-k3`、`ZHIPU/GLM-5.2` 等第三方模型时，若其原生支持多模态（如 GLM-5.2 的图文理解），需在 `extra_body` 中传入对应格式（如 `"images": [...]`），百炼网关负责协议转换与路由分发。

## 关键参数和配置

| 参数 | 作用域 | 说明 | 示例 |
|------|--------|------|------|
| `input` | 全模型/API | 多模态输入容器，结构由模型能力决定。**必须严格匹配目标模型文档定义**，不可自由扩展字段。 | `{"prompt": "写诗", "image": "oss://bucket/key.jpg"}`（VL模型）<br>`{"audio_url": "https://x.mp3"}`（ASR模型） |
| `modalities` | Realtime API | 控制输出模态组合，仅允许 `["text"]` 或 `["text","audio"]`。影响服务端流式事件类型与客户端解析逻辑。 | `["text", "audio"]` |
| `parameters.texture_quality` | Tripo 3D模型 | 控制生成模型贴图质量，是典型的模态专属参数。 | `{"texture_quality": "detailed"}` |
| `enable_thinking` | Qwen3+/DeepSeek/Kimi等 | 启用多步推理链，常用于复杂多模态任务（如“根据图表+文字描述推导趋势结论”）。 | `{"enable_thinking": true}` |
| `cache_control` | Application Call / Responses API | 对多模态输入（如图文组合）启用确定性缓存，避免重复计算。需配合 `cache_key` 使用。 | `{"cache_control": {"type": "ephemeral"}}` |

> ⚠️ 注意：  
> - 所有 `input` 字段中的 URL 必须为公网可访问地址（OSS/HTTPS），或已预上传获得 `file_token`；本地文件需先调用 `/files/upload` 接口。  
> - 多模态输入存在严格尺寸/时长限制（如单图 ≤1600万像素、视频 ≤2小时、音频 ≤5分钟），超限将返回 `400 Bad Request` 并附具体错误码。  
> - `qwen3.7-max` 等旗舰模型**不支持结构化 JSON 输出**，若需多模态结果结构化（如 OCR 表格提取、视频关键帧坐标），请选用 `qwen3.7-plus` 或专用模型（如 `qwen3.5-ocr`）。

## 面向开发者，简洁实用

- **选型优先看 `input` 支持矩阵**：在 [model experience](model-experience.md) 中查目标模型是否列出 `image`/`audio`/`video` 等输入字段，而非仅看“多模态”标签。
- **调试用控制台在线调试工具**：上传图片/音频后，直接在 API 调试页粘贴 `input` JSON，实时查看服务端解析结果与错误提示。
- **生产环境必设 `workspace_id`**：多模态应用涉及文件存储、异步任务队列等资源隔离，未传 `workspace_id` 将导致 `403 Forbidden`。
- **[流式输出](streaming-output.md)注意事件类型**：Realtime API 中 `response.text.delta` 和 `response.audio.chunk` 是独立事件流，需分别监听并按时间戳对齐渲染。
- **第三方模型多模态需验签兼容性**：调用 `kimi/kimi-k3` 前，确认其 OpenAI 兼容层是否支持 `content` 数组含 `image_url`——百炼仅透传，不作格式转换。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [use cases](../guides/use-cases.md)
- [application call](../api/application-call.md)


