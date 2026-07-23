# start using

阿里云百炼平台提供低门槛、高灵活性的 AI 应用构建能力，开发者可通过零代码配置或 API 集成快速启动智能体、工作流及高代码应用。核心路径包括：选择模型与 Prompt 定义角色、接入知识库增强领域理解、配置技能与参数后发布应用。所有操作均在控制台可视化完成，亦支持全链路 API 调用。

## 支持的模型/功能

- **模型支持**：  
  - 智能体应用支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 及 DeepSeek 系列模型（如 DeepSeek-V2、DeepSeek-Coder）；  
  - 工作流应用支持 `qwq-plus`、`qwq-32b`、DeepSeek 系列及[多模态](../concepts/multi-modal.md)生成节点（图像/视频/音频生成）；  
  - 知识库向量化默认使用 `text-embedding-v4`，兼容 `v3`，图片解析可选 `qwen-vl-max` 或 `qwen-vl-plus` [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **核心功能**：  
  - 零代码构建私有知识问答应用，含 Prompt 设计、欢迎语/预设问题配置、知识库绑定与发布全流程 [原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)；  
  - 知识库类型覆盖**文档**、**数据**（RDS/DMS/自建 MySQL）、**图片**、**音视频**四类，支持 HTML、Excel、PDF、DOCX、MP4、MP3 等格式；  
  - 新版智能体应用（Agent 2.0）统一知识库与 MCP 为工具，支持自主规划调用顺序与过程可视化 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 明确指出智能体应用已支持 `qwq-plus`、`qwen-vl-plus-latest` 等更多模型，且 `qwq` 系列具备更强推理能力（数学/代码/IFEval 指标达 DeepSeek-R1 满血版水平）。实际选型应以控制台实时可用模型为准，旧文档中“仅推荐千问-Max”的表述已过时。

## 关键参数

- **知识库检索参数**：  
  - `初步向量检索 TopK` 与 `初步关键词检索 TopK` 可手动调低，以减少送入排序模型的 [Token](../concepts/token.md) 量，显著降低模型调用费用 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
  - 多知识库场景下支持按信息源重要性设置**权重**，系统优先召回高权重知识库内容；  
  - 检索配置中可开启“[多模态](../concepts/multi-modal.md)回复增强”，启用后智能体可解析知识库内图表/图像并结合视觉信息生成回答。  
- **应用级参数**：  
  - System Prompt（角色定义）直接影响模型行为边界，需明确任务范围与输出约束；  
  - “知识检索增强”开关启用后，可配置回答范围（如“仅基于知识库回答”）、是否展示引用来源等；  
  - 工作流应用支持异步运行模式：请求中设置 `background=true`，立即返回 Task ID，后续通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询结果。

## 使用方式

1. **零代码快速启动（推荐入门）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 设置 System Prompt → 配置欢迎语与预设问题 → 发布前绑定知识库（支持直接上传文件创建，无需预导入数据连接器）[原文标题](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)；  
   - 知识库创建流程已简化：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面 → 选择类型（文档/数据/图片）→ 直接上传文件或配置数据源 → 启用“智能切分” → 完成。  

2. **API 集成调用**：  
   - 同步调用：使用 Responses API（兼容 OpenAI 格式），适用于实时交互场景；  
   - 异步调用：设置 `background=true`，通过 Task ID 轮询结果；  
   - 知识库管理：支持 `CreateIndex`（含音视频）、`UpdateIndex`、`GetIndexMonitor` 等 API；  
   - [长期记忆](../concepts/long-term-memory.md)：新版[长期记忆](../concepts/long-term-memory.md) API 支持多应用共享、自动信息提取与语义检索 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包（标准版/旗舰版）两种模式 [原文标题](../../raw/application-user-guide/start-using/application-release-notes.md)；  
- **权限与隔离**：知识库支持子账号开通与标签分账，便于部门级成本归属；  
- **调试与验证**：编辑智能体应用时，可使用内置**调试面板**在线调整知识库参数并实时验证召回效果；  
- **模型能力边界**：QwQ 系列模型虽推理能力强，但当前不支持插件、流程编排及音视频交互能力（见文档 2 2026 年 4 月条目）；  
- **文件处理限制**：非结构化知识库导入 Excel 时，若含复杂公式或宏，可能无法完整解析；音视频知识库依赖 ASR/OCR 能力，原始音画质量直接影响检索精度。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


