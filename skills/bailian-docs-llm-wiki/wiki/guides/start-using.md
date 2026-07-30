# start using

阿里云百炼平台提供零代码与低代码能力，帮助开发者快速构建基于大模型的智能应用。本文档聚焦“开始使用”路径，涵盖从创建首个智能体应用、配置知识库到发布上线的核心流程，并同步说明当前支持的功能范围、关键参数配置项、调用方式及重要限制。所有操作均可在控制台完成，无需部署后端服务。

## 支持的模型/功能

- **基础模型支持**：智能体应用支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest` 等主流模型；工作流应用额外支持 DeepSeek 系列模型（如 DeepSeek-V2、DeepSeek-Coder）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel 等）、**数据型**（RDS、DMS、自建 MySQL 表）、**图片/音视频型**（支持上传 MP4、MP3、JPG/PNG 及自动语音转写、图文解析）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **增强能力**：  
  - [多模态](../concepts/multi-modal.md)回复增强（需开启并关联含图像/音视频的知识库）；  
  - [长期记忆](../concepts/long-term-memory.md)（新 API 版本，支持多应用共享、自动信息提取与语义检索）；  
  - MCP（Model Calling Protocol）服务集成，可调用预置或自定义外部工具 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不建议新项目采用；当前推荐路径为智能体应用（Agent 2.0）或工作流应用，其能力覆盖更全、维护持续 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- **知识库检索参数**：可在智能体应用的「检索配置」中调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低召回 [Token](../concepts/token.md) 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库权重**：当一个智能体应用关联多个知识库时，支持为每个知识库设置权重值（1–10），系统按权重优先召回高相关性内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务边界，建议明确限定领域（如“你是一位阿里云百炼手机导购…”），避免泛化回答；同时支持 FewShot Prompt 样例库提升准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建智能体应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→ 设置名称、选择模型（推荐 `qwen-max` 或 `qwq-plus`）、填写 System Prompt 与欢迎语/预设问题。  
2. **构建知识库**：  
   - 文档型：直接在知识库创建页上传文件（支持 DOCX、PDF、HTML、Excel、音视频等），选择「智能切分」策略；  
   - 数据型：选择「结构化知识库」，配置 RDS/DMS/MySQL 数据源表；  
   - 图片/音视频型：上传媒体文件，系统自动执行 ASR、OCR、VL 模型解析。  
3. **绑定与发布**：进入应用配置页 → 「技能」→ 「知识库」→ 点击 `+` 添加已创建的知识库 → 确认后点击「发布」。  
4. **调用方式**：  
   - 控制台内测：右侧对话框直接提问；  
   - API 调用：支持同步（`Responses API`）与异步（`background=true` + Task ID 查询）两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
   - 外部集成：通过 H5/APP SDK、钉钉/微信机器人、MCP SDK 等渠道嵌入。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；免费额度仅限部分模型，详情见 [知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base) [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型能力边界**：QwQ 系列模型虽推理能力强，但**不支持插件、音视频交互及流程编排能力**，仅适用于纯文本深度推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试依赖**：知识库调试需使用新版「调试面板」（编辑智能体应用时可见），旧版无实时召回验证能力；若未启用该面板，建议先升级至 Agent 2.0 架构 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[文件处理](../concepts/file-processing.md)限制**：单次上传文档大小上限为 100 MB；音视频文件最长支持 2 小时，超长内容将被截断处理。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)



