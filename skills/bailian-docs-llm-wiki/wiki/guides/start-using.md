# start using

阿里云百炼平台提供零代码与高代码双路径快速启动能力，开发者可基于控制台或 API 快速构建、配置并发布智能体应用、工作流应用或高代码应用。核心流程包括模型选择、Prompt 设计、知识库集成与发布部署，全程支持可视化操作与程序化调用。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：支持千问-Max、QwQ 系列（`qwq-plus`、`qwq-32b`）、DeepSeek 系列、Qwen-VL 系列（`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25`）等主流大模型；支持[多模态](../concepts/multi-modal.md)回复增强、文件问答升级（全文引用/切片检索/自定义处理）、自动模型切换等能力 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **工作流应用**：支持 DeepSeek 系列、QwQ 系列模型；新增[多模态](../concepts/multi-modal.md)生成节点、批量节点、异步运行模式及 Dify 工作流一键导入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：分为**文档**、**数据**、**图片**三类；支持非结构化（PDF/DOCX/Excel/HTML/音视频）与结构化（RDS/DMS/自建MySQL）数据源；支持图文检索、音视频知识库、text-embedding-v4 模型（推荐替代 v3）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **其他能力**：[长期记忆](../concepts/long-term-memory.md)（新）API、MCP 市场与外部调用、Prompt 样例库、应用观测、调试面板等。

> **注意**：文档 1 中提及“建议选择千问-Max”，但文档 2 显示 QwQ 和 DeepSeek 系列已全面支持智能体与工作流应用，且 QwQ 在数学/代码任务上显著优于同源 Distill 版本。实际选型应依据任务类型（如推理密集型优先 QwQ，[多模态](../concepts/multi-modal.md)优先 Qwen-VL），而非仅依赖旧版推荐。

## 关键参数

- **知识库检索配置**：
  - `初步向量检索TopK` 与 `初步关键词检索TopK`：可调低以减少送入排序模型的 [Token](../concepts/token.md) 量，直接降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
  - 权重设置：当应用关联多个知识库时，按信息源重要性分配权重，系统优先召回高权重知识库内容。
- **智能体应用参数**：
  - `多模态回复增强` 开关：启用后支持解析知识库中图表与图像内容，需配合 Qwen-VL 等多模态模型。
  - `检索配置`：控制回答范围、来源展示、是否启用[长期记忆](../concepts/long-term-memory.md)等。
- **API 调用参数**：
  - 同步调用：适用于实时交互，兼容 OpenAI SDK；
  - 异步调用：设置 `background=true` 返回 Task ID，适用于长耗时任务（如音视频处理、批量推理）。

## 使用方式

1. **零代码快速启动（推荐入门）**：
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 配置 System Prompt 与欢迎语 → 添加知识库（支持直接上传文件或从 DMS/RDS 同步）→ 发布 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
   - 知识库创建已简化：无需预先在「数据连接」页面导入，可于知识库创建流程中直接上传或同步数据。

2. **程序化接入（生产集成）**：
   - 调用智能体/工作流应用：使用 [Responses API](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)（同步）或 [异步调用 API](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference)；
   - 管理知识库：通过 `CreateIndex`、`UpdateIndex`、`GetIndexMonitor` 等 API 实现自动化运维；
   - 集成[长期记忆](../concepts/long-term-memory.md)：调用新版 [长期记忆（新）API](https://help.aliyun.com/zh/model-studio/long-term-memory-2-0)，支持多应用共享记忆库。

3. **高代码定制**：
   - 使用 [高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/) 类型，基于 Python 项目结构部署 AI 后端服务，内置可观测性与日志能力。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列在智能体应用中**不支持插件、流程、音视频交互能力**（仅限文本推理），该限制未在文档 1 中体现，需特别注意 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库解析时效**：文档上传后解析耗时因大小而异，通常 1–6 分钟；音视频解析耗时更长，建议预估并监控 `GetIndexMonitor` 数据。
- **权限与分账**：子账号可独立开通知识库，并通过标签实现分账管理，适用于多部门/多项目场景。
- **调试建议**：编辑智能体应用时，利用内置「调试面板」实时调整知识库参数并验证召回效果，避免发布后反复迭代。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


