# release notes

百炼平台的 release notes 汇总了模型生命周期管理（上架、下线）、平台功能演进及关键能力更新。本文面向开发者，聚焦可操作信息：当前支持的模型与能力边界、核心参数含义、调用方式变更、以及必须规避的限制项。所有模型下线决策均遵循统一通知机制，新模型上线与功能迭代均同步开放 API 和控制台支持。

## 支持的模型/功能

- **新增模型**：2026年7月起，平台陆续上线 `qwen3.8-max`（2.4T MoE旗舰）、`qwen-image-3.0`/`qwen-image-3.0-pro`（4.5k token输入、10px小字渲染）、`qwen-audio-3.0-asr-flash-*`（30语种+方言+古诗词优化）、`kimi/kimi-k3`（2.8T参数、100万上下文）等；视频生成领域新增 `wan3.0-video`、`pixverse/pixverse-motioncontrol`、`vidu/viduq3-drama_reference2video` 等专用模型。详情见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型类型扩展**：自2026年5月起，模型调优全面支持图像生成（Wan/Wanx）、视频生成（万相系列）、视觉理解（VL）三类模型；2026年2月起支持声音复刻 API 调用；2026年4月起支持[多模态](../concepts/multimodal.md)翻译 API（文本/图片/文档/网页）。  
- **平台能力升级**：2026年6月上线知识检索服务与知识问答服务；2026年7月发布 Responses API 异步调用模式（`background=true`）；2026年6月起支持模型导入国际站（OSS LoRA）、API Key 临时令牌生成、智能体托管运行时 API；2026年3月起记忆库支持[长期记忆](../concepts/long-term-memory.md)与跨应用共享。

## 关键参数

- **模型标识**：主线模型（如 `qwen3.7-plus`）代表稳定主干版本；快照模型（如 `qwen3-max-2026-01-23`）含日期后缀，用于精确版本控制与灰度验证。
- **上下文长度**：`qwen3.7-flash`、`glm-5.2`、`deepseek-v4-pro` 等主流模型均原生支持 1M token 上下文；`qwen-audio-3.0-asr-flash-streaming` 支持实时流式长音频转写。
- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`kimi/kimi-k2.7-code-highspeed` 输出速度达 260 [Token](../concepts/token.md)/s（短上下文）；`qwen3.7-plus` 具备[多模态](../concepts/multimodal.md)交互混合智能体能力，支持 GUI 操作与视觉参考代码生成。
- **计费单元**：模型部署支持按模型单元（MU）时长计费；[Token](../concepts/token.md) Plan 团队版支持跨坐席共享 Credits 弹性用量包；Coding Plan Pro 套餐首月特惠 ¥39.90。

## 使用方式

- **模型调用**：所有新模型均通过标准 DashScope API 接入，支持 OpenAI Responses / Anthropic Messages 协议；异步任务可通过事件总线 HTTP 回调或 RocketMQ 主动推送完成事件，避免轮询。
- **模型调优**：图像/视频/VL 模型调优需在控制台选择对应类型；DPO 偏好训练适用于千问2.5/3全系列（32B/14B/8B等）；强化学习（RL）训练当前为邀约制。
- **知识库与RAG**：知识检索服务支持多知识库联合检索与混合排序；Retrieve 接口支持排序模型选项与指令干预模式；知识库日志全量投递至 SLS，可用于审计与告警。
- **部署与集成**：预置吞吐部署（PTU）支持长输入与前缀缓存；Spring AI Alibaba 框架已提供百炼智能体调用文档；[多模态](../concepts/multimodal.md)交互开发套件覆盖 Android/iOS/Linux/C++/RTOS SDK。

## 限制和注意事项

- **模型下线时效**：快照模型下线前30天通知，主线模型下线前3个月通知；通知仅触达近3个月有调用记录的用户。自通知发布日起逐步缩减 QPM/TPM，正式下线后推理服务立即终止，调优与部署功能同步关闭（已训练/部署模型不受影响）。详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- > **注意**：文档1中列出 `qwen3.7-plus` 同时作为多个模型（如 `aitryon`、`qwen-math-plus`）的替代模型，但文档2明确 `qwen3.7-plus` 于2026年6月1日上线，而文档1中部分下线模型（如 `qwen-plus-2025-12-01-us`）的下线时间为2026年10月10日——这意味着 `qwen3.7-plus` 在其上线后即承担替代职责，但实际兼容性需以[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)中“替代模型”列为准，不可直接假设所有同名模型完全等效。
- > **注意**：文档3中“7月10日”与“7月9日”分别发布“部分老旧模型下线通知”和“部分老旧长尾模型下线通知”，但两则公告链接均为 `https://www.aliyun.com/notice/118434` 和 `https://www.aliyun.com/notice/118427`，与文档1中引用的同一公告编号冲突。开发者应以文档1所列具体模型清单为准，避免依赖公告标题的字面含义。
- **功能弃用**：企业知识库（旧）已于2026年7月16日下线；`qwen-turbo` 资源包于2026年6月28日启动退市；`gte-rerank` 模型已于2026年5月30日下线，替代模型为 `qwen3-rerank`；`qwen-m` 模型已于2025年5月8日下线，无替代模型。
- **地域与接入**：2026年6月12日起新增美国、德国、日本地域部署；API 域名已升级为业务空间专属推理域名；网关变更已于2026年7月13日生效，需检查客户端配置。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


