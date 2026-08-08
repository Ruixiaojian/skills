# start using

阿里云百炼平台提供开箱即用的智能体应用构建能力，开发者无需编写代码即可快速搭建私有知识问答、多模态交互等AI应用。本文档聚焦“开始使用”路径，涵盖模型与功能选型、关键参数配置、操作流程及重要限制，适用于首次接入百炼平台的开发者。

## 支持的模型/功能

- **基础模型**：支持千问-Max、QwQ系列（qwq-plus、qwq-32b）、DeepSeek系列、Qwen-VL系列（qwen-vl-plus-latest、qwen-vl-plus-2025-01-25）等主流大模型；其中QwQ模型具备深度推理能力，输出包含显式思考链 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **知识库类型**：支持文档、数据、图片三类非结构化/结构化知识库；自2025年9月起，创建流程已按场景分类优化 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多模态能力**：支持音视频知识库（2025年12月上线）、图文混合检索（2024年9月支持）、Qwen-VL模型解析复杂图表（2025年5月支持）；智能体应用可通过开启“多模态回复增强”开关启用视觉内容理解 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **高级功能**：[长期记忆](../concepts/long-term-memory.md)（新版API支持自动提取与用户画像）、MCP服务集成、工作流异步运行模式、批量节点处理等。

> **注意**：文档1中提及的“Assistant API（下线中）”已明确标注为历史接口，不推荐新项目使用；当前标准调用方式应为[Responses API](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)，详见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)中2025年11月发布的同步/异步调用能力。

## 关键参数

- **知识库检索参数**：支持调整`初步向量检索TopK`和`初步关键词检索TopK`以控制召回[Token](../concepts/token.md)量，直接影响模型调用成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当应用关联多个知识库时，可为各知识库设置权重，系统优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt配置**：System Prompt定义角色与任务边界（如“你是一位阿里云百炼手机导购…”），直接影响回答专业性与一致性 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **Embedding模型**：知识库默认使用text-embedding-v4（2025年7月上线），相比v3在语种覆盖与代码片段向量化效果上更优；v3仍可用但非推荐 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建应用**：访问[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用” → “立即创建”，命名并选择模型（如千问-Max）。
2. **配置Prompt与交互**：设置System Prompt、欢迎语及预设问题，用于引导模型行为与用户启动对话 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
3. **构建知识库**：
   - 非结构化知识库：直接上传文档（支持DOCX、PDF、Excel、HTML、音视频等格式），选择“智能切分”策略；
   - 结构化知识库：支持从DMS、RDS或自建MySQL同步数据表 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
4. **绑定与发布**：在应用配置页 → “技能” → “知识库”中添加已创建的知识库，确认后点击“发布”。
5. **调用方式**：
   - 控制台内测：右侧对话框直接提问；
   - API调用：使用Responses API（同步/异步模式），兼容OpenAI SDK风格 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自2026年1月4日起正式商业化，费用由规格费+模型调用费构成；支持后付费与资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ系列模型虽支持深度推理，但**不支持插件、流程编排及音视频交互能力**（仅限文本生成场景） [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **调试依赖**：知识库参数在线调试需通过编辑智能体应用时的“调试面板”完成，该功能自2025年9月起可用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[文件处理](../concepts/file-processing.md)限制**：音视频知识库需经ASR/OCR预处理，原始文件大小与时长受控制台上传限制约束；复杂图片解析建议指定qwen-vl-max模型并传入精准Prompt [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


