# start using

阿里云百炼平台提供低代码/无代码方式快速构建智能体应用的能力，开发者可基于预置模型、知识库与工具链，在数分钟内完成私有知识问答等场景的部署。本文档聚焦“开始使用”路径，梳理核心能力、关键配置项、接入方式及当前约束，适用于首次接触百炼应用构建的开发者。

## 支持的模型/功能

- **基础模型**：支持千问系列（如 `qwen-max`）、QwQ 系列（`qwq-plus`、`qwq-32b`）、Qwen-VL 多模态模型（`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25`）及 DeepSeek 系列模型，覆盖文本生成、深度推理、图文理解等能力 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **知识库类型**：支持文档型（PDF/DOCX/HTML/Excel）、音视频型（MP4/MOV/WAV）、图片型及结构化数据型（RDS/DMS/自建MySQL）知识库；非结构化知识库支持图文混合检索与 metadata 自定义 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **增强能力**：  
  - 智能体应用支持“多模态回复增强”开关，启用后可解析知识库中的图表与图像内容；  
  - 新版智能体应用（Agent 2.0）将知识库、MCP 统一为工具，由模型自主规划调用时序与逻辑；  
  - 工作流应用支持多模态生成节点、批量节点及异步运行模式。

> **注意**：文档 1 中推荐使用 `千问-Max` 作为入门模型，但文档 2 明确指出 `qwen-vl-plus-2025-01-25` 属于 Qwen2.5-VL 系列且上下文扩展至 128k，而 `千问-Max` 并未在功能动态中被明确标注为最新主力型号。建议以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中列出的模型名称为准，避免依赖旧版命名。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以控制成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权重设置**：当智能体应用关联多个知识库时，可为每个知识库设置权重，系统优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **Prompt 配置**：System Prompt 定义角色与任务边界，需清晰、具体（例如：“你是一位阿里云百炼手机导购，任务是帮助客户对比手机参数…”），直接影响模型行为一致性。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md) API 支持自动信息提取、语义检索与用户画像管理，替代旧版需手动维护的方案。

## 使用方式

1. **零代码构建流程**（约 5 分钟）：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 设置 System Prompt → 配置欢迎语与预设问题；  
   - 进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 创建标准版知识库 → 直接上传文件或同步 DMS/RDS 数据（无需预先创建连接器）→ 启用“智能切分”；  
   - 返回应用配置页 → 在“技能 > 知识库”中添加已创建的知识库 → 发布应用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 调用**：  
   - 同步调用：兼容 OpenAI 格式，适用于实时交互场景；  
   - 异步调用：设置 `background=true`，返回 Task ID 后通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果；  
   - 知识库与[长期记忆](../concepts/long-term-memory.md)均提供独立 RESTful API（如 `CreateIndex`、`GetIndexMonitor`、`长期记忆（新）`）。  

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**，仅适用于纯文本推理场景；而工作流应用则完整支持 QwQ 系列。  
- **调试与验证**：编辑智能体应用时，可使用内置“调试面板”在线调整知识库参数并实时验证检索效果，避免发布后才发现召回偏差。  
- **文档时效性**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，全代码 RAG 开发应转向标准 API 或高代码应用类型；文档 2 中“智能体编排应用”已于 2024 年 12 月 16 日被工作流应用整合，相关节点（如条件判断）现统一归入工作流能力。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


