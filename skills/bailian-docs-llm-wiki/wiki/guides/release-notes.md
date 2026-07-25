# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力演进、平台功能增强及关键使用约束。所有信息均基于官方发布内容整理，面向开发者提供可直接落地的参考依据。建议结合具体业务场景选择模型与功能，并关注下线通知以规避服务中断风险。

## 支持的模型/功能

- **新增模型**：2026年7月起，华北2（北京）地域陆续上线 Qwen3.7-Flash 系列（`qwen3.7-flash`）、Qwen-Image-3.0-Pro（`qwen-image-3.0-pro`）、Kimi K3（`kimi/kimi-k3`）、PixVerse 多模态视频模型（`pixverse/pixverse-lipsync`、`pixverse/pixverse-motioncontrol`、`pixverse/pixverse-upscale`）、Qwen-Audio-Realtime 系列（`qwen-audio-3.0-realtime-plus`）、Vidu 参考生视频系列（`vidu/viduq3-ad_reference2video`）等。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **平台功能扩展**：2026年6月起，新增知识检索服务与知识问答服务（支持多知识库联合检索与混合排序）、智能体托管运行时 API、Skill 能力包、数据连接模块（支持 MySQL/语雀/OSS）、模型导入 API（含 LoRA 微调模型 OSS 导入）、Responses API 异步调用模式（`background=true`）等。详情参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **调优与部署能力**：自2025年10月起，千问3-VL系列（`qwen3-vl-8b-instruct` 等）支持 SFT 微调；2026年5月起，模型调优新增强化学习（RL）训练（邀约制）及 0 代码安全合规强化流程；2026年4月起，支持图像生成、视觉理解、视频生成三类模型的定制训练。相关能力说明见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 关键参数

- **上下文长度**：Kimi K3 支持 100 万 token 上下文窗口；Qwen3.5-OCR 扩展至 128K；GLM-5.1 支持 200K 输入 + 128K 输出；Qwen3.7-Max 系列仅支持纯文本输入，不支持图像/视频（[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中明确标注）。
- **计费粒度**：DeepSeek-V4-Pro 的 `cached_token` 单价为 1 元/百万 token（2026-04-29 更新），标准 `input_token` 不变；[模型部署](../concepts/model-deployment.md)支持按模型单元（MU）时长计费（2025-10-24 起）；部分资源包（如 qwen-turbo）已启动退市流程（2026-06-28）。
- **输入模态限制**：Qwen3.7-Max 系列（含 `qwen3.7-max-preview`、`qwen3.7-max-2026-05-20`）明确标注“> 不支持图像与视频输入”；而 Qwen3.7-Plus、Qwen3.7-Flash 等则原生支持视觉-语言[多模态输入](../concepts/multimodal-input.md)。

## 使用方式

- **API 调用**：文本生成统一入口支持 OpenAI Responses 与 Anthropic Messages 接口分类（2025-05-15）；异步任务可通过事件总线 EventBridge 主动推送完成事件，避免轮询（2026-04-23）；新版智能体应用 DashScope API 支持单轮/多轮、流式、文件问答与视觉理解（2025-05-11）。
- **SDK 接入**：多模态交互开发套件已提供 Linux C++ SDK（2026-02-28）、Android/iOS Lite SDK（2026-02-06）、服务端 Java SDK（2026-04-28）及移动端 Android SDK（2026-04-14）；Spring AI Alibaba 框架调用百炼应用文档已上线（2026-06-01）。
- **[模型部署](../concepts/model-deployment.md)与调优**：预置吞吐部署（PTU）支持长输入与前缀缓存（2026-06-15）；模型导入支持从 OSS 加载 LoRA 微调模型（2026-06-05）；视觉理解与视频生成模型均支持定制训练（2025-01-22 / 2025-01-21）。

## 限制和注意事项

> **注意**：文档1中 `kimi/kimi-k2.6`（2026-04-26）与 `kimi-k2.6`（2026-04-21）模型标识不一致（前者带斜杠，后者无），且功能描述存在细微差异（前者强调“文本、图片与视频输入”，后者未明确提及视频输入），实际调用请以控制台或 API 文档为准。  
> **注意**：文档1中 `qwen3.7-max-preview`（2026-05-25）与 `qwen3.7-max`（2026-05-21）均标注“仅支持纯文本输入”，但文档1同节 `qwen3.7-max-2026-06-08` 却注明“增加了视觉模态理解能力”，存在明显矛盾。建议优先采用 `qwen3.7-max-2026-06-08` 及之后版本，并通过 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新快照确认能力边界。  
> **注意**：企业知识库（旧）已于2026-07-16下线，用户需迁移至新版知识库；部分老旧模型（含长尾模型）于2026-07-09起分批下线，具体清单需查阅 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)，该机制在两篇原始文档中均被引用，是判断模型生命周期的核心依据。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


