# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、视觉、音视频、3D、音乐等全模态生成与理解任务。本文档聚焦于模型功能边界、关键参数配置及工程化使用约束，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与API行为。

## 支持的模型/功能

百炼提供覆盖[多模态](../concepts/multi-modal.md)场景的模型矩阵，按能力域划分如下：

- **文本生成**：支持长上下文（最高1000万[Token](../concepts/token.md)）、Function Calling、内置工具（联网搜索/代码解释器）、结构化JSON输出及深度思考模式。旗舰模型 `qwen3.7-plus` 与 `qwen3.7-max` 均支持完整能力栈，但 `qwen3.7-max` 不支持结构化输出 [文本生成 (raw/model-user-guide/model-experience/text-generation-model.md)](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus`、`qwen3.6-flash` 等支持图像/视频输入（最长2小时）、1600万像素单图、多图参考编辑及结构化输出；OCR专用模型 `qwen3.5-ocr` 未在通用视觉模型列表中体现，需单独选用 [视觉理解 (raw/model-user-guide/model-experience/vision-model.md)](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片与视频生成**：`wan2.7-image-pro` 支持文生图（4096×4096）与多图编辑；`happyhorse-1.1-t2v` 支持有声视频生成（1080P，3–15秒）；`wan2.7-i2v-2026-04-25` 支持首尾帧续写，适用于长视频构建 [图片生成与编辑 (raw/model-user-guide/model-experience/image-model.md)](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D生成**：Tripo系列仅限华北2（北京）地域，需异步调用。`Tripo/Tripo-P1.0`（2万面，快速预览）与 `Tripo/Tripo-H3.1`（200万面，影视级）通过 `input.prompt` / `input.image` / `input.images` 字段区分模式，贴图质量由 `parameters.texture_quality` 控制 [Tripo 3D模型生成 (raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：`fun-asr` 系列支持说话人分离；`qwen3.5-omni-plus` 支持Prompt上下文注入与情感识别；`qwen-audio-3.0-realtime-plus` 支持Function Calling；`fun-music-v1` 支持歌词/提示词双输入及性别选择 [语音识别 (raw/model-user-guide/model-experience/asr-model.md)](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **向量与重排序**：`text-embedding-v4` 支持64–2048维可配；`qwen3-rerank` 支持最多500文档重排；`qwen3-vl-rerank` 支持文本+图像混合排序 [向量与重排序 (raw/model-user-guide/model-experience/embedding-rerank-model.md)](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 对 `qwen3.7-plus` 的结构化输出支持描述一致，但文档 1 明确指出 `qwen3.7-max` **不支持**结构化输出，而文档 2 表格中 `qwen3.7-max-2026-06-08` 对应列为 `\--`（空值），二者逻辑一致，无矛盾。  
> **注意**：文档 4 中 `wan2.7-i2v-2026-04-25` 被标注为“首帧生视频、首尾帧生视频、视频续写”，但文档 4 其他位置将“首尾帧生视频”归入 `wan2.7-i2v-2026-04-25`，而 `wan2.7-i2v`（无日期后缀）仅描述为“图生视频”，存在版本粒度不一致。实际使用应以带日期后缀的快照版本为准。

## 关键参数

各模态模型共性参数与关键字段如下：

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model` | 全部 | 模型ID，必须精确匹配（含快照版本如 `-2026-05-26`） | `"qwen3.7-plus"` |
| `input` | [多模态](../concepts/multi-modal.md) | 输入数据容器，结构因模型而异：<br>- 文本：`{"prompt": "..."}`<br>- 图像：`{"image": "https://..."}`<br>- 多图：`{"images": [{"file_token": "..."}, ...]}`<br>- 音频：`{"audio_url": "https://..."}` | 见 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) |
| `parameters` | 部分模型 | 模型特有控制参数：<br>- `texture_quality`: `standard`/`detailed`（Tripo）<br>- `geometry_quality`: `standard`/`ultra`（Tripo-H3.1）<br>- `format`: `mp3`/`wav`（Fun-Music） | `{"texture_quality": "detailed"}` |
| `enable_thinking` | Qwen3+文本模型 | 开启逐步推理（非所有Qwen3模型默认启用） | `true` |
| `reasoning.effort` | Responses API | 替代 `enable_thinking` 的细粒度控制 | `"high"` |

- **音频类模型**：`qwen-audio-3.0-realtime-plus` 通过系统提示词选择音色，不支持SSML；`cosyvoice-v3.5-plus` 支持指令控制（如“温柔语速稍慢”）和SSML/LaTeX公式朗读 [语音合成 (raw/model-user-guide/model-experience/tts-model.md)](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **Embedding模型**：`text-embedding-v4` 维度需显式指定（如 `{"dimension": 1024}`），默认1024；`qwen3-vl-embedding` 默认2560维，不可修改。

## 使用方式

- **同步 vs 异步**：  
  - 文本/语音/Embedding等低延迟任务使用HTTP同步调用（如 `/api/v1/services/llm/text-generation`）。  
  - 3D/视频生成等耗时任务强制异步：先发请求获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询状态（有效期24小时）[Tripo 3D模型生成 (raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  

- **协议与接入**：  
  - 实时类（ASR/TTS/S2S）优先使用WebSocket；非实时类（文件转写/批量生成）使用HTTP。  
  - SDK支持：Qwen-Audio-TTS/CosyVoice/Qwen-ASR 支持Java/Python/Android/iOS SDK；其他模型需按协议直连。  

- **地域限制**：  
  - Tripo 3D模型 **仅限华北2（北京）**；  
  - Fun-Music **仅限华北2（北京）**；  
  - 所有模型均需在对应地域控制台开通服务并获取API Key。

## 限制和注意事项

- **输入约束**：  
  - 视觉模型单图最高1600万像素，[Token](../concepts/token.md)消耗公式为 `h × w / (32 × 32) + 2`；  
  - 视频输入：`qwen3.7-plus` 支持最长2小时/2GB，但 `qwen3-vl-plus` 仅支持1小时；  
  - Fun-ASR非实时模型最大支持12小时/2GB音频，Qwen3.5-Omni非实时最大3小时/2GB；  
  - Tripo多图输入限2–4张，每张≤20MB、宽高20–6000像素。

- **功能互斥性**：  
  - `qwen-audio-3.0-realtime-plus` 支持Function Calling，但**不支持联网搜索与思考模式**；  
  - `qwen3.5-omni-plus` 同时支持Function Calling与联网搜索，但**二者不可同时启用**；  
  - 思考模式启用时，`qwen3-omni-flash` 仅输出文本，**不生成语音**。

- **版本与兼容性**：  
  - 旧版模型（如 `qwen2.5-omni-7b`、`paraformer` 系列）已停止更新，新项目应使用Qwen3.5+系列；  
  - `qwen3.7-max` 的快照版本（如 `qwen3.7-max-2026-06-08`）与主版本能力一致，但结构化输出始终不支持；  
  - `qwen-omni-turbo` 仅支持中英文，已被 `qwen3.5-omni-plus` 全面替代。

- **计费与资源**：  
  - Tripo模型按任务计费，GLB文件URL有效期2小时；  
  - Fun-Music生成的MP3/WAV URL有效期依模型策略而定，需及时下载；  
  - 批量推理（Batch Inference）适用于延迟不敏感场景，可降低单请求成本 [文本生成 (raw/model-user-guide/model-experience/text-generation-model.md)](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


