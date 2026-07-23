# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及基础设施层面的持续演进，涵盖新增能力、计费调整、模型上下架、接口变更与关键限制。开发者应结合自身业务场景关注模型兼容性、调用方式变更及生命周期策略，避免因模型下线或 API 升级导致服务中断。所有变更均以平台实际生效时间为准，历史快照模型（如 `qwen3.7-plus-2026-05-26`）需显式指定版本标识符调用。

## 支持的模型/功能

- **新增模型类型覆盖全模态**：2026年7月起，平台新增实时多模态语音模型（`qwen-audio-3.0-realtime-plus`）、高保真图像生成模型（`qwen-image-3.0-pro`）、参考生视频（`vidu/viduq3-ad_reference2video`）、3D生成（`Tripo/Tripo-H3.1`）及音乐生成（`fun-music-v1`）等能力，详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **智能体与工作流增强**：6月上线智能体托管运行时 API（[了解详情](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview)），支持会话与工具执行全托管；同时新增 Skill 能力包机制，允许智能体动态加载官方或自定义技能 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **RAG 与知识服务升级**：6月同步上线知识检索服务与知识问答服务，支持多知识库联合检索、混合排序及基于大模型的端到端生成回答 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 关键参数

- **模型标识规范**：新上架模型（如 `kimi/kimi-k3`、`pixverse/pixverse-lipsync`）采用 `provider/model-name` 命名空间格式；快照模型（如 `qwen3.7-plus-2026-05-26`）必须显式指定时间后缀，否则默认调用最新稳定版。
- **上下文与缓存**：`qwen3.7-max` 等模型支持显式缓存（`cache_control` 字段），但 `qwen3.6-flash` 等 Flash 档位模型暂不支持；GLM-5.1 支持 200K 上下文，最大输出 128K Token。
- **异步任务控制**：Responses API 新增 `background=true` 参数启用异步模式；异步任务完成事件可通过 EventBridge HTTP 回调或 RocketMQ 主动推送，无需轮询 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 使用方式

- **API 调用入口**：文本生成统一入口已聚合 OpenAI Responses 与 Anthropic Messages 接口分类；新版智能体应用 DashScope API 支持单/多轮、流式、文件问答与视觉理解 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **部署与调优**：模型部署支持按模型单元（MU）时长计费，适用于 `qwen-flash`/`qwen-plus` 等预置模型；模型调优新增 RL 训练（邀约制）、0 代码安全合规强化及 DPO 偏好训练（千问2.5/3系列）。
- **SDK 与客户端**：多模态交互开发套件提供 Linux C++、Android/iOS Lite、RTOS C 等多端 SDK；接入工具新增 Kilo CLI，支持 Token Plan/Coding Plan/按量三种计费方式接入。

## 限制和注意事项

> **注意**：文档 1 中“6月28日 qwen-turbo 资源包启动退市通知”与文档 2 中“2026-06-15 qwen3.7-plus”存在隐含冲突——qwen-turbo 已进入退市流程，但同月上线的 qwen3.7-plus 系列未明确标注是否继承其资源包兼容性。建议开发者避免在新项目中依赖 qwen-turbo 资源包，改用 qwen3.7-plus 或更高版本配套的 Token Plan。
>
> **注意**：文档 2 明确指出 `qwen3.6-flash` “不支持图像与视频输入”，而文档 1 中“1月22日模型调优新增视觉理解(VL)模型类型支持”未限定适用模型范围。实际调用时，`qwen3.6-flash` 无法处理多模态输入，需选用 `qwen3.7-plus` 或 `qwen3.7-max` 等原生 VL 模型。
>
> **注意**：企业知识库（旧）已于 2026年7月16日下线，所有存量调用将失效；新知识库 RAG 服务需通过独立 API（如 `/knowledge/retrieve`）接入，且日志全量投递至 SLS，不再复用旧版监控路径 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

- **模型生命周期**：老旧模型（含长尾型号）分批下线，具体清单与宽限期见 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)；部分模型（如 `qwen-turbo`）已启动退市，不可用于新部署。
- **地域与部署约束**：新增美国、德国、日本地域，但部分模型（如 `qwen-image-3.0-pro`）当前仅限华北2（北京）部署，跨地域调用需确认服务可用性。
- **免费额度策略**：启用“免费额度用完即停”后，额度耗尽将返回 `AllocationQuota.FreeTierOnly` 错误码，而非自动转为付费，需主动配置用量告警或预留 Credits。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


