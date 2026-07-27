# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及计费策略等关键变更，面向开发者提供可落地的版本演进信息。内容涵盖新增模型支持、核心能力上线、参数与调用方式更新，以及已知限制。所有变更均以实际可用性为准，建议结合具体 API 文档与控制台状态验证。最新动态请同步参考 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 和 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 支持的模型/功能

- **新增模型（2026年7月起）**：`qwen3.7-flash`、`qwen3.7-max`（含多模态能力）、`qwen-image-3.0-pro`（支持10px小字渲染与12国语言）、`kimi/kimi-k3`（100万token上下文）、`qwen-audio-3.0-realtime-plus`（端到端实时语音）、`vidu/viduq3-ad_reference2video`（广告向参考生视频）、`pixverse/pixverse-lipsync`（视频对口型）等。详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **新增功能模块**：
  - 知识库 RAG：上线知识检索服务与知识问答服务（支持多知识库联合检索与混合排序）；
  - 智能体托管：新增 Managed Agent 运行时 API，支持平台托管会话与工具执行；
  - [数据连接](../concepts/data-connection.md)：支持 MySQL/语雀/OSS 等数据源接入，并提供 `ListCategory` 与 `ChangeParseSetting` 接口；
  - Prompt 工程：上线 Prompt 模板管理 API；
  - 模型评测：新增排行榜（Leaderboard）与综合评测能力，支持 BLEU_4、ROUGE 等评分方法；
  - 多模态交互开发套件：覆盖 Java SDK（服务端）、Android/iOS Lite SDK、RTOS C SDK 及 Linux C++ SDK。
- **模型调优增强**：支持强化学习（RL）训练（邀约制）、0代码安全合规强化、视觉理解（VL）、视频生成、图像生成模型类型；DPO 偏好训练已覆盖千问3/2.5全系列。

> **注意**：文档1中“2026年7月16日企业知识库（旧）下线通知”与文档2未提及该模块当前状态，实际使用中请确认是否已完全迁移至新版知识库 RAG 服务。旧版接口可能已不可用。

## 关键参数

- **模型单元（MU）计费**：自2026年1月起，模型部署 API 支持按 MU 时长计费，适用于 `qwen-flash`/`qwen-plus` 等预置模型；MU 配置直接影响性能与成本，需在部署时显式指定。
- **上下文缓存**：`cached_token` 单价独立计费（如 `deepseek-v4-pro` 为 1元/百万 token），非缓存 token（`input_token`）单价不变；需通过 `enable_cache=true` 显式启用。
- **异步任务**：`Responses API` 支持 `background=true` 提交长耗时任务，结果通过轮询或事件总线（EventBridge HTTP 回调 / RocketMQ）获取。
- **临时 API Key**：新增生成临时 [Token](../concepts/token.md) 能力，适用于不可信环境，有效期可配置，避免永久密钥泄露风险。
- **视觉输入约束**：部分模型（如 `qwen3.6-max-preview`）明确标注“不支持图像与视频输入”，调用前须校验模型规格说明。

## 使用方式

- **API 调用**：
  - 新版智能体应用统一使用 DashScope API（支持单/多轮、流式、文件问答、视觉理解）；
  - 文本生成 API 入口已聚合 OpenAI Responses 与 Anthropic Messages 接口分类；
  - 模型导入 API 已上线，支持从 OSS 导入 LoRA 微调模型（国际站可用）；
  - Spring AI Alibaba 框架已提供百炼智能体/工作流集成文档。
- **SDK 接入**：
  - 多模态交互开发套件提供跨平台 SDK（Java/Android/iOS/Lite/RTOS C/Linux C++）；
  - Codex 客户端已接入百炼，支持终端 AI 编程助手快速对接。
- **部署与托管**：
  - PTU 部署支持长输入与前缀缓存；
  - Managed Agent 运行时需通过专属 API 创建与管理会话生命周期；
  - UI 设计器支持低代码拖放构建网页应用，输出可直接发布。

## 限制和注意事项

- **模型下线机制**：老旧模型分批次下线（如2026年7月10日、9日多次通知），具体清单及过渡期见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)；部分模型延期下线（如7月6日通知），但不保证长期可用。
- **地域限制**：新增美国、德国、日本地域部署，但部分模型（如 `qwen-image-3.0-pro`）仅限华北2（北京）可用，调用前需确认模型地域支持列表。
- **免费额度策略**：新人免费额度启用“用完即停”功能（返回 `AllocationQuota.FreeTierOnly` 错误码），避免意外扣费；用量统计看板已上线，建议定期监控。
- **兼容性风险**：
  - `qwen-turbo` 资源包已启动退市（2026年6月28日），存量用户需迁移至其他资源包；
  - 企业知识库（旧）已于2026年7月16日下线，依赖该模块的应用必须迁移到新版 RAG 服务；
  - `kimi/kimi-k2.6` 与 `kimi-k2.6` 在文档2中重复列出且链接指向不同文档（阿里云 vs 月之暗面），实际调用应以控制台模型详情页为准。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


