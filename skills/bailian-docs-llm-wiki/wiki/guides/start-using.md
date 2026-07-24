# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，支持零代码快速搭建私有知识问答应用，也支持通过 API 进行深度集成。开发者可基于智能体（Agent）、工作流（Workflow）或高代码应用三种范式启动项目，核心路径为：选择模型 → 配置 Prompt 与技能（如知识库）→ 测试并发布。所有操作均可在控制台完成，也可通过标准化 API 调用。

## 支持的模型/功能

- **基础模型**：支持千问系列（如 `qwen-max`、`qwen-vl-plus-latest`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、DeepSeek 系列（`deepseek-chat`）等，其中 QwQ 模型适用于需强推理的场景，DeepSeek 系列支持智能体与工作流双路径调用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **[多模态](../concepts/multi-modal.md)能力**：`qwen-vl-plus-2025-01-25`（即 `qwen-vl-plus-0125`）支持 128k 上下文及增强版图文理解；知识库支持音视频文件导入与解析，可用于直播回放问答、课程助教等场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **应用类型**：  
  - *智能体应用（Agent 2.0）*：统一将知识库、MCP 作为工具，由模型自主规划调用顺序，完整展示思考链 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - *工作流应用*：支持[多模态](../concepts/multi-modal.md)生成节点、批量节点、异步运行模式及 Dify 工作流一键导入；  
  - *高代码应用*：基于 Python 项目结构部署，内置运维与可观测性能力。

> **注意**：文档 1 中推荐使用“千问-Max”模型，但文档 2 显示该模型已非最新命名规范（当前控制台显示为 `qwen-max`），且 `qwen-vl-plus-latest` 等新版本已替代旧版 VL 模型。实际选型请以 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 实时列表为准。

## 关键参数

- **知识库检索配置**：  
  - `初步向量检索 TopK` 与 `初步关键词检索 TopK`：降低数值可减少送入排序模型的 [Token](../concepts/token.md) 量，从而降低成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - 多知识库权重设置：当应用关联多个知识库时，可按信息源重要性分配权重，系统优先召回高权重知识库内容；  
  - “[多模态](../concepts/multi-modal.md)回复增强”开关：开启后支持解析知识库中图表与图像内容，生成结合视觉信息的回答。
- **[长期记忆](../concepts/memory.md)**：新版[长期记忆](../concepts/memory.md)（Long-Term Memory 2.0）支持自动提取关键信息、语义检索、用户画像管理，并可通过开放 API 接入任意应用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[Prompt 工程](../concepts/prompt-engineering.md)**：支持 System Prompt 定义角色与任务，同时提供 Prompt 样例库（FewShot）能力，通过录入 Query-Answer 对提升客服、问答类场景准确性。

## 使用方式

- **零代码方式**（适合快速验证）：  
  1. 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用；  
  2. 选择模型、配置 Prompt、设置欢迎语与预设问题；  
  3. 通过 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 上传文档，再在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建标准版知识库（支持文档/数据/图片三类）；  
  4. 在应用配置中绑定知识库，测试后点击“发布” [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **API 方式**（适合生产集成）：  
  - 同步调用：使用 Responses API，兼容 OpenAI SDK，适用于实时交互；  
  - 异步调用：设置 `background=true`，立即返回 Task ID，后续通过任务中心查询结果；  
  - 知识库管理：支持 `CreateIndex`（含音视频）、`UpdateIndex`、`GetIndexMonitor` 等 API；  
  - 所有 API 文档详见 [同步调用 API 参考](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference) 与 [异步调用 API 参考](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用由规格费 + 模型调用费构成；支持后付费与资源包两种模式，资源包需单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持[插件](../concepts/plugin.md)、流程、音视频交互能力**，仅适用于纯文本推理场景；而工作流应用则完整支持 QwQ 的多节点编排能力。
- **知识库类型约束**：非结构化知识库支持 PDF/DOCX/Excel/HTML/音视频等格式，但图片解析需显式选择 `qwen-vl-max` 或 `qwen-vl-plus` 模型；结构化知识库支持 RDS、DMS、自建 MySQL 数据源，但不支持直接上传 Excel 作为结构化数据源（需先转为数据库表）。
- **调试与观测**：编辑智能体应用时可使用知识库调试面板实时验证检索效果；应用发布后，可通过 [应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe) 查看端到端处理流程与性能指标。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


