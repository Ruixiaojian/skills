# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建、测试并发布智能体应用、工作流应用及高代码应用。核心流程围绕模型选择、Prompt 设计、知识库集成与发布部署展开，适用于私有知识问答、多模态交互、自动化业务流程等场景。所有操作均可通过控制台完成，同时提供完整 API 支持。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：支持千问系列（如 `qwen-max`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、DeepSeek 系列及 Qwen-VL 多模态模型（如 `qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25`），具备自动工具规划能力，统一调用知识库、MCP 和[长期记忆](../concepts/long-term-memory.md) [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **知识库类型**：支持三类结构化分类——**文档**（PDF/DOCX/HTML/Excel）、**数据**（RDS、DMS、自建 MySQL）、**图片/音视频**（支持上传 MP4、MP3、JPG/PNG 及自动语音转写与视觉解析）；非结构化知识库新增图文检索、自定义 metadata 和标签分类能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **高级能力**：  
  - 多模态回复增强（需开启开关，依赖 `qwen-vl-plus` 等模型）；  
  - [长期记忆](../concepts/long-term-memory.md) 2.0（API 驱动、语义检索优化、自动画像提取）；  
  - MCP 市场集成（预置与自定义服务一键接入）；  
  - 工作流应用支持异步运行模式、批量节点、多模态生成节点及 Dify 一键导入。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 显示截至 2026 年 2 月，`qwen-max` 已非最新主力推荐型号；实际应优先选用 `qwen-plus` 或 `qwen-turbo`（见[模型上下架与更新](https://help.aliyun.com/zh/model-studio/newly-released-models)），且 `qwen-max` 在部分区域已下线。请以控制台模型广场实时列表为准。

## 关键参数

- **知识库检索配置**：  
  - `初步向量检索 TopK` 与 `初步关键词检索 TopK`：可调低以减少排序模型 [Token](../concepts/token.md) 消耗，直接降低成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - 多知识库权重设置：当应用关联多个知识库时，按信息源重要性分配权重，影响召回优先级；  
  - 检索模式：文件问答支持全文引用、切片检索、自定义处理三种模式。
- **智能体 Prompt 控制**：  
  - System Prompt 定义角色与任务边界（如“你是一位阿里云百炼手机导购…”）；  
  - 支持 FewShot Prompt 样例库，通过 Query-Answer 对提升回答准确性；  
  - 欢迎语与预设问题用于引导用户交互起点。
- **[长期记忆](../concepts/long-term-memory.md)与用户画像**：新版 API 支持自动关键信息提取、去重及语义检索，无需手动维护记忆条目。

## 使用方式

1. **零代码构建（推荐入门）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 配置 Prompt / 欢迎语 / 预设问题；  
   - 进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 创建标准版知识库 → 直接上传文件或同步数据库（免经[数据连接](../concepts/data-connection.md)器步骤，见文档 2 2025 年 9 月优化）；  
   - 返回应用配置页 → 在「技能 > 知识库」中添加已建知识库 → 启用「知识检索增强」→ 发布应用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用**：  
   - 同步调用：使用 `Responses API`，兼容 OpenAI SDK，适用于实时对话；  
   - 异步调用：设置 `background=true`，返回 Task ID，适用于长耗时任务（如音视频处理、批量推理）；  
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现全生命周期控制。

3. **调试与验证**：  
   - 编辑智能体应用时，可使用内置「调试面板」实时调整知识库参数并验证召回效果；  
   - 应用观测（App Observe）提供端到端链路追踪，定位延迟瓶颈与失败节点。

## 限制和注意事项

- **计费变更**：知识库自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包（标准版/旗舰版）两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程编排及音视频交互能力**（仅限纯文本推理）；而工作流应用中可完整使用 `qwq-plus`、`qwq-32b`。
- **文件限制**：单次上传文档大小上限为 100 MB；音视频文件需 ≤ 2 GB，且时长建议 ≤ 2 小时以保障解析稳定性。
- **权限管控**：子账号可开通知识库并启用分账管理（通过标签标记业务空间），但需主账号授予 `AliyunServiceRoleForSFMTelemetry` 等必要服务关联角色。
- **Deprecated 功能**：`Assistant API` 已标注为“下线中”，新项目请勿采用；智能体编排应用已下线，其能力由新版工作流应用承接。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


