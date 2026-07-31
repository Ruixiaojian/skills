# start using

阿里云百炼平台提供零代码与高代码两种路径，帮助开发者快速构建具备私有知识问答、[多模态](../concepts/multi-modal.md)理解、工作流编排等能力的 AI 应用。本文档面向开发者，聚焦“开始使用”阶段的核心操作与关键约束，涵盖模型支持、参数配置、接入方式及已知限制，所有内容均基于当前控制台与 API 的实际行为整理。

## 支持的模型/功能

- **基础模型**：智能体应用默认支持 `qwen-max`（推荐）、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest` 等系列模型；工作流应用额外支持 DeepSeek 系列模型（如 `deepseek-chat`）[原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **[多模态](../concepts/multi-modal.md)能力**：`qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 支持 128k 上下文及增强型图文/视频理解；非结构化知识库支持导入 PDF、DOCX、Excel、HTML、音视频文件，并可选 `qwen-vl-max` 或 `qwen-vl-plus` 进行图像解析 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：分为**文档型**（非结构化）、**数据型**（结构化，支持 RDS/DMS/自建 MySQL 同步）和**图片型**三类；自 2025 年 9 月起创建流程已按此分类简化 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级功能**：新版智能体应用（Agent 2.0）统一将知识库、MCP 作为工具由模型自主规划调用；[长期记忆](../concepts/long-term-memory.md)（新）提供语义检索、自动信息提取与用户画像管理能力。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不应在新项目中采用；当前标准调用方式为 [Responses API](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)，支持同步与异步模式 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 关键参数

- **知识库检索**：可通过“调试面板”在线调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以控制成本；多知识库场景下支持按权重分配召回优先级。  
- **Prompt 配置**：System Prompt 定义角色与任务（如“你是一位阿里云百炼手机导购…”），建议明确限定回答范围与输出格式；支持 FewShot Prompt 样例库提升准确性。  
- **模型切换策略**：智能体应用在主模型表现受限时会自动降级或切换至更优模型（如 QwQ 系列用于复杂推理），但该行为不可显式配置。  
- **音视频处理**：启用“[多模态](../concepts/multi-modal.md)回复增强”开关后，智能体可解析知识库中的图表与图像内容，结合视觉信息生成回答。

## 使用方式

1. **零代码快速启动**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型（如 `qwen-max`）→ 设置 System Prompt 与欢迎语 → 发布前绑定知识库。  
   - 知识库创建路径：[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 创建 → 上传文件（支持 DOCX/Excel/HTML/音视频）→ 选择“智能切分” → 完成。  

2. **API 集成**：  
   - 同步调用：使用 `/v1/applications/{app_id}/responses` 接口，兼容 OpenAI SDK；  
   - 异步调用：设置 `background=true`，获取 `task_id` 后通过 `/v1/tasks/{task_id}` 查询结果；  
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现程序化创建与监控 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  

3. **高级能力启用**：  
   - [长期记忆](../concepts/long-term-memory.md)：调用新版 `LongTermMemory` API，支持跨应用共享记忆库；  
   - MCP 集成：在 [MCP 市场](https://bailian.console.aliyun.com/#/mcp-market) 开通服务后，在智能体或工作流中直接引用。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独购买 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权限约束**：子账号可开通知识库并启用分账管理（通过标签标记业务空间），但需主账号授予 `AliyunServiceRoleForSFMAccessingMNS` 等服务关联角色。  
- **文件限制**：单次上传非结构化文档最大 100 MB；音视频文件需先转码为 MP4/MP3 格式，且总时长不超过 2 小时。  
- **模型兼容性**：QwQ 系列模型暂不支持插件、音视频交互及流程节点；DeepSeek 模型仅限工作流与智能体应用，不可用于高代码应用部署。  
- **调试依赖**：知识库“调试面板”仅在编辑智能体应用时可用，无法在工作流或高代码应用中实时验证召回效果。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


