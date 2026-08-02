# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、多模态理解、工作流编排等能力的智能应用。本文档面向开发者，聚焦“开始使用”的核心操作路径与关键约束，涵盖模型支持、参数配置、接入方式及重要限制，所有内容均基于当前控制台与 API 的实际能力整理。

## 支持的模型/功能

- **智能体应用**：默认支持 `qwen-max`、`qwen-plus` 等千问系列模型；自 2025 年 4 月起支持 `QwQ` 系列（如 `qwq-plus`、`qwq-32b`），适用于数学推理与代码生成场景；自 2025 年 3 月起支持 `qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 多模态视觉语言模型 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **工作流应用**：支持 `DeepSeek` 系列模型（自 2025 年 2 月起）、`QwQ` 系列（自 2025 年 3 月起）及多模态生成节点（2026 年 1 月新增）。  
- **[知识库](../concepts/knowledge-base.md)类型**：分为**文档型**（支持 PDF/DOCX/HTML/Excel 等）、**数据型**（支持 RDS、DMS、自建 MySQL）和**图片型**（支持图文联合检索）三类，2025 年 9 月起正式分类并简化创建流程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **音视频能力**：自 2025 年 12 月起支持上传音视频文件构建[知识库](../concepts/knowledge-base.md)；2026 年 1 月起支持通过 API 创建音视频[知识库](../concepts/knowledge-base.md) [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  

> **注意**：文档 1 中推荐的“千问-Max”模型名称已过时，当前控制台显示为 `qwen-max`；且文档 1 未提及 `QwQ`、`DeepSeek` 及音视频知识库等 2025–2026 年新增模型与能力，实际使用请以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 为准。

## 关键参数

- **知识库检索配置**：在智能体应用中启用“知识检索增强”后，可设置：
  - `初步向量检索 TopK` 与 `初步关键词检索 TopK`（2026 年 1 月新增，用于降低 Token 成本）；
  - 多知识库权重（2025 年 4 月起支持，按信息源重要性分配召回优先级）；
  - “多模态回复增强”开关（2025 年 3 月起支持，启用后解析图表与图像内容）。
- **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md)（2026 年 1 月上线）提供自动信息提取、语义检索与用户画像管理能力，替代旧版 API [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **[Prompt 工程](../concepts/prompt-engineering.md)**：支持 System Prompt 定义角色与任务，同时可启用 Prompt 样例库（FewShot 能力，2024 年 12 月上线），提升客服与问答场景准确性。

## 使用方式

1. **零代码构建**：通过控制台完成三步操作——  
   - 创建智能体应用（[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建应用 → 智能体应用）；  
   - 配置模型、System Prompt、欢迎语与预设问题；  
   - 关联知识库（支持直接上传文件或从 DMS/RDS 同步数据，2025 年 9 月起流程简化）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 调用**：  
   - 同步调用：兼容 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，适用于实时交互；  
   - 异步调用：设置 `background=true` 返回 Task ID，适用于长耗时任务（如音视频处理）；  
   - 工作流异步模式自 2026 年 1 月起支持，任务状态可在 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查看。  
3. **调试与验证**：编辑智能体应用时，可使用内置**知识库调试面板**（2025 年 9 月上线），在线调整参数并实时验证检索效果。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用由**规格费**（RAG 标准版/旗舰版资源包）与**模型调用费**（含 embedding 与 LLM 调用）两部分构成；免费额度仅限新用户首月，详情见 [知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。  
- **模型兼容性限制**：`QwQ` 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**（2025 年 4 月公告），需选用工作流应用或高代码应用实现完整能力组合。  
- **权限与分账**：知识库支持子账号开通与标签分账（2026 年 1 月起），但需提前配置服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`），否则应用观测等功能不可用。  
- **文件处理限制**：非结构化知识库导入 Excel 时，若含复杂公式或宏，可能无法完整解析；音视频知识库仅支持 MP4/MOV/AVI/WAV/MP3 格式，且单文件大小上限为 2 GB（控制台页面未明示，需参考 API 文档 `CreateIndex` 接口限制）。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


