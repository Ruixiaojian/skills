# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建、配置并发布智能体应用、工作流应用及高代码应用。核心流程包括模型选择、Prompt 设计、知识库集成与发布部署，全程可在控制台完成，亦可通过 API 实现自动化集成。本文档聚焦“开始使用”阶段的关键能力与实操要点，适用于首次上手的开发者。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：自 2025 年 12 月起全面上线，统一将知识库、MCP 等能力抽象为可自主规划调用的工具，完整展示模型思考链与工具执行过程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **支持模型**：包括 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 及 DeepSeek 系列模型；QwQ 系列模型支持深度推理与分步思考，但**不支持插件、音视频交互等扩展能力**（仅限基础文本生成）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：支持三类结构化分类——**文档**（PDF/DOCX/HTML/Excel 等）、**数据**（RDS、DMS、自建 MySQL）、**图片**（含图文联合检索）；非结构化知识库亦支持上传音视频文件并启用多模态解析 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多模态增强**：智能体应用中可开启“多模态回复增强”，结合 `qwen-vl-plus` 等视觉语言模型解析知识库中的图表与图像内容，提升回答准确性。

> **注意**：文档 1 中推荐的“千问-Max”模型在文档 2 的最新功能列表中未被明确列为当前主推或默认推荐型号；而文档 2 明确指出 QwQ 系列模型“不包括插件、流程、音视频交互能力”，但文档 1 的全流程示例未涉及该限制说明。实际选型时请以控制台实时可用模型为准，并确认目标能力是否受模型限制。

## 关键参数

- **知识库检索配置**：支持调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低召回 [Token](../concepts/token.md) 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当智能体应用关联多个知识库时，可为各知识库设置权重，系统优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)（2.0）支持自动信息提取、语义检索与用户画像管理，API 层面提供更细粒度的会话上下文控制能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 工程支持**：除 System Prompt 外，支持 FewShot Prompt 样例库，通过录入 Query-Answer 对提升客服、问答等场景的输出一致性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→ 选择「智能体应用」→ 命名并进入配置页。
2. **配置模型与 Prompt**：在模型选择页指定大模型（如 `qwen-max` 或 `qwq-plus`），在 System Prompt 区域输入角色定义（例如：“你是一位阿里云百炼手机导购……”）。
3. **添加知识库**：
   - 先在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建知识库（支持文档/数据/图片三类）；
   - 返回应用配置页 → 「技能」→ 「知识库」→ 「+」添加已创建的知识库；
   - 可启用调试面板实时验证检索效果（文档 2 提及，文档 1 未覆盖）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
4. **发布与调用**：
   - 点击「发布」使变更生效；
   - 支持同步/异步两种 API 调用方式：同步适用于实时交互，异步返回 Task ID 供轮询查询 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
   - 高代码应用支持 Python 项目结构部署，内置可观测性与运维能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **知识库商业化计费**：自 2026 年 1 月 4 日起，知识库服务正式计费，费用由规格费 + 模型调用费构成；支持后付费与资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列模型虽具备强推理能力，但明确**不支持插件、音视频交互、流程编排等功能**；若需上述能力，应选用 `qwen-vl-plus` 或 `qwen-max` 等通用大模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **文件处理限制**：文档 1 中“0代码构建”教程默认使用 DOCX 文件，但文档 2 明确支持 Excel、HTML、音视频、图片等多种格式，且非结构化知识库支持自定义 metadata 与标签分类，建议按实际数据形态选择知识库类型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)兼容性**：新版长期记忆（2.0）API 与旧版不兼容，迁移需重写集成逻辑；其优势在于多应用共享、低延迟与自动画像提取，旧版已进入下线流程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


