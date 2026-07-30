# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力增强、平台功能迭代及关键使用变更。所有信息均基于官方发布内容整理，面向开发者提供可直接落地的参考依据。建议结合具体业务场景选择适配模型，并关注下线通知以规避服务中断风险。

## 支持的模型/功能

- **文本生成与智能体**：新增 `qwen3.7-flash`（2026-07-21）、`glm-5.2-fast-preview`（2026-07-09）、`kimi/kimi-k3`（2026-07-17）等高吞吐/长上下文模型；`qwen3.7-max-2026-06-08` 已支持视觉模态理解，具备[多模态](../concepts/multi-modal.md)交互混合智能体能力。  
- **[多模态](../concepts/multi-modal.md)生成**：图片生成新增 `qwen-image-3.0-pro`（2026-07-20），支持 4.5k token 输入与 10px 小字精准渲染；视频生成新增 `vidu/viduq3-pro-fast_img2video`（2026-07-09）、`pixverse/pixverse-motioncontrol`（2026-07-14）等专用能力模型。  
- **语音与音频**：实时语音合成新增 `qwen-audio-3.0-tts-plus`（高质量）与 `qwen-audio-3.0-tts-flash`（低延迟）双版本；实时语音对话新增 `qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-realtime-flash`，端到端响应时延优化至低水平。  
- **向量与识别**：文本向量新增 `qwen3.7-text-embedding`（2026-07-15），支持 256~2560 维自定义维度；OCR 新增 `qwen3.5-ocr`（2026-06-16），在卡证类业务场景抽取效果显著提升。  
- **平台级能力**：新增 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中描述的多项能力，包括知识检索服务、智能体托管运行时 API、Skill 能力包、数据连接模块等，详见该文档。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流旗舰模型均支持 100 万 token 上下文；`qwen3.7-flash` 等 Flash 系列模型在保持长上下文的同时侧重推理速度优化。  
- **输入限制**：`vidu/viduq3-fast_reference2image` 支持 0–14 张参考图；`pixverse/pixverse-v6-r2v` 支持 2–7 张图像输入；`fun-asr-flash-2026-06-15` ASR 模型支持 ≤5 分钟音频转写。  
- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`kimi/kimi-k2.7-code-highspeed` 编程输出速度达 180–260 [Token](../concepts/token.md)/s；`qwen3.7-text-embedding` 在 MTEB 多语言检索任务上效果提升 20%。  
- **部署规格**：模型部署支持按模型单元（MU）时长计费，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中“1月23日”条目。

## 使用方式

- **API 调用**：文本生成统一入口已聚合 OpenAI Responses 与 Anthropic Messages 接口分类（[详见文档2 5月15日更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）；Responses API 新增 `background=true` 异步调用模式（2026-06-01）。  
- **SDK 接入**：[多模态](../concepts/multi-modal.md)交互开发套件已提供 Linux C++、Android、iOS Lite、RTOS C 等多端 SDK（[详见文档2 2月/4月条目](../../raw/model-user-guide/release-notes/model-release-notes.md)）；Spring AI Alibaba 框架调用百炼应用文档已上线（2026-06-01）。  
- **模型部署**：预置吞吐部署（PTU）新增长输入与前缀缓存能力（2026-06-15）；国际站支持从 OSS 导入 LoRA 微调模型（2026-06-05）。  
- **智能体开发**：可通过 Skill 能力包添加官方或自定义技能（2026-06-10）；Managed Agent 运行时 API 支持平台托管会话与工具执行（2026-06-29）。

## 限制和注意事项

- > **注意**：文档1中 `kimi/kimi-k2.7-code`（2026-06-15）与 `kimi/kimi-k2.7-code-highspeed`（2026-06-17）被描述为“同一个模型”，但文档1未说明二者是否共享同一模型 ID 或 API 路径。实际调用前请以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中列出的模型 ID 为准，并验证接口兼容性。  
- > **注意**：文档2中“7月10日”与“7月9日”分别提及“部分老旧模型下线”和“部分老旧长尾模型下线”，但未明确具体模型清单；而文档1中大量模型（如 `qwen3.6-flash-2026-04-16`、`qwen-image-2.0-pro-2026-04-22`）标注为历史快照版。建议开发者主动查阅 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation) 并监控控制台通知，避免依赖已标记为“快照”或无后续更新的模型。  
- 所有 Flash/Plus/Pro/Turbo 等后缀模型均代表不同性能-成本权衡点，例如 `qwen-audio-3.0-tts-flash` 侧重低延迟，`qwen-audio-3.0-tts-plus` 侧重音质细节，不可混用配置参数。  
- 视频生成类模型（如 `vidu/viduq3-drama_reference2video`、`wan2.7-r2v-2026-06-12`）对输入参考图数量、格式、分辨率有明确要求，超出范围将导致任务失败或效果劣化，需严格遵循各模型文档说明。  
- 模型调优功能当前对部分模型类型（如视频生成、VL 模型）仍为邀约制或有限开放（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 5月31日、5月28日、1月21日条目），非全量可用。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)



