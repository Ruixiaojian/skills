# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架/下线）、平台功能迭代及关键能力变更。本文面向开发者，聚焦可操作信息：当前支持的核心模型与替代关系、关键参数约束、调用方式更新、以及必须规避的限制项。所有模型状态与功能时效性均以官方公告为准，建议通过 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 和 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 实时校验。

## 支持的模型/功能

- **新增主力模型（2026年7月起）**：`qwen3.8-max`（2.4T MoE，原生VL）、`qwen3.7-flash`（[多模态](../concepts/multimodal.md)Agent强化）、`qwen-image-3.0`（4.5k token输入，10px小字渲染）、`qwen-audio-3.0-asr-flash-streaming`（支持30语种+方言+古诗词优化）、`kimi/kimi-k3`（2.8T，1M上下文）、`glm-5.2-fast-preview`（TPS提升1.5–2倍）。详见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **主流替代路径**：千问Max系列已全面迁移至 `qwen3.7-max` 及 `qwen3.8-max`；千问VL系列主推 `qwen3-vl-plus` 和 `qwen3.6-flash`；语音合成统一升级至 `cosyvoice-v3.5-plus` 或 `qwen-audio-3.0-tts-plus/flash`；图像生成推荐 `qwen-image-3.0` 或 `wan3.0-video`。
- **功能模块扩展**：2026年6月起支持知识库RAG联合检索与问答服务、智能体托管运行时API、Skill能力包、数据连接（MySQL/OSS/语雀）、[多模态](../concepts/multimodal.md)翻译API、模型压缩（量化部署）、强化学习训练（RL，邀约制）；2026年7月上线记忆库商业化、Managed Agent商业化及企业知识库（旧）下线。

> **注意**：文档2中 `qwen3.6-`（末尾截断）为明显录入错误，实际应为 `qwen3.6-plus` 或 `qwen3.6-max`，请以控制台模型列表或 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中完整ID为准。

## 关键参数

- **上下文长度**：`qwen3.7-max`/`qwen3.8-max`/`kimi-k3`/`glm-5.2` 等旗舰模型支持 **1M token**；`qwen3.7-flash`/`qwen-audio-3.0-asr-flash` 等Flash系列侧重低延迟，上下文通常为128K–512K。
- **限流策略**：主线模型下线前3个月、快照模型下线前30天启动QPM/TPM逐步缩减；具体默认限流值见 [默认限流](https://help.aliyun.com/zh/model-studio/rate-limit)，扩容申请用户将先恢复至该基准再缩减。
- **地域与部署**：新增美国、德国、日本地域（2026年6月12日）；模型部署支持按模型单元（MU）时长计费（2026年1月23日），PTU部署支持长输入与前缀缓存（2026年6月15日）。

## 使用方式

- **API调用**：文本生成API已聚合OpenAI Responses与Anthropic Messages接口（2026年5月15日）；Responses API支持异步调用（`background=true`，2026年6月1日）；异步任务可通过事件总线HTTP回调或RocketMQ推送完成事件（2026年4月23日）。
- **SDK与客户端**：[多模态](../concepts/multimodal.md)交互开发套件提供Linux C++、Android/iOS Lite、RTOS C SDK（2026年2–4月）；新增Codex终端AI编程助手接入（2026年6月24日）；Spring AI Alibaba调用百炼应用文档已上线（2026年6月1日）。
- **模型调优与部署**：支持视觉理解（VL）、视频生成（Wan/Wanx）、图像生成模型的定制训练（2026年1–5月）；DPO偏好训练覆盖千问2.5/3全量尺寸（2025年9月）；模型导入功能国际站上线，支持OSS导入LoRA（2026年6月5日）。

## 限制和注意事项

- **模型下线影响**：自正式下线日起，模型推理服务立即终止；新调优与部署操作不可用（已训练/部署模型不受影响）；控制台功能与文档同步下线。快照模型（如 `qwen-max-2025-01-25`）与主线模型（如 `qwen3-max`）下线通知周期不同，需分别关注 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **兼容性风险**：`qwen-turbo` 资源包已启动退市（2026年6月28日），且 `qwen-turbo` 系列模型本身将于2026年10月10日下线，务必切换至 `qwen3.7/3.8` 系列。
- **功能弃用**：企业知识库（旧）已于2026年7月16日下线；`gte-rerank` 模型已于2026年5月30日下线，替代模型为 `qwen3-rerank`；`qwen-audio-asr` 等千问Audio旧版模型于2026年3月30日下线，需迁移到 `qwen3-asr-flash` 系列。
- **地域限制**：部分新模型（如 `wan3.0-video`）仅上架北京、新加坡地域；`qwen-audio-3.0-tts-plus/flash` 等音频模型暂未在全部地域开放，调用前需确认目标Region支持情况。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


