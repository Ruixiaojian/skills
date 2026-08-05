# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架/下线）、平台功能迭代及关键参数变更，面向开发者提供可落地的版本演进信息。所有变更均以稳定性、兼容性与生产就绪为前提，模型下线严格遵循通知期机制，新功能上线同步配套 API、SDK 与控制台支持。建议开发者定期查阅本页，并通过 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 和 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 获取完整上下文。

## 支持的模型/功能

- **新增模型**：2026年7月起，Qwen3.8系列旗舰模型 `qwen3.8-max` 正式发布；`qwen-image-3.0` 与 `qwen-image-3.0-pro` 均支持4.5k token输入、10px小字渲染及12国语言原生字体；语音方向新增 `qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-tts-plus`（高表现力）与 `qwen-audio-3.0-realtime-flash`（端到端延时<200ms）三类子模型；第三方模型如 `glm-5.2-fast-preview`、`kimi/kimi-k3`、`deepseek-v4-pro` 等已全量接入。详情见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
  
- **下线模型**：2026年10月10日将集中下线大量历史模型，包括主线模型（如 `qwen3.6-max-preview`、`qwen-vl-flash`）和快照模型（如 `qwen3-max-2026-01-23`、`qwen3-vl-flash-2026-01-22`），以及语音、图像、视频等全模态老旧模型（如 `aitryon`、`qwen-tts`、`paraformer-v1`）。已下线模型包括 `gte-rerank`（2026-05-30）、`qwen-audio-asr`（2026-03-30）等。完整清单请参考 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

- **平台功能**：2026年6月起，知识库 RAG 新增「知识检索服务」与「知识问答服务」；智能体托管运行时（Managed Agent）正式商业化；模型部署支持 PTU 长输入与前缀缓存；API 层面新增 Responses API 异步调用（`background=true`）、事件总线 HTTP 回调、临时 API Key 生成等能力；多模态交互开发套件已覆盖 Android/iOS/Lite/Linux C++/RTOS C/Java 全端 SDK。

> **注意**：文档 3 中“6月10日 Skill 能力包上线”与文档 2 中“2026-06-15 kimi/kimi-k2.7-code”存在隐含冲突——后者明确声明支持“Agent 任务”，但未说明是否依赖 Skill 能力包。实际集成时请以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 Skill 的 API 文档为准，避免假设模型原生兼容未声明的能力。

## 关键参数

- **模型标识**：主线模型（如 `qwen3.7-plus`）无日期后缀，代表持续演进的稳定版本；快照模型（如 `qwen3.7-plus-2026-05-26`）含精确日期，适用于确定性场景，但受30天下线通知约束。
  
- **上下文长度**：`qwen3.8-max`、`glm-5.2`、`kimi/kimi-k3` 等旗舰模型支持 1M token；`qwen3.7-text-embedding` 支持 256–2560 维自定义向量维度；`qwen-audio-3.0-asr-flash` 支持 5 分钟音频上下文转写。

- **性能指标**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`kimi/kimi-k2.7-code-highspeed` 输出速度达 180–260 [Token](../concepts/token.md)/s；`pixverse/pixverse-v6-r2v` 支持 15 秒长视频生成。

- **计费单元**：模型部署支持按模型单元（MU）时长计费（见文档 3 “1月23日”条目）；资源包类商品（如 `qwen-turbo` 资源包）已启动退市（文档 3 “6月28日”），需迁移至 [Token](../concepts/token.md) Plan 或按量计费。

## 使用方式

- **模型调用**：统一通过 DashScope API 接入，文本生成推荐使用 OpenAI-compatible `Responses` 接口（支持流式、异步、文件问答）；多模态任务（如图生视频）需指定 `vidu/viduq3-fast_reference2image` 等完整模型 ID；语音类模型（ASR/TTS/Realtime）须按 `qwen-audio-3.0-*` 命名规范选择子型号。

- **功能启用**：新功能均通过控制台或 OpenAPI 开放。例如，知识库联合检索需调用 `/v1/rag/knowledge_retrieval`；Skill 能力包需在智能体配置中显式绑定；临时 API Key 生成需调用 `/v1/auth/create_temporary_token`（文档 3 “6月3日”）。

- **模型迁移**：下线模型用户应优先测试替代模型效果（如 `qwen-turbo` → `qwen3.7-flash`），并利用 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 页面验证调用量与性能差异。迁移后需更新代码中硬编码的模型 ID，并检查参数兼容性（如 `max_tokens`、`temperature` 等通用参数保持一致，但 `top_p` 行为可能因模型架构微调而变化）。

## 限制和注意事项

- **下线影响**：自下线通知发布日起，QPM/TPM 将逐步缩减；正式下线后，API 返回 `404 Model Not Found`，已部署模型实例不受影响，但不可新建调优或部署任务。部分模型（如 `qwen-vl-ocr`）下线后仍保留调优入口，以通知为准。

- **地域与权限**：2026年6月新增美国、德国、日本地域部署（文档 3 “6月12日”），但部分新模型（如 `qwen3.8-max`）当前仅限华北2（北京）可用；企业版用户需确认业务空间（Workspace）已开通对应地域权限。

- **兼容性风险**：`qwen3.5-ocr`（2026-06-16 上线）替换旧 OCR 模型时，输出 JSON 结构中 `text` 字段语义增强，但 `bounding_box` 坐标系单位由像素改为归一化值（0–1），需适配前端渲染逻辑。

- **过时信息**：文档 1 中“千问Turbo 快照模型 `qwen-turbo-latest` 下线时间为 2026-05-13”，但文档 3 “6月28日” 明确 `qwen-turbo` 资源包“启动退市”，二者时间点不一致。实际以资源包退市为最终信号，模型 ID 本身仍可调用至 2026-10-10，但不再享受资源包折扣。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


