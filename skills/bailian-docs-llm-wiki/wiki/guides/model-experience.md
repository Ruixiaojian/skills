# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、图像、视频、语音、音乐、3D、多模态及向量检索等全栈AI能力。本文档聚焦核心模型能力、关键参数、标准接入方式及实际使用限制，帮助开发者快速匹配业务场景与最优模型，避免常见配置陷阱。

## 支持的模型/功能

百炼平台提供六大类模型能力，按输入输出模态和典型任务组织：

- **文本生成**：支持聊天、编程、办公文档处理、长文本推理（`qwen3.7-plus`、`qwen3.7-max`、`qwen-long`）；所有Qwen3及以上模型均支持思考模式、Function Calling 和结构化JSON输出 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：涵盖图像分析、OCR、视频理解（最长2小时）、多模态结构化提取；`qwen3.7-plus` 和 `qwen3.5-ocr` 分别为通用与专用OCR首选 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：文生图（最高4096×4096）、多图参考编辑、角色一致性生成；`wan2.7-image-pro` 为全能型推荐，`z-image-turbo` 适用于低成本批量生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：文生视频（1080P/15秒）、图生视频、参考生视频、视频编辑；`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别适用于标准生成与首尾帧续写 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **语音与音频**：  
  - 语音识别（ASR）：`fun-asr`（支持说话人分离）、`qwen3.5-omni-plus`（支持Prompt上下文注入）；  
  - 语音合成（TTS）：`qwen-audio-3.0-tts-plus`（支持声音复刻+指令控制）、`cosyvoice-v3.5-plus`（支持声音设计）；  
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）、`qwen3.5-livetranslate-flash-realtime`（60语种实时翻译）；  
  - 音乐生成：`fun-music-v1`（支持歌词/提示词生成+男/女声选择），当前仅邀测可用 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **3D与跨模态**：Tripo 3D模型生成（仅北京地域）、全模态理解（`qwen3.5-omni-plus`）、[向量嵌入](../concepts/vector-embedding.md)与重排序（`text-embedding-v4`、`qwen3-rerank`）。

> **注意**：文档中多次提及 `qwen3.5-omni-plus` 同时支持 WebSocket 和 HTTP 接入，但文档 8 明确指出其 WebSocket 模式不支持联网搜索（“Qwen3.5-Omni 实时（WebSocket）模式……不支持此功能”），而文档 10 又称“Qwen3.5-Omni（HTTP / WebSocket）”支持联网搜索。该矛盾需以文档 8 的说明为准：**联网搜索仅在 HTTP 模式下可用，WebSocket 模式下不可用**。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

| 参数 | 说明 | 典型取值示例 |
|------|------|--------------|
| `model` | 必填，模型ID（如 `qwen3.7-plus`、`wan2.7-image-pro`） | 见各模型文档的“推荐模型”表格 |
| `input` | 输入数据结构，依模型类型变化：<br>- 文本模型：`{"prompt": "..."}`<br>- 图像模型：`{"prompt": "...", "image": "url"}` 或 `{"images": [...]}`<br>- 视频模型：`{"prompt": "...", "parameters": {"texture_quality": "standard"}}`<br>- 音乐模型：`{"prompt": "...", "gender": "female"}` 或 `{"lyrics": "..."}` | [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 中明确要求 `input` 字段互斥（`prompt`/`image`/`images` 三选一） |
| `parameters` | 模型特有控制参数：<br>- 图片/视频：`texture_quality`（`standard`/`detailed`）、`geometry_quality`（`standard`/`ultra`）<br>- 音乐：`format`（`mp3`/`wav`）、`is_instrumental`（`true`/`false`）<br>- TTS：`voice_id`（音色ID）、`speed`（语速） | `parameters.texture_quality: "detailed"` 可提升Tripo模型贴图精度 |
| `enable_thinking` / `reasoning.effort` | 控制思考模式（逐步推理），适用于数学、代码、法律等复杂任务 | Qwen3系列默认混合模式，可按请求动态开启 |
| `max_output_tokens` | 输出长度上限（部分模型支持） | `qwen3.7-plus` 最大输出64k tokens |

## 使用方式

统一通过百炼 REST API 调用，核心流程一致：

1. **开通服务**：在[模型广场](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)开通对应模型（部分如 `fun-music-v1` 需邀测申请）；  
2. **获取凭证**：创建并配置 `DASHSCOPE_API_KEY` 环境变量；  
3. **构造请求**：  
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/{service}/{action}`（如 `/services/aigc/video-generation/3d-generation`）；  
   - Headers：`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`；  
   - Body：JSON 格式，含 `model`、`input`、`parameters`（如适用）；  
4. **处理响应**：  
   - 同步模型（如文本、TTS）直接返回结果；  
   - 异步模型（如Tripo 3D、视频生成）返回 `task_id`，需轮询 `/api/v1/tasks/{task_id}` 获取状态（有效期24小时）；  
   - 流式模型（WebSocket TTS/S2S）需建立长连接并处理二进制流。

> **注意**：Tripo 3D 模型**仅支持华北2（北京）地域**，且必须使用该地域的API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；Fun-Music 模型同样**仅限北京地域**且处于邀测阶段。

## 限制和注意事项

- **地域限制**：Tripo 3D、Fun-Music、部分旧版模型（如 `wanx2.1-imageedit`）仅在北京地域可用；  
- **输入约束**：  
  - 图片：单图生3D要求 JPEG/PNG，20–6000px，≤20MB；  
  - 视频：`qwen3.7-plus` 支持最长2小时/2GB，但 `qwen3-omni-flash` 仅支持20分钟/100MB；  
  - 音频：`fun-asr` 非实时最大12小时/2GB，`qwen3-asr-flash` 非实时仅限5分钟/10MB；  
- **功能兼容性**：  
  - Function Calling 与联网搜索**不可同时启用**（文档 10 明确说明）；  
  - 思考模式下**不支持生成语音**（文档 8）；  
  - `qwen-audio-3.0-realtime-plus` 支持 Function Calling，但**不支持联网搜索和思考模式**；  
- **版本管理**：快照模型（如 `qwen3.7-plus-2026-05-26`）用于稳定性需求，但主推模型（如 `qwen3.7-plus`）会持续更新；旧版模型（如 `qwen2.5-vl-72b-instruct`、`paraformer-v1`）已不推荐新项目使用；  
- **计费差异**：Qwen3-TTS Flash 系列按 [Token](../concepts/token.md) 计费，而 Qwen-Audio-TTS/CosyVoice 系列按请求+时长计费；  
- **语言支持**：`qwen3.5-livetranslate-flash-realtime` 支持60种语言，但其中31种仅输出文本（无语音），需根据业务需求核对语言表。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


