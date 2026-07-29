# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建、配置并发布智能体应用、工作流应用及高代码应用。本文档聚焦“开始使用”核心流程，涵盖模型/功能选型、关键参数配置、操作方式及重要限制，适用于首次接入的开发者。所有操作均基于控制台可视化界面或标准 API，无需预置基础设施。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：默认支持 `qwen-max`、`qwen-plus`、`qwq-plus`、`qwq-32b` 及 `deepseek-*` 系列模型；自 2025 年 12 月起，新版智能体统一将知识库、MCP 作为可规划调用的工具，并完整展示思考链与工具执行过程 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **多模态能力**：`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 支持图文理解与音视频内容解析；知识库节点支持文档、图片、表格、音视频等多种格式输入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：分为**文档型**（非结构化）、**数据型**（结构化，支持 RDS/MySQL/DMS 同步）和**图片型**三类；自 2025 年 9 月起创建流程已按此分类简化 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md)（2.0）提供自动信息提取、语义检索、用户画像管理等能力，API 兼容多应用共享同一记忆库 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不建议新项目采用；应优先使用智能体应用或工作流应用的标准化调用接口。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以控制成本（自 2026 年 1 月 6 日起生效）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库权重**：当智能体应用关联多个知识库时，可为每个知识库设置权重，系统优先召回高权重知识源的内容（2025 年 4 月上线）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务边界，建议明确限定领域范围（如“你是一位阿里云百炼手机导购…”），避免泛化回答 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **多模态回复增强**：开关位于智能体应用“检索配置”中，开启后启用知识库内图表/图像的视觉理解能力（2025 年 3 月上线）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用” → “立即创建”，填写名称并选择模型（推荐 `qwen-max` 或 `qwq-plus`）。  
2. **配置 Prompt 与交互元素**：设置 System Prompt、欢迎语及预设问题，提升首屏引导效果 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
3. **构建知识库**：  
   - 文档型：直接上传 `.docx`/`.pdf`/`.xlsx`/`.html`/音视频文件（2025 年 9 月起支持离线 HTML 与 Excel 导入）；  
   - 数据型：从 RDS、DMS 或自建 MySQL 表同步结构化数据；  
   - 创建时可选“智能切分”策略，并启用调试面板实时验证召回效果（2025 年 9 月上线）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
4. **绑定与发布**：在应用配置页 → “技能” → “知识库” → 添加已创建的知识库 → 点击“发布”。  
5. **调用方式**：  
   - 控制台内测：右侧对话框直接提问；  
   - API 调用：支持同步（`Responses API`）与异步（`background=true`）两种模式，兼容 OpenAI SDK 接口规范（2025 年 11 月上线）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；免费额度仅限部分模型，需前往 [模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 查看详情 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **模型能力边界**：QwQ 系列模型虽具备强推理能力，但**不支持[插件](../concepts/plugin.md)、流程编排及音视频交互能力**（2025 年 4 月说明）；若需多步骤自动化，应选用工作流应用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库时效性**：上传文档后需等待 1–6 分钟完成解析（非结构化）或 1–2 分钟（结构化），期间不可用于检索 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **权限与分账**：子账号可独立开通知识库，通过标签实现分账管理（2026 年 1 月上线），但需主账号授权对应 RAM 权限 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


