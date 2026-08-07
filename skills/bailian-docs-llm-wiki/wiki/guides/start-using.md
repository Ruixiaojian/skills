# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，支持零代码快速搭建私有知识问答应用，也兼容全代码集成与深度定制。本文档面向开发者，聚焦“开始使用”的核心路径：从创建第一个应用到配置关键能力，涵盖模型选择、参数控制、调用方式及重要限制。所有操作均基于控制台或标准 API，无需额外部署基础设施。

## 支持的模型/功能

- **基础模型**：智能体应用默认支持 `qwen-max`（推荐）、`qwq-plus`、`qwq-32b` 等推理增强型模型；工作流应用额外支持 `DeepSeek` 系列模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[多模态](../concepts/multi-modal.md)能力**：`qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25`（即 `qwen-vl-plus-0125`）已上线，支持 128k 上下文及图像/视频深度理解 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建 MySQL）、**图片型**（含图文检索与 Qwen-VL 解析）；音视频知识库亦可通过 API 创建 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级功能**：新版智能体应用（Agent 2.0）统一将知识库、MCP 作为可规划工具；[长期记忆](../concepts/long-term-memory.md)（新）提供自动信息提取、语义检索与用户画像管理能力。

> **注意**：文档 1 中提及的“千问-Max”为旧称，当前控制台中对应模型标识为 `qwen-max`；且文档 1 未体现 `qwq` 系列、`DeepSeek` 及 `qwen-vl-plus` 等已上线模型，实际可用模型请以 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 实时列表为准。

## 关键参数

- **知识库检索配置**：可在智能体应用中开启“知识检索增强”，并设置：
  - `初步向量检索TopK` 与 `初步关键词检索TopK`：降低数值可减少送入排序模型的 [Token](../concepts/token.md) 量，直接降低成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
  - 多知识库权重：当关联多个知识库时，按信息源重要性分配权重，系统优先召回高权重结果；
  - “[多模态](../concepts/multi-modal.md)回复增强”开关：启用后支持解析知识库中图表与图像内容，生成结合视觉信息的回答。
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md) API 支持自动去重、语义检索及用户画像字段自定义，不依赖手动输入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 控制**：System Prompt 定义角色与任务（如“你是一位阿里云百炼手机导购…”），同时支持 FewShot Prompt 样例库提升回答准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码构建（推荐入门）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→「立即创建」；  
   - 选择模型（如 `qwen-max`）、配置 System Prompt、欢迎语与预设问题；  
   - 通过 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 上传文档，再在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面一键创建并关联至应用；  
   - 最后点击「发布」完成部署 —— 全程约 5 分钟，详见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用**：  
   - 同步调用：使用 Responses API（兼容 OpenAI 接口），适用于实时交互场景；  
   - 异步调用：设置 `background=true`，立即返回 Task ID，后续通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果；  
   - 知识库管理：支持 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等标准 API 操作 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高代码扩展**：  
   - 高代码应用支持 Python 项目结构部署，内置运维、可观测性与日志服务；  
   - 工作流应用支持 Dify 一键导入、批量节点、异步运行模式等企业级编排能力。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件处理限制**：非结构化知识库支持 DOCX/PDF/HTML/Excel/图片/音视频，但单文件大小上限为 100 MB；上传后解析耗时通常为 1–6 分钟，取决于文档复杂度与体积 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **模型能力边界**：QwQ 系列模型虽具备强推理能力，但**不支持插件、流程编排与音视频交互能力**；`qwen-vl-plus` 模型需配合图文知识库与“[多模态](../concepts/multi-modal.md)回复增强”开关方可生效 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权限与分账**：子账号可独立开通知识库，并通过标签实现分账管理，适用于多部门/多项目成本归属场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


