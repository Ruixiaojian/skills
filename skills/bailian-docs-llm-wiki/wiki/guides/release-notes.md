# release notes

百炼平台的 Release Notes 汇总了模型生命周期管理（上架/下线）、平台功能迭代及关键参数变更，面向开发者提供可落地的操作依据。所有变更均以实际生效时间为准，模型下线遵循分级通知机制，平台功能更新覆盖 API、部署、调优、RAG 等核心链路。开发者应定期查阅本页并结合控制台告警与通知渠道及时响应。

## 支持的模型/功能

- **新模型上架**：2026年7月起，平台陆续上线 `qwen3.8-max`（2.4万亿参数MoE旗舰）、`qwen-image-3.0`（4.5k token输入、10px小字渲染）、`qwen-audio-3.0-asr-flash-streaming`（支持30语种+方言+古诗词识别）等[多模态](../concepts/multi-modal.md)模型；第三方模型如 `kimi/kimi-k3`（2.8万亿参数）、`glm-5.2`（1M上下文）亦同步接入。详见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **模型下线范围**：截至2026年10月10日，将集中下线千问系列历史主线与快照模型（如 `qwen-turbo`、`qwen-vl-max-latest`、`qwen3-coder-plus-2025-07-22`）、第三方模型（如 `glm-4.5`、`deepseek-v3.2-exp`）、语音/图像/视频类旧模型（如 `aitryon`、`stable-diffusion-v1.5`）等。已下线模型包括 `gte-rerank`（2026-05-30）、`qwen-audio-asr`（2026-03-30）。完整清单见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **平台功能新增**：2026年6月起，上线知识检索服务、知识问答服务、Skill能力包、数据连接模块（MySQL/语雀/OSS）；7月新增智能体托管运行时API、Managed Agent商业化、记忆库商业化；8月启用模型升级通知与个人版[Token](../concepts/token.md) Plan权益升级。功能详情参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

> **注意**：文档2中 `qwen3.7-max-2026-06-08` 描述为“增加视觉模态理解能力”，但文档1中同日下线的 `qwen3-vl-flash-2026-01-22-us` 等VL模型未明确标注是否影响该能力继承路径；建议以控制台实际可用模型列表为准，避免依赖快照ID的隐含能力假设。

## 关键参数

- **上下文长度**：`qwen3.8-max`、`kimi/kimi-k3`、`glm-5.2`、`deepseek-v4-pro` 等主流模型支持 1M token 超长上下文；`qwen3.7-flash` 等Flash系列默认上下文为 128k–256k，具体以模型文档为准。
- **推理延迟**：`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms；`qwen-audio-3.0-realtime-flash` 端到端响应时延经全向流式优化后达行业领先水平。
- **[多模态](../concepts/multi-modal.md)能力标识**：模型ID含 `-vl`（Visual-Language）、`-ocr`、`-asr`、`-tts`、`-video` 等后缀表示原生支持对应模态；无后缀模型（如 `qwen3.7-plus`）默认仅支持文本，但部分已扩展视觉理解（见文档2中 `qwen3.7-plus` 的“全面升级视觉-语言能力”描述）。
- **部署计费单元**：自2026年1月起，模型部署支持按模型单元（MU）时长计费，适用于 `qwen-flash`、`qwen-plus` 等预置模型；PTU部署自2026年6月起支持长输入与前缀缓存。

## 使用方式

- **模型调用**：通过 DashScope SDK 或 RESTful API 调用，需指定 `model` 参数为有效模型ID（如 `qwen3.8-max`），快照模型（如 `qwen3-max-2026-01-23`）在下线前仍可调用，但不保证长期兼容性。
- **功能集成**：
  - 新增 RAG 场景使用 `knowledge_retrieval` 和 `knowledge_qa` 接口（2026-06-23上线）；
  - 智能体开发需接入 `managed-agents-api`（2026-06-29）或使用 Skill 能力包（2026-06-10）；
  - 异步任务推荐采用事件总线 HTTP 回调（2026-04-23支持），避免轮询。
- **模型调优**：2026年起支持图像生成（Wan/Wanx）、视频生成（万相）、VL模型的SFT与DPO训练；安全合规强化支持0代码注入（2026-05-04）；强化学习（RL）训练为邀约制（2026-05-31）。

## 限制和注意事项

- **模型下线影响**：自下线通知发布日起，QPM/TPM 将逐步缩减；正式下线后，API 推理、新调优/部署操作立即失效，但已部署模型实例不受影响。快照模型（如日期型ID）提前30天通知，主线模型提前3个月通知 —— 详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与部署限制**：2026年6月新增美国、德国、日本地域部署，但部分新模型（如 `wan3.0-video`）初始仅限华北2（北京）可用，跨地域调用需确认模型部署状态。
- **兼容性风险**：文档2中 `qwen3.7-flash` 与文档1中下线的 `qwen-flash-us` 名称近似，但二者无继承关系；`qwen-turbo` 已于2026-10-10下线，其资源包自2026-06-28启动退市，不可用于新部署。
- **免费额度策略**：2025年7月起启用“免费额度用完即停”机制（文档3），开发者需监控用量看板，避免服务中断。

> **注意**：文档3中“2026年7月10日部分老旧模型下线通知”链接指向官网公告（https://www.aliyun.com/notice/118434），但该公告内容实际已被文档1中更详尽的下线表格覆盖；开发者应以文档1的结构化表格为准，官网公告仅作辅助参考。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


