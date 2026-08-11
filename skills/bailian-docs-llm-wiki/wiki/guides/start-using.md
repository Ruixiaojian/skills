# start using

阿里云百炼平台提供零代码与低代码两种路径，支持快速构建智能体、工作流、知识库等 AI 应用。开发者可基于控制台界面完成应用创建、知识库配置与发布，也可通过 API 集成至自有系统。本文档聚焦核心使用路径，涵盖模型/功能支持范围、关键参数配置、调用方式及重要限制，适用于初次接入的开发者。

## 支持的模型/功能

百炼当前支持多类模型与能力组合，覆盖文本、[多模态](../concepts/multi-modal.md)、推理与嵌入场景：

- **大语言模型**：`qwen-max`（推荐入门）、`qwq-plus`、`qwq-32b`、`deepseek-*` 系列，以及 `qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 等[多模态](../concepts/multi-modal.md)视觉语言模型 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)；
- **嵌入模型**：`text-embedding-v4`（推荐，默认启用）、`text-embedding-v3`，v4 在语种覆盖、代码向量化与维度灵活性上优于 v3 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
- **知识库能力**：支持文档、音视频、图片、结构化数据（MySQL/RDS/DMS）四类知识源；非结构化知识库支持 HTML、Excel、PDF、DOCX 及离线文件导入；结构化知识库支持增量同步与表头类型设置 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
- **高级功能**：[长期记忆](../concepts/long-term-memory.md)（新）API 提供自动信息提取、语义检索与用户画像管理；MCP 市场支持预置及自定义服务集成；工作流支持批量节点、[多模态](../concepts/multi-modal.md)生成节点与 Dify 一键导入。

> **注意**：文档 1 中提及“智能体应用支持 QwQ 系列模型（不包括[插件](../concepts/plugin.md)、流程、音视频交互能力）”，但文档 2 的实操流程未体现该限制；实际使用中，QwQ 模型在智能体应用中**不支持音视频实时互动**，该能力仅对 `qwen-vl-*` 等多模态模型开放。请以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的明确说明为准。

## 关键参数

以下参数直接影响效果与成本，需在配置阶段显式设置或评估：

- **知识库检索 TopK**：`初步向量检索TopK` 与 `初步关键词检索TopK` 可调低以减少送入排序模型的 [Token](../concepts/token.md) 量，显著降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
- **知识库权重**：当智能体关联多个知识库时，可通过权重控制召回优先级，数值越高越优先被检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
- **切分策略**：创建知识库时推荐选择“智能切分”，该策略经评测对多数文档具备最优检索效果（见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)）；
- **多模态识别开关**：智能体应用的“检索配置”中需手动开启“多模态回复增强”，否则无法解析知识库中的图表与图像内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

### 控制台零代码流程（推荐快速验证）
1. **创建应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用” → 设置模型（如 `qwen-max`）、System Prompt、欢迎语与预设问题；
2. **构建知识库**：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，上传文档 → 选择“标准版” → 使用“智能切分” → 完成创建；
3. **绑定与发布**：在应用配置页 → “技能” → “知识库” → 添加已建知识库 → 点击“发布”。

### API 集成方式
- **同步调用**：适用于实时交互，兼容 OpenAI SDK 接口风格，详见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中的“同步调用 API 参考”；
- **异步调用**：对耗时任务（如长视频处理），设置 `background=true`，立即返回 Task ID，后续通过 `/tasks/{id}` 查询结果；
- **知识库管理**：支持 `CreateIndex`（含音视频类型）、`UpdateIndex`、`GetIndexMonitor` 等 API，用于程序化运维 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费生效时间**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费，后付费与资源包两种模式并存 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
- **模型能力边界**：QwQ 系列模型虽支持强推理，但**不支持[插件](../concepts/plugin.md)调用、音视频交互及流程编排**；若需上述能力，应选用 `qwen-vl-*` 或 `qwen-max` 等通用大模型；
- **调试与观测**：知识库编辑页提供在线调试面板，可实时验证检索召回效果；应用发布后，可通过 [应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe) 查看端到端链路与性能指标；
- **权限与分账**：子账号可开通知识库，结合“标签”功能实现部门/项目级分账管理，但需确保服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`）已正确授权 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)
- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)


