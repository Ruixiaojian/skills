# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键能力变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型观测」和「通知中心」主动跟踪影响范围。模型与功能的可用性、计费策略及 API 行为可能随版本动态调整，需以最新文档和接口响应为准。

## 支持的模型/功能

- **新增模型**：2026年7–8月集中上线多模态旗舰模型，包括 `qwen3.8-max`（2.4T MoE 视觉语言模型）、`deepseek-v4-pro-0813`（1.6T MoE，百万上下文）、`kimi/kimi-k3`（2.8T 参数）、`pixverse/pixverse-v6-r2v-omni`（混合参考视频生成）等；语音方向新增 `qwen-audio-3.0-realtime-flash`（端到端延时 <200ms）与 `qwen-audio-3.0-tts-plus`（高表现力合成）；向量模型新增 `qwen3.7-text-embedding`（支持256–2560维自定义）。完整列表详见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
  
- **平台功能**：2026年6月起全面支持异步调用（`background=true`）、事件总线 HTTP/RocketMQ 回调；新增 Skill 能力包、数据连接模块（MySQL/语雀/OSS）、知识检索与问答服务；模型部署支持 PTU 长输入与前缀缓存；模型调优扩展至图像生成、视频生成、视觉理解（VL）模型类型；RAG 场景新增多知识库联合检索与混合排序。

- **SDK 与接入**：多模态交互开发套件已覆盖 Android/iOS Lite、Android、Linux C++、RTOS C 及服务端 Java SDK；新增 Codex 终端接入、Kilo CLI 工具；Spring AI Alibaba 集成文档正式发布。

> **注意**：文档 2 中 `qwen3.7-flash-2026-07-15` 与文档 3 中 `qwen3.7-flash`（6月17日条目）存在命名冗余，实际为同一模型快照，建议以控制台显示的 `qwen3.7-flash` 为准，避免硬编码带日期后缀的 ID。

## 关键参数

- **上下文长度**：主流新模型普遍支持 1M token（如 `qwen3.8-max`、`glm-5.2`、`kimi-k3`），部分轻量模型（如 `deepseek-v4-flash-0731`）同样原生支持百万级上下文。
- **推理模式**：`-flash` 后缀模型（如 `qwen3.7-flash`）侧重低延迟与高 TPS；`-plus`/`-max` 后缀强调综合能力与多模态深度；`-realtime-flash` 与 `-realtime-plus` 分别优化首包延时与回复质量。
- **部署单位**：模型部署支持按「模型单元（MU）」计费，性能可调、成本可预测；PTU 部署新增长输入与缓存能力，提升长文本场景吞吐。
- **调优能力**：SFT 支持全参与 LoRA；DPO 偏好训练已覆盖千问2.5/3全系列；强化学习（RL）训练当前为邀约制开放。

## 使用方式

- **模型调用**：通过标准 DashScope API（兼容 OpenAI Anthropic Messages 接口分类）或 Responses API（支持同步/异步模式）调用；[异步任务](../concepts/asynchronous-task.md)结果可通过轮询或 EventBridge 回调获取。
- **模型切换**：使用待下线模型的用户应通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 确认调用记录，并在测试替代模型效果后切换；快照模型（如 `qwen-max-2025-01-25`）需提前30天迁移，主线模型需提前3个月。
- **功能启用**：新功能（如 Skill、数据连接、记忆库 Memory 2.0）在控制台对应模块中直接配置；API Key 加密存储与专属域名已默认启用，无需额外操作。
- **本地集成**：推荐使用官方 SDK（如 Spring AI Alibaba、Codex CLI）或标准 HTTP 客户端，避免自行拼接鉴权头；临时 API Key 适用于不可信环境，见 [生成临时 API Key 文档](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 限制和注意事项

- **模型下线影响**：自下线通知发布日起，QPM/TPM 将逐步缩减；正式下线后，推理服务立即终止，且**不再支持基于该模型的新调优与新部署**（已部署实例不受影响）。详情请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
  
- **地域与服务范围**：2026年6月起新增美国、德国、日本地域部署，但部分模型（如 `qwen-audio-3.0-realtime-*`）当前仅限华北2（北京）可用，调用前需确认地域白名单。

- **兼容性风险**：`qwen-turbo` 资源包已于2026年6月28日启动退市；企业知识库（旧）于7月16日下线，需迁移至新版知识库；API 入口聚合后，旧版单一文本生成接口路径可能失效，建议统一迁移到 `/v1/services/aigc/text-generation` 下的 OpenAI 或 Anthropic 兼容入口。

- **计费变更**：GLM-5.2 Fast mode 于7月14日降价；通义千问VL系列、千问全系列模型已多次调价；[Token](../concepts/token.md) Plan 团队版自2026年6月30日起支持跨坐席共享 Credits 弹性用量包。价格变动均以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)中公告链接为准。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


