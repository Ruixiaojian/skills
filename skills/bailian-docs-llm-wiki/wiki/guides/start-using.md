# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建基于大模型的智能应用。本文档聚焦“开始使用”核心流程，涵盖从创建首个智能体应用、配置知识库到发布调用的完整链路，并同步说明当前平台支持的关键能力、参数控制点及重要限制。所有操作均基于控制台 Web 界面或标准 API，无需预置开发环境。

## 支持的模型/功能

- **基础模型支持**：智能体应用默认支持 `qwen-max`、`qwen-plus` 等 Qwen 系列模型；自 2026 年起，`qwq-plus`、`qwq-32b`（用于工作流）及 `DeepSeek` 系列模型也已正式接入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。QwQ 模型启用需注意其不支持插件、音视频交互等扩展能力（仅限纯文本推理场景）。
- **[多模态](../concepts/multimodal.md)能力**：`qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 已上线，支持图像理解与图文联合检索；知识库支持导入图片、PDF、Excel、HTML 及音视频文件，并可选 `qwen-vl-max` 或 `qwen-vl-plus` 进行解析 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：分为**文档型**（非结构化）、**数据型**（结构化，支持 RDS/MySQL/DMS 同步）和**图片型**三类，创建时按场景自动归类；音视频知识库需通过 API 创建，Web 控制台暂仅支持上传与基础配置 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **高级功能**：新版智能体应用（Agent 2.0）统一将知识库、MCP 作为可规划工具；[长期记忆](../concepts/memory.md)（新）API 提供语义检索、自动画像提取与多应用共享能力；工作流应用支持异步运行模式、批量节点及 Dify 一键导入。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不应作为新项目集成方案；所有 RAG 类应用应优先使用智能体应用 + 知识库组合，或通过标准 Responses API 调用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- **知识库检索控制**：
  - `初步向量检索TopK` 与 `初步关键词检索TopK`：可手动下调以减少排序模型 [Token](../concepts/token.md) 消耗，直接降低模型调用费用（见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 2026-01-06 条目）。
  - 多知识库权重：当应用关联多个知识库时，可为每个库设置权重值（1–10），系统优先召回高权重库内容。
- **智能体行为配置**：
  - “[多模态](../concepts/multimodal.md)回复增强”开关：启用后，模型可结合知识库中解析出的图表/图像内容生成回答（需知识库已启用图文解析）。
  - “检索配置”：控制是否展示引用来源、限定回答范围（如“仅基于知识库回答”）、启用全文引用或切片检索模式。
- **Embedding 模型选择**：知识库默认使用 `text-embedding-v4`（2026 年起推荐），较 v3 在语种覆盖与代码向量化上更优；v3 仍可用，但 v2 已不建议。

## 使用方式

1. **创建智能体应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→「智能体应用」→ 设置名称、选择模型（如 `qwen-max`）、配置 System Prompt 与欢迎语/预设问题。
2. **构建知识库**：
   - *快捷方式*：在应用配置页直接上传文件（如 `.docx`、`.pdf`），跳过独立数据连接器步骤（2025-09-23 起优化）[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)；
   - *结构化方式*：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，选择「数据型」→ 绑定 RDS/MySQL 表或 DMS 数据源；
   - *音视频/图片*：需调用 `CreateIndex` API 并指定 `type=audio_video` 或 `type=image`。
3. **绑定与发布**：在应用配置页 → 「技能」→ 「知识库」→ 「+」添加已建知识库 → 点击「发布」。发布后可通过右侧测试面板或 Responses API 调用。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；免费额度仅覆盖部分模型调用，不包含知识库存储与检索资源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、MCP、音视频交互及[长期记忆](../concepts/memory.md)功能**（见文档 2 2026-04-01 条目），若需全能力，应选用 `qwen-max` 或 `qwen-plus`。
- **调试与监控**：知识库支持在线调试面板（实时验证召回效果），但该功能仅在编辑智能体应用时可见；生产环境监控需通过 `GetIndexMonitor` API 或控制台「应用观测」模块查看端到端链路 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **文件限制**：单次上传文档大小上限为 100 MB；音视频文件需先转码为 MP4/MKV/MP3/WAV 格式，且总时长建议 ≤ 2 小时以保障解析稳定性。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


