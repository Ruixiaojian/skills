# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及基础设施层面的重要更新，涵盖新增能力、计费调整、上下架模型、技术升级与限制变更。所有变更均面向开发者设计，需结合实际调用场景评估兼容性与迁移成本。最新动态持续同步至平台控制台与文档中心，建议定期查阅 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 获取完整时间线。

## 支持的模型/功能

- **新增模型**：2026年6月起密集上线多模态与垂直领域模型，包括 `qwen3.8-max`（2.4万亿参数MoE旗舰）、`qwen-image-3.0`（支持4.5k token输入与10px小字渲染）、`qwen-audio-3.0-asr-flash-streaming`（方言+古诗词优化ASR）、`pixverse/pixverse-motioncontrol`（动作迁移视频生成）等。完整列表见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **核心功能演进**：
  - 智能体托管：6月29日上线 `Managed Agent` 运行时 API，支持会话状态与工具执行全托管；
  - RAG增强：6月23日上线知识检索与问答服务，支持多知识库联合检索与混合排序；
  - 模型调优：5月31日开放强化学习（RL）训练（邀约制），1月起支持VL、视频生成模型SFT/DPO训练；
  - 多模态SDK：4月起陆续发布Android/iOS Lite、Linux C++、RTOS C SDK，覆盖嵌入式与移动端接入。

> **注意**：文档1中“企业知识库（旧）下线通知”（7月16日）与当前知识库RAG服务（6月23日上线）存在明确替代关系，旧版知识库已不可用，新RAG服务需通过 `/knowledge_retrieval` 和 `/knowledge_qa` 接口调用。

## 关键参数

- **模型单元（MU）计费**：自1月23日起，模型部署API支持按MU时长计费，适用于 `qwen-flash`/`qwen-plus` 等预置模型，需在请求中指定 `model_unit` 参数；
- **[异步任务](../concepts/asynchronous-task.md)控制**：Responses API 新增 `background=true` 参数（6月1日），用于提交长耗时任务；异步事件推送支持 EventBridge HTTP回调或RocketMQ（4月23日）；
- **上下文长度**：`glm-5.2`、`qwen3.5-livetranslate-flash-realtime` 等模型支持1M token超长上下文，调用时需确保 `max_tokens` 与 `input` 总长度不超过该阈值；
- **向量维度**：`qwen3.7-text-embedding` 支持256~2560维自定义输出，通过 `output_dimension` 参数指定。

## 使用方式

- **API调用**：
  - 文本生成统一入口支持 OpenAI Responses 与 Anthropic Messages 兼容模式（5月15日）；
  - 新版智能体应用 DashScope API（5月11日）提供单轮/多轮、流式、文件问答、视觉理解能力；
  - 模型导入API（6月3日）支持从OSS导入LoRA微调模型，需调用 `/models/import` 创建任务。
- **SDK集成**：
  - Spring AI Alibaba 框架调用文档已上线（6月1日），适配百炼智能体与工作流；
  - 多模态交互开发套件提供 Java（4月28日）、Android（4月14日）、Linux C++（2月28日）等SDK，需按平台要求配置 `app_id` 与 `access_token`。
- **临时凭证**：6月3日新增生成临时API Key文档，适用于不可信环境，通过 `/tokens/temporary` 接口获取，有效期可设（最长24小时）。

## 限制和注意事项

- **模型下线**：7月10日及9日分两批下线部分老旧模型，6月28日启动 `qwen-turbo` 资源包退市；具体清单与过渡期详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-release-notes.md)；
- **地域限制**：6月12日新增美国、德国、日本地域部署，但部分模型（如 `qwen-image-3.0`）仅限华北2（北京）可用，调用前需确认 `region_id`；
- **免费额度**：12月22日上线用量看板，但7月29日启用“免费额度用完即停”策略，超出后API将直接返回 `403 Forbidden`，需主动购买资源包或开通付费账号；
- **兼容性风险**：`qwen3.7-max-2026-05-20` 与 `qwen3.7-max-2026-06-08` 均为快照版本，后者新增视觉模态能力，若代码硬编码模型ID且未处理模态字段变更，可能导致解析失败。

> **注意**：文档1中“记忆库商业化通知”（7月21日）与“记忆库 Memory 2.0 上线”（3月20日）存在功能延续性，但商业化后需单独购买配额，免费版记忆库已停用，历史数据迁移需手动触发。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


