# model experience

`model experience` 是百炼平台面向开发者提供的模型能力概览与使用指南，涵盖文本、视觉、音视频、3D、Embedding 等全模态模型的选型逻辑、核心参数与接入方式。本文档聚焦实用性，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型能力快照，并明确标注地域、协议与功能边界。

## 支持的模型/功能

百炼提供覆盖[多模态](../concepts/multimodal.md)场景的模型矩阵，按能力维度可划分为以下几类：

- **文本生成**：支持长上下文（最高 10M [Token](../concepts/token.md)）、Function Calling、结构化输出、思考模式（`enable_thinking` 或 `reasoning.effort`）及批量推理。主力模型为 `qwen3.8-max`（最强推理）、`qwen3.7-plus`（平衡首选）和 `qwen3.7-flash`（高性价比），均支持 1M 上下文与完整工具链 [文本生成 (raw/model-user-guide/model-experience/text-generation-model.md)](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：支持图像、视频（最长 2 小时）、OCR 及多图输入。`qwen3.7-plus` 和 `qwen3.7-flash` 是通用视觉理解首选，而 `qwen3.5-ocr` 专用于文档/手写体文字提取 [视觉理解 (raw/model-user-guide/model-experience/vision-model.md)](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面与高保真渲染；`wan2.7-image-pro` 提供品牌色控制与角色一致性；视频侧 `happyhorse-1.1-i2v`（首帧生视频）与 `wan2.7-i2v-2026-04-25`（首尾帧续写）是主流选择。  
- **语音与音乐**：语音合成（TTS）支持声音复刻（`qwen-audio-3.0-tts-plus`）与声音设计（`cosyvoice-v3.5-plus`）；语音识别（ASR）区分实时（`qwen-audio-3.0-asr-flash-streaming`）与文件转写（`qwen-audio-3.0-asr-flash-filetrans`）；音乐生成（Fun-Music）需邀测开通，仅限华北2（北京）地域 [音乐生成 (raw/model-user-guide/model-experience/fun-music.md)](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **全模态与 S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频联合理解、联网搜索与 Function Calling；`qwen3.5-livetranslate-flash-realtime` 专注 60 种语言实时翻译；S2S 模型（如 `qwen-audio-3.0-realtime-plus`）实现端到端语音对话，低延迟且感知语调情绪。  
- **向量与重排序**：`text-embedding-v4` 为文本 Embedding 默认推荐；跨模态检索优先选用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）；重排序任务使用 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（[多模态](../concepts/multimodal.md)）。  
- **3D 生成**：Tripo 系列（`Tripo/Tripo-P1.0` 与 `Tripo/Tripo-H3.1`）仅支持华北2（北京）地域，必须通过异步任务 API 调用，且需显式配置 `X-DashScope-Async: enable` 头 [Tripo 3D模型生成 (raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

> **注意**：文档 1 与文档 2 均称 `qwen3.7-plus` 支持“内置工具”，但文档 2 表格中明确列出仅 `qwen3.7-max-2026-06-08`、`qwen3.7-plus`、`qwen3.6-plus` 等特定快照版本支持，而文档 1 的表格未标注快照版本。实际使用应以文档 2 的快照版本为准，避免直接使用无后缀的 `qwen3.7-plus`（可能指向不稳定别名）。

## 关键参数

各模型系列的关键控制参数如下（非 exhaustive，仅列高频必需项）：

- **文本/视觉模型**：  
  - `enable_thinking`（布尔）或 `reasoning.effort`（字符串，如 `"medium"`/`"high"`）：开启逐步推理模式，适用于数学计算、代码调试等场景。  
  - `tools`：定义 Function Calling 工具列表，格式为 OpenAI-style schema。  
  - `response_format`：指定结构化输出，如 `{"type": "json_object"}`。  
  - `max_tokens`：控制输出长度，部分模型（如 `qwen3.7-plus`）默认上限为 64k。  

- **视觉模型**：  
  - 图像分辨率影响 [Token](../concepts/token.md) 消耗：公式为 `h × w / (32 × 32) + 2`，单图最高支持 1600 万像素。  
  - 视频输入需注意时长与大小限制（如 `qwen3.7-plus` 支持最长 2 小时 / 2GB）。  

- **语音模型**：  
  - TTS：`gender`（`"male"`/`"female"`）、`format`（`"mp3"`/`"wav"`）、指令控制（自然语言描述语速/情绪）。  
  - ASR：`hotword`（热词表）、`prompt`（上下文注入）、`speaker_diarization`（说话人分离，仅 `qwen-audio-3.0-asr-flash-filetrans` 支持）。  
  - S2S：`enable_search`（联网搜索，仅 `qwen3.5-omni-*` 支持）、`enable_function_calling`（Function Calling，`qwen3.5-omni-*` 与 `qwen-audio-3.0-realtime-plus` 支持）。  

- **Tripo 3D**：  
  - `input.prompt` / `input.image` / `input.images`：三者互斥，决定生成模式。  
  - `parameters.texture_quality`（`"standard"`/`"detailed"`）控制贴图精度；`parameters.geometry_quality`（仅 `Tripo-H3.1` 支持，`"standard"`/`"ultra"`）控制面数。  

- **Embedding/Rerank**：  
  - `dimensions`：`text-embedding-v4` 支持 64~2048 维，默认 1024。  
  - `top_n`：重排序模型（如 `qwen3-rerank`）最大支持 500 条输入。

## 使用方式

- **API 协议**：  
  - 实时交互（语音助手、直播分析）优先使用 **WebSocket**（如 `qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-asr-flash-streaming`）。  
  - 批处理、文件分析、异步任务使用 **HTTP**（如 `qwen3.7-plus` 文本生成、`qwen-audio-3.0-asr-flash-filetrans`、Tripo 3D 生成）。  
  - Tripo 必须启用异步头 `X-DashScope-Async: enable` 并轮询 `task_id` 获取结果 [Tripo 3D模型生成 (raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  

- **地域约束**：  
  - Tripo 3D、Fun-Music 仅支持 **华北2（北京）** 地域，API Endpoint 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。  
  - 其他模型（如 `qwen3.7-plus`、`qwen-image-3.0-pro`）在多地域（北京、新加坡、美国、法兰克福）可用，需按控制台链接确认。  

- **认证与配置**：  
  - 所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。  
  - Workspace ID 必须替换为真实值，获取方式见[业务空间管理](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。  

- **输入格式**：  
  - [多模态](../concepts/multimodal.md)输入（图文/音视频）需通过 `input` 字段嵌套传递，例如：  
    ```json
    {
      "model": "qwen3.7-plus",
      "input": {
        "messages": [...],
        "images": ["https://..."],
        "videos": ["https://..."]
      }
    }
    ```  
  - Tripo 输入严格区分 `prompt`（文本）、`image`（单图 URL）、`images`（2~4 张图 URL 列表）。

## 限制和注意事项

- **地域与服务开通**：Tripo 3D 和 Fun-Music 为邀测服务，需单独申请开通，且仅限华北2（北京）地域；其他模型需在对应地域的[模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)启用。  
- **功能兼容性**：  
  - `qwen-audio-3.0-realtime-plus` 支持 Function Calling，但**不支持联网搜索与思考模式**；`qwen3.5-omni-plus` 同时支持二者，但二者不可同时启用。  
  - 思考模式（`reasoning.effort`）启用时，**不支持生成语音输出**（S2S 场景下会静音）。  
  - `qwen3-long`（10M 上下文）**不支持 Function Calling、内置工具与思考模式**，仅支持结构化输出。  
- **性能与成本权衡**：  
  - `qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下，成本显著降低，适合效果验证与高吞吐场景。  
  - `z-image-turbo` 生成速度快 10 倍、成本约 1/5，但**不支持图片编辑功能**。  
- **版本稳定性**：文档中大量模型以快照形式存在（如 `qwen3.7-plus-2026-05-26`），推荐生产环境锁定具体快照 ID，避免使用无日期后缀的泛型名称（如 `qwen3.7-plus`），以防底层模型变更导致行为漂移。  
- **音频规格**：ASR 模型对输入有明确约束——`qwen-audio-3.0-asr-flash-streaming` 无时长限制，但 `qwen-audio-3.0-asr-flash-filetrans` 最大支持 12 小时 / 2GB；TTS 输出 `wav` 格式体积较大，需评估存储与带宽成本。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


