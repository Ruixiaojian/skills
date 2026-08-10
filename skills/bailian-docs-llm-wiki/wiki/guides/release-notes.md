# release notes

百炼平台的 release notes 汇总了模型生命周期管理（上架、下线）、平台功能演进及关键能力更新，面向开发者提供可落地的版本变更信息。内容聚焦于**实际可用性变化**，包括新增/停用模型列表、核心参数调整、调用方式变更、已知限制与迁移建议。所有信息均基于平台当前生效策略，不包含营销性描述。

## 支持的模型/功能

- **新增模型**：2026年7月起，平台陆续上线 `qwen3.8-max`（2.4万亿参数MoE旗舰）、`kimi/kimi-k3`（3万亿级开源模型）、`wan3.0-video`（全能参考视频生成）、`qwen-audio-3.0-realtime-plus/flash`（双工语音对话）、`pixverse/pixverse-motioncontrol`（动作迁移）等数十个模型，覆盖文本、视觉、语音、视频、3D、音乐等模态。详细清单见 [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能扩展**：2026年6月起，平台新增知识检索服务、知识问答服务、智能体托管运行时 API、Skill 能力包、数据连接模块（支持 MySQL/语雀/OSS）、[多模态](../concepts/multi-modal.md)翻译 API、[异步任务](../concepts/asynchronous-task.md)事件总线回调（EventBridge/RocketMQ）等能力；模型调优支持强化学习（RL）、0代码安全合规强化、视频/图像/视觉理解模型类型；模型部署支持 PTU 长输入与前缀缓存、按模型单元（MU）时长计费。
- **平台服务变更**：企业知识库（旧）已于2026年7月16日下线；Managed Agent 于7月16日启动商业化；记忆库于2026年3月20日升级为 Memory 2.0，支持[长期记忆](../concepts/long-term-memory.md)与多应用共享。

> **注意**：文档2中列出的 `qwen3.7-max-2026-06-08` 和 `qwen3.7-max-2026-05-20` 均标注为“快照”模型，但文档1明确将快照模型定义为“名称含具体日期标识（如 qwen-max-2025-01-25）”，而 `qwen3.7-max-2026-06-08` 符合该定义，应适用**30天提前通知**下线规则；但文档2未说明其是否属于快照模型，开发者需以控制台实际显示的模型ID命名格式为准判断通知周期。

## 关键参数

- **上下文长度**：`qwen3.8-max`、`kimi-k3`、`glm-5.2`、`xiaomi/mimo-v2.5-pro` 等主流模型均支持 **1M token** 超长上下文；`deepseek-v4-flash` 激活参数仅13B，但同样原生支持百万级上下文。
- **性能指标**：`deepseek-v4-flash-0731` 输出 TPS 为标准版 GLM-5.2 的 1.5～2 倍；`kimi-k2.7-code-highspeed` 编程场景输出速度约 180 [Token](../concepts/token.md)/s（中位数输入），短上下文可达 260 [Token](../concepts/token.md)/s；`qwen-audio-3.0-tts-flash` 首包延时 ≤200ms。
- **限流策略**：模型下线前将逐步缩减 QPM/TPM，先恢复至[默认限流](https://help.aliyun.com/zh/model-studio/rate-limit)再递减；具体数值需通过 [模型观测](https://bailian.console.aliyun.com/#/model-telemetry) 查看实时配额。

## 使用方式

- **模型调用**：所有新模型均通过统一推理 API 接入，支持 OpenAI Responses / Anthropic Messages 兼容接口（2026年5月起）；视频/语音类模型需按模态选择对应 endpoint（如 `/audio/tts`、`/video/generate`）。
- **[异步任务](../concepts/asynchronous-task.md)**：`Responses API` 自2026年6月1日起支持 `background=true` 异步提交，配合事件总线 HTTP 回调或 RocketMQ 主动推送结果（避免轮询），详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型部署与调优**：预置模型（如 `qwen-flash`）可通过 API 直接部署；自定义微调模型支持 LoRA/SFT/DPO/RL 训练，并可使用模型压缩模块量化部署；视频/图像/VL 模型调优能力自2026年5月起全面开放。
- **通知订阅**：下线/升级通知通过短信、邮件、站内信推送，**仅面向近3个月有调用记录的用户**；所有公告同步发布于官网公告页，建议主动订阅 [阿里云百炼公告中心](https://www.aliyun.com/notice/)。

## 限制和注意事项

- **模型下线影响**：自正式下线日起，模型推理服务立即终止；**已创建的应用若调用下线模型将无法返回结果**；模型调优与部署功能同步禁用（已训练/部署模型不受影响）；控制台模型广场、体验页及官方文档同步移除。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与兼容性**：2026年6月12日起新增美国、德国、日本地域部署；部分新功能（如 Skill 能力包、数据连接）需在新版应用架构下启用，旧版应用需迁移。
- **资源包与计费**：`qwen-turbo` 资源包已于2026年6月28日启动退市；`GLM-5.2 Fast mode` 于7月14日降价；团队版 [Token](../concepts/token.md) Plan 新增共享用量包（6月30日生效）。价格变动不影响已购资源包有效期。
- **兼容性风险**：`qwen3.7-max-preview`（2026-05-17）仅支持思考模式，与完整版 `qwen3.7-max`（2026-05-20）能力不一致；`fun-music-preview` 为预览快照版，不承诺生产环境稳定性。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


