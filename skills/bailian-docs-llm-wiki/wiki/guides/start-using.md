# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，支持开发者通过零代码配置或 API 集成快速启动智能体、工作流及高代码应用。核心路径包括模型选择、Prompt 设计、知识库接入与发布部署，适用于私有知识问答、[多模态](../concepts/multimodal.md)交互、自动化业务流程等场景。所有能力均基于统一控制台与标准化 API，兼顾易用性与工程可控性。

## 支持的模型/功能

- **基础模型**：支持千问系列（Qwen-Max、Qwen-VL-Plus 等）、QwQ 系列（qwq-plus、qwq-32b）、DeepSeek 系列（DeepSeek-V2、DeepSeek-Coder）及 text-embedding-v4/v3 等向量模型。其中 QwQ 系列模型具备深度推理能力，输出含显式思考链；Qwen-VL 系列支持图文联合理解 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **应用类型**：覆盖三类主流形态：
  - **智能体应用（Agent 2.0）**：支持知识库、MCP 工具统一调度，可展示完整规划与调用过程；
  - **工作流应用**：支持[多模态](../concepts/multimodal.md)生成节点、批量节点、异步运行模式及 Dify 一键导入；
  - **高代码应用**：基于 Python 项目结构部署，内置运维、可观测性与日志能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库能力**：支持文档、数据、图片三类知识库；非结构化知识库兼容 DOCX、PDF、Excel、HTML、音视频文件；结构化知识库支持 RDS、DMS、自建 MySQL 数据源；新增图文检索、[多模态](../concepts/multimodal.md)回复增强、权重设置等功能 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 明确指出智能体应用已支持 QwQ、DeepSeek 及 Qwen-VL 系列模型，且 QwQ 在数学/代码任务上显著优于同源精简版。因此“仅推荐千问-Max”属过时建议，实际应按任务需求选型。

## 关键参数

- **知识库检索配置**：可在智能体应用中启用“知识检索增强”，并调整“初步向量检索 TopK”和“初步关键词检索 TopK”以平衡效果与成本（降低数值可减少 [Token](../concepts/token.md) 消耗）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md)（Long-term Memory 2.0）支持自动信息提取、语义检索与用户画像管理，API 响应延迟更低、召回更准。
- **权重设置**：当一个智能体关联多个知识库时，可通过权重参数控制各知识库的召回优先级。
- **多模态增强开关**：在智能体应用的“检索配置”中开启后，系统将调用 Qwen-VL 模型解析知识库中的图表与图像内容，实现视觉信息融合回答。

## 使用方式

1. **零代码快速启动**（适用于原型验证）：
   - 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用；
   - 设置 System Prompt（如：“你是一位阿里云百炼手机导购…”）；
   - 配置欢迎语与预设问题；
   - 上传文档构建知识库（支持直接导入，无需预先创建连接器）；
   - 在应用配置中添加知识库并发布 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 集成调用**（适用于生产集成）：
   - 同步调用：使用 Responses API（兼容 OpenAI 格式），适用于实时交互场景；
   - 异步调用：设置 `background=true`，返回 Task ID 后轮询结果；
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现全生命周期控制 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高级定制开发**：
   - 使用 MCP SDK 接入自定义工具；
   - 基于高代码应用模板部署 Python 后端服务；
   - 利用 Prompt 样例库（FewShot）提升特定场景回答准确性。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用由规格费 + 模型调用费构成；支持后付费与资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列虽支持深度推理，但文档 1 明确标注其“不包括插件、流程、音视频交互能力”，即无法在智能体中调用外部工具或处理音视频输入。
- **调试与观测**：知识库调试面板支持在线调整参数并实时验证召回效果；应用观测功能提供端到端链路追踪，需开通 `AliyunServiceRoleForSFMTelemetry` 角色。
- **权限与分账**：知识库支持子账号开通与标签分账，适用于多部门/项目成本隔离场景。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


