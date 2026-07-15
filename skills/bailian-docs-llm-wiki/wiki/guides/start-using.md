# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，支持零代码快速搭建私有知识问答应用，也支持高代码深度定制。开发者可通过控制台可视化配置或 API 编程方式接入模型、知识库、[长期记忆](../concepts/long-term-memory.md)等核心能力，适用于从原型验证到生产部署的全周期场景。本文档聚焦“开始使用”路径，梳理关键能力、参数与约束，帮助开发者高效启动。

## 支持的模型/功能

- **基础模型**：智能体应用和工作流应用均支持千问系列（如 `qwen-max`）、QwQ 系列（如 `qwq-plus`、`qwq-32b`）及 DeepSeek 系列模型；其中 QwQ 模型具备强推理能力，输出含显式思考链 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **[多模态能力](../concepts/multi-modal.md)**：`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等视觉语言模型支持图文理解与生成；知识库支持导入图片、音视频文件，并启用“多模态回复增强”开关以解析图表内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：分为**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建 MySQL）、**图片型**三类；非结构化知识库支持离线 HTML、Excel 及自定义 metadata，结构化知识库支持图文检索与音视频解析 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级能力**：[长期记忆](../concepts/long-term-memory.md)（新）API 支持多应用共享、自动信息提取与语义检索；MCP 服务可作为插件集成至智能体或工作流；工作流应用支持异步运行模式与批量节点。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不应再用于新项目开发；当前推荐路径为智能体应用（Agent 2.0）或工作流应用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- **知识库检索参数**：`初步向量检索TopK` 和 `初步关键词检索TopK` 可调低以减少送入排序模型的 Token 量，直接降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库权重**：当智能体应用关联多个知识库时，可为每个知识库设置权重，系统优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务（如“你是一位阿里云百炼手机导购…”），直接影响模型行为边界；支持 FewShot Prompt 样例库提升回答准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版长期记忆支持自动提取对话关键信息、用户画像标签管理，无需手动构造记忆条目。

## 使用方式

1. **零代码入门**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型（推荐 `qwen-max`）→ 设置 System Prompt 与欢迎语 → 添加知识库（支持直接上传文件，无需预创建连接器）→ 发布 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 调用**：  
   - 同步调用：使用 Responses API，兼容 OpenAI SDK，适用于实时交互场景；  
   - 异步调用：设置 `background=true`，返回 Task ID，通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果；  
   - 知识库/长期记忆/工作流节点均提供独立 RESTful API（如 `CreateIndex`、`GetIndexMonitor`、`UpdateIndex`）。  
3. **调试与观测**：编辑智能体应用时可使用内置**知识库调试面板**实时验证检索效果；应用发布后可通过 [应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe) 查看端到端处理链路与性能指标。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需通过控制台单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**，仅适用于纯文本推理场景；DeepSeek 系列模型仅支持工作流与智能体应用，不支持旧版智能体编排应用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权限与分账**：知识库支持子账号开通与标签分账，但需提前配置服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`）以启用应用观测功能 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件限制**：单次上传文档大小上限为 100 MB；音视频文件需符合格式规范（MP4/MOV/AVI/WAV/MP3），且解析依赖 `qwen-vl` 系列模型。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


