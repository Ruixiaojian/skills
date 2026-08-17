# 多模态

多模态（Multimodal）指模型能够同时理解、生成或处理两种及以上类型的数据模态（如文本、图像、音频、视频、3D 几何、结构化向量等），并实现跨模态语义对齐与联合推理。在百炼平台中，多模态不是单一能力，而是贯穿模型选型、API 设计、输入组织与参数配置的系统性架构原则。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型选型层面**：百炼将模型按模态支持能力分层归类。纯文本模型（如 `qwen3.7-plus`）仅接受文本输入；视觉模型（如 `qwen3.7-flash`）明确支持 `image`/`video` 字段；全模态旗舰模型（如 `qwen3.5-omni-plus`）可混合接收文本+图像+音频+视频，并输出文本+语音，是真正意义上的端到端多模态理解与生成中枢。

- **API 输入组织层面**：多模态能力通过 `input` 字段的结构化设计体现。不同模态对应不同键名：
  - 文本：`{"prompt": "..."}`  
  - 图像：`{"prompt": "...", "image": "url"}` 或 `"images": ["url1", "url2"]`  
  - 视频：`{"video": "url"}` 或 `{"media": [{"type": "video", "url": "..."}]}`  
  - 音频：`{"audio": "url"}`（ASR/TTS/S2S 场景）  
  - 3D：三选一 `{"prompt": "..."}` / `{"image": "url"}` / `{"images": [...]}`  
  混合输入时，字段共存即触发多模态处理逻辑（如图文问答需同时传 `prompt` + `image`）。

- **功能扩展层面**：多模态是高级能力的基础载体：
  - **多模态 Function Calling**：视觉/全模态模型可在理解图像内容后，动态调用工具（如 OCR 提取表格、识别商品条码后查库存）；
  - **多模态 Embedding/Rerank**：`qwen3-vl-embedding` 将图文统一映射至融合向量空间，`qwen3-vl-rerank` 支持图文混合检索排序；
  - **多模态生成控制**：图生视频（I2V）需首帧图像 + 文本提示；参考生视频（R2V）支持图像+视频+音色多源参考。

- **协议与部署层面**：所有多模态模型均强制要求异步调用（`X-DashScope-Async: enable`），因跨模态预处理（如视频解帧、3D 网格重建）耗时显著；且严格绑定地域（如 Tripo 3D 仅限华北2），确保模态数据低延迟协同处理。

## 关键参数和配置

- **`model`**：必须选用明确标注多模态支持的模型 ID（如 `qwen3.5-omni-plus`、`qwen3-vl-plus`、`Tripo/Tripo-H3.1`）。使用纯文本模型传入 `image_url` 将报错 `Unexpected item type in content`。

- **`input` 结构**：是多模态行为的开关，必须严格匹配目标模型支持的模态组合：
  - 全模态理解模型：支持 `prompt` + `image` + `audio` + `video` 组合（顺序无关，缺失模态自动忽略）；
  - 图像生成模型：`prompt` 必填，`image`/`images` 可选（用于 I2I/R2V）；
  - 3D 模型：`prompt`、`image`、`images` 三者**互斥且必选其一**。

- **`parameters` 中的模态特有配置**：
  - 视觉/视频：`{"duration": 10}`（视频秒数）、`{"aspect_ratio": "9:16"}`（竖屏适配）；
  - 3D：`{"geometry_quality": "ultra"}`（仅 H3.1）、`{"texture_quality": "detailed"}`；
  - 音频：`{"voice_id": "xxx"}`（TTS 声音复刻）、`{"hotwords": ["阿里云"]}`（ASR 术语增强）；
  - 全模态：`{"enable_search": true}`（联网搜索，仅 `qwen3.5-omni-plus` 等支持）。

- **协议头约束**：
  - 所有多模态模型调用**必须携带** `X-DashScope-Async: enable`；
  - 若启用思考模式（`enable_thinking: true`），则必须同时设置 `stream: true` 和 `incremental_output: true`（HTTP 流式）或使用 WebSocket。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.5-omni-plus` 发送含 `prompt` + `image` 的请求，即可测试图文联合理解；用 `qwen-image-3.0-pro` 发送 `prompt` + `image` 即可测试图生图。
- ⚠️ **避坑提示**：
  - 不要混用模态字段与模型能力——传 `video` 给 `qwen3.7-plus` 会失败；
  - 多模态 URL（图片/视频/音频）必须公网可访问、无鉴权、格式合规（如视频需 MP4/H.264）；
  - 异步任务（视频/3D）务必用 `task_id` 轮询，勿尝试同步等待；
  - 免费额度按**成功输出结果**计费（如生成 1 张图、1 段视频、1 个 GLB 模型），输入失败不扣量。
- 📌 **最佳实践**：
  - 优先使用业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），提升多模态数据传输稳定性；
  - 对长视频/高面数 3D 等重载任务，主动设置合理 `timeout`（SDK 默认 300s，建议设为 600s）；
  - 多模态调试时，在 `prompt` 中明确指令模态意图（如“请根据这张产品图，用中文描述其材质与尺寸”），避免歧义。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [preparations](../api/preparations.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


