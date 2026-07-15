# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，支持零代码快速搭建私有知识问答应用，也兼容全代码集成场景。开发者可通过控制台可视化配置或 API 调用两种方式启动应用开发，核心路径包括模型选择、Prompt 设计、知识库接入与发布部署。本文档聚焦“开始使用”阶段的关键技术要素，面向实际开发需求提炼结构化指引。

## 支持的模型/功能

- **基础模型**：智能体应用默认支持 `qwen-max`（文档推荐为“千问-Max”），同时已全面支持 `qwq-plus`、`qwq-32b`（工作流应用）、`qwen-vl-plus-latest` 及 `qwen-vl-plus-2025-01-25` 等多模态与推理增强模型 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **知识库类型**：支持文档型（.docx/.pdf/.xlsx/.html 等）、音视频型（MP4/Audio/WAV）、图片型及结构化数据型（RDS/DMS/自建 MySQL）知识库 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **增强能力**：  
  - 多模态回复增强（需在智能体应用检索配置中开启）；  
  - [长期记忆](../concepts/long-term-memory.md)（新版 API 支持自动信息提取与用户画像管理）；  
  - MCP 工具集成（含预置服务与自定义 MCP）；  
  - 文件问答支持全文引用、切片检索、自定义处理三种模式。

> **注意**：文档 1 中提及“建议选择千问-Max”，但文档 2 明确指出智能体应用已支持 `qwq` 系列及 `qwen-vl-plus` 等新模型，且 `qwq` 模型具备更强的数学/代码推理能力。实际开发中应优先参考 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的最新模型支持列表，而非文档 1 的示例性建议。

## 关键参数

- **知识库检索参数**：  
  - `初步向量检索TopK` 与 `初步关键词检索TopK`：可调低以减少送入排序模型的 [Token](../concepts/token.md) 量，直接降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - 知识库权重：当应用关联多个知识库时，可按信息源重要性设置权重，系统优先召回高权重知识库内容；  
  - 切分策略：推荐使用“智能切分”，经评测对多数文档效果最优 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md) API 支持自动去重、语义检索及用户画像字段自定义，无需手动维护记忆条目。  
- **调用参数**：  
  - 同步调用（`Responses API`）适用于实时交互；  
  - 异步调用需设置 `background=true`，返回 Task ID 后通过任务中心查询结果。

## 使用方式

1. **零代码快速启动**（适用于原型验证与业务试用）：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用；  
   - 配置 System Prompt（如“你是一位阿里云百炼手机导购…”）；  
   - 上传知识文档 → 创建知识库 → 在应用技能中绑定知识库；  
   - 发布前可使用右侧调试面板实时验证检索召回效果 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  

2. **API 集成开发**（适用于生产环境与定制化需求）：  
   - 调用 `CreateIndex` API 创建音视频/结构化知识库；  
   - 使用 `GetIndexMonitor` 和 `UpdateIndex` 管理知识库状态与配置；  
   - 通过 `Responses API`（同步/异步）调用已发布应用，兼容 OpenAI SDK 接口风格 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用由规格费 + 模型调用费构成；支持后付费与资源包两种模式，资源包需通过控制台单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：`QwQ` 系列模型在智能体应用中**不支持[插件](../concepts/plugin.md)、流程、音视频交互能力**，仅限纯文本推理场景；而工作流应用则完整支持其多节点编排能力。  
- **知识库时效性**：非结构化知识库导入 Excel 文档时，若原始文件含复杂公式或宏，可能无法完全解析；结构化知识库从 RDS 同步数据时，需确保数据库账号具备 `SELECT` 权限。  
- **调试依赖**：知识库调试面板仅在编辑智能体应用时可用，工作流应用需通过任务中心查看节点执行日志。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


