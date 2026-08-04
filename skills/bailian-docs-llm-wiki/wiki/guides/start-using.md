# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建基于大模型的智能应用。本文档聚焦“开始使用”核心流程，涵盖从创建首个智能体应用、配置知识库到发布调用的完整链路，并同步说明当前平台支持的关键能力、参数控制点及重要限制。所有操作均通过控制台可视化完成，亦可通过 API 实现自动化集成。

## 支持的模型/功能

- **基础模型**：智能体应用支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest` 等主流模型；工作流应用额外支持 DeepSeek 系列模型（如 `deepseek-chat`）[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **多模态能力**：自 2025 年 3 月起，智能体应用支持 `qwen-vl-plus-2025-01-25` 等 VL 模型，并可开启「多模态回复增强」开关以解析知识库中的图表与图像内容 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建 MySQL 表）、**图片/音视频型**（支持上传并解析视觉内容）[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级功能**：新版智能体应用（Agent 2.0）已统一将知识库、MCP 工具纳入自主规划调用流程；[长期记忆](../concepts/long-term-memory.md)（新）API 提供自动信息提取、语义检索与用户画像管理能力 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及的「千问-Max」为旧版命名，当前控制台实际显示为 `qwen-max`；且其推荐步骤中未体现 Agent 2.0 的工具自主编排机制，该能力已在 2025 年 12 月上线，应作为默认行为参考 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 关键参数

- **知识库检索**：支持调整「初步向量检索 TopK」和「初步关键词检索 TopK」以降低 [Token](../concepts/token.md) 消耗与成本 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；多知识库场景下可设置权重，控制召回优先级 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Embedding 模型**：非结构化知识库默认使用 `text-embedding-v4`（2025 年 7 月起），较 v3 在语种、代码片段向量化效果上更优；v3 仍可用但非推荐 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试与观测**：编辑智能体应用时，可直接使用内置「调试面板」实时验证知识库检索效果；应用发布后，可通过「应用观测」端到端追踪请求处理链路 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建智能体应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→「立即创建」；设置应用名、选择模型（如 `qwen-max`）、配置 System Prompt（角色定义）及欢迎语/预设问题 [原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **构建知识库**：  
   - *文档型*：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，点击「创建知识库」→ 选择「文档」类型 → 直接上传文件（支持 DOCX/PDF/HTML/Excel 等），无需预先创建连接器（2025 年 9 月起流程简化）[原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
   - *数据型*：选择「数据」类型，直连 RDS/DMS 或自建 MySQL 表；  
   - *音视频型*：选择「文档」或「图片」类型后上传音视频文件，系统自动转录与向量化 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
3. **关联与发布**：在应用配置页 →「技能」→「知识库」→「+」添加已建知识库；确认无误后点击「发布」。发布后即可通过控制台测试或调用 API 使用。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包两种模式 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型（如 `qwq-plus`）在智能体应用中**不支持插件、流程编排及音视频交互能力**，仅适用于纯文本推理场景 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件限制**：单次上传文档大小上限为 100 MB；音视频文件需 ≤ 2 GB，且仅支持 MP4/MOV/AVI/WAV/MP3 格式；OCR 与 VL 解析依赖 `qwen-vl-plus` 等专用模型，不可混用通用文本模型 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权限要求**：子账号开通知识库需主账号授权「SFMFullAccess」或「SFMReadOnlyAccess」策略，并启用分账标签以实现费用归属管理 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


