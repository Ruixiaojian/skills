# model experience

`model experience` 是百炼平台面向开发者提供的统一模型能力体验层，涵盖文本、图像、视频、3D、语音、音乐、多模态及向量检索等全栈AI模型服务。所有模型均通过标准化API（HTTP/WebSocket）接入，支持结构化输出、Function Calling、思考模式、[异步任务](../concepts/asynchronous-task.md)等核心能力，并按场景提供推荐选型与参数配置指南。开发者可基于具体需求（如延迟敏感度、精度要求、成本约束、输入模态）快速定位最优模型。

## 支持的模型/功能

百炼平台提供覆盖全模态的模型矩阵，按能力域组织如下：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持100万上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化JSON输出及逐步推理（`enable_thinking`）。轻量场景可选用 `qwen3.7-flash` 或 `deepseek-v4-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **图像生成与编辑**：`wan2.7-image-pro` 集成文生图（最高4096×4096）、多图编辑与角色一致性；`qwen-image-3.0-pro`（邀测中）支持负向提示词与多语言字体渲染；`z-image-turbo` 适用于低成本写实人像生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v` 支持有声文生视频（1080P，3–15秒）；`wan2.7-i2v-2026-04-25` 支持首尾帧续写；`wan2.2-animate-move` 提供角色动画迁移（pro/std双模式） [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **视觉理解**：`qwen3.7-plus` 支持图像（最高1600万像素）、视频（最长2小时/2GB）联合分析，具备Function Calling与结构化输出能力；`qwen3.5-ocr` 专用于文档/手写体OCR [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **3D生成**：Tripo系列（`Tripo/Tripo-P1.0` / `Tripo/Tripo-H3.1`）支持文生3D、单图生3D、多图生3D，仅限华北2（北京）地域，需异步轮询获取GLB结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：  
  - 合成：`qwen-audio-3.0-tts-plus`（指令控制+声音复刻）、`cosyvoice-v3.5-plus`（声音设计）；  
  - 识别：`fun-asr`（支持说话人分离）、`qwen3.5-omni-plus`（Prompt上下文注入）；  
  - 全模态：`qwen3.5-omni-plus-realtime`（实时音视频对话）、`qwen3.5-livetranslate-flash-realtime`（60语种同传）；  
  - 音乐：`fun-music-v1`（歌词/提示词生成带人声歌曲，MP3/WAV输出） [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：`text-embedding-v4`（文本嵌入，维度可配64–2048）、`qwen3-vl-embedding`（图文融合向量）、`qwen3-rerank`（纯文本重排序，支持500文档） [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  

> **注意**：文档 9 和文档 11 中关于 `qwen3.5-omni-plus-realtime` 的联网搜索支持存在矛盾——文档 9 明确标注其支持联网搜索，而文档 11 的“S2S 单模型的附带能力”章节称“Qwen3.5-Omni 实时（WebSocket）模式……不支持此功能”。实际以文档 9 为准，该模型在 WebSocket 模式下支持联网搜索，但需注意与 Function Calling 不可同时启用。

## 关键参数

各模型共性参数与关键字段如下：

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `model` | string | 模型ID，必须精确匹配（含快照版本） | `"qwen3.7-plus"`、`"Tripo/Tripo-P1.0"` |
| `input` | object | 输入数据容器，结构因模态而异 | `{"prompt": "夏日民谣"}`（音乐）、`{"image": "url"}`（3D） |
| `parameters` | object | 模型特有配置 | `{"texture_quality": "detailed"}`（Tripo）、`{"format": "wav"}`（音乐） |
| `reasoning.effort` | string | 控制思考模式深度（仅部分Qwen3模型） | `"low"` / `"medium"` / `"high"` |
| `X-DashScope-Async` | header | [异步任务](../concepts/asynchronous-task.md)必需头（如Tripo、视频生成） | `"enable"` |
| `is_instrumental` | boolean | Fun-Music 纯音乐开关 | `true` |

- **[异步任务](../concepts/asynchronous-task.md)**：Tripo 3D、视频生成等长耗时任务必须使用 `X-DashScope-Async: enable` 头，并轮询 `/api/v1/tasks/{task_id}` 获取结果（有效期24小时）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **[多模态输入](../concepts/multi-modal-input.md)**：视觉理解与全模态模型支持混合输入（如文本+图片+视频），但需注意 `qwen3.7-plus` 最大图片数2048张、视频数64个；`qwen3.5-omni-plus` 视频最大时长3小时 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **语言与方言**：Fun-ASR 支持超100种语言及方言（含吴语、闽南语等），而 Qwen3.5-Livetranslate 仅对60种语言输出语音，“仅文本”语言不生成音频 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。

## 使用方式

- **协议选择**：  
  - 实时交互（语音助手、直播字幕）→ **WebSocket**（`qwen-audio-3.0-realtime-plus`、`fun-asr-realtime`）；  
  - 批量处理（文件转写、视频分析）→ **HTTP**（`qwen3.5-omni-plus`、`fun-asr`）；  
  - 超长任务（3D生成、视频合成）→ **异步HTTP**（Tripo、HappyHorse）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **认证**：所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 必须在对应地域（如Tripo仅限华北2）开通并配置 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **SDK支持**：Qwen-Audio-TTS/CosyVoice、Fun-ASR 支持 Python/Java/Android/iOS SDK；其他模型建议直接调用REST API。  
- **快速验证**：新项目优先选用 `qwen3.7-plus`（文本）、`wan2.7-image-pro`（图像）、`qwen3.5-omni-plus`（多模态）进行效果验证，再按成本/性能需求降级至 `-flash` 系列。

## 限制和注意事项

- **地域限制**：Tripo 3D、Fun-Music 仅在华北2（北京）可用；部分Wan视频模型（如 `wan2.6-t2v-us`）专用于美国地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **资源约束**：  
  - 视频理解：`qwen3.7-plus` 单次请求最大视频大小2GB、时长2小时；  
  - 图像分辨率：每张图[Token](../concepts/token.md)消耗 = `h × w / (32 × 32) + 2`，高分辨率显著增加成本；  
  - 重排序：`qwen3-rerank` 最多处理500个文档，超限需分批。  
- **能力冲突**：  
  - 联网搜索与 Function Calling 不可同时启用（Qwen3.5-Omni）；  
  - 思考模式下不支持语音输出（Qwen3-Omni-Flash HTTP 模式除外）；  
  - `qwen-long`（1000万上下文）不支持 Function Calling 与内置工具 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **版本兼容性**：旧版模型（如 `qwen2.5-omni-7b`、`paraformer`）已停止更新，新项目应使用 Qwen3.5+ 或 Fun 系列；快照版本（如 `qwen3.7-plus-2026-05-26`）用于生产环境稳定性保障。  
- **成本提示**：`-flash` 后缀模型普遍比 `-plus` 成本低30–50%，但部分能力受限（如 `deepseek-v4-flash` 不支持内置工具）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)


