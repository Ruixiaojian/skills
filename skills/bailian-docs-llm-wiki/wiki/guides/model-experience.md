# model experience

`model experience` 是百炼平台面向开发者提供的模型能力概览与使用指南，涵盖视觉理解、文本生成、多模态处理、语音/音频、3D生成及向量检索等核心AI能力。本文档聚焦于模型选型逻辑、关键参数约束、标准化调用方式及实际部署注意事项，所有信息均基于当前（2026年中）稳定可用的模型版本，不包含营销性描述或过时推荐。

## 支持的模型/功能

百炼平台提供覆盖全模态场景的模型体系，按能力域划分如下：

- **视觉理解**：支持图像OCR、视频理解、结构化输出及Function Calling。旗舰模型 `qwen3.7-plus` 支持1M上下文、2小时视频输入、2048张图片和64段视频；轻量模型 `qwen3.6-flash` 在保持相同上下文长度与功能集的前提下显著降低成本 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **文本生成**：适用于AI编程、办公文档处理、长文本摘要等场景。`qwen3.7-plus` 和 `qwen3.6-flash` 均支持思考模式（`enable_thinking`）、Function Calling、内置工具（联网搜索、代码执行）及结构化JSON输出；超长文档处理推荐 `qwen-long`（10M上下文），但其不支持思考模式与内置工具 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **图片与视频生成/编辑**：`wan2.7-image-pro` 支持4096×4096文生图与多图参考编辑；`happyhorse-1.1-t2v` 和 `wan2.7-t2v-2026-06-12` 均支持1080P有声视频生成，后者额外支持自定义音频文件注入 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。  
- **语音与音乐**：S2S（语音转语音）模型如 `qwen3.5-omni-plus-realtime` 支持端到端音频理解与生成，兼具Function Calling与联网搜索能力；Fun-Music模型（`fun-music-v1`）支持[prompt](prompt.md)/lyrics双输入、性别选择及纯音乐生成，但仅限华北2（北京）地域 [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **3D与向量能力**：Tripo 3D模型（`Tripo/Tripo-P1.0`）需通过异步API调用，仅支持北京地域，且必须使用该地域API Key [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；向量模型中，`text-embedding-v4` 为文本Embedding默认推荐，`qwen3-rerank` 支持最多500文档的纯文本重排序 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 2 中称 `qwen3.7-max` “不支持结构化输出”，但文档 1 明确列出 `qwen3.7-max-2026-06-08` 的结构化输出列为“不支持”，而 `qwen3.7-plus` 为“支持”。两者一致，无矛盾；但文档 2 表格中将 `qwen3.7-max` 的结构化输出标为“不支持”属正确表述，非错误。

## 关键参数

各模型共性关键参数如下（单位均为Token，除非特别注明）：

| 参数 | 说明 | 典型值/范围 | 约束说明 |
|------|------|-------------|----------|
| `max_context` | 输入上下文长度上限 | `qwen3.7-plus`: 1M；`qwen-long`: 10M；`text-embedding-v4`: 8,192 | 超出将被截断，不报错 |
| `max_output_tokens` | 单次响应最大输出长度 | `qwen3.7-plus`: 64k；`qwen3-rerank`: 4,000/条 | 输出受模型能力与计费策略双重限制 |
| `max_image_count` / `max_video_count` | 单请求最大媒体数 | `qwen3.7-plus`: 2048图/64视频；`qwen3.5-omni-plus`: 256图/512视频 | 图像分辨率影响Token消耗：`h × w / (32 × 32) + 2` [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) |
| `texture_quality` / `geometry_quality` | Tripo 3D模型贴图与几何精度控制 | `standard` / `detailed`；`standard` / `ultra` | 仅 `Tripo/Tripo-H3.1` 支持 `geometry_quality` |
| `format` | 音频/视频输出格式 | `mp3` / `wav`；`720P` / `1080P` | `wav` 无损但体积大；视频输出帧率固定为24/30 fps |

## 使用方式

- **同步调用**：适用于文本生成、TTS、ASR、Embedding等低延迟场景。HTTP POST请求，`Content-Type: application/json`，模型ID置于`model`字段，输入数据置于`input`对象内（如`{"prompt": "..."}` 或 `{"audio_url": "..."}`）。  
- **异步调用**：适用于3D生成、长视频生成等耗时任务。首请求返回`task_id`，后续轮询 `GET /api/v1/tasks/{task_id}` 获取结果，状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`，有效期24小时 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **流式调用**：WebSocket协议用于实时语音对话（`-realtime`后缀模型）、流式TTS/ASR。需维持长连接，服务端分块推送响应（如语音PCM片段或识别文本流）。  
- **多模态输入**：视觉/全模态模型接受混合输入。例如 `qwen3.5-omni-plus` 的`input`可同时含`text`、`audio_url`、`image_url`、`video_url`字段；Tripo模型则通过互斥字段`prompt`/`image`/`images`区分生成模式 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  

## 限制和注意事项

- **地域限制**：Tripo 3D模型、Fun-Music、部分S2S/ASR模型（如`qwen3.5-livetranslate-flash`）**仅支持华北2（北京）地域**，且必须使用该地域API Key与Endpoint [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **功能互斥**：Qwen3.5-Omni系列在启用联网搜索时**不可同时启用Function Calling**；思考模式下**不支持生成语音输出**（仅文本） [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **旧版模型弃用**：Qwen2.5-VL、Qwen-Omni、Qwen-VL等旧系列模型已明确标注“不再作为首选推荐”，新项目应使用Qwen3.6或Qwen3.5系列 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **音频规格硬约束**：Fun-ASR非实时模型支持最大12小时/2GB音频；Qwen3.5-Omni非实时模型限3小时/2GB；而Qwen3-omni-flash HTTP模式仅支持20分钟/100MB [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **语言覆盖差异**：Qwen3.5-Livetranslate支持60种语言（29种输出语音+文本），但Qwen3-Omni-Flash仅支持11种输出语言；方言支持因模型版本而异（如`fun-asr-realtime`支持数十种中文方言，而`paraformer-8k-v2`仅支持普通话） [全模态](../../raw/model-user-guide/model-experience/omni.md)。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


