# start using

阿里云百炼平台提供低代码/零代码与高代码双路径，支持开发者快速构建基于大模型的智能应用。本文档面向开发者，聚焦“开始使用”阶段的核心操作路径、能力边界与关键配置项，涵盖模型选择、功能启用、参数调用及计费约束等实操要点。所有操作均基于控制台界面或标准 API 接口，不依赖特定 SDK 或前端框架。

## 支持的模型/功能

- **基础模型**：智能体应用默认支持 `qwen-max`（推荐）、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest` 等系列模型；工作流应用额外支持 DeepSeek 系列模型（如 `deepseek-chat`）[原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **多模态能力**：自 2025 年 3 月起，智能体应用支持 `qwen-vl-plus-2025-01-25`（即 Qwen2.5-VL），上下文扩展至 128k，显著增强图像/视频理解能力；知识库支持导入音视频文件并实现内容检索与问答 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建 MySQL）、**图片型**（含图文联合检索）；非结构化知识库支持自定义 metadata 与标签分类 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级功能**：新版智能体应用（Agent 2.0）统一将知识库、MCP 服务作为可自主规划调用的工具；[长期记忆](../concepts/memory.md)（新）提供语义检索、自动信息提取与用户画像管理能力 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及的“千问-Max”为旧版命名，当前控制台已统一为 `qwen-max`；且文档 1 未说明 `qwq` 系列模型在智能体应用中**不支持[插件](../concepts/plugin.md)与音视频交互能力**（见文档 2 2025 年 4 月条目），该限制需明确遵循。

## 关键参数

- **知识库检索参数**：可通过调试面板或 API 调整 `top_k`（初步向量/关键词召回数），降低该值可减少送入排序模型的 [Token](../concepts/token.md) 量，从而直接降低模型调用费用 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权重配置**：当智能体应用关联多个知识库时，支持按信息源重要性设置权重，系统优先召回高权重知识库内容 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务边界，建议明确限定领域范围（如“你是一位阿里云百炼手机导购…”），避免泛化回答；同时支持 FewShot Prompt 样例库提升准确性 [原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **调用模式参数**：API 调用支持 `background=true` 启用异步模式，立即返回 Task ID；同步模式兼容 OpenAI 格式，便于生态迁移 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码路径**（适用于快速验证）：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用 → 选择模型（如 `qwen-max`）→ 设置 System Prompt → 配置欢迎语与预设问题 → 发布前绑定知识库（支持直接上传文件，无需预创建连接器）[原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
   - 知识库创建流程已简化：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面 → 选择类型（文档/数据/图片）→ 直接上传文件或配置数据源 → 选用“智能切分”策略 → 完成解析。  

2. **API 调用路径**（适用于集成部署）：  
   - 同步调用：使用 `/v1/applications/{app_id}/messages` 接口，传入 `user_message` 即可获取实时响应；  
   - 异步调用：同接口加 `background=true` 参数，后续通过 `/v1/tasks/{task_id}` 查询结果；  
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现全生命周期控制 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  

3. **高代码路径**（适用于深度定制）：  
   - 使用高代码应用类型，基于 Python 项目结构部署后端服务，内置可观测性与日志能力；  
   - 可结合 Assistant API（下线中）或新版[长期记忆](../concepts/memory.md) API 构建 RAG 流水线 [原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独开通 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型能力边界**：`qwq` 系列模型在智能体应用中**不支持[插件](../concepts/plugin.md)、流程编排及音视频交互能力**，仅适用于纯文本推理场景；若需多模态交互，应选用 `qwen-vl-plus` 系列模型 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权限与分账**：子账号可独立开通知识库，支持通过标签（Tag）进行分账管理，适用于多部门/多项目成本归集 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试与观测**：所有应用均支持 [应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe) 查看端到端处理链路；知识库调试面板支持在线调整参数并实时验证召回效果 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


