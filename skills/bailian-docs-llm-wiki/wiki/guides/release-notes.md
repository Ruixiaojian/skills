# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力增强、平台功能迭代及关键使用变更。所有信息均基于官方发布内容整理，面向开发者提供可直接落地的参考依据。建议结合具体业务场景选择适配模型，并关注下线通知以规避服务中断风险。

## 支持的模型/功能

- **语音识别**：新增 `qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-asr-flash-filetrans`（非实时）等三款 Flash 系列模型，支持汉语七大方言、20+ 地区口音、古诗词优化、30 语种识别及 context 上下文能力 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)；`fun-asr-flash-2026-06-15` 同样覆盖方言与多语种，但上下文限制为 5 分钟音频。
- **文本生成与智能体**：`qwen3.7-flash` 和 `qwen3.7-flash-2026-07-15` 为原生视觉语言 Flash 模型，强化多模态 Agent 执行能力；`glm-5.2-fast-preview` 支持 1M 上下文，TPS 较标准版提升 1.5～2 倍；`kimi/kimi-k3` 为 2.8T 参数旗舰模型，原生支持视觉理解与 100 万 token 上下文 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **图片生成**：`qwen-image-3.0-pro` 支持最大 4.5k token 输入、10px 小字渲染、12 国语言与 20+ 字体原生渲染；`vidu/viduq3-fast_reference2image` 成本比 Pro 版降低约 50%，适用于高速高质低成本场景。
- **视频生成**：`pixverse/pixverse-motioncontrol` 支持动作迁移；`vidu/viduq3-drama_reference2video` 专用于精品剧/AI漫剧生产；`wan2.7-t2v-2026-06-12` 为万相 2.7 文生视频 6 月 12 日快照版本。
- **平台功能**：2026 年 7 月起，新增 Managed Agent 商业化、记忆库商业化、知识检索服务、知识问答服务、Skill 能力包、数据连接模块（MySQL/语雀/OSS）等核心能力 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro`、`xiaomi/mimo-v2.5-pro` 等主流模型均支持 1M token；`qwen3.7-text-embedding` 支持 256~2560 维用户自定义向量维度。
- **输入限制**：`vidu/viduq2-pro_reference2image` 等参考生图模型支持 0–14 张参考图片；`pixverse/pixverse-v6-r2v` 支持 2–7 张图像输入；`happyhorse-1.1-r2v` 最多支持 9 张参考图片。
- **性能指标**：`kimi-k2.7-code-highspeed` 输出速度约 180 [Token](../concepts/token.md)/s（中位数输入），短上下文可达 260 [Token](../concepts/token.md)/s；`qwen3.5-livetranslate-flash-realtime` 支持 60 种语言听懂、29 种语言说出。

> **注意**：文档 1 中 `qwen3.7-max-2026-06-08` 描述其“增加了视觉模态理解能力”，而同系列 `qwen3.7-plus`（2026-06-01）已明确具备“全面升级的视觉-语言能力”；二者发布时间相近但能力描述存在重叠，建议以 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新快照（如 `qwen3.7-max-2026-06-08`）为准进行验证。

## 使用方式

- **API 调用**：文本生成类模型统一通过 DashScope API 接入，支持 OpenAI Responses / Anthropic Messages 兼容接口；异步任务可通过 `background=true` 参数提交并轮询结果，或配置事件总线 HTTP 回调/RocketMQ 主动推送 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **部署与调优**：预置模型（如 `qwen-flash`）支持通过 API 直接部署，计费模式含按模型单元（MU）时长；模型调优已支持文本、视觉理解（VL）、图像生成（Wan/Wanx）、视频生成（万相）四类模型类型，含 SFT、DPO、RL（邀约制）等多种训练方式。
- **SDK 集成**：多模态交互开发套件提供 Linux C++、Android/iOS Lite、RTOS C、Java 等多端 SDK；Spring AI Alibaba 框架已支持调用百炼智能体与工作流应用。

## 限制和注意事项

- **模型下线**：2026 年 7 月起分批下线老旧模型（如 `qwen-turbo` 资源包启动退市、部分老旧长尾模型下线），具体清单与机制详见 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)；企业知识库（旧）已于 7 月 16 日下线，需迁移至新版知识库 RAG 服务。
- **地域与权限**：6 月新增美国、德国、日本地域部署范围；API Key 已升级为加密存储，并支持生成临时 [Token](../concepts/token.md) 用于不可信环境，避免永久密钥泄露风险。
- **兼容性约束**：`qwen3.5-livetranslate-flash-realtime` 仅支持实时音视频同传，离线翻译需调用对应离线版本；`qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-realtime-flash` 功能描述高度相似，但前者强调“高质量回复结果”，后者强调“极致响应速度”，实际选型需按延迟敏感度区分。
- **资源包与计费**：GLM-5.2 Fast mode、通义千问 VL 系列、Qwen3-Coder-Plus 等模型存在阶段性价格调整，详见各资源包优惠公告 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


