# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、API 变更及平台能力演进等关键动态，面向开发者提供可落地的技术更新概览。内容覆盖模型支持范围、核心参数变更、调用方式升级、已知限制与兼容性注意事项。所有信息均基于平台近期正式发布版本，建议开发者结合自身场景关注模型生命周期状态与接口兼容性。

## 支持的模型/功能

- **新增模型**：2026年7月起，华北2（北京）地域陆续上线 `qwen-audio-3.0-realtime-plus`（实时多模态）、`vidu/viduq3-ad_reference2video`（参考生视频）、`happyhorse-1.1-t2v`（文生视频）、`fun-music-v1`（音乐生成）、`Tripo/Tripo-H3.1`（3D生成）等数十款模型，覆盖语音、图像、视频、3D、音乐及全模态场景。详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型能力扩展**：Qwen3.7系列全面增强多模态交互混合智能体能力；Kimi K2.7 Code 系列新增高速档位（`kimi/kimi-k2.7-code-highspeed`），推理速度提升5~6倍；GLM-5.1 支持200K上下文与128K最大输出；DeepSeek-V4-Pro 支持 `cached_token` 单价调整为1元/百万token（见[文档 2](../../raw/model-user-guide/release-notes/newly-released-models.md)）。
- **功能模块上线**：6月新增知识检索服务与知识问答服务（支持多知识库联合检索与混合排序）；6月上线智能体托管运行时 API；5月起模型调优支持强化学习（RL）、0代码安全合规强化、视频/图像/视觉理解模型类型；4月起多模态交互开发套件覆盖 Android/iOS Lite、Linux C++、RTOS C 等全端 SDK。

> **注意**：文档 1 中提及“Qwen3-VL-8B-Instruct/Thinking 支持 SFT 调优”（2025年10月），但文档 2 中未列出该模型上架记录，且其命名与当前主流 Qwen3.5/Qwen3.6/Qwen3.7 系列不一致，建议以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中实际发布的模型列表为准，避免使用非公开快照模型。

## 关键参数

- **计费模式**：模型部署支持按模型单元（MU）时长计费（自2025年10月起），适用于 `qwen-flash`/`qwen-plus` 等预置模型；`deepseek-v4-pro` 的 `cached_token` 单价明确为 **1 元/百万 token**（标准 `input_token` 不变）。
- **上下文与输出**：GLM-5.1 支持 200K 上下文与 128K 最大输出；Qwen3.5-OCR 上下文扩展至 128K；Qwen3.7-Max 系列仅支持纯文本输入，默认开启思考模式，支持显式缓存。
- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`qwen3.6-flash` 系列在代码智能体基准中大幅超越前代；`wan2.7-r2v` 支持单张多宫格故事板一键生成剧本化视频。

## 使用方式

- **API 调用**：
  - Responses API 新增异步调用模式（`background=true`），适用于长耗时任务；
  - 异步任务支持通过事件总线 EventBridge 主动推送完成事件（HTTP 回调或 RocketMQ），替代轮询；
  - 新增临时 API Key 生成机制，适用于不可信环境，规避永久密钥泄露风险；
  - 智能体托管运行时、知识检索/问答、Prompt 工程、数据连接等模块均已提供完整 API 文档（参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **SDK 与集成**：
  - 多模态交互开发套件提供 Android/iOS Lite、Android、iOS、Linux C++、RTOS C 等 SDK；
  - Spring AI Alibaba 框架已支持调用百炼智能体与工作流应用；
  - Codex 终端 AI 编程助手、Kilo CLI 工具均完成百炼接入适配。

## 限制和注意事项

- **模型下线**：2026年7月起分批下线部分老旧及长尾模型（如7月10日、7月9日通知），同时存在延期下线安排（7月6日通知）。具体清单与机制请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **地域与部署**：新模型（如 `qwen-audio-3.0-realtime-plus`、`vidu` 系列）当前仅部署于华北2（北京）地域，国际站用户需确认服务可用性；6月12日新增美国、德国、日本地域，但模型覆盖需单独验证。
- **功能约束**：
  - `qwen3.6-max-preview` 明确不支持图像与视频输入；
  - `kimi/kimi-k2.7-code` 仅支持思考模式；
  - `qwen3.5-omni-plus` 为全模态模型，但具体输入模态组合需查阅对应 API 文档；
  - 免费额度用完即停功能启用后，将返回错误码 `AllocationQuota.FreeTierOnly`，需在客户端做好容错处理。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


