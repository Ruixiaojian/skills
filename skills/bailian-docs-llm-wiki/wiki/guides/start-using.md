# start using

阿里云百炼平台提供零代码与低代码能力，帮助开发者快速构建基于大模型的智能应用（如私有知识问答、工作流自动化等）。本文档聚焦“开始使用”路径，涵盖从创建首个应用、配置核心能力到生产部署的关键步骤。所有操作均通过控制台完成，也支持 API 集成。

## 支持的模型/功能

- **基础模型支持**：智能体应用和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等主流模型；DeepSeek 系列模型已在智能体与工作流中全面可用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel 等）、**数据型**（RDS、DMS、自建 MySQL）、**图片/音视频型**（支持上传并解析视觉内容）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **增强能力**：  
  - 多模态回复增强（需在智能体应用中手动开启）；  
  - [长期记忆](../concepts/long-term-memory.md)（新版 API 支持自动信息提取与用户画像管理）；  
  - MCP 工具集成（含官方预置与自定义服务）；  
  - 文件问答升级（支持全文引用、切片检索、自定义处理三种模式）。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不应作为新项目开发路径；当前推荐使用 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 或 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) 的标准 API 接口 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低 [Token](../concepts/token.md) 消耗与成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多知识库权重**：当智能体关联多个知识库时，可为每个知识库设置权重，系统优先召回高权重源的内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型切换策略**：智能体应用支持自动模型降级/升档（如主模型受限时切换至更优模型），但该行为不可显式配置，仅由平台内部策略触发 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”或“工作流应用”创建空白应用；建议首次使用 `qwen-max` 或 `qwq-plus` 作为基础模型 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
2. **配置 Prompt 与交互**：设置 System Prompt（角色定义）、欢迎语、预设问题；智能体应用支持 FewShot Prompt 样例库提升回答准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
3. **接入知识库**：
   - 文档型知识库：可直接在创建知识库流程中上传文件（无需预先走“数据连接”步骤），支持 DOCX/PDF/HTML/Excel/音视频等格式；
   - 结构化知识库：支持 RDS、DMS、自建 MySQL 同步；
   - 图文/音视频知识库：启用后支持上传图片并结合视觉内容生成回答。
4. **调试与发布**：编辑界面内置知识库调试面板，可实时验证检索召回效果；确认无误后点击“发布”即完成上线。

## 限制和注意事项

- **知识库计费生效**：自 2026 年 1 月 4 日起，知识库服务正式商业化，费用包含规格费与模型调用费两部分；免费额度仅限模型调用，不覆盖知识库资源消耗 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **音视频处理延迟**：音视频知识库导入与解析耗时显著高于文本，通常需 5–15 分钟，且依赖 `qwen-vl-plus` 等多模态模型进行内容提取 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **API 调用兼容性**：同步调用 API 兼容 OpenAI 格式，异步调用需通过 Task ID 查询结果；工作流应用新增异步运行模式，适用于长耗时任务 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **权限约束**：子账号可开通知识库并支持分账管理，但需主账号授予 `AliyunServiceRoleForSFMTelemetry` 等必要服务关联角色 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


