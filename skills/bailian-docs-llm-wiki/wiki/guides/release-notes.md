# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键能力变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型观测」和「通知中心」及时获取最新动态。本文档不包含营销性描述，仅提炼技术事实与约束条件。

## 支持的模型/功能

- **新增模型**：2026年7–8月集中上架[多模态](../concepts/multi-modal.md)旗舰模型，包括 `qwen3.8-max`（2.4T MoE，100万上下文）、`kimi/kimi-k3`（2.8T，KDA注意力）、`deepseek-v4-pro-0813`（1.6T/49B激活）、`pixverse/pixverse-v6-r2v-omni`（混合参考视频生成）等；语音方向新增 `qwen-audio-3.0-asr-flash-streaming`（实时ASR）、`qwen-audio-3.0-tts-plus`（高表现力TTS）及 `qwen-audio-3.0-realtime-plus`（双工对话）三类模型。详情见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能扩展**：2026年6月起全面支持视频生成模型调优（如万相系列）、图像生成模型调优（`qwen-image-3.0-pro`）、视觉理解模型（VL）调优（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）；7月上线知识检索服务与知识问答服务，支持多知识库联合检索与混合排序；8月新增模型升级通知机制，提升版本变更透明度。
- **平台能力升级**：2026年6月起支持 API Key 加密存储与业务空间专属推理域名；7月上线智能体托管运行时 API；8月支持 Responses API 异步调用（`background=true`）；模型评测模块于6月新增排行榜与 BLEU_4 等综合评分方法。

## 关键参数

- **上下文长度**：主流新模型（如 `qwen3.8-max`、`glm-5.2`、`kimi-k3`）原生支持 **100 万 [Token](../concepts/token.md)** 上下文；`qwen-image-3.0` 支持最大 **4.5k token 输入**；`pixverse/pixverse-v6-r2v-omni` 支持最长 **16 秒视频生成**。
- **性能指标**：`deepseek-v4-flash-0731` 输出延迟低、QPM 高，适用于高并发轻量化任务；`kimi-k2.7-code-highspeed` 编程输出速度达 **180–260 [Token](../concepts/token.md)/s**；`qwen-audio-3.0-tts-flash` 首包延时 **≤200ms**；`qwen-audio-3.0-realtime-flash` 实现端到端低时延双工交互。
- **向量与嵌入**：`qwen3.7-text-embedding` 支持 **256–2560 维自定义向量维度**，在 MTEB 多语言检索任务中效果较 v4 提升 20%。

## 使用方式

- **模型调用**：所有新模型均通过标准 DashScope API 接入，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`）与 Anthropic Messages 格式（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）；视频/图像类模型需按具体文档指定输入格式（如 `pixverse/pixverse-v6-r2v-omni` 要求图片+视频混合参考）。
- **部署与调优**：预置模型（如 `qwen-flash`）支持 API 直接部署并按模型单元（MU）时长计费；微调模型支持 LoRA/全参 SFT 及 DPO 偏好训练（千问2.5/3系列、GLM-5.1/5.2）；图像/视频/视觉理解模型调优能力已于 2026 年 5–6 月全面开放。
- **异步与事件驱动**：长耗时任务（如视频生成、大文件 RAG）推荐使用 Responses API 异步模式；异步任务完成事件可通过事件总线（EventBridge）HTTP 回调或 RocketMQ 主动推送，避免轮询。

## 限制和注意事项

- > **注意**：文档 1 中称“主线模型下线前通知期为 3 个月”，但文档 3 显示 2026 年 7 月 10 日发布的 [部分老旧模型下线通知](https://www.aliyun.com/notice/118434) 对应 2026 年 10 月 10 日下线，实际通知期仅约 3 个月；而同日发布的 [部分老旧长尾模型下线通知](https://www.aliyun.com/notice/118427) 未明确下线日期。此处以文档 1 的通用规则为准，但开发者须以具体公告日期为最终依据。
- > **注意**：文档 2 列出 `qwen3.7-flash-2026-07-15` 与 `qwen3.7-flash` 并存，但未说明二者是否为同一模型快照。结合文档 3 中 6 月已上线 `qwen3.7-flash` 调优支持，推断 `-2026-07-15` 为该模型的明确快照标识，非独立模型，调用时应优先使用无日期后缀的稳定 ID（如 `qwen3.7-flash`），避免依赖快照 ID 导致未来不可用。
- 模型下线后，**已部署应用将立即失效**：自正式下线日起，API 推理、新调优/新部署均停止；已训练/已部署模型不受影响，但无法再创建新实例。务必通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 定期检查存量模型状态。
- 部分功能存在地域限制：新增美国、德国、日本地域部署范围（2026年6月12日），但 `pixverse`、`vidu`、`Tripo` 等第三方模型当前仅在华北2（北京）可用，调用前需确认 endpoint 区域。
- 企业知识库（旧）已于 2026 年 7 月 16 日下线，迁移至新版知识库 RAG 服务；`qwen-turbo` 资源包于 6 月 28 日启动退市，不再售卖。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


