# start using

阿里云百炼平台提供零代码与高代码双路径的模型应用构建能力，开发者可快速创建智能体、工作流或高代码应用，并通过知识库、[长期记忆](../concepts/long-term-memory.md)、MCP 等能力扩展大模型在私有场景下的表现。本文档聚焦“开始使用”核心路径，涵盖模型选择、功能配置、调用方式及关键约束，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型**：支持千问系列（如 `qwen-max`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、Qwen-VL 多模态模型（`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25`）及 DeepSeek 系列模型（[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 和 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) 均已支持）。  
- **核心功能模块**：
  - **知识库**：支持文档、音视频、图片、结构化数据（MySQL、RDS、DMS）等多种数据源；支持智能切分、图文检索、多模态回复增强、权重设置（多知识库优先级控制）；自 2026 年 1 月 4 日起正式商业化计费 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
  - **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md)（Long-Term Memory 2.0）提供 API 接入、自动信息提取、语义检索与用户画像管理能力，显著优于旧版 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
  - **MCP（Model Calling Protocol）**：支持预置 MCP 服务调用及自定义 MCP 部署，可用于扩展工具能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
  - **文件问答**：支持全文引用、切片检索、自定义处理三种模式，覆盖文档、图片、音视频等格式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 明确指出智能体应用已支持 QwQ、DeepSeek 及 Qwen-VL 系列等更多模型，且部分模型具备更强推理或视觉理解能力。实际选型应依据任务类型（如数学推理选 QwQ，图文理解选 Qwen-VL），而非仅限千问-Max。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 Token 量以控制成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 设计**：System Prompt 定义角色与任务边界（如“你是一位阿里云百炼手机导购…”），直接影响回答一致性与领域适配性；支持 FewShot Prompt 样例库提升准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多知识库权重**：当应用关联多个知识库时，可为每个知识库设置权重值，系统按权重优先召回相关内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **长期记忆配置**：新版长期记忆支持自动提取对话关键信息、去重及语义检索，无需手动维护记忆条目 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码快速启动（推荐入门）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→「立即创建」；  
   - 选择模型、配置 System Prompt、设置欢迎语与预设问题；  
   - 通过 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 上传文档（如 `.docx`），再进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建并关联至应用；  
   - 最后发布应用并测试。详细步骤见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用**：  
   - 同步调用：使用 Responses API（兼容 OpenAI 格式），适用于实时交互场景；  
   - 异步调用：设置 `background=true` 返回 Task ID，适用于长耗时任务（如音视频处理、批量节点执行）；  
   - 知识库/长期记忆/工作流等均提供独立 API（如 `CreateIndex`、`GetIndexMonitor`、`UpdateIndex`），详见各功能模块文档 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高代码开发**：  
   - 支持基于 Python 项目结构部署 AI 后端服务，内置运维、可观测性与日志能力，适用于需深度定制逻辑的场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **知识库计费变更**：自 2026 年 1 月 4 日起，知识库服务按规格费 + 模型调用费计费，不再提供免费额度；支持后付费与资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列模型虽推理能力强，但明确不支持插件、流程编排及音视频交互能力；Qwen-VL 模型需配合“多模态回复增强”开关启用图像理解 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **调试与验证**：编辑智能体应用时，可使用内置「调试面板」在线调整知识库参数并实时验证检索效果，避免发布后才发现召回偏差 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **数据源兼容性**：非结构化知识库支持 Excel、HTML、PDF、DOCX 等格式；结构化知识库支持 RDS、DMS、自建 MySQL；音视频知识库需通过专用 API 创建 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


