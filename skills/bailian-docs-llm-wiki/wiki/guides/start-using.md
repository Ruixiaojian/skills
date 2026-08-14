# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建基于大语言模型的智能体应用、工作流应用及高代码应用。本文档聚焦“开始使用”核心流程，涵盖模型选择、功能配置、参数调用及关键限制，适用于首次接入的开发者。所有操作均需通过百炼控制台（`bailian.console.aliyun.com`）或 API 完成。

## 支持的模型/功能

- **智能体应用**：支持 Qwen 系列（如 `qwen-max`、`qwen-vl-plus-latest`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、DeepSeek 系列模型；支持知识库、[长期记忆](../concepts/long-term-memory.md)（新）、MCP 工具、多模态回复增强（需开启）等能力。  
- **工作流应用**：支持 QwQ、DeepSeek、Qwen-VL 等模型；提供多模态生成节点、批量节点、异步运行模式、Dify 一键导入等功能。  
- **知识库类型**：分为**文档**、**数据**、**图片**三类（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)），支持非结构化（PDF/DOCX/HTML/Excel/音视频）与结构化（RDS/DMS/自建 MySQL）数据源；音视频知识库自 2025 年 12 月起正式支持（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。  
- **高代码应用**：2025 年 9 月上线，支持 Python 项目部署，内置运维、可观测性与日志服务（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。

> **注意**：文档 1 中推荐使用“千问-Max”作为入门模型，但该模型名称已过时；当前控制台实际可选模型为 `qwen-max` 或 `qwen-plus`，请以[模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)为准。

## 关键参数

- **知识库检索参数**：可在智能体应用“检索配置”中调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低 [Token](../concepts/token.md) 消耗与成本（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。  
- **权重设置**：当智能体关联多个知识库时，可为各知识库设置权重，系统优先召回高权重知识源（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)（2.0）支持自动信息提取、语义检索与用户画像管理，API 接口兼容多应用共享（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。  
- **调用参数**：同步调用需传入 `input` 字段；异步调用需设置 `background=true` 并通过 Task ID 查询结果（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。

## 使用方式

1. **零代码构建智能体应用**（约 1 分钟）：  
   - 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击**创建应用** → **智能体应用** → **立即创建**；  
   - 选择模型（如 `qwen-max`），配置 System Prompt（角色定义）、欢迎语与预设问题；  
   - 发布前需完成知识库绑定（见下步）。

2. **构建知识库**（约 3 分钟）：  
   - 方式一（简化流程）：在创建知识库时直接上传文件（支持 DOCX/PDF/HTML/Excel/音视频），选择“智能切分”；  
   - 方式二（结构化）：从 RDS/DMS/自建 MySQL 同步表数据；  
   - 创建后等待解析完成（通常 1–2 分钟）。

3. **关联与发布**：  
   - 在应用配置页 → **技能** → **知识库** → **+ 添加知识库**；  
   - 点击**发布**生效。测试时右侧提问即可验证知识增强效果。

4. **API 调用**：  
   - 同步调用：使用 `Responses API`，兼容 OpenAI SDK；  
   - 异步调用：设置 `background=true`，通过 `/tasks/{task_id}` 查询结果；  
   - 知识库管理：支持 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式（[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)）。  
- **模型能力边界**：QwQ 系列模型暂不支持[插件](../concepts/plugin.md)、流程编排与音视频交互能力（仅限文本推理）；Qwen-VL 系列需显式启用“多模态回复增强”开关方可解析图表内容。  
- **调试与监控**：智能体编辑页内置知识库调试面板，可实时验证检索召回效果；应用观测功能支持端到端流程追踪（需开通 `AliyunServiceRoleForSFMTelemetry` 角色）。  
- **权限与分账**：知识库支持子账号开通与标签分账，适用于多部门/项目成本归集。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


