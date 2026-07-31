# start using

阿里云百炼平台提供零代码与高代码两种路径，帮助开发者快速构建基于大语言模型的智能应用。本文档面向开发者，聚焦“开始使用”阶段的核心操作路径、能力边界与关键配置项，涵盖模型选择、功能启用、参数调用及计费约束等实用信息。所有操作均基于控制台 Web 界面或标准 API 接口，无需额外部署基础设施。

## 支持的模型/功能

- **基础模型**：智能体应用支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等主流模型；工作流应用额外支持 DeepSeek 系列模型（如 `deepseek-chat`）[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **多模态能力**：自 2025 年 3 月起，智能体应用支持开启“多模态回复增强”开关，解析知识库中的图表与图像内容；知识库本身支持上传音视频、图片、Excel、HTML 等非结构化文件，并可选用 `qwen-vl-max` 或 `qwen-vl-plus` 进行视觉解析 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：按场景划分为**文档型**（PDF/DOCX/HTML）、**数据型**（RDS/DMS/MySQL 表）、**图片型**三类；结构化知识库支持图文检索，非结构化知识库支持自定义 metadata 与标签分类 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级能力**：[长期记忆](../concepts/long-term-memory.md)（新）API 提供自动信息提取、语义检索与用户画像管理；MCP 市场支持预置及自定义服务接入；工作流应用支持异步运行模式与批量节点。

> **注意**：文档 1 中推荐使用“千问-Max”作为入门模型，但该名称已过时——当前控制台中对应模型标识为 `qwen-max`，且 `qwen-max` 已被 `qwen-plus` 等新版本逐步替代。实际建模请以 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 实时列表为准。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量，从而优化成本 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库权重**：当智能体应用关联多个知识库时，可为每个知识库设置权重值（0–100），系统优先召回高权重知识源 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务边界，建议明确限定领域范围（如“你是一位阿里云百炼手机导购…”），避免泛化回答；同时支持 FewShot Prompt 样例库提升准确性 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md) API 支持 `auto_extract=true` 自动提取对话关键信息，并通过 `user_id` + `session_id` 组合实现跨会话用户画像聚合。

## 使用方式

1. **零代码快速启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击“创建应用” → 选择“智能体应用” → 设置模型、Prompt、欢迎语与预设问题 → 发布即用。  
2. **知识库集成**：在应用配置页 > “技能” > “知识库”中点击 `+` 添加已创建的知识库；支持直接上传文件创建知识库（无需预先在数据连接页导入）[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
3. **API 调用**：  
   - 同步调用：使用 `Responses API`，兼容 OpenAI SDK，适用于实时交互场景；  
   - 异步调用：设置 `background=true`，返回 `task_id`，后续通过 `/tasks/{task_id}` 查询结果；  
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现全生命周期控制 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
4. **调试验证**：编辑智能体应用时，可直接打开知识库调试面板，实时调整检索参数并验证召回效果 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需通过 [RAG标准版](https://common-buy.aliyun.com/?commodityCode=sfm_ragservicestandard_dp_cn) 或 [RAG旗舰版](https://common-buy.aliyun.com/?commodityCode=sfm_ragserviceenterprise_dp_cn) 单独开通 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型能力边界**：QwQ 系列模型虽具备强推理能力，但**不支持插件、流程编排与音视频交互能力**；qwen-vl 系列仅支持图像/视频理解，不可用于纯文本生成任务。  
- **权限与分账**：知识库支持子账号开通与标签分账，但需主账号提前配置 RAM 权限策略及分账标签；未配置标签的资源将计入主账号账单。  
- **兼容性说明**：`Assistant API` 已标记为“下线中”，新项目请统一使用 `Responses API` 或工作流/智能体应用 API；旧版长期记忆 API（`/v1/long-term-memory`）已停用，必须迁移至新版 `/v2/long-term-memory`。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


