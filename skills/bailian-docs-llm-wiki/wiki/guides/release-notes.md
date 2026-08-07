# release notes

本页面汇总百炼平台近期模型上架、功能更新与下线机制等关键变更，面向开发者提供可操作的版本演进概览。所有信息均来自官方发布文档，重点关注模型能力边界、调用方式变化及生命周期管理策略，不包含营销性描述。

## 支持的模型/功能

- **新上架模型**：涵盖多模态生成与理解全栈能力。视频生成类新增 `wan3.0-video`（All-in-One 参考视频生成，最长30秒）、`vidu/viduq3-pro-fast_img2video`（16秒时长扩展）及 `pixverse/pixverse-lipsync`（精准对口型）；图片生成类包括 `qwen-image-3.0`（4.5k token输入、10px小字渲染）与 `qwen-image-3.0-pro`（强调“好用”生产力属性）；文本与视觉理解旗舰模型 `qwen3.8-max`（2.4万亿参数MoE架构）和 `kimi/kimi-k3`（2.8万亿参数、100万token上下文）已上线；语音方向新增 `qwen-audio-3.0-asr-flash-streaming`（实时方言识别）、`qwen-audio-3.0-tts-plus`（高音质表现力）与 `qwen-audio-3.0-realtime-plus`（低延迟双工对话）。完整列表详见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **平台功能更新**：2026年7月起，新增智能体托管运行时 API（[了解详情](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview)）、知识检索与问答服务（支持多知识库联合检索）、Responses API 异步调用模式（`background=true`）、模型导入国际站支持（OSS LoRA 导入）及 Spring AI Alibaba 集成文档。6月起支持 PTU 长输入与前缀缓存、新增地域（美/德/日）部署范围、Coding Plan 联网搜索 MCP 升级为 Streamable HTTP 协议。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **下线模型机制**：快照模型（含日期标识）提前30天下线通知，主线模型提前3个月通知。自通知发布日起逐步限流（QPM/TPM缩减），正式下线后停止推理服务，且不再支持新调优与部署（已部署模型不受影响）。下线清单覆盖图像生成（如 `aitryon` 系列）、视频生成（如 `wan2.7-r2v`）、语音合成（如 `qwen-tts`）及大量历史快照模型（如 `qwen3-max-2026-01-23`）。具体规则与列表见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

> **注意**：文档1中 `qwen-image-3.0` 与 `qwen-image-3.0-pro` 的功能描述高度重合（均提及4.5k token输入、10px小字渲染等），但未明确二者定位差异；文档3将 `qwen-image-2.0` 列为 `aitryon` 等下线模型的替代项，而文档1未提及其与 `qwen-image-3.0` 系列的关系。开发者需以控制台实际可用模型为准，并通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 验证业务效果。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`xiaomi/mimo-v2.5-pro` 等支持 100 万 token；`qwen3.8-max` 采用 MoE 架构，参数规模达 2.4 万亿；`qwen3.7-text-embedding` 支持 256~2560 维用户自定义向量维度。
- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`qwen-audio-3.0-realtime-flash` 实现“极致响应速度”；`glm-5.2-fast-preview` 输出 TPS 较标准版提升 1.5~2 倍；`kimi/kimi-k2.7-code-highspeed` 编程场景输出速度约 180 [Token](../concepts/token.md)/s（中位数输入）。
- **多模态能力**：`qwen3.8-max`、`qwen3.7-plus`、`kimi/kimi-k3` 均原生支持视觉理解；`qwen3.5-ocr` 在业务卡证关键信息提取上效果显著提升；`pixverse/pixverse-motioncontrol` 支持从参考视频提取动作并迁移至目标人物图片。

## 使用方式

- **模型调用**：通过 DashScope API 调用，支持 OpenAI Responses / Anthropic Messages 兼容接口（[API 入口聚合说明](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)）；[异步任务](../concepts/asynchronous-task.md)可通过 `background=true` 提交并轮询结果，或配置事件总线 HTTP 回调/RocketMQ 主动推送。
- **[模型部署](../concepts/model-deployment.md)与调优**：支持预置模型 API 部署（如 `qwen-flash`/`qwen-plus`），计费模式含按模型单元（MU）时长；模型调优覆盖文本、视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（万相系列）四类，支持 SFT（全参/LoRA）、DPO 偏好训练及强化学习（RL，邀约制）。
- **配套能力集成**：知识库 RAG 支持多知识库联合检索与混合排序；数据连接模块接入 MySQL/语雀/OSS；Skill 能力包支持添加官方或自定义技能；通义多模态翻译 API 覆盖文本/图片/文档/网页翻译。

## 限制和注意事项

- **模型生命周期**：所有下线模型（如 `qwen-turbo`、`qwen-vl-max`、`qwen-audio-asr` 等）自正式下线日起不可用于新推理请求，且无法发起新调优/部署任务。已部署模型可继续运行，但建议尽快迁移至替代模型（如 `qwen3.7-plus` 或 `qwen3.6-flash`）。
- **地域与权限**：新增美国、德国、日本地域部署，但部分功能（如 Managed Agent 商业化、记忆库 Memory 2.0）可能受限于账号类型或地域；API Key 加密存储与业务空间专属推理域名已升级，需检查客户端配置兼容性。
- **兼容性风险**：`qwen3.7-plus` 在文档1中被列为多个下线模型（如 `qwen-vl-ocr`、`qwen3-vl-flash`）的替代项，但其自身在文档3中亦被标记为“2026年10月10日将下线”，存在版本迭代冲突。开发者应避免依赖即将下线的替代模型，优先选用 `qwen3.8-max` 或 `qwen3.7-max` 等最新主线模型。
- **资源约束**：免费额度用完即停功能已启用；部分老旧模型（如 `qwen-turbo` 资源包）已启动退市流程；企业知识库（旧）已于2026年7月16日下线，需迁移至新版知识库服务。

## 来源文档

- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)


