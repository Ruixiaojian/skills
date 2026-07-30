# 多模态

多模态（Multimodal）指模型能够同时理解、生成或处理多种类型数据（如文本、图像、音频、视频等）的能力，是百炼平台实现跨模态语义对齐与协同推理的核心技术基础。它不仅支持单一模态输入+单一模态输出（如文生图），更强调多模态联合建模——例如图文混合输入驱动文本响应、音视频同步生成、或跨模态检索与排序。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中并非单一 API，而是贯穿多个服务层级的统一能力范式，按使用方式可分为三类：

- **输入侧多模态**：允许一次请求中混合提交不同模态数据。  
  - 应用调用（`application call`）：通过 OpenAI 兼容 `messages` 数组传入 `role: "user"` + `content: [{type: "text", text: "..."}, {type: "image_url", image_url: {url: "data:image/jpeg;base64,..."}]`；智能体需选用 VL 模型（如 `qwen3.7-plus`），工作流节点需将变量名设为 `imageList`。  
  - Omni Realtime API：支持 PCM 音频（16 kHz）与 JPG/JPEG 图像（≤1080p，Base64 编码 ≤256 KB）实时流式输入。  
  - 向量与排序（`vector and sort`）：`qwen3-vl-embedding` 接受文本+图像/视频组合输入，生成融合向量或独立模态向量。

- **输出侧多模态**：指定返回结果的模态组合。  
  - Omni Realtime API：通过 `modalities: ["text", "audio"]` 控制同步返回文本流与 PCM 音频流（24 kHz）。  
  - 图像生成：虽为单模态输出（图像），但其 [prompt](../guides/prompt.md) 理解依赖文本-图像联合建模，属于典型的多模态生成任务。

- **跨模态能力复用**：将多模态能力作为底层能力被其他服务调用。  
  - [Token](token.md) Plan：图像/视频/语音模型（如 `wan2.7-image-pro`, `happyhorse-1.1-t2v`, `qwen-audio-3.0-tts-plus`）需通过 Skill/Agent/Slash Command 封装后接入，不可直连 OpenAI Base URL。  
  - 视觉理解：`qwen3.7-plus` 原生支持图像/视频/OCR 输入并输出结构化文本；纯文本模型（如 `glm-5`）需借助 Skill 或 Agent 扩展视觉能力。  
  - 多模态排序：`qwen3-vl-rerank` 支持 query 与 document 的任意模态组合（如“一张产品图” vs “10段商品描述文本”），实现真正跨模态相关性打分。

> ⚠️ 注意：文件输入（PDF/Word 等）仅在**智能体应用**中支持，且必须配置为“全文引用”或“切片检索”模式；工作流和纯模型 API 不直接支持原始文件上传。

## 关键参数和配置

| 参数/配置项 | 说明 | 典型值/约束 | 适用场景 |
|-------------|------|--------------|----------|
| `input.messages`（OpenAI 兼容） | 多模态输入标准格式，每个 `content` 项可含 `text`/`image_url`/`audio_url` 等子项 | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}]` | Application Call、[Token](token.md) Plan（Skill 封装后）、Omni Realtime |
| `imageList`（工作流变量名） | 工作流中接收图像输入的预定义变量名 | 必须命名为 `imageList`，类型为 `array<string>`（图片 URL 列表） | 工作流节点配置 |
| `modalities` | 指定输出模态组合 | `["text"]` 或 `["text","audio"]`（Omni Realtime）；`["text","image"]` 尚未开放，当前仅支持 `text`+`audio` | Omni Realtime、Realtime API |
| `enable_fusion`（向量） | 控制是否将多模态输入融合为单向量 | `true` / `false`；设为 `true` 时返回一个融合向量，`false` 时返回各模态独立向量 | `qwen3-vl-embedding` |
| `X-DashScope-Async`（Header） | 异步任务必需头，用于图像生成、3D 生成等长耗时多模态任务 | `"enable"` | Image Generation、Tripo 3D、Fun-Music 等 |

- **模型选择硬性要求**：  
  - 图像理解/生成：必须选用 `qwen3-vl-*`、`wan2.*`、`qwen-image-*` 等显式标注 VL（Vision-Language）或 multimodal 的模型 ID；`qwen3.7-plus` 等文本模型虽支持图像输入，但本质是 VL 模型的文本分支，仍属多模态能力。  
  - 实时音视频：必须选用 `qwen3.5-omni-*` 系列模型，`qwen-audio-*` 等纯语音模型不支持图像输入。  
- **地域限制**：所有多模态能力（除部分异步图像生成外）当前均**仅限华北2（北京）地域**可用，调用时务必确认 `workspace_id` 和 endpoint 匹配。

## 面向开发者，简洁实用

- ✅ **快速验证**：控制台 → 应用卡片 → 发布 → API 调试，选择支持 VL 的应用，粘贴含 `image_url` 的 messages 即可测试图文理解。  
- ✅ **SDK 推荐**：  
  - Python：优先用 `openai>=1.0.0` SDK（兼容 OpenAI 格式），配合 `base_url` 指向 [Token](token.md) Plan 或 DashScope 兼容接口；  
  - 实时交互：用 `dashscope` 官方 SDK（WebSocket）或 `aiortc`（WebRTC）；  
  - 批量向量：用 `dashscope.BatchTextEmbedding`（异步）或 `openai.Embedding`（同步）。  
- ✅ **避坑提示**：  
  - 图像 Base64 编码前需确保格式为 JPG/JPEG，PNG 可能触发 400 错误；  
  - `application call` 中 `background=true`（异步）**不支持多模态[流式输出](streaming-output.md)**，需改用同步调用；  
  - Token Plan 的多模态模型（如 `wan2.7-image-pro`）**不能直接通过 OpenAI Base URL 调用**，必须走 Skill/Agent 封装路径。  
- 🚀 **进阶建议**：构建 RAG 应用时，优先选用 `qwen3-vl-embedding` + `qwen3-vl-rerank` 组合，实现文档 PDF（含图表）→ 文本+图像向量化 → 跨模态重排序的端到端链路。

## 关联主题页

- [application call](../api/application-call.md)
- [token plan guide](../guides/token-plan-guide.md)
- [image generation](../api/image-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [model experience](../guides/model-experience.md)
- [use cases](../guides/use-cases.md)
- [vector and sort](../api/vector-and-sort.md)


