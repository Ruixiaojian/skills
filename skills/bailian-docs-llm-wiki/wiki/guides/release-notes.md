# release notes

本页汇总百炼平台近期模型与功能更新，面向开发者提供关键变更、可用能力及使用约束的结构化参考。内容涵盖新上线模型、平台功能迭代、参数与接口变动，以及已知限制。所有信息均基于官方发布文档整理，建议结合具体 API 文档与 SDK 版本验证兼容性。

## 支持的模型/功能

- **新增模型**（2026年7月）：  
  - 实时多模态：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`（端到端低延时语音交互）；  
  - 语音合成：`qwen-audio-3.0-tts-plus`（高品质）、`qwen-audio-3.0-tts-flash`（首包延时 ≤200ms）；  
  - Vidu 系列图像/视频生成：`vidu/vidu-image_reference2image`、`vidu/viduq3-ad_reference2video`、`vidu/viduq3-pro-fast_img2video` 等；  
  - Qwen 系列：`qwen3.7-max-2026-06-08`（新增视觉模态理解）、`qwen3.7-plus`（多模态交互混合智能体能力）；  
  - OCR：`qwen3.5-ocr`（128K上下文、多轮对话、卡证识别增强）。  
  完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

- **平台功能新增**（2026年6–7月）：  
  - 智能体托管运行时 API（[了解详情](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview)）；  
  - 知识检索服务与知识问答服务（支持多知识库联合检索与混合排序）；  
  - Responses API 新增异步调用模式（`background=true`）；  
  - 模型导入功能国际站上线（支持从 OSS 导入 LoRA 微调模型）；  
  - Skill 能力包上线（支持添加官方或自定义技能）。  
  功能动态详情见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

> **注意**：文档 1 中 `qwen3.7-max-2026-06-08` 标注“具备多模态交互混合智能体能力”，但文档 2 未提及该模型的多模态输入支持；而文档 1 同期列出的 `qwen3.7-plus` 明确支持视觉参考生成代码等能力。建议以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中的模型规格说明为准，并在实际调用前验证输入模态兼容性。

## 关键参数

- **模型输入约束**：  
  - `qwen3.7-max` 及 `qwen3.6-max-preview` 等 Max 系列模型**仅支持纯文本输入**，不接受图像或视频（见文档 1 中 2026-04-20 条目）；  
  - `kimi/kimi-k2.7-code` 仅支持思考模式；  
  - `qwen3.5-ocr` 上下文长度扩展至 128K，支持多轮对话；  
  - `qwen-audio-3.0-tts-flash` 首包延时控制在 200ms 以内。

- **部署与计费参数**：  
  - PTU 部署支持长输入与前缀缓存（2026-06-15 上线）；  
  - 模型部署支持按模型单元（MU）时长计费（2026-01-23 起）；  
  - `deepseek-v4-pro` 的 `cached_token` 单价调整为 1 元/百万 token（2026-04-29），标准 `input_token` 不变。

## 使用方式

- **模型调用**：  
  - 所有模型通过统一推理 API 接入，支持 OpenAI Responses 与 Anthropic Messages 接口分类（2026-05-15 更新）；  
  - 新增 DashScope 智能体应用 API（2026-05-11），支持单轮/多轮、流式、文件问答与视觉理解；  
  - 异步任务支持事件总线 HTTP 回调与 RocketMQ 主动推送（2026-04-23），避免轮询。

- **开发集成**：  
  - 多模态交互开发套件提供 Java SDK（服务端）、Android/iOS Lite SDK、RTOS C SDK 及 Linux C++ SDK；  
  - Spring AI Alibaba 框架已支持调用百炼智能体与工作流应用（2026-06-01）；  
  - Codex 终端 AI 编程助手于 2026-06-24 接入百炼。

- **模型定制**：  
  - 模型调优支持图像生成（Wan/Wanx）、视觉理解（VL）、视频生成三类模型（2026-05-28 / 01-22 / 01-21）；  
  - 支持强化学习（RL）训练（邀约制，2026-05-31）及 0 代码安全合规强化（2026-05-04）。

## 限制和注意事项

- **地域与部署范围**：多数新模型（如 Vidu、Qwen-Audio 系列）当前仅限中国内地服务，美国、德国、日本等新地域于 2026-06-12 启用，需显式指定 region 参数（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

- **模型下线风险**：  
  - 2026-07-10 起已启动部分老旧模型下线通知（含长尾模型），具体清单与机制参见 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)；  
  - `qwen-turbo` 资源包已于 2026-06-28 启动退市，存量资源包到期后不可续购。

- **兼容性约束**：  
  - `qwen3.6-max-preview` 明确标注“> 不支持图像与视频输入”（文档 1，2026-04-20），与同系列 `qwen3.7-plus` 的多模态能力形成对比，调用前须核对模型文档；  
  - `kimi/kimi-k2.7-code-highspeed` 与 `kimi/kimi-k2.7-code` 功能一致但速度提升 5~6 倍，二者不可混用同一缓存策略。

- **免费额度与用量**：新人免费额度启用“用完即停”功能（2025-07-29 上线），耗尽后返回 `AllocationQuota.FreeTierOnly` 错误码，需主动升级付费计划。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


