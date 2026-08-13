# release notes

百炼平台的 release notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键参数变更等核心信息，旨在帮助开发者及时掌握服务可用性、能力边界与接入方式。所有变更均以实际生效日期为准，建议通过控制台或 API 主动查询最新状态，避免依赖静态文档。

## 支持的模型/功能

- **新模型上架**：覆盖文本生成、视觉理解、视频生成、语音识别/合成、实时对话、3D 生成、[多模态](../concepts/multimodal.md)翻译等全模态类型。例如 `qwen3.8-max`（2.4T MoE，100万上下文）、`pixverse/pixverse-v6-r2v-omni`（混合参考视频生成）、`kimi/kimi-k3`（2.8T 参数，KDA 注意力架构）等，详见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **平台功能新增**：包括智能体托管运行时（`Managed Agent`）、知识检索与问答服务（RAG）、[多模态](../concepts/multimodal.md)交互开发套件（Android/iOS/Linux C++/RTOS SDK）、Prompt 工程 API、异步调用（`background=true`）、事件总线回调（EventBridge）、数据连接（MySQL/OSS/语雀）、Skill 能力包等。
- **模型调优扩展**：自 2025 年起逐步支持视频生成（万相系列）、图像生成（Wan/Wanx）、视觉理解（VL）模型的 SFT/DPO/RL 训练；2026 年新增 0 代码安全合规强化流程。

> **注意**：文档 2 中列出的 `qwen3.7-max-2026-06-08` 与 `qwen3.7-max-2026-05-20` 均标注为“Max 模型”，但前者明确声明“增加了视觉模态理解能力”，后者仅称“开放纯文本模型能力”。二者能力存在实质性差异，应以具体快照 ID 和控制台实际能力描述为准，不可混用。

## 关键参数

- **上下文长度**：主流旗舰模型（如 `qwen3.8-max`、`glm-5.2`、`kimi-k3`）普遍支持 100 万 token；轻量模型（如 `deepseek-v4-flash-0731`）同样原生支持百万上下文。
- **限流策略**：模型下线前会按类型缩减 QPM/TPM —— 快照模型提前 30 天、主线模型提前 3 个月启动限流，详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **部署计费单元**：支持按模型单元（MU）时长计费（[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)），适用于预置模型（如 `qwen-flash`）和自定义部署场景，提供可预测成本。

## 使用方式

- **模型调用**：统一通过 DashScope API 接入，支持 OpenAI-compatible（`/v1/chat/completions`）与 Anthropic Messages 协议；新版智能体应用 API 已支持单轮/多轮、流式、文件问答、视觉理解等完整能力。
- **功能启用**：新功能（如记忆库 Memory 2.0、知识库日志投递至 SLS、异步任务事件总线回调）无需额外开通，直接在控制台对应模块或 API 中使用；部分能力（如 RL 训练、Managed Agent 商业化）需关注对应公告是否已正式商用。
- **迁移适配**：当模型下线时，需主动切换至替代模型。建议通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 页面确认当前调用模型状态，并在测试环境验证业务效果后灰度切换。

## 限制和注意事项

- **模型下线影响**：自正式下线日起，模型推理服务终止，已创建的应用将无法返回结果；模型调优与部署功能同步关闭（已训练/部署模型不受影响）。控制台功能与官方文档亦同步下线。
- **快照模型时效性**：带日期标识的快照模型（如 `wan2.7-t2v-2026-06-12`）仅保证该版本稳定性，不享受主线模型的长期维护周期，下线通知期为 30 天。
- **地域与部署范围**：2026 年 6 月起新增美国、德国、日本地域支持，但并非所有模型均全球可用，需在控制台地域列表中确认目标模型的部署状态。
- **API 兼容性**：`Responses API` 新增异步模式（`background=true`）后，同步接口行为不变；但旧版异步轮询逻辑需升级为事件总线回调以降低延迟。

> **注意**：文档 3 中 2026 年 7 月 10 日与 7 月 9 日分别发布“部分老旧模型下线通知”和“部分老旧长尾模型下线通知”，但文档 1 的下线清单中未体现这两项通知的具体模型名称与时间。开发者应以官网公告链接（如 `https://www.aliyun.com/notice/118434`）为准，不可仅依赖文档 1 的静态列表。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


