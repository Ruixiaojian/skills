# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力演进、平台功能增强及关键使用变更。所有信息均基于官方发布记录整理，面向开发者提供可直接落地的参考依据。建议结合具体模型文档与 API 参考手册进行集成。

## 支持的模型/功能

- **新增模型**：2026年7月起，Qwen-Image-3.0-Pro（[原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)）、Kimi K3（2.8万亿参数，100万token上下文）、PixVerse系列视频模型（lipsync/motioncontrol/upscale）、Qwen-Audio-3.0-realtime-plus 与 flash 版本、Vidu 多版本 reference2image/reference2video/img2video、Wan2.7-r2v-2026-06-12 等集中上线，覆盖图像生成、视频对口型、动作模仿、超清增强、实时语音交互等场景。
- **[多模态](../concepts/multi-modal.md)能力扩展**：Qwen3.7-plus 及 Qwen3.7-max-2026-06-08 明确支持视觉模态理解；qwen3.5-ocr 提供128K上下文与多卡证识别；Tripo-H3.1/P1.0 支持文生/图生/多图生3D；Fun-music-v1 支持歌词驱动的中英文歌曲生成。
- **平台级功能新增**：2026年6月起，知识检索服务（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）与知识问答服务上线，支持多知识库联合检索与混合排序；智能体托管运行时 API（6月29日）、Responses API 异步调用（6月1日）、模型导入 API（6月3日）均已正式可用；5月起模型调优支持强化学习训练（RL，邀约制）、图像/视频/视觉理解模型类型定制训练。

> **注意**：文档1中多次出现 `kimi/kimi-k2.6` 与 `kimi-k2.6` 两种命名（如2026-04-26与2026-04-21条目），且后者链接指向 `https://help.aliyun.com/zh/model-studio/kimi-api`（非月之暗面专属页），而前者统一链接至 `https://help.aliyun.com/zh/model-studio/kimi-api-by-moonshot-ai`。建议以 `kimi/kimi-k2.6` 为准，该命名与文档2中“Kimi-月之暗面”官方标识一致，且符合平台模型命名规范。

## 关键参数

- **上下文长度**：Kimi K3 支持 100 万 token；qwen3.5-ocr、glm-5.1 分别支持 128K、200K；qwen3.7-max 系列仅支持纯文本输入，不接受图像/视频。
- **部署规格**：Qwen-Audio-3.0-realtime-plus 与 flash 版本分别面向高品质专业场景与低延迟实时交互；PixVerse 系列明确区分 lipsync/motioncontrol/upscale 功能边界；Vidu 模型按 `reference2image`/`reference2video`/`img2video` 后缀标识任务类型。
- **计费与资源**：deepseek-v4-pro 的 `cached_token` 单价调整为 1 元/百万 token（文档1，2026-04-29）；qwen-turbo 资源包已启动退市（文档2，2026-06-28）；[模型部署](../concepts/model-deployment.md)支持按模型单元（MU）时长计费（文档2，2026-01-23）。

## 使用方式

- **API 调用**：文本生成 API 已聚合 OpenAI Responses 与 Anthropic Messages 接口分类（文档2，2026-05-15）；Responses API 新增 `background=true` 异步模式（文档2，2026-06-01）；异步任务支持事件总线 HTTP 回调与 RocketMQ 主动推送（文档2，2026-04-23），避免轮询。
- **SDK 与客户端**：[多模态](../concepts/multi-modal.md)交互开发套件提供 Linux C++ SDK（2026-02-28）、Android/iOS Lite SDK（2026-02-06）、Java SDK（2026-04-28）及 RTOS C SDK（2026-04-09）；Kilo CLI 支持 [Token](../concepts/token.md) Plan/Coding Plan/按量计费三种接入方式（文档2，2026-02-22）；Spring AI Alibaba 文档已上线（文档2，2026-06-01）。
- **安全与鉴权**：新增生成临时 API Key 文档（文档2，2026-06-03），适用于不可信环境；API Key 加密存储与业务空间专属推理 API 域名已完成升级（文档2，2026-06-29）。

## 限制和注意事项

- **模型下线机制**：老旧模型分批次下线，包括“部分老旧模型下线通知”（2026-07-10）、“部分老旧长尾模型下线通知”（2026-07-09）及“延期下线通知”（2026-07-06）。具体清单需参考 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)，该机制在两篇原始文档中均被引用（[原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 和 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **地域与部署范围**：新增美国、德国、日本地域（文档2，2026-06-12），但文档1中所有模型当前仅标注“中国内地”服务范围，跨地域调用需确认模型是否已同步部署。
- **功能兼容性**：qwen3.6-max-preview 明确注明“> 不支持图像与视频输入”（文档1，2026-04-20），而同系列 qwen3.7-plus 则明确支持视觉-语言能力，版本间能力差异显著，不可混用。
- **免费额度策略**：新人免费额度启用“用完即停”功能后，耗尽将返回 `AllocationQuota.FreeTierOnly` 错误（文档2，2025-07-29），避免意外计费；2026年7月起企业知识库（旧）已下线（文档2，2026-07-16），迁移需使用新版知识库RAG服务。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


