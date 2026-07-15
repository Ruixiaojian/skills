# model experience

`model experience` 是百炼平台面向开发者提供的统一模型能力体验层，涵盖文本、图像、视频、语音、音乐、3D、多模态及向量/重排序等全栈AI模型服务。所有模型均通过标准化 API 接入，支持异步任务、流式响应、结构化输出与工具调用等核心能力，并按场景提供推荐选型路径。开发者可基于具体需求（如延迟敏感度、精度要求、成本约束）快速定位适配模型，无需关注底层基础设施。

## 支持的模型与功能

百炼平台当前提供覆盖多模态的模型矩阵，按能力域划分如下：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 100 万上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）。轻量场景可选用 `qwen3.6-flash`，效果接近且成本更低 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **图像生成与编辑**：`wan2.7-image-pro` 支持文生图（最高 4096×4096）、多图参考编辑、角色一致性生成；`qwen-image-2.0-pro` 支持负向提示词与单次最多 6 张变体；`z-image-turbo` 适用于低成本写实人像生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视觉理解**：`qwen3.7-plus` 支持图像（最高 1600 万像素）、视频（最长 2 小时 / 2GB）、OCR 及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 针对文档/手写内容优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v` 支持文生视频（1080P，3–15 秒），`wan2.7-i2v-2026-04-25` 支持首尾帧续写；`happyhorse-1.0-video-edit` 和 `wan2.7-videoedit` 分别覆盖基础编辑与特效/运镜复刻 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **语音合成（TTS）**：`qwen-audio-3.0-tts-plus` 支持指令控制（语速/情绪）；`cosyvoice-v3.5-plus` 同时支持声音复刻与声音设计；Qwen3-TTS 系列通过 `-realtime` 后缀区分 WebSocket 流式接入 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **语音转语音（S2S）**：`qwen3.5-omni-plus-realtime` 提供端到端低延迟对话，支持音频语调感知；`qwen3.5-livetranslate-flash-realtime` 覆盖 60 种语言实时翻译（29 种输出语音） [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **语音识别（ASR）**：`fun-asr`（非实时）支持说话人分离；`qwen3.5-omni-plus`（HTTP）支持 Prompt 注入领域上下文；`qwen3-asr-flash-realtime` 支持情感识别 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **音乐生成**：`fun-music-v1` 支持 [prompt](prompt.md)/lyrics 输入、男声/女声选择及纯音乐模式（`is_instrumental=true`），仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **3D 生成**：`Tripo/Tripo-P1.0`（快速预览）与 `Tripo/Tripo-H3.1`（影视级）支持文生3D、单图/多图生3D，需通过异步任务 API 调用 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **向量与重排序**：`text-embedding-v4`（文本）与 `qwen3-vl-embedding`（多模态）支持跨模态检索；`qwen3-rerank` 用于 RAG 结果精排，支持 100+ 语言 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **全模态理解**：`qwen3.5-omni-plus` 统一处理文本/音频/图片/视频输入，支持 Function Calling、联网搜索及音视频分析；`qwen3-omni-flash` 为轻量替代方案，支持思考模式 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 3（视觉理解）与文档 11（全模态）均提及 `qwen3.5-omni-plus` 支持“联网搜索”，但文档 8（S2S）明确说明“Qwen3.5-Omni 实时（WebSocket）模式不支持此功能”，而文档 11 表格中 `qwen3.5-omni-plus-realtime` 的“联网搜索”列为“支持”。此处存在矛盾——实际能力以 API 文档为准：联网搜索仅在 HTTP 模式下可用，WebSocket 实时模式不可用。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

- **`model`**：必需，指定模型 ID（如 `qwen3.7-plus`、`wan2.7-image-pro`）。  
- **`input`**：必需，结构因模型类型而异：  
  - 文本类：`{"messages": [...]}` 或 `{"prompt": "..."}`；  
  - 图像类：`{"prompt": "...", "image": "url"}` 或 `{"images": ["url1", "url2"]}`；  
  - 视频类：`{"prompt": "...", "video": "url"}`；  
  - 音频类：`{"audio": "url"}` 或 `{"prompt": "...", "audio": "url"}`；  
  - 3D 类：`{"prompt": "..."}`、`{"image": "url"}` 或 `{"images": [...]}`。  
- **`parameters`**：可选，控制生成行为：  
  - 文本：`temperature`（默认 0.8）、`top_p`（默认 0.8）、`max_tokens`；  
  - 图像：`texture_quality`（`standard`/`detailed`）、`size`（如 `"1024x1024"`）；  
  - 视频：`duration`（秒）、`fps`；  
  - TTS：`format`（`mp3`/`wav`）、`gender`（`male`/`female`）；  
  - 音乐：`is_instrumental`（`true`/`false`）、`format`；  
  - 3D：`texture_quality`、`geometry_quality`（仅 `Tripo-H3.1`）。  
- **`enable_thinking`**：布尔值，启用逐步推理（仅 Qwen3 及以上文本/全模态模型支持）。  
- **`X-DashScope-Async: enable`**：异步任务必需头（如 Tripo、Fun-Music），返回 `task_id` 后轮询结果。  

## 使用方式

- **同步调用（HTTP）**：适用于低延迟要求场景（如聊天机器人），直接返回结果。示例：  
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.7-plus","input":{"messages":[{"role":"user","content":"你好"}]}}'
  ```
- **流式调用（WebSocket）**：适用于实时交互（如语音助手），需建立长连接并处理 `event: message` 流。模型名含 `-realtime` 后缀（如 `qwen3.5-omni-plus-realtime`）。  
- **异步调用（HTTP + 轮询）**：适用于耗时任务（如 3D 生成、长视频处理），先提交任务获 `task_id`，再 GET `/api/v1/tasks/{task_id}` 查询状态。Tripo 和 Fun-Music 必须使用此方式 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **批量推理（HTTP）**：适用于高吞吐、低延迟容忍场景，通过 `/batch` 接口提交多请求，降低单位成本 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  

## 限制和注意事项

- **地域限制**：Tripo 3D 模型仅支持华北2（北京）；Fun-Music 仅限华北2（北京）且需邀测开通；部分模型（如 `wanx2.1-imageedit`）明确标注“仅支持北京地域” [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **输入约束**：  
  - 图像：单图最高 1600 万像素，[Token](../concepts/token.md) 消耗公式为 `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 最长 2 小时 / 2GB，`qwen3-vl-plus` 最长 1 小时 / 2GB；  
  - 音频：ASR 文件最大 12 小时 / 2GB，S2S 实时流无时长限制但单次输入建议 ≤2 小时。  
- **功能兼容性**：  
  - 思考模式（`enable_thinking`）与语音输出互斥：启用思考模式时，S2S/Qwen-Audio 模型不生成语音 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)；  
  - Function Calling 与联网搜索不可同时开启（Qwen3.5-Omni HTTP 模式）；  
  - `qwen-long`（1000 万上下文）不支持 Function Calling、内置工具或思考模式。  
- **版本管理**：推荐使用快照版本（如 `qwen3.7-plus-2026-05-26`）保障稳定性；`-latest` 或无后缀版本可能随平台升级变更行为。  
- **旧版模型**：Qwen3、Qwen2.5 等系列已归为“旧版”，新项目应优先选用 Qwen3.6/Qwen3.7 或 Qwen3.5-Omni 系列 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


