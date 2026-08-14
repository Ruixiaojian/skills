# release notes

本页汇总百炼平台近期模型上架、功能更新与下线机制等关键变更，面向开发者提供可直接用于集成与迁移的结构化信息。所有模型均已在华北2（北京）地域正式发布，部分新模型同步支持美国、德国、日本等新增地域（详见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。请务必关注模型下线通知，及时完成替代方案验证与切换。

## 支持的模型/功能

- **文本生成与深度思考**：`deepseek-v4-pro-0813`（1.6T总参/49B激活）、`qwen3.8-2.4t-a95b`（2.4T MoE）、`qwen3.8-max`（2.4T Max旗舰）、`kimi/kimi-k3`（2.8T）、`glm-5.2`（1M上下文）、`xiaomi/mimo-v2.5-pro`（1M上下文）；轻量级选项含 `deepseek-v4-flash-0731`（284B总参/13B激活）与 `glm-5.2-fast-preview`（TPS提升1.5–2倍）。
- **视觉理解与多模态**：`qwen3.8-max`、`qwen3.7-max`、`kimi/kimi-k2.7-code`、`MiniMax/MiniMax-M3` 均原生支持图文混合输入与Agent执行；`qwen3.5-ocr` 专精文档解析与卡证信息抽取。
- **图片生成**：`qwen-image-3.0`（4.5k token输入、10px小字渲染）、`qwen-image-3.0-pro`（强化“好用”导向）、`vidu/viduq2-pro_reference2image`（工业级稳定性）、`vidu/viduq3-fast_reference2image`（成本降低约50%）。
- **视频生成**：`pixverse/pixverse-v6-r2v-omni`（图片+视频混合参考）、`wan3.0-video`（All-in-One参考生视频）、`vidu/viduq3-drama_reference2video`（剧集专用）、`happyhorse-1.1-t2v/r2v/i2v`（语义/一致性/质感三重升级）。
- **语音能力**：ASR系列含 `qwen-audio-3.0-asr-flash-streaming`（实时）、`fun-asr-flash-2026-06-15`（30语种+古诗词优化）；TTS系列含 `qwen-audio-3.0-tts-plus`（高表现力）与 `qwen-audio-3.0-tts-flash`（首包<200ms）；实时对话含 `qwen-audio-3.0-realtime-plus`（高质量）与 `qwen-audio-3.0-realtime-flash`（极速版）。
- **其他模态**：`Tripo/Tripo-P1.0`（2秒生成引擎可用3D网格）、`Tripo/Tripo-H3.1`（十亿体素级精度）、`fun-music-v1`（歌曲生成）。

> **注意**：文档1中 `qwen3.7-flash-2026-07-15` 与 `qwen3.7-flash` 并列列出，但未说明二者差异；结合文档2中“7月10日部分老旧模型下线通知”及文档3的快照模型30天下线规则，建议优先使用无日期后缀的主线版本（如 `qwen3.7-flash`），避免依赖快照版本。该矛盾已在[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)中明确规范。

## 关键参数

- **上下文长度**：主流旗舰模型（`qwen3.8-max`、`deepseek-v4-pro-0813`、`kimi-k3`、`glm-5.2`）均支持 **100万[Token](../concepts/token.md)**；`qwen3.7-flash` 等Flash系列亦原生支持百万级。
- **向量维度**：`qwen3.7-text-embedding` 支持 **256–2560维** 用户自定义。
- **视频时长**：`wan3.0-video` 最长30秒；`vidu/viduq3-pro-fast_img2video` 支持16秒；`pixverse/pixverse-v6-r2v` 支持15秒。
- **ASR方言覆盖**：`qwen-audio-3.0-asr-flash-*` 与 `fun-asr-flash-2026-06-15` 均支持汉语七大方言及20+地区口音，但后者明确列出30个语种，前者仅提“中、英、日、韩等共30个语种”，细节需以[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)中API文档为准。
- **TTS延迟**：`qwen-audio-3.0-tts-flash` 首包延时 **≤200ms**；`qwen-audio-3.0-tts-plus` 未标注延迟，强调音质与表现力。

## 使用方式

- **模型调用**：通过 DashScope API 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（如 `/v1/chat/completions`）调用，需指定 `model` 参数（如 `"model": "qwen3.8-max"`）。流式响应支持 `stream=true`。
- **多模态输入**：视觉理解类模型（如 `qwen3.8-max`）接受 base64 编码图片或 OSS URL；视频生成类（如 `pixverse/pixverse-v6-r2v-omni`）支持图片+视频混合参考输入。
- **[异步任务](../concepts/async-task.md)**：长耗时操作（如视频生成、大文件处理）推荐使用 Responses API 的异步模式（`background=true`），并通过轮询或事件总线（EventBridge HTTP/RocketMQ）接收结果。
- **模型部署与调优**：支持 PTU 部署（含前缀缓存）、SFT/DPO 训练（千问/智谱系列）、LoRA 微调（国际站支持 OSS 导入）；视频/图像生成模型亦开放调优（见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **知识库与RAG**：知识检索与问答服务已上线，支持多知识库联合检索与混合排序；企业知识库（旧）已于7月16日下线，需迁移至新版。

## 限制和注意事项

- **模型下线风险**：快照模型（含日期后缀）将在下线前30天通知，主线模型提前3个月通知。自通知发布日起即开始限流（QPM/TPM逐步缩减），正式下线后推理、新调优/部署全部停止。请定期检查[模型观测](https://bailian.console.aliyun.com/#/model-telemetry)并测试替代模型。
- **地域限制**：新增美国、德国、日本地域于6月12日上线，但并非所有模型均同步支持；具体地域可用性需在控制台模型详情页确认。
- **资源包退市**：`qwen-turbo` 资源包已于6月28日启动退市；部分老旧模型（如7月10日通知）已进入下线流程，不可用于新应用创建。
- **API兼容性**：文本生成API已聚合OpenAI Responses与Anthropic Messages两类入口（5月15日更新），调用前请确认所用SDK版本兼容性。
- **安全合规**：模型调优新增0代码安全合规强化流程（5月4日上线），适用于对输出内容有强管控要求的场景。

## 来源文档

- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)


