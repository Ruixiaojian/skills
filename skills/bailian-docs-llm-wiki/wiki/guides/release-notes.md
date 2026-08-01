# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力增强、平台功能迭代及关键使用变更。所有信息均基于官方发布文档整理，面向开发者提供可直接落地的参考依据。建议结合具体业务场景选择适配模型，并关注下线通知以规避服务中断风险。

## 支持的模型/功能

百炼平台持续扩展多模态模型矩阵，覆盖文本生成、语音识别与合成、图像与视频生成、3D建模、向量嵌入等核心能力域。新增模型包括：

- **语音识别**：`qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-asr-flash-filetrans`（非实时）等系列，支持汉语七大方言、20+地区口音、古诗词优化及30语种识别；详见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **文本生成与智能体**：`qwen3.7-flash`、`kimi/kimi-k3`（100万token上下文）、`glm-5.2-fast-preview`（TPS提升1.5–2倍）等，强化长程推理、Agent执行与多模态交互能力。
- **图像生成**：`qwen-image-3.0-pro`（支持4.5k token输入、10px小字渲染、12国语言原生字体）、`vidu/viduq3-pro-fast_img2video`（16秒视频生成）等。
- **视频生成**：`pixverse/pixverse-motioncontrol`（动作迁移）、`vidu/viduq3-drama_reference2video`（剧集专用）、`wan2.7-r2v-2026-06-12`（5图/视频混合参考）等。
- **向量与OCR**：`qwen3.7-text-embedding`（支持256–2560维自定义维度）、`qwen3.5-ocr`（卡证关键信息抽取显著提升）。
- **平台级功能**：新增知识检索服务、智能体托管运行时API、Skill能力包、数据连接模块（MySQL/语雀/OSS）、多模态翻译API、模型压缩模块等；详见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

> **注意**：文档1中 `kimi/kimi-k2.7-code` 与 `kimi/kimi-k2.7-code-highspeed` 均标注为“同一模型但输出速度不同”，但文档2未提及该高速版；实际调用时请以控制台或API返回的模型能力描述为准，避免依赖过时别名。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流大模型支持 **100万token**；`qwen3.7-max-2026-06-08` 新增视觉模态后仍维持同等上下文能力。
- **向量维度**：`qwen3.7-text-embedding` 支持用户自定义 **256–2560维**，需在请求参数中显式指定 `dimension` 字段。
- **输入限制**：
  - 图片生成类（如 `vidu/viduq3-fast_reference2image`）支持 **0–14张参考图**；
  - 视频生成类（如 `pixverse/pixverse-v6-r2v`）支持 **2–7张图像输入**；
  - 实时语音对话模型（如 `qwen-audio-3.0-realtime-plus`）要求音频流符合 **16kHz单声道PCM** 格式，且端到端延迟 ≤300ms。
- **性能指标**：`kimi-k2.7-code-highspeed` 在短上下文场景下可达 **260 Token/s**；`qwen3.7-flash` 相比 `qwen3.6-27b` 在Agentic coding任务中推理速度提升显著。

## 使用方式

- **模型调用**：统一通过 DashScope API 接入，推荐使用新版 [智能体应用 DashScope API](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference)（文档2中5月11日首发），支持单轮/多轮、流式、文件问答与视觉理解。
- **部署与调优**：
  - 预置模型（如 `qwen-flash`）可通过 [模型部署 API](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start) 快速部署，支持按模型单元（MU）时长计费；
  - 自定义训练支持 SFT（LoRA/全参）、DPO 偏好训练（千问2.5/3系列）、强化学习（RL，邀约制）及图像/视频/视觉理解模型专项调优（文档2中5月28日、1月22日、1月21日更新）。
- **平台能力集成**：
  - 知识库RAG：使用新增的 [知识检索服务](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval) 实现多知识库联合检索；
  - 数据连接：通过 [数据连接模块](https://help.aliyun.com/zh/model-studio/data-connection) 接入 MySQL/语雀/OSS，驱动动态内容生成；
  - Prompt工程：调用 [Prompt 工程 API](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir-prompt-engineering) 管理模板，提升提示词复用性。

## 限制和注意事项

- **模型下线**：部分老旧模型已启动下线流程，包括 `qwen-turbo` 资源包（6月28日启动退市）、企业知识库（旧）（7月16日下线）、以及多批“老旧长尾模型”（7月9日、7月10日通知）。请查阅 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation) 并及时迁移。
- **地域与合规**：新增美国、德国、日本地域部署（6月12日），但部分模型（如 `fun-music-v1`）仅限中国内地调用；涉及音视频生成的服务需遵守《生成式AI服务管理暂行办法》，禁止生成违法不良信息。
- **计费变更**：记忆库、Managed Agent、GLM-5.2 Fast mode 等已商业化（7月相关通知），免费额度用完即停功能默认启用（7月29日上线），超额调用将触发 `AllocationQuota.FreeTierOnly` 错误码。
- **兼容性风险**：文档1中 `qwen3.7-max` 与 `qwen3.7-max-2026-05-20`、`qwen3.7-max-2026-06-08` 等版本存在能力差异（后者新增视觉模态），但文档2未明确其API兼容策略；建议优先使用带时间戳的完整模型ID（如 `qwen3.7-max-2026-06-08`）以确保行为确定性。
- **SDK支持**：多模态交互开发套件已提供 Linux C++、Android/iOS Lite、RTOS C 及 Java SDK（文档2中2月、4月更新），但 `fun-music-preview` 等预览模型暂不保证所有SDK通道可用。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


