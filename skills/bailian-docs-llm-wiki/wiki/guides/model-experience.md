# model experience

`model experience` 是百炼平台统一的模型能力体验层，面向开发者提供覆盖文本、视觉、音频、3D、视频等[多模态](../concepts/multi-modal.md)任务的标准化调用接口与能力矩阵。所有模型均通过统一的 DashScope API 接入，支持同步/异步、流式/非流式、HTTP/WebSocket 等多种交互模式，并在功能支持（如 Function Calling、思考模式、结构化输出）、上下文长度、输入模态和计费维度上形成清晰的分层体系。选型应优先依据任务类型与核心能力需求，再结合成本、延迟与地域约束综合决策。

## 支持的模型与功能

百炼平台按模态与任务类型组织模型能力，主要分为以下五类：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及 `enable_thinking` 控制的深度推理模式；轻量场景可选用 `qwen3.6-flash` 或 `deepseek-v4-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 同时支持图像、视频（最长2小时）、OCR 及多图理解；专用 OCR 模型 `qwen3.5-ocr` 在文档/手写识别上更优；Qwen3-VL 系列（如 `qwen3-vl-plus`）专为图文联合建模优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑与角色一致性；`qwen-image-3.0-pro`（邀测中）支持负向提示词与多语言字体渲染；`z-image-turbo` 适用于低成本快速生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D/视频/音频生成**：Tripo 系列（`Tripo/Tripo-P1.0`）支持文/图/多图生3D；视频生成推荐 `happyhorse-1.1-t2v`（文生视频）或 `wan2.7-i2v-2026-04-25`（首尾帧续写）；Fun-Music（`fun-music-v1`）支持歌词/提示词驱动的歌曲生成，但需申请邀测 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **语音与全模态**：语音识别推荐 `fun-asr`（支持说话人分离）或 `qwen3.5-omni-plus`（支持 Prompt 注入与情感识别）；语音合成首选 `qwen-audio-3.0-tts-plus`（支持声音复刻与指令控制）；全模态模型 `qwen3.5-omni-plus` 支持音视频+文本联合理解与 Function Calling [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解首选，但文档 2 明确其支持“最长2小时视频”，而文档 1 未提及视频能力——该差异源于文档 1 聚焦通用文本生成，视觉能力属延伸支持，实际调用需以文档 2 的视觉输入规格为准。

## 关键参数

不同模态模型共用核心参数，但语义与约束各异：

- `model`：必填，指定模型 ID（如 `qwen3.7-plus`, `wan2.7-image-pro`, `Tripo/Tripo-P1.0`）。  
- `input`：结构因模态而异：  
  - 文本/语音：`{"text": "..."}` 或 `{"audio_url": "..."}`；  
  - 视觉：`{"image": "url"}`, `{"images": ["url1", "url2"]}`, `{"video": "url"}`；  
  - 3D：`{"prompt": "..."}`, `{"image": "url"}`, 或 `{"images": [...]}`（三者互斥）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；  
  - 音乐：`{"prompt": "...", "gender": "female"}` 或 `{"lyrics": "...", "is_instrumental": true}`。  
- `parameters`：控制生成行为：  
  - `texture_quality`（Tripo）、`format`（Fun-Music）、`geometry_quality`（Tripo-H3.1）；  
  - `reasoning.effort`（文本思考深度）、`enable_thinking`（布尔开关）；  
  - `max_output_tokens`（部分模型限制输出长度）。  
- `X-DashScope-Async: enable`：异步任务必需头（如 Tripo 3D、批量视频生成）。

## 使用方式

统一采用 RESTful API，基础流程如下：

1. **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传入 API Key（需在华北2北京地域开通）；  
2. **端点**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/{service}/{action}`，其中 `service` 如 `aigc/text-generation`、`audio/music/generation`、`aigc/video-generation/3d-generation`；  
3. **同步调用**：HTTP POST 直接返回结果（适用于文本、TTS、ASR 小文件）；  
4. **异步调用**：  
   - 先 POST 创建任务获 `task_id`；  
   - 再 GET `/api/v1/tasks/{task_id}` 轮询状态（建议间隔 ≥15 秒）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；  
5. **流式响应**：WebSocket 连接（实时 TTS/ASR/S2S）或 HTTP chunked encoding（部分文本/语音模型）。

## 限制和注意事项

- **地域与服务开通**：Tripo 3D、Fun-Music 仅限华北2（北京）；部分模型（如 `qwen3.8-max-preview`）需 [Token](../concepts/token.md) Plan 权限 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **输入约束**：  
  - 图像：单图 ≤1600万像素，[Token](../concepts/token.md) 数 = `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 最长2小时/2GB，`qwen3-vl-plus` 限1小时；  
  - 音频：`fun-asr` 非实时最大 12小时/2GB，`qwen3.5-omni-plus` 非实时限3小时/2GB。  
- **能力冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式下不支持语音输出 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）保障稳定性，但旧版模型（Qwen3、Qwen2.5 系列）已停止更新，新项目应使用 Qwen3.6+ [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **跨模态兼容性**：[多模态](../concepts/multi-modal.md) Embedding（`qwen3-vl-embedding`）与重排序（`qwen3-vl-rerank`）需配套使用，不可混用文本 Embedding 模型。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


