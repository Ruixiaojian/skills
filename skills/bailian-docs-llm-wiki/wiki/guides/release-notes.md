# release notes

本页汇总百炼平台近期模型与功能更新的核心信息，面向开发者提供可直接用于集成与调用的关键变更。内容聚焦于新增/下线模型、平台能力升级、关键参数调整及使用约束，所有信息均源自官方发布文档，不包含营销性描述或主观评价。

## 支持的模型/功能

- **新增模型**：截至2026年8月，平台新增多类旗舰模型，包括：
  - 文本与多模态：`qwen3.8-max`（2.4万亿参数MoE架构）、`kimi/kimi-k3`（2.8万亿参数，100万token上下文）、`glm-5.2-fast-preview`（1M上下文，TPS提升1.5–2倍）；
  - 语音识别：`qwen-audio-3.0-asr-flash-streaming`等3个ASR子型号，支持30语种、方言及古诗词优化；
  - 图像生成：`qwen-image-3.0-pro`（支持4.5k token输入、10px小字渲染、12国语言原生字体）；
  - 视频生成：`vidu/viduq3-pro-fast_img2video`（16秒时长）、`pixverse/pixverse-motioncontrol`（动作迁移）、`wan2.7-t2v-2026-06-12`（文生视频快照）；
  - 向量与合成：`qwen3.7-text-embedding`（支持256–2560维自定义维度）、`qwen-audio-3.0-tts-plus`（高表现力）与`qwen-audio-3.0-tts-flash`（首包延时<200ms）。
- **平台功能扩展**：新增知识检索服务与知识问答服务（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）、智能体托管运行时API（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）、模型导入API（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）、多模态翻译API目录（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）等关键能力。

> **注意**：文档1中多次出现`kimi-k2.7-code`与`kimi/kimi-k2.7-code`两种ID写法，且`kimi/kimi-k3`在文档1中标注为“全球首个开源的3万亿级别模型”，但该表述与公开技术事实不符（Kimi K3未开源），请以[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)中实际可用模型ID为准，避免依赖非官方口径。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro`、`xiaomi/mimo-v2.5-pro`等主流大模型均支持100万token上下文；`qwen3.5-livetranslate-flash-realtime`支持60种语言输入、29种语言输出。
- **性能指标**：
  - `qwen-audio-3.0-tts-flash`首包延时≤200ms；
  - `kimi/kimi-k2.7-code-highspeed`输出速度约180–260 [Token](../concepts/token.md)/s；
  - `qwen3.7-text-embedding`向量维度支持256–2560可调；
  - `qwen-image-3.0-pro`支持最大4.5k token输入与10px级文字渲染精度。
- **多模态能力**：`qwen3.8-max`、`qwen3.7-plus`、`stepfun/step-3.7-flash`等明确标注支持视觉理解与Agent混合交互；`pixverse/pixverse-lipsync`支持音频/TTS与嘴部动作精准同步。

## 使用方式

- **模型调用**：所有新模型通过标准DashScope API接入，文本生成类支持OpenAI Responses与Anthropic Messages兼容接口（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）；实时语音类（如`qwen-audio-3.0-realtime-flash`）需启用流式响应与双工协议。
- **平台能力集成**：
  - 知识库RAG场景应优先使用新增的`知识检索服务`与`知识问答服务`（支持多知识库联合检索与混合排序）；
  - 智能体开发推荐使用`智能体托管运行时API`（平台托管会话与工具执行）；
  - 自定义模型部署需通过`模型导入API`上传LoRA微调模型（国际站已支持OSS导入）；
  - 异步任务建议采用事件总线HTTP回调或RocketMQ推送，避免轮询（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 限制和注意事项

- **模型下线**：2026年7月起分批下线老旧模型，包括`部分老旧模型`（7月10日）、`部分老旧长尾模型`（7月9日），具体清单需参考[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)；`qwen-turbo`资源包已于6月28日启动退市。
- **地域与部署**：新增美国、德国、日本地域部署（6月12日），但部分模型（如`qwen3.8-max`）当前仅限华北2（北京）可用，跨地域调用需确认模型部署状态。
- **计费与额度**：`记忆库`、`Managed Agent`、`GLM-5.2 Fast mode`等已商业化（7月通知）；新人免费额度启用“用完即停”策略（返回`AllocationQuota.FreeTierOnly`错误码），避免意外扣费。
- **兼容性风险**：`qwen3.7-max`系列存在多个快照版本（如`qwen3.7-max-2026-05-20`、`qwen3.7-max-2026-06-08`），其中后者新增视觉模态能力，而`qwen3.7-max-2026-05-17`（预览版）仅支持思考模式——生产环境应严格按版本后缀区分能力边界。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


