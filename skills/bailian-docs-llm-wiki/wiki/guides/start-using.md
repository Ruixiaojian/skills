# start using

阿里云百炼平台提供零代码与高代码双路径快速启动能力，开发者可基于控制台或 API 快速构建、配置并发布智能体应用、工作流应用或高代码应用。核心流程包括模型选择、Prompt 设计、知识库集成及发布调用，全程支持可视化操作与程序化管理。本文档聚焦初始使用路径，涵盖关键能力边界与实操约束。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：支持千问-Max、QwQ 系列（如 `qwq-plus`、`qwq-32b`）、DeepSeek 系列、Qwen-VL 系列（含 `qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25`）等主流大模型；支持多模态回复增强、文件问答（全文引用/切片检索/自定义处理）、[长期记忆](../concepts/long-term-memory.md)（新）及 MCP 工具调用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **知识库类型**：支持文档型（PDF/DOCX/HTML/Excel）、音视频型（MP4/MOV/WAV）、图片型及结构化（MySQL/RDS/DMS 表）三类知识库；非结构化知识库支持图文混合检索与自定义 metadata [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **工作流应用**：支持多模态生成节点、批量节点、异步运行模式、Dify 工作流一键导入；大模型节点兼容 QwQ、DeepSeek 及多模态模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **高代码应用**：支持基于 Python 项目结构部署 AI 后端服务，内置运维、可观测性与日志能力（参见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中 2025 年 9 月功能）。

> **注意**：文档 1 中推荐“千问-Max”作为默认模型，但文档 2 显示 QwQ 系列与 DeepSeek 系列已全面支持智能体应用，且 QwQ 具备更强推理能力（AIME 24/25、IFEval 等指标达 DeepSeek-R1 满血版水平）。实际选型应以 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 实时状态为准，避免依赖过时推荐。

## 关键参数

- **知识库检索参数**：可通过调试面板实时调整 `初步向量检索TopK` 与 `初步关键词检索TopK`，降低送入排序模型的 Token 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当智能体应用关联多个知识库时，支持按信息源重要性设置权重，系统优先召回高权重知识库内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)配置**：新版[长期记忆](../concepts/long-term-memory.md) API 支持自动提取对话关键信息、语义检索、用户画像管理，显著提升召回准确率与响应速度 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 配置项**：System Prompt 定义角色与任务（如“阿里云百炼手机导购”），配合预设问题与欢迎语构成基础交互逻辑 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 使用方式

1. **控制台快速启动（零代码）**  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 设置 System Prompt 与预设问题 → 发布前绑定知识库（支持直接上传文件创建，无需预导入数据）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
   - 知识库创建路径：[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 创建标准版 → 选择文档/音视频/数据类目 → 启用智能切分 → 完成解析。

2. **API 调用（程序化）**  
   - 同步调用：使用 Responses API（兼容 OpenAI 格式），适用于实时交互场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
   - 异步调用：设置 `background=true` 获取 Task ID，通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
   - 知识库管理：支持 `CreateIndex`（含音视频）、`UpdateIndex`、`GetIndexMonitor` 等 API，实现全生命周期管控 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用由规格费 + 模型调用费构成；支持后付费与 RAG 资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列在智能体应用中**不支持插件、流程、音视频交互能力**（仅限纯文本推理）；而 Qwen-VL 系列需显式开启“多模态回复增强”开关才启用图像理解 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库时效性**：上传文档后需等待 1–6 分钟完成解析（非结构化）或 1–2 分钟（结构化），期间无法用于检索 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **权限与分账**：子账号可开通知识库并启用标签分账，但需主账号授权对应 RAM 权限 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


