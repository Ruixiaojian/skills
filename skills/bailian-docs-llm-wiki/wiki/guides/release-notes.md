# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架、下线）、平台功能迭代及关键能力变更，面向开发者提供可落地的版本演进信息。所有变更均以实际生效日期为准，模型 ID 与 API 行为严格对齐控制台与 SDK 实现。建议开发者定期查阅本页，并结合 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 和 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 进行兼容性评估。

## 支持的模型/功能

- **新增模型（2026年7月起重点）**：`qwen3.8-max`（2.4T MoE旗舰）、`kimi/kimi-k3`（2.8T KDA架构）、`qwen-audio-3.0-realtime-plus`/`-flash`（双版本实时语音对话）、`vidu/viduq3-drama_reference2video`（剧集专用视频生成）、`pixverse/pixverse-motioncontrol`（动作迁移）、`qwen3.7-text-embedding`（256–2560维可调向量）。完整列表见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块升级**：
  - 智能体托管：6月29日上线 `Managed Agent` 运行时 API，支持会话与工具执行全托管；
  - RAG 增强：6月23日上线知识检索与知识问答服务，支持多知识库联合检索与混合排序；
  - 模型部署：6月15日 PTU 部署新增长输入与前缀缓存能力；1月23日支持按模型单元（MU）时长计费；
  - API 能力：5月11日发布新版智能体应用 DashScope API（支持单/多轮、流式、文件问答、视觉理解）；6月1日 Responses API 新增异步调用（`background=true`）；
  - 安全与合规：5月4日模型调优新增 0 代码安全合规强化流程。

> **注意**：文档 2 中 `qwen3.7-flash-2026-07-15` 与文档 3 中 `qwen3.7-flash`（7月3日条目）指向同一模型，但文档 2 明确其为“Qwen3.7原生视觉语言系列Flash模型”，而文档 3 未提及其[多模态](../concepts/multi-modal.md)能力——请以 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 的功能说明为准。

## 关键参数

- **上下文长度**：`qwen3.8-max`、`kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流旗舰模型均支持 **1M token** 上下文；`qwen-audio-3.0-asr-flash-filetrans` 支持最长 5 分钟音频转录。
- **推理性能**：`deepseek-v4-flash` 激活参数 13B，输出 TPS 较标准版提升 1.5–2 倍；`kimi-k2.7-code-highspeed` 输出速度约 180–260 [Token](../concepts/token.md)/s。
- **视频生成时长**：`vidu/viduq3-pro-fast_img2video` 支持 16 秒视频；`pixverse/pixverse-upscale` 支持 4K 超分；`wan2.7-t2v-2026-06-12` 支持戏剧化镜头调度。
- **向量维度**：`qwen3.7-text-embedding` 支持用户自定义 256–2560 维输出。

## 使用方式

- **模型调用**：通过 `/v1/services/aigc/text-generation/generation`（文本）、`/v1/services/aigc/image-generation/generation`（图像）等标准化路径调用，模型 ID 直接传入 `model` 字段（如 `"model": "qwen3.8-max"`）。
- **异步任务**：使用 Responses API 时添加 `background=true` 参数提交任务，后续通过 `GET /v1/tasks/{task_id}` 轮询或配置 EventBridge HTTP 回调接收完成事件（文档 3，4月23日）。
- **模型部署**：PTU 部署需指定 `model_id` 与 `instance_type`（如 `qwen3.8-max` + `ptu.gn7i.2xlarge`），支持长输入与前缀缓存（文档 3，6月15日）。
- **模型调优**：图像/视频/视觉理解模型（如 Wan、PixVerse、Qwen-VL）已全面支持 SFT 与 DPO 训练（文档 3，5月28日、1月21日、9月12日）。

## 限制和注意事项

- **模型下线通知周期**：快照模型（含日期标识，如 `qwen-max-2025-01-25`）提前 30 天通知；主线模型提前 3 个月通知。通知后即开始限流（QPM/TPM 逐步缩减），正式下线后推理、新调优/部署全部停止（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **已下线模型不可恢复**：2026年7月10日公告的“部分老旧模型下线”（[官网公告 118434](https://www.aliyun.com/notice/118434)）与7月9日“部分老旧长尾模型下线”（[官网公告 118427](https://www.aliyun.com/notice/118427)）已生效，对应模型 ID 不再接受新请求。
- **功能弃用**：企业知识库（旧）已于7月16日下线（文档 3）；`qwen-turbo` 资源包于6月28日启动退市（文档 3）；2024年4月22日及更早批次下线模型无专项公告（文档 1）。
- **地域与协议约束**：新增美国、德国、日本地域接入（文档 3，6月12日）；实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）强制要求 WebSocket 或低延迟 HTTP/2 流式连接，不支持普通 REST 同步调用。

> **注意**：文档 1 列出“2026年10月10日将下线”模型，但文档 3 中 7月10日公告（118434）与7月9日公告（118427）已明确部分模型提前至7月下线。开发者应以最新公告日期为准，切勿依赖文档 1 中的静态列表。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


