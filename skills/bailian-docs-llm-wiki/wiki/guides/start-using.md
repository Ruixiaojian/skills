# start using

阿里云百炼平台提供零代码与低代码两种路径，支持开发者快速构建智能体、工作流、知识库等 AI 应用。本文档面向开发者，聚焦“开始使用”阶段的核心能力、参数配置与调用方式，不包含营销性描述。所有功能均基于控制台操作或标准 API 接口，适用于生产环境集成。

## 支持的模型/功能

百炼平台当前支持以下主流应用类型及对应能力：

- **智能体应用（Agent）**：支持 Qwen 系列（如 `qwen-max`）、QwQ 系列（如 `qwq-plus`、`qwq-32b`）、DeepSeek 系列模型，以及 `qwen-vl-plus-latest` 等[多模态](../concepts/multimodal.md)视觉模型；新版智能体（Agent 2.0）统一将知识库、MCP 作为可自主规划调用的工具，并支持音视频实时互动、文件问答（全文引用/切片检索/自定义处理）等能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **工作流应用（Workflow）**：支持大模型节点调用 QwQ、DeepSeek 等推理模型；新增[多模态](../concepts/multimodal.md)生成节点（图像/视频/音频生成）、批量节点、Dify 工作流一键导入；知识库节点支持必定调用、智能调用、旧版调用三种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库（RAG）**：支持文档、数据、图片三类结构化/非结构化知识库；支持音视频文件上传与解析（含直播回放问答、字幕生成等场景）；支持自建 MySQL、云数据库 RDS、DMS 等结构化数据源；非结构化知识库支持 Excel、HTML、PDF、DOC 等格式及自定义 metadata [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md) & 用户画像**：新版[长期记忆](../concepts/long-term-memory.md)（Long-term Memory 2.0）提供开放 API，支持多应用共享、自动信息提取、语义检索与用户画像管理，显著优于旧版接口 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 2 中提及的“Assistant API（下线中）”已明确进入下线流程，不应在新项目中采用；请优先使用 Responses API 或工作流/智能体应用的标准调用接口。

## 关键参数

以下为高频使用的可配置参数（均通过控制台或 API 设置）：

- **知识库检索参数**：`top_k`（初步向量/关键词召回数量）、`rerank_top_k`（重排序后返回数量）、`weight`（多知识库权重，范围 0–100）；降低 `top_k` 可减少送入排序模型的 [Token](../concepts/token.md) 量，直接降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **智能体应用参数**：`retrieval_config`（含“[多模态](../concepts/multimodal.md)回复增强”开关）、`system_prompt`（角色定义）、`enable_knowledge_retrieval`（知识检索增强开关）；开启多模态增强后，智能体可解析知识库中的图表与图像内容。
- **工作流异步运行**：请求中设置 `background=true` 即启用异步模式，API 立即返回 `task_id`，后续通过 `GetTaskResult` 查询结果；任务历史可在 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查看 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Embedding 模型选择**：知识库默认使用 `text-embedding-v4`（推荐），亦支持 `v3`；`v4` 在语种覆盖、代码片段向量化效果和维度灵活性上全面升级 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码快速启动（推荐入门）**：  
   按照 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 流程，5 分钟内完成智能体创建 → 知识库上传与构建 → 关联发布。该流程完全基于控制台图形界面，无需编码，适用于 PoC 或业务部门快速验证。

2. **API 集成调用**：  
   - 同步调用：复用 OpenAI 兼容 SDK，请求 `POST /v1/chat/completions`，传入 `app_id` 和 `messages`；适用于实时交互场景。  
   - 异步调用：在同步请求中添加 `background=true`，获取 `task_id` 后轮询 `GET /v1/tasks/{task_id}` 获取结果。  
   - 知识库管理：使用 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现自动化运维 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高代码扩展**：  
   对于需深度定制逻辑的场景，可选用“高代码应用”类型，基于 Python 项目结构部署，内置可观测性、日志服务与自动化运维能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费生效时间**：知识库服务自 2026 年 1 月 4 日起正式计费，费用由规格费 + 模型调用费构成；资源包（RAG 标准版/旗舰版）可有效降低成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性限制**：QwQ 系列模型在智能体应用中**不支持[插件](../concepts/plugin.md)、流程编排、音视频交互能力**；仅限纯文本推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **权限与分账**：子账号可开通知识库并启用标签分账，但需主账号预先配置服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`）以支持应用观测 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **调试与验证**：编辑智能体时，知识库调试面板支持在线调整参数并实时验证召回效果；测试知识库页面支持图文混合输入，用于评估多模态检索能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)
- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)


