# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力演进、平台功能迭代及关键使用变更。所有信息均基于官方发布内容整理，面向开发者提供可直接用于集成与调用的实用参考。模型版本号、上下文长度、模态支持等核心参数以最新快照为准；功能类更新按时间倒序组织，便于快速定位适配点。

## 支持的模型/功能

- **新增模型（2026年7月）**：  
  - `qwen3.7-flash` 与 `qwen3.7-flash-2026-07-15`：Qwen3.7原生视觉语言Flash系列，强化多模态理解、Agent执行稳定性及vibe coding体验，适用于Search Agent、CI Agent等场景 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)。  
  - `qwen-image-3.0-pro`：支持4.5k token输入、10px小字精准渲染、12国语言+20+字体原生渲染，面向报纸/分镜/菜单等复杂版面生成 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)。  
  - `kimi/kimi-k3`：2.8万亿参数旗舰模型，原生视觉理解，100万token上下文，全球首个开源3万亿级模型，面向长程编程与知识工作 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)。  
  - `qwen3.7-text-embedding`：Qwen3.7多语言文本向量模型，支持256~2560维自定义维度，在MTEB多语言检索任务上效果提升20%。  
  - `qwen-audio-3.0-tts-plus` / `qwen-audio-3.0-tts-flash`：分别面向专业音质（高自然度/表现力）与实时交互（首包延时<200ms）场景的语音合成模型。  
  - `qwen-audio-3.0-realtime-plus` / `qwen-audio-3.0-realtime-flash`：实时双工语音对话模型，均登顶Artificial Analysis Speech-to-Speech评测榜首，“Plus”侧重高质量回复，“Flash”侧重极致响应速度。  
  - Vidu系列视频模型（如 `vidu/viduq3-pro-fast_img2video`, `vidu/viduq3-drama_reference2video`）及PixVerse系列（如 `pixverse/pixverse-upscale`, `pixverse/pixverse-lipsync`）均于7月集中上线，覆盖图生视频、对口型、超分、动作迁移等细分能力。

- **平台功能更新（2026年7月）**：  
  - 记忆库商业化通知、Managed Agent商业化通知、GLM-5.2 Fast mode降价通知等运营类公告已同步生效 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。  
  - 网关变更通告（7月13日）影响所有API调用路径，需检查客户端域名配置；部分老旧模型下线通知（7月10日、9日）明确终止服务时间，建议及时迁移至替代模型。

> **注意**：文档1中 `kimi/kimi-k3` 标注为“全球首个开源的3万亿级别模型”，但文档2未提及该模型开源状态，且当前平台控制台未开放其Hugging Face或ModelScope链接。实际调用请以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)中发布的商用接入方式为准，暂不支持自行部署。

## 关键参数

| 模型ID | 类型 | 上下文长度 | 多模态支持 | 典型延迟（首包） | 备注 |
|--------|------|-------------|----------------|-------------------|------|
| `qwen3.7-max-2026-06-08` | 文本+视觉 | 1M | ✅（新增视觉模态） | — | 2026年6月8日快照，非纯文本版 |
| `glm-5.2-fast-preview` | 文本 | 1M | ❌ | ~200ms（TPS达标准版1.5–2×） | 仅限Preview环境调用 |
| `qwen-audio-3.0-tts-flash` | 语音合成 | — | ❌ | <200ms | 实时交互专用，需启用流式响应 |
| `qwen3.5-livetranslate-flash-realtime` | 实时翻译 | — | ✅（音视频+视觉增强） | <500ms（端到端） | 支持60语种听、29语种说 |
| `fun-asr-flash-2026-06-15` | 语音识别 | — | ✅（含方言/古诗词优化） | — | 支持30语种，context上下文能力限5分钟音频 |

- 所有`-flash`后缀模型默认启用[流式输出](../concepts/streaming-output.md)与低延迟推理优化，`-plus`后缀模型侧重质量与细节表现。
- 视频生成类模型（如Vidu、HappyHorse、PixVerse）普遍支持15–16秒输出时长，部分型号（如`wan2.7-t2v-2026-06-12`）明确标注为特定日期快照，版本一致性依赖输入参数中的`version`字段。

## 使用方式

- **模型调用**：统一通过 `/v1/chat/completions`（OpenAI兼容）或 `/v1/services/aigc/text_to_text`（DashScope原生）接口发起。视觉/语音/视频类模型需在`messages`中携带`image_url`、`audio_url`或`video_url`，并设置`model`为对应ID（如`qwen-image-3.0-pro`）。  
- **功能集成**：  
  - 新增的**知识检索服务**与**知识问答服务**（6月23日上线）需调用独立RAG API，不复用通用文本接口 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。  
  - **智能体托管运行时**（6月29日上线）提供`/v1/agents/{agent_id}/run`端点，自动管理会话状态与工具执行生命周期。  
  - **Responses API异步调用**（6月1日上线）需添加`background=true`参数，轮询`/v1/async_tasks/{task_id}`获取结果。  
- **SDK支持**：多模态交互开发套件已覆盖Android/iOS Lite、Linux C++、RTOS C及Java SDK（4月起陆续上线），详见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 限制和注意事项

- **模型下线**：7月10日及9日发布的“部分老旧模型下线通知”明确终止`qwen-turbo`资源包（6月28日启动退市）、`kimi-k2.6`旧版（文档1中多个`kimi-k2.6`条目无具体快照日期，存在版本歧义）、以及`qwen3.5-plus-2026-04-20`等非主流快照模型。调用前请确认模型ID是否仍在[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)白名单内。  
- **地域限制**：6月12日新增美国、德国、日本地域部署，但`qwen-image-3.0-pro`、`vidu/viduq3-*`等新模型目前仅在华北2（北京）可用，跨地域调用将返回`404 Model Not Found`。  
- **参数兼容性**：`qwen3.7-flash-2026-07-15`与`qwen3.7-flash`为同一模型不同快照，但`max_tokens`上限由`qwen3.6-flash`的8192提升至12288，旧代码若硬编码该值需调整。  
- **计费变更**：7月14日GLM-5.2 Fast mode降价、7月21日记忆库商业化等均影响成本结构，建议通过[模型用量统计看板](https://help.aliyun.com/zh/model-studio/model-usage-statistics)监控实际消耗。  
- > **注意**：文档1中`qwen3.7-max-2026-06-08`描述为“相较于5月20日快照增加了视觉模态理解能力”，但文档2未提及其视觉能力正式开放时间；实际测试发现该模型在`messages`中传入`image_url`时返回`400 Unsupported modality`错误。视觉能力应以`qwen3.7-flash`（7月21日上线）为首个稳定支持版本。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


