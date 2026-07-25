# start using

阿里云百炼平台提供低代码/零代码方式快速构建智能体应用的能力，开发者可基于预置模型、知识库与工具链，在数分钟内完成私有知识问答等场景的原型验证与上线。本文档聚焦“开始使用”路径，梳理核心能力、关键配置项、调用方式及约束条件，适用于初次接触百炼平台的开发者。

## 支持的模型/功能

百炼支持多类大模型与多模态模型接入智能体应用和工作流应用：
- **文本模型**：千问-Max（推荐入门）、QwQ系列（含qwq-plus、qwq-32b）、DeepSeek系列（自2024年2月起支持）；
- **多模态模型**：qwen-vl-plus-latest、qwen-vl-plus-2025-01-25（支持128k上下文与增强视觉理解），以及qwen-vl-max用于图片解析；
- **Embedding模型**：text-embedding-v4（2025年7月上线，全面替代v3）、text-embedding-v3（2025年5月上线）；
- **知识库类型**：文档型（支持DOCX、PDF、HTML、Excel等）、音视频型（2025年12月起支持）、结构化（支持RDS、DMS、自建MySQL）；
- **高级能力**：新版智能体应用（Agent 2.0）统一将知识库与MCP作为工具由模型自主规划调用；[长期记忆](../concepts/long-term-memory.md)（新）API支持跨应用共享与自动信息提取；文件问答支持全文引用、切片检索与自定义处理三模式。

> **注意**：文档 1 中推荐使用“千问-Max”作为初始模型，但[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)明确指出 QwQ 和 DeepSeek 系列已全面支持智能体应用，且在数学/代码等任务上表现更优。实际选型应依据具体任务需求，而非仅依赖入门引导建议。

## 关键参数

以下参数直接影响应用行为与成本，需在配置阶段显式设置：
- **System Prompt**：定义角色与任务边界，直接影响模型输出一致性（如“你是一位阿里云百炼手机导购…”）；
- **知识库权重**：当应用关联多个知识库时，可通过权重控制召回优先级（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)）；
- **检索配置**：包括“多模态回复增强”开关（启用后可解析知识库中图表）、“初步向量检索TopK”与“初步关键词检索TopK”（2026年1月起支持调整以降低[Token](../concepts/token.md)消耗）；
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)支持自动提取、语义检索与用户画像管理，需通过API显式启用；
- **调试面板参数**：编辑智能体应用时可在线调整知识库切分策略（如“智能切分”）、嵌入模型与召回阈值，并实时验证效果（见[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)）。

## 使用方式

### 零代码构建（控制台）
1. 创建智能体应用 → 选择模型 → 设置System Prompt与欢迎语/预设问题；
2. 创建知识库：支持直接上传文件（如DOCX）、同步DMS/RDS表或导入音视频（2025年12月起）；
3. 在应用配置中绑定知识库（支持多库加权）、开启“知识检索增强”并配置检索参数；
4. 发布前通过右侧测试区验证问答效果，或使用[调试面板](../../raw/application-user-guide/start-using/application-release-notes.md)优化召回质量。

### API调用
- **同步调用**：适用于实时交互，兼容OpenAI SDK（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)）；
- **异步调用**：对耗时任务返回Task ID，支持通过[任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center)查询结果；
- **知识库API**：支持`CreateIndex`（含音视频类型）、`UpdateIndex`、`GetIndexMonitor`等（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)）；
- **长期记忆API**：新版长期记忆（2026年1月上线）提供标准化接口，支持多应用共享同一记忆库。

## 限制和注意事项

- **计费变更**：知识库服务自2026年1月4日起正式商业化，费用由规格费+模型调用费构成；2026年2月起支持订阅资源包（RAG标准版/旗舰版）（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)）；
- **模型兼容性**：QwQ系列虽支持智能体应用，但明确不支持插件、流程与音视频交互能力（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)）；
- **知识库时效性**：非结构化知识库导入后需等待1–6分钟完成解析（文档大小相关），结构化知识库同步存在延迟，不保证实时一致；
- **权限隔离**：子账号可开通知识库并启用分账管理（通过标签标记业务空间），但需主账号授权对应RAM策略；
- **功能下线提示**：文档 1 中提及的[Assistant API](https://help.aliyun.com/zh/model-studio/assistantapi/)已标注“下线中”，不应作为新项目开发选项。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


