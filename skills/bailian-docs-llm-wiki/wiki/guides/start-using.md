# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建、配置并发布智能体应用、工作流应用及高代码应用。核心流程包括模型选择、Prompt 设计、知识库集成与发布部署，适用于私有知识问答、[多模态](../concepts/multi-modal.md)生成、自动化业务流程等场景。所有操作均可通过控制台完成，同时提供完备的 API 接口供程序化调用。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：支持千问系列（如 `qwen-max`、`qwen-vl-plus-latest`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、DeepSeek 系列模型；支持音视频实时互动、[多模态](../concepts/multi-modal.md)回复增强、文件问答（全文引用/切片检索/自定义处理）等能力 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **工作流应用**：支持大模型节点调用 QwQ、DeepSeek 及[多模态](../concepts/multi-modal.md)模型；新增多模态生成节点、批量节点、异步运行模式；支持 Dify 工作流一键导入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：分为**文档**、**数据**（结构化，支持 RDS/MySQL/DMS）、**图片**三类；支持非结构化知识库导入 Excel、HTML、音视频文件；结构化知识库支持图文检索与图片索引 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高代码应用**：基于 Python 项目结构部署 AI 后端服务，内置运维、可观测性与日志能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 显示当前控制台已支持更丰富的模型选型（如 `qwen-vl-plus-latest`、`qwq-plus`），且 `qwen-max` 已非唯一推荐项；实际建模应以控制台可用模型列表为准，避免硬编码模型名。

## 关键参数

- **知识库检索参数**：可调整「初步向量检索 TopK」和「初步关键词检索 TopK」以平衡召回精度与 [Token](../concepts/token.md) 成本；多知识库场景下支持按权重分配优先级 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **智能体 Prompt 配置**：System Prompt 定义角色与任务边界；支持 FewShot Prompt 样例库提升回答准确性；调试阶段可启用「检索配置」开关控制来源展示、回答范围等 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)（2.0）支持自动信息提取、语义检索、用户画像管理，API 层面提供独立的 `CreateMemory` / `QueryMemory` 接口，与知识库解耦 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调用参数**：同步调用需传入 `input` 字段；异步调用需设置 `background: true` 并轮询 `Task ID`；工作流与智能体编排应用支持自定义参数透传 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码启动（推荐入门）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 设置 System Prompt 与欢迎语 → 添加预设问题 → 发布前绑定知识库（支持直接上传文档或关联已有知识库）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
   - 知识库创建可跳过「数据连接」前置步骤，直接在知识库创建页上传文件或选择 DMS/RDS 表 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  

2. **API 集成**：  
   - 同步调用：使用 `Responses API`（兼容 OpenAI 格式），适用于实时交互场景；  
   - 异步调用：设置 `background=true` 获取 `Task ID`，后续通过 `/v1/tasks/{task_id}` 查询结果；  
   - 知识库管理：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现全生命周期控制 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  

3. **高级能力启用**：  
   - 多模态：在智能体应用中开启「多模态回复增强」，并确保知识库含图片/音视频内容；  
   - [长期记忆](../concepts/long-term-memory.md)：调用新版 `LongTermMemory 2.0` API，无需依赖旧版 `long-term-memory/` 路径；  
   - MCP 集成：通过 MCP 市场开通预置服务，或使用 SDK 自定义部署 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独购买 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**，仅限纯文本推理场景；若需完整能力，请选用 `qwen-vl-plus` 或 `qwen-max` [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试与监控**：知识库调试面板支持在线调整参数并实时验证召回效果；应用观测（App Observe）提供端到端链路追踪，需授权 `AliyunServiceRoleForSFMTelemetry` 角色 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件限制**：非结构化知识库单次上传文件大小上限为 100 MB；音视频文件需为 MP4/MOV/AVI/WAV/MP3 格式，且时长建议 ≤ 2 小时以保障解析稳定性。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


