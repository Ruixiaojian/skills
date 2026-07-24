# release notes

百炼平台的 Release Notes 汇总了模型、功能、API 及平台能力的最新动态，涵盖新增支持、参数变更、使用方式更新及下线安排。开发者应定期查阅以确保调用兼容性、成本可控性与功能时效性。所有变更均面向生产环境生效，部分能力需开通邀约权限或满足地域/配额条件。

## 支持的模型/功能

- **新增模型**：2026年7月起，华北2（北京）陆续上线 `qwen-image-3.0-pro`（图像生成）、`kimi/kimi-k3`（100万token上下文推理）、`qwen-audio-3.0-realtime-plus`（实时语音双工对话）、`vidu/viduq3-ad_reference2video`（广告向参考生视频）等数十款多模态与专业领域模型；详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **核心功能扩展**：
  - 知识库RAG：6月23日上线知识检索服务与知识问答服务，支持多知识库联合检索与混合排序 [了解详情](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval)；
  - 智能体托管：6月29日发布 Managed Agent 运行时 API，提供会话托管与工具执行生命周期管理；
  - 模型调优：5月31日新增强化学习（RL）训练（邀约制），5月28日支持图像生成模型（Wan/Wanx）调优，1月21日新增视频生成模型类型支持；
  - 多模态交互：4月28日上线服务端 Java SDK，2月28日新增 Linux C++ SDK，覆盖全端接入场景；
  - 数据连接：6月10日上线数据连接模块，支持 MySQL/语雀/OSS 等数据源直连；
  - Prompt 工程：4月7日上线 Prompt 工程 API，提供模板版本化与变量注入能力。

> **注意**：文档1中“6月29日 智能体托管运行时上线”与文档2未提及该能力，但文档1明确提供了 [智能体托管运行时 API](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview) 文档链接，应以文档1为准；文档2聚焦模型上架，二者互补而非矛盾。

## 关键参数

- **计费与资源单位**：
  - 模型部署支持按模型单元（MU）时长计费（1月23日上线），适用于 `qwen-flash`/`qwen-plus` 等预置模型；
  - `deepseek-v4-pro` 的 `cached_token` 单价自2026年4月29日起调整为 **1元/百万token**（[原文标题](../../raw/model-user-guide/release-notes/newly-released-models.md)）；
  - `qwen3.6-max-preview` 仅支持纯文本输入，不支持图像与视频输入（文档2明确标注）。
- **上下文与性能**：
  - `kimi/kimi-k3` 原生支持 100 万 token 上下文窗口；
  - `glm-5.1` 支持 200K 上下文，最大输出 128K [Token](../concepts/token.md)；
  - `qwen3.5-ocr` 上下文扩展至 128K，支持多轮对话；
  - PTU 部署自6月15日起支持长输入与前缀缓存（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 使用方式

- **API 调用**：
  - Responses API 自6月1日起支持异步调用（`background=true`），适用于长耗时任务；
  - [异步任务](../concepts/asynchronous-task.md)可配置事件总线 HTTP 回调或 RocketMQ 主动推送（4月23日上线），替代轮询；
  - 新增生成临时 API Key 文档（6月3日），推荐在不可信环境使用；
  - Spring AI Alibaba 框架集成文档已上线（6月1日），支持调用百炼智能体与工作流应用。
- **模型部署与调优**：
  - 模型导入 API 自6月3日起完整开放，支持 LoRA 微调模型从 OSS 导入（[原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)）；
  - DPO 偏好训练（9月上线）支持千问3/2.5系列，降低幻觉并提升人类偏好对齐；
  - 模型压缩模块（5月25日上线）提供量化算法，将全精度微调模型转为低精度部署版本。

## 限制和注意事项

- **模型下线与兼容性**：
  - 7月10日、7月9日分别发布“部分老旧模型下线通知”与“部分老旧长尾模型下线通知”，7月6日同步发布延期下线公告，开发者需及时迁移；
  - 企业知识库（旧）已于7月16日下线，须迁移到新版知识库服务；
  - `qwen-turbo` 资源包自6月28日起启动退市流程；
  - `qwen-image-2.0-pro-2026-04-22` 等快照模型为临时版本，后续可能被新快照覆盖，生产环境建议使用稳定版别名（如 `qwen-image-2.0-pro`）。
- **地域与协议限制**：
  - 新增美国、德国、日本地域部署（6月12日），但部分模型（如 `kimi/kimi-k3`）当前仅限中国内地可用；
  - `qwen3.6-max-preview` 明确不支持图像与视频输入，调用时需校验输入格式；
  - 通义听悟 Agent 工业指令转写仅支持 WebSocket 协议（5月21日上线），不支持 HTTP 同步调用。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


