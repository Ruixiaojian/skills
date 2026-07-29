# start using

阿里云百炼平台提供低代码/零代码与高代码两种路径，帮助开发者快速构建并部署大模型应用。本文档面向开发者，聚焦“开始使用”阶段的核心操作路径、能力边界与关键配置项，涵盖从应用创建、模型选择、知识增强到发布调用的完整链路。所有操作均基于控制台界面或标准 API，无需预置基础设施。

## 支持的模型/功能

- **基础模型支持**：智能体应用默认支持 `qwen-max`、`qwen-vl-plus` 系列（含 `qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25`），以及 `qwq-plus`、`qwq-32b` 等深度思考模型；工作流应用额外支持 DeepSeek 系列模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **多模态能力**：自 2025 年 3 月起，智能体应用支持开启“多模态回复增强”开关，可解析知识库中的图表与图像内容；知识库亦支持上传音视频文件并构建非结构化知识库 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel等）、**数据型**（RDS/DMS/自建MySQL同步）、**图片型**（支持图文联合检索与Qwen-VL模型解析）；非结构化知识库还支持自定义 metadata 与标签分类 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级能力**：[长期记忆](../concepts/long-term-memory.md)（新）API 提供自动信息提取、语义检索与用户画像管理；MCP 市场支持接入预置或自定义外部服务；工作流应用支持异步运行模式与批量节点。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确标注为下线状态，不建议新项目采用；应优先使用 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 或 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) 的当前稳定接口。

## 关键参数

- **知识库检索参数**：可通过调试面板实时调整 `初步向量检索TopK` 与 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库权重**：当智能体应用关联多个知识库时，可为每个知识库设置权重，系统将优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Embedding 模型**：知识库默认使用 `text-embedding-v4`（2025年7月起），相比 v3 在语种覆盖与代码片段向量化上更优；v3 仍可用，但 v4 为推荐选项。  
- **Prompt 配置**：System Prompt 定义角色与任务边界；智能体应用支持 Prompt 样例库（FewShot），通过 Query-Answer 对提升回答准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码快速启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→「立即创建」；选择模型（如 `qwen-max`）、配置 System Prompt、设置欢迎语与预设问题 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **知识库集成**：  
   - 创建知识库时可直接上传文件（如 DOCX），无需预先在数据连接页面导入（2025年9月起流程简化）；  
   - 支持音视频、HTML、Excel 等多格式；结构化知识库可直连 RDS/DMS/MySQL；  
   - 在应用配置页 → 「技能」→ 「知识库」→ 「+」添加，支持多库加权 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
3. **API 调用**：  
   - 同步调用：兼容 OpenAI 格式，适用于实时交互场景；  
   - 异步调用：设置 `background=true` 返回 Task ID，通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型调用限制**：`qwq` 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**，仅限纯文本推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试与验证**：编辑智能体应用时，可使用内置「调试面板」在线调整知识库参数并实时验证召回效果，避免发布后才发现检索偏差 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[长期记忆](../concepts/long-term-memory.md)兼容性**：新版[长期记忆](../concepts/long-term-memory.md)（2026年1月上线）API 与旧版不兼容，迁移需重写集成逻辑；新版本支持多应用共享记忆库、自动信息提取与语义检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


