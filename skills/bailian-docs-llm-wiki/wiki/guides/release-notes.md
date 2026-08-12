# release notes

百炼平台的 release notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键能力演进。本文面向开发者，聚焦可操作信息：哪些模型可用/将停用、核心参数与调用方式变化、新功能接入路径，以及必须规避的限制项。所有变更均以实际生效日期为准，建议通过[模型观测](https://bailian.console.aliyun.com/#/model-telemetry)持续监控生产环境依赖。

## 支持的模型/功能

- **新增模型**（2026年7月起）：`qwen3.8-max`（2.4T MoE旗舰）、`kimi/kimi-k3`（2.8T KDA架构）、`wan3.0-video`（全能参考视频生成）、`qwen-audio-3.0-asr-flash-streaming`（实时方言ASR）、`pixverse/pixverse-lipsync`（精准口型同步）等，覆盖文本、视觉、语音、视频、3D全模态。详细清单见[模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能扩展**：2026年6月起支持图像/视频生成模型调优（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)），7月上线知识检索服务与知识问答服务（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)），8月新增模型升级通知机制（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **平台能力升级**：异步调用（`background=true`）、事件总线HTTP回调、Managed Agent托管运行时API、Skill能力包、多知识库联合检索、Spring AI Alibaba集成框架等均已GA。

> **注意**：文档2中 `qwen3.7-max-2026-06-08` 描述为“增加视觉模态理解能力”，但文档3中同日发布的功能动态未提及该能力上线，且文档2未说明是否需启用特定API参数或配置。请以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)中明确标注的功能列表为准，视觉能力需结合`qwen3.7-plus`或`qwen3.8-max`等明确标注“视觉理解”的模型使用。

## 关键参数

- **上下文长度**：`qwen3.8-max`/`kimi-k3`/`glm-5.2` 等旗舰模型支持100万token；`deepseek-v4-flash` 为284B总参/13B激活，兼顾[长上下文](../concepts/long-context.md)与低延迟。
- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时≤200ms；`kimi-k2.7-code-highspeed` 输出速度达260 [Token](../concepts/token.md)/s（短上下文）；`qwen3.5-ocr` 在真实卡证场景抽取效果显著提升。
- **部署单元**：模型部署支持按模型单元（MU）计费，提供可预测的固定成本（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)）；PTU部署新增长输入与前缀缓存能力（2026年6月15日）。

## 使用方式

- **模型调用**：统一通过DashScope API，支持OpenAI兼容（`/v1/chat/completions`）与Anthropic Messages接口分类（2026年5月15日更新）；新版智能体应用API支持单轮/多轮、流式、文件问答、视觉理解（2026年5月11日）。
- **新功能接入**：
  - 异步任务：提交时添加`background=true`，轮询或配置EventBridge HTTP回调接收结果（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)）；
  - 知识库RAG：调用`/v1/rag/retrieve`接口启用排序模型与指令干预模式（2026年2月5日）；
  - 模型导入：国际站支持OSS导入LoRA微调模型（2026年6月5日）；
  - Prompt工程：通过Prompt Engineering API管理模板（2026年4月7日）。
- **安全与鉴权**：支持生成临时API Key用于不可信环境（2026年6月3日）；API Key已升级为加密存储（2026年6月29日）。

## 限制和注意事项

- **模型下线**：快照模型（如`qwen-max-2025-01-25`）下线前30天通知，主线模型提前3个月通知；下线后推理服务立即终止，调优与部署功能同步禁用（已训练/部署模型不受影响）。完整机制详见[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **资源限制**：自下线通知发布日起，待下线模型QPM/TPM将逐步缩减至默认限流值（[文档 1](../../raw/model-user-guide/release-notes/model-depreciation.md)）；部分老旧模型下线存在延期（如2026年7月6日公告），需以最新通知为准。
- **功能弃用**：企业知识库（旧）已于2026年7月16日下线；`qwen-turbo`资源包启动退市（2026年6月28日）；2026年7月10日、9日分别发布“部分老旧模型”与“部分老旧长尾模型”下线通知，涉及模型ID需自查控制台。
- **兼容性**：`qwen3.7-max-preview`（2026-05-17）仅支持思考模式，纯文本能力受限；`fun-music-preview`为预览快照版，不承诺SLA。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


