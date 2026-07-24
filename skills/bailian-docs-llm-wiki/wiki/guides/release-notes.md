# release notes

百炼平台的 Release Notes 汇总了模型、API、平台功能及计费策略的最新变更，面向开发者提供可落地的技术更新信息。内容涵盖新增模型支持、关键能力上线、参数调整、使用方式变更及下线计划，所有信息均以实际生效日期为准。建议开发者定期查阅本页，并结合 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md) 和 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 获取原始公告与技术细节。

## 支持的模型/功能

- **新增模型（2026年7月起）**：  
  - `qwen-image-3.0-pro`（图像生成，支持长文本输入与图中图密集排版）  
  - `kimi/kimi-k3`（100万 token 上下文，原生视觉理解）  
  - `qwen-audio-3.0-realtime-plus` / `qwen-audio-3.0-realtime-flash`（端到端实时语音大模型，双工交互优化）  
  - `vidu/viduq3-ad_reference2video` 等 Vidu 参考生视频系列（广告/短剧方向）  
  - `pixverse/pixverse-lipsync`（视频对口型）、`pixverse/pixverse-motioncontrol`（动作模仿）  
  - `qwen3.5-ocr`（128K上下文，多轮对话支持，卡证识别增强）  

- **核心功能上线**：  
  - 知识检索服务与知识问答服务（2026年6月23日）[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)  
  - 智能体托管运行时 API（2026年6月29日），支持平台托管会话与工具执行  
  - Responses API 异步调用模式（`background=true`，2026年6月1日）  
  - 模型评测排行榜与综合评测能力（2026年6月9日），支持 BLEU_4 等评分方法  
  - [多模态](../concepts/multi-modal.md)翻译 API 全面覆盖（文本/图片/文档/网页翻译，2026年5月26日）  

> **注意**：文档2中 `kimi/kimi-k2.6` 与 `kimi-k2.6` 为同一模型不同命名，但文档1未提及该模型；文档2中 `qwen3.6-max-preview` 明确标注“不支持图像与视频输入”，而文档1中同日发布的 `qwen3.7-plus` 则明确支持视觉-语言能力——请以模型文档页（如 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)）中具体模型规格说明为准，避免混淆。

## 关键参数

- **模型单元（MU）计费**：自2026年1月起，模型部署 API 支持按 MU 时长计费，适用于 `qwen-flash`/`qwen-plus` 等预置模型，提供可预测的固定成本与性能弹性调节能力。  
- **缓存相关参数**：  
  - `cached_token` 单价已调整（如 `deepseek-v4-pro` 为 1元/百万 token，2026年4月29日）  
  - PTU 部署支持前缀缓存（2026年6月15日）  
- **上下文长度**：  
  - `glm-5.1` 支持 200K 输入上下文（2026年4月14日）  
  - `qwen3.5-ocr` 扩展至 128K（2026年6月16日）  
- **异步任务回调**：支持通过事件总线 EventBridge 主动推送完成事件（HTTP 回调或 RocketMQ），替代轮询（2026年4月23日）。

## 使用方式

- **API 调用**：  
  - 新增 DashScope 智能体应用 API（2026年5月11日），支持单轮/多轮、流式、文件问答、视觉理解  
  - Responses API 启用 `background=true` 参数提交异步任务，后续通过 `GET /v1/async/{task_id}` 轮询结果  
  - 模型导入 API 已上线（2026年6月3日），支持从 OSS 导入 LoRA 微调模型  
- **SDK 接入**：  
  - [多模态](../concepts/multi-modal.md)交互开发套件提供 Linux C++ SDK（2026年2月28日）、Android/iOS Lite SDK（2026年2月6日）、RTOS C SDK（2026年4月9日）  
  - Codex 客户端接入（2026年6月24日），支持终端 AI 编程助手直连  
- **安全与鉴权**：  
  - API Key 支持加密存储与业务空间专属推理域名（2026年6月29日）  
  - 新增生成临时 API Key 文档（2026年6月3日），适用于不可信环境  

## 限制和注意事项

- **模型下线计划**：  
  - 2026年7月起分批下线部分老旧模型（7月10日、7月9日通知），含长尾模型与 `qwen-turbo` 资源包（6月28日启动退市）  
  - 企业知识库（旧）已于2026年7月16日下线，需迁移至新版知识库 RAG 服务  
  - 记忆库于2026年7月21日启动商业化，旧版免费额度不再适用  
- **地域与部署限制**：  
  - 新增美国、德国、日本地域（2026年6月12日），但部分模型（如 `qwen-audio-3.0-realtime-plus`）当前仅限华北2（北京）可用，详见各模型文档  
- **功能兼容性**：  
  - `qwen3.6-max-preview` 仅支持纯文本输入，不支持图像/视频（2026年4月20日）  
  - `kimi/kimi-k2.7-code-highspeed` 仅支持思考模式（2026年6月18日）  
- **免费额度策略**：  
  - 免费额度用完即停功能已启用（2025年7月29日），超额调用返回 `AllocationQuota.FreeTierOnly` 错误码  
  - 新人免费额度有效期已调整，详情见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


