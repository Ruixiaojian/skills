# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、视觉、音视频、3D、语音、音乐等全模态生成与理解能力。本文档聚焦核心模型能力、关键参数、标准使用方式及硬性约束，不包含营销性描述，所有信息均基于当前稳定版 API 与模型服务规范。

## 支持的模型/功能

百炼提供覆盖[多模态](../concepts/multi-modal.md)的模型矩阵，按任务类型组织如下：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）和结构化 JSON 输出；`qwen3.7-flash` 在效果接近的前提下显著降低成本；`qwen3.7-max` 和 `qwen3.8-max-preview`（仅 [Token](../concepts/token.md) Plan 可用）适用于复杂推理场景 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 同时支持图像、视频（最长 2 小时）、OCR 和结构化输出；`qwen3.5-ocr` 专用于高精度文档/手写体文字提取；`qwen3-vl-plus` 等 VL 系列模型支持多图输入与视频理解 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片与视频生成**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图编辑与角色一致性；`happyhorse-1.1-t2v` 和 `wan2.7-t2v-2026-06-12` 分别适用于通用文生视频与带自定义音频的高质量生成；`tripo-p1.0` 和 `tripo-h3.1` 提供文/图/多图生 3D 模型能力，但仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音乐**：`fun-asr` 系列支持热词增强与说话人分离；`qwen3.5-omni-plus` 支持音视频联合理解与情感识别；`fun-music-v1` 支持 [prompt](prompt.md)/lyrics 双路输入与 gender 控制；`qwen-audio-3.0-tts-plus` 和 `cosyvoice-v3.5-plus` 均支持声音复刻与指令控制（如“温柔语速稍慢”）[原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **向量与重排序**：`text-embedding-v4` 为文本 Embedding 默认推荐，支持 64–2048 维可调；`qwen3-vl-embedding` 适用于图文混合检索；`qwen3-rerank` 支持最多 500 文档的纯文本重排序 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  

> **注意**：文档 1 中称 `qwen3.7-max` “不支持结构化输出”，但文档 2 的表格明确列出 `qwen3.7-plus` 和 `qwen3.7-flash` 均支持结构化输出，而 `qwen3.7-max` 对应列为“不支持”。该差异非矛盾，而是功能设计差异——`qwen3.7-max` 定位强推理，牺牲部分生成稳定性以换取逻辑深度，此行为符合其产品定位。

## 关键参数

各模态模型共性参数与典型取值如下：

| 参数名 | 说明 | 典型取值/约束 | 来源 |
|--------|------|----------------|------|
| `model` | 模型 ID，必须精确匹配（含快照版本） | `qwen3.7-plus`, `wan2.7-image-pro`, `fun-music-v1` | 全部文档 |
| `input` | 输入内容载体，结构因模态而异 | 文本：`{"prompt": "..."}`；图像：`{"image": "url"}`；音频：`{"audio_url": "..."}`；3D：`{"prompt": "...", "images": [...]}` | [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) |
| `parameters` | 模型特有配置 | `texture_quality: "standard"`（Tripo）、`format: "mp3"`（Fun-Music）、`reasoning.effort: "medium"`（Qwen 思考模式） | 全部文档 |
| `X-DashScope-Async` | 异步任务必需 Header | `"enable"`（Tripo、Fun-Music 等长耗时任务） | [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) |
| `Authorization` | 认证凭证 | `Bearer $DASHSCOPE_API_KEY`，需提前配置环境变量或显式传入 | 全部文档 |

> **注意**：文档 10 与文档 11 均指出 `qwen3.5-omni-plus-realtime` 支持联网搜索，但文档 10 明确标注“联网搜索与 Function Calling 不可同时开启”，而文档 11 未提及此互斥限制。实际调用中必须遵守该约束，否则请求将失败。

## 使用方式

统一采用 RESTful API 调用，遵循以下通用流程：

1. **准备凭证**：获取 API Key 并配置至环境变量 `DASHSCOPE_API_KEY` 或请求头；  
2. **构造请求**：  
   - HTTP 模式：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/{service}/{endpoint}`；  
   - WebSocket 模式：连接 `wss://dashscope.aliyuncs.com/api/v1/services/{service}/{endpoint}`；  
3. **提交输入**：按模型要求组织 `input` 字段（如文本、URL、base64、文件 token）；  
4. **处理响应**：  
   - 同步接口：直接返回结果（如 TTS 音频 URL、ASR 文本）；  
   - 异步接口（Tripo、Fun-Music）：先获 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 获取 `SUCCEEDED` 状态及产物 URL；  
   - 流式接口（Realtime ASR/TTS）：建立 WebSocket 连接后，接收分块数据帧。  

所有模型均需指定 `WorkspaceId`（业务空间 ID），且多数服务（Tripo、Fun-Music、Fun-ASR）仅在华北2（北京）地域可用。跨地域调用需确认模型是否在目标 Region 发布（如文档 1 中列出的新加坡/美国/法兰克福链接）。

## 限制和注意事项

- **地域限制**：Tripo 3D、Fun-Music、Fun-ASR 等模型**仅支持华北2（北京）**，调用前必须确认 Endpoint 域名含 `cn-beijing`；其他模型（如 Qwen3 系列）在多 Region 可用，但需通过控制台确认具体部署状态 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **输入规格**：  
  - 图像：单图最高 1600 万像素，[Token](../concepts/token.md) 消耗 = `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 支持最长 2 小时/2GB，`qwen3-vl-plus` 限 1 小时；  
  - 音频：Fun-ASR 非实时最大 12 小时/2GB，Qwen3.5-Omni 非实时限 3 小时/2GB；  
  - 3D 多图输入：仅接受 2–4 张 JPEG/PNG，单图 ≤ 20MB；  
- **功能互斥**：  
  - `qwen3.5-omni-plus` 的联网搜索与 Function Calling 不可同时启用；  
  - `qwen3-omni-flash` 的思考模式启用时**不生成语音输出**（仅文本）；  
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）提供确定性行为，但需主动维护；`-latest` 或无后缀版本自动更新，适合快速迭代但需监控变更日志。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)



