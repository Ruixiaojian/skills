# release notes

本页汇总百炼平台近期模型与功能更新，涵盖新模型上线、已有模型能力演进、平台功能迭代及关键使用约束。所有信息均基于官方发布内容整理，面向开发者提供可直接用于集成与调用的结构化参考。模型能力以实际 API 接口为准，建议结合 [原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md) 和 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md) 查阅原始技术细节与上下文。

## 支持的模型/功能

- **文本生成与深度思考**：新增 `qwen3.7-flash`（2026-07-21）、`glm-5.2-fast-preview`（2026-07-09）、`xiaomi/mimo-v2.5-pro`（2026-05-18）等模型；`kimi/kimi-k3`（2026-07-17）为首个开源 2.8T 参数模型，支持 100 万 token 上下文与原生视觉理解。
- **多模态与视觉理解**：`qwen3.7-flash`、`qwen3.7-plus`、`qwen3.7-max-2026-06-08` 均强化视觉-语言联合推理与 Agent 执行能力；`qwen3.5-ocr`（2026-06-16）专精文档解析与卡证关键信息抽取。
- **图像生成**：`qwen-image-3.0-pro`（2026-07-20）支持 4.5k token 输入、10px 小字渲染与 12 国语言字体原生渲染；`vidu/viduq3-fast_reference2image`（2026-07-09）成本较 Pro 版降低约 50%。
- **视频生成**：`vidu/viduq3-drama_reference2video`（2026-07-09）专注剧集一致性与动效美学；`pixverse/pixverse-motioncontrol`（2026-07-14）支持从参考视频提取动作并迁移至目标人物图；`wan2.7-r2v-2026-06-12`（2026-07-01）支持最多 5 图/视频混合参考及音频音色参考。
- **语音与音频**：`qwen-audio-3.0-tts-plus`（2026-07-14）强调音质与表现力，适用于有声书/影视配音；`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms，适配语音助手等低延迟场景；`fun-asr-flash-2026-06-15` 支持 30 语种及汉语七大方言体系。
- **向量与嵌入**：`qwen3.7-text-embedding`（2026-07-15）支持 256~2560 维自定义输出维度，在 MTEB 多语言检索任务上效果提升 20%。
- **平台级功能**：新增知识检索服务与知识问答服务（2026-06-23）、智能体托管运行时 API（2026-06-29）、Skill 能力包（2026-06-10）、数据连接模块（2026-06-10）、Responses API 异步调用（2026-06-01）；模型调优已支持图像生成、视觉理解、视频生成三类模型（见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 关键参数

- **上下文长度**：`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro`、`xiaomi/mimo-v2.5-pro` 等主流旗舰模型均支持 100 万 token 上下文；`qwen-audio-3.0-realtime-plus` 未公开上下文长度，但明确标注“端到端响应时延控制在低水平”。
- **输入限制**：
  - 图片生成类（如 `vidu/viduq2-pro_reference2image`）支持 0–14 张参考图；
  - 视频生成类（如 `pixverse/pixverse-v6-r2v`）支持 2–7 张图像输入；
  - `fun-asr-flash-2026-06-15` 支持 ≤5 分钟音频转写。
- **输出控制**：
  - `qwen-audio-3.0-tts-plus` 与 `qwen-audio-3.0-tts-flash` 均支持细粒度标签控制情绪、语气、角色、语速、音量；
  - `pixverse/pixverse-lipsync` 支持嘴部动作与输入音频/TTS 精准同步；
  - `qwen3.7-text-embedding` 允许用户指定向量维度（256–2560）。
- **性能指标**：
  - `kimi/kimi-k2.7-code-highspeed` 输出速度约 180 [Token](../concepts/token.md)/s（中位数输入），短上下文可达 260 [Token](../concepts/token.md)/s；
  - `qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；
  - `Tripo/Tripo-P1.0` 生成专业级拓扑 3D 资产耗时约 2 秒。

> **注意**：文档 1 中 `kimi/kimi-k2.7-code`（2026-06-15）与 `kimi/kimi-k2.7-code-highspeed`（2026-06-17）被描述为“同一个模型”，但文档 1 同时列出二者为独立模型 ID，且后者明确标注“输出速度约为普通版的 5–6 倍”。实际调用时请以 API 文档中 `model_id` 实际可用性为准，避免混淆。

## 使用方式

- **模型调用**：所有模型通过百炼统一 API 接口调用，支持 OpenAI-compatible（`/v1/chat/completions`）与 DashScope 原生协议（`/v1/services/aigc/text-generation/generation`）。具体 endpoint、鉴权方式与请求格式详见各模型文档。
- **平台功能接入**：
  - 新增功能如 Skill 能力包、数据连接模块、知识检索服务均需通过对应 API 或控制台启用；
  - Responses API 异步调用需设置 `background=true` 并轮询 `/v1/async_tasks/{task_id}` 获取结果；
  - 智能体托管运行时（Managed Agent）需调用 `/v1/agents/run` 接口，会话与工具执行由平台托管。
- **模型部署与调优**：
  - 预置模型（如 `qwen-flash`、`qwen-plus`）支持通过 API 直接部署（见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）；
  - 自定义模型导入支持 LoRA 微调模型从 OSS 导入（2026-06-05 国际站上线）；
  - 视觉理解、视频生成、图像生成模型均已开放 SFT/DPO/RL 训练支持（见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 限制和注意事项

- **模型下线**：平台按季度清理老旧模型，2026年7月已发布《部分老旧模型下线通知》与《部分老旧长尾模型下线通知》；历史快照模型（如 `wan2.7-t2v-2026-04-25`）可能随时不可用，生产环境应避免硬编码快照 ID。
- **地域与权限**：新增美国、德国、日本地域部署（2026-06-12），但部分模型（如 `qwen-audio-3.0-realtime-plus`）当前仅限华北2（北京）可用；API Key 加密存储与业务空间专属域名已于 2026-06-29 升级，旧域名将逐步停用。
- **资源与计费**：
  - `qwen-turbo` 资源包已启动退市（2026-06-28）；
  - 记忆库、Managed Agent、企业知识库（旧）等平台功能已商业化或下线（2026-07）；
  - 模型上下文缓存、Qwen-VL 系列、千问系列模型均有降价通知（见 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。
- **兼容性风险**：
  - `qwen3.7-max`（2026-05-21）与 `qwen3.7-max-2026-05-20` 在文档 1 中并存，但后者为前者的快照标识；实际调用应优先使用无时间后缀的 `qwen3.7-max`，其能力随平台自动更新；
  - `vidu/viduq3-mix_reference2video`（2026-04-28）与 `vidu/viduq3_reference2video`（2026-04-27）功能描述高度重合，且均标注“万物可参，声画同出”，建议以最新版本 `viduq3-mix` 为准，旧版可能受限或归档。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


