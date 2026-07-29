# start using

阿里云百炼平台提供低代码/零代码构建智能体应用的能力，开发者可快速创建具备私有知识问答、多模态理解、工作流编排等能力的 AI 应用。本文档面向开发者，聚焦“开始使用”阶段的核心路径与关键约束，涵盖模型支持、参数配置、接入方式及已知限制，不包含营销性描述。所有操作均基于控制台 Web 界面或标准 API 接口，适用于生产环境快速验证与迭代。

## 支持的模型/功能

- **基础模型**：智能体应用支持 `qwen-max`（推荐入门）、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 及 DeepSeek 系列模型；工作流应用额外支持 `text-embedding-v4` 作为向量模型（优于 v3），并支持 `qwen-vl-max`/`qwen-vl-plus` 解析图片内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel 等非结构化文本）、**数据型**（RDS、DMS、自建 MySQL 同步的结构化表）、**图片型**（含图文检索与图表识别能力）；自 2025 年 9 月起，创建流程已按此分类简化 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **增强能力**：  
  - 智能体应用支持「多模态回复增强」开关（启用后可解析知识库中图表并结合视觉信息作答）；  
  - 新版智能体应用（Agent 2.0）将知识库、MCP 统一为工具，由模型自主规划调用时序与逻辑 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - 文件问答支持全文引用、切片检索、自定义处理三种模式，覆盖文档/图片/音视频 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但该名称已过时；当前控制台显示为 `qwen-max`，且 `qwen-plus`、`qwq` 系列等更优模型已全面可用。请以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中的模型列表为准，避免依赖旧命名。

## 关键参数

- **知识库检索参数**：  
  - `初步向量检索TopK` 与 `初步关键词检索TopK` 可手动下调，用于减少送入排序模型的 [Token](../concepts/token.md) 量，直接降低模型调用费用（自 2026 年 1 月 6 日起生效）；  
  - 多知识库场景下支持按源设置权重，系统优先召回高权重知识库内容（2025 年 4 月上线）；  
  - 调试面板支持在线调整参数并实时验证召回效果（2025 年 9 月新增）。
- **Prompt 配置**：System Prompt 定义角色与任务边界，需明确指令（如“你是一位阿里云百炼手机导购…”），避免模糊表述；欢迎语与预设问题用于引导用户交互，不影响核心推理逻辑。
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)（2026 年 1 月上线）支持自动提取对话关键信息、语义检索、用户画像管理，API 接口开放且支持多应用共享同一记忆库。

## 使用方式

1. **零代码构建（推荐快速验证）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用 → 选择模型 → 设置 System Prompt → 配置欢迎语与预设问题；  
   - 进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，创建知识库（可直传文件，无需预先导入至数据连接器）→ 选择“智能切分”策略 → 关联至应用；  
   - 在应用配置页 > 技能 > 知识库，点击 `+` 添加已创建的知识库，发布后即可测试 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用（生产集成）**：  
   - 同步调用：使用 `Responses API`，兼容 OpenAI SDK，适用于实时交互场景；  
   - 异步调用：设置 `background=true`，立即返回 Task ID，后续通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果；  
   - 知识库管理：支持 `CreateIndex`（含音视频）、`UpdateIndex`、`GetIndexMonitor` 等标准 API（2026 年 1 月起全面可用）。

3. **高代码扩展**：  
   - 高代码应用支持 Python 项目部署，内置运维、可观测性与日志服务；  
   - 工作流应用支持 Dify 一键导入、批量节点、异步运行模式（2025 年 12 月 & 2026 年 1 月上线）。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包两种模式，资源包需单独购买 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列模型虽在数学/代码任务上表现优异，但**不支持插件、流程编排及音视频交互能力**（仅限纯文本推理）；qwen-vl 系列模型支持图文理解，但需显式开启「多模态回复增强」开关。
- **权限与安全**：子账号可开通知识库并启用分账管理（通过标签标记业务空间），但需主账号授予 `AliyunServiceRoleForSFMTelemetry` 等服务关联角色以启用观测能力。
- **兼容性提示**：`Assistant API` 已标注“下线中”，新项目请勿采用；所有新功能（如 Agent 2.0、[长期记忆](../concepts/long-term-memory.md) 2.0、音视频知识库）均通过标准 REST API 或控制台提供，无历史接口强依赖。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


