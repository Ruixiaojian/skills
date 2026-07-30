# start using

阿里云百炼平台提供低代码/零代码方式快速构建智能体应用的能力，开发者可基于预置模型、[知识库](../concepts/knowledge-base.md)与工具链，在数分钟内完成私有知识问答、多模态交互等场景的原型验证与上线。本文档聚焦“开始使用”路径，梳理核心能力、关键配置项、接入方式及约束条件，适用于首次接触百炼平台的开发者。

## 支持的模型/功能

百炼支持多种模型类型与增强能力，覆盖文本、多模态与推理场景：

- **文本大模型**：千问-Max、QwQ系列（qwq-plus、qwq-32b）、DeepSeek 系列（自2025年2月起支持）等，其中 QwQ 模型具备显式思维链输出能力，适用于数学/代码类任务 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **多模态模型**：qwen-vl-plus-latest、qwen-vl-plus-2025-01-25（即 qwen-vl-plus-0125），支持 128k 上下文与高精度图文理解，可用于图表解析与音视频内容分析 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **嵌入模型**：text-embedding-v4（2025年7月上线，全面替代 v3）、text-embedding-v3（2025年5月上线），推荐在新建[知识库](../concepts/knowledge-base.md)时优先选用 v4 版本以获得更优语义召回效果；  
- **[知识库](../concepts/knowledge-base.md)类型**：支持文档型（PDF/DOCX/HTML/Excel）、音视频型（MP4/MOV/WAV）、结构化（MySQL/RDS/DMS 表）三类知识库，其中音视频知识库自2025年12月起正式可用 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **增强能力**：[长期记忆](../concepts/memory.md)（新版 API 已上线，支持自动信息提取与用户画像管理）、MCP 外部调用、Prompt 样例库（FewShot 优化）、多模态回复增强（需手动开启）等。

> **注意**：文档 1 中提及“建议选择千问-Max”，但文档 2 显示 QwQ 和 DeepSeek 系列已在智能体与工作流中全面支持，且部分场景下性能更优。实际选型应依据任务类型（如推理优先选 QwQ，通用对话可选千问-Max），而非仅依赖旧版引导建议。

## 关键参数

以下参数直接影响应用行为与成本，需在配置阶段明确设置：

- **知识库权重**：当一个智能体应用关联多个知识库时，可通过权重控制检索优先级，数值越高越优先召回 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **初步召回 TopK**：在知识库检索配置中可调整 `初步向量检索TopK` 与 `初步关键词检索TopK`，降低该值可减少送入排序模型的 [Token](../concepts/token.md) 数量，从而显著降低模型调用费用；  
- **检索配置开关**：包括“多模态回复增强”（启用后支持解析知识库中图表/图像）、“展示回答来源”、“限定回答范围”等，位于智能体应用的「知识检索增强」子菜单下；  
- **[长期记忆](../concepts/memory.md)策略**：新版[长期记忆](../concepts/memory.md)支持自动提取对话关键信息并去重，无需手动维护，但需通过 API 显式启用或配置生命周期策略。

## 使用方式

快速上手分为三类路径，按复杂度递增：

- **零代码构建（推荐入门）**：通过控制台可视化流程创建智能体应用 → 选择模型 → 编写 System Prompt → 配置欢迎语与预设问题 → 创建并上传知识库 → 绑定至应用 → 发布。完整流程详见 [原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)；  
- **API 调用**：支持同步（`Responses API`，兼容 OpenAI 接口）与异步（返回 Task ID）两种模式，适用于集成到自有系统；工作流应用还支持批量节点与异步运行模式；  
- **高代码开发**：2025年9月上线的「高代码应用」类型支持 Python 项目部署，内置运维、可观测性与日志服务，适用于需要深度定制逻辑与架构的场景。

## 限制和注意事项

- **知识库商业化计费**：自2026年1月4日起，知识库服务按规格费 + 模型调用费计费，不再提供免费额度；支持后付费与资源包两种模式，资源包需单独购买 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **模型调用限制**：QwQ 系列在智能体应用中**不支持插件、流程编排与音视频交互能力**（仅限纯文本推理），若需组合能力，请选用千问或 qwen-vl 系列；  
- **文件处理限制**：非结构化知识库导入 Excel 时，若含多表结构或混合格式（如嵌入 PDF），建议先统一为 DOCX 或 HTML；音视频文件单次上传上限为 2GB，且需确保音频采样率 ≤48kHz、视频分辨率 ≤1080p；  
- **调试与观测**：知识库调试面板支持在线调整参数并实时验证召回效果，但仅限编辑态生效；应用观测功能可端到端追踪请求链路，需提前授权 `AliyunServiceRoleForSFMTelemetry` 角色。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


