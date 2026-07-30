# start using

阿里云百炼平台提供零代码与低代码能力，帮助开发者快速构建基于大模型的智能应用。本文档聚焦“开始使用”路径，涵盖从创建首个智能体应用、配置知识库到发布上线的核心流程，并同步说明当前支持的功能范围、关键参数配置项、调用方式及重要限制。所有操作均可在控制台完成，亦支持通过 API 进行自动化集成。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：自 2025 年 12 月起全面启用新版架构，将知识库、MCP 等统一为工具，由模型自主规划调用时序与逻辑，完整展示思考链与工具执行过程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **支持模型**：包括 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 及 DeepSeek 系列模型；其中 QwQ 系列适用于强推理场景（如数学、代码），Qwen-VL 系列支持[多模态](../concepts/multi-modal.md)图文理解 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：支持三类结构化分类——**文档**（PDF/DOCX/HTML/Excel 等）、**数据**（RDS、DMS、自建 MySQL）、**图片**（含图文联合检索）；非结构化知识库亦支持音视频文件上传与解析 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **扩展能力**：[长期记忆](../concepts/long-term-memory.md)（新）、MCP 市场服务、Prompt 样例库、[多模态](../concepts/multi-modal.md)生成节点、异步工作流运行等均已上线并可用。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确标记为下线状态，不建议新项目采用；应优先使用 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 或 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) 的标准 API 接口。

## 关键参数

- **知识库检索参数**：可在智能体应用的“检索配置”中调整 `初步向量检索 TopK` 和 `初步关键词检索 TopK`，降低召回 [Token](../concepts/token.md) 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当一个智能体关联多个知识库时，可为每个知识库设置权重值（1–10），系统优先召回高权重知识库中的内容。
- **Embedding 模型**：知识库默认使用 `text-embedding-v4`（2026 年 7 月起推荐），兼容 `v3`；若需更高精度的多语言或代码向量化，可显式指定。
- **[多模态](../concepts/multi-modal.md)识别开关**：“多模态回复增强”需在智能体应用的检索配置中手动开启，启用后模型可解析知识库中图表/图像内容并融合进回答。

## 使用方式

1. **创建智能体应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→ 选择「智能体应用」→ 设置名称、模型（如 `qwen-max`）、System Prompt（角色定义）、欢迎语与预设问题。
2. **构建知识库**：
   - 文档类：直接在知识库创建流程中上传文件（支持 DOCX/PDF/HTML/Excel/音视频等），选择「智能切分」策略；
   - 数据类：选择 RDS、DMS 或自建 MySQL 作为数据源，配置表名与字段映射；
   - 图片类：上传图片并启用图文解析，支持后续图文混合提问。
3. **绑定与调试**：在应用配置页 → 「技能」→ 「知识库」→ 添加已创建的知识库；编辑时可使用内置「调试面板」实时验证检索效果。
4. **发布与调用**：
   - 控制台内点击「发布」即刻生效；
   - API 调用支持同步（`Responses API`）与异步（`background=true`）两种模式，兼容 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **知识库计费生效**：自 2026 年 1 月 4 日起，知识库服务正式商业化，费用 = 规格费 + 模型调用费；免费额度仅覆盖部分模型调用，不包含知识库存储与检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列虽支持深度推理，但**不支持插件、音视频交互及流程编排能力**；若需完整工具链，应选用 `qwen-max` 或 `qwen-vl-plus` 等通用大模型。
- **文件处理限制**：单次上传文档大小上限为 100 MB；音视频文件需 ≤ 2 小时且格式为 MP4/MOV/MP3/WAV；OCR 与 VL 模型对模糊、低分辨率图像识别效果下降明显。
- **权限与分账**：子账号可独立开通知识库，但需主账号授权并配置标签实现分账管理，避免跨部门费用混淆。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


