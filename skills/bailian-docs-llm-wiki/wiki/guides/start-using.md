# start using

阿里云百炼平台提供低代码/零代码方式快速构建智能体应用的能力，开发者无需编写后端逻辑即可完成私有知识问答、多模态交互等场景的部署。核心路径为：创建应用 → 配置模型与 Prompt →（可选）接入知识库 → 发布并调用。所有操作均可通过控制台可视化完成，也可通过 API 进行自动化集成。

## 支持的模型/功能

- **基础模型支持**：智能体应用和工作流应用均支持 Qwen 系列（如 `qwen-max`、`qwen-vl-plus-latest`）、QwQ 系列（`qwq-plus`、`qwq-32b`）及 DeepSeek 系列模型；其中 QwQ 模型具备深度推理能力，输出含思考链 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)；Qwen-VL 系列支持图文理解，适用于图表解析类任务 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel 等非结构化文本）、**数据型**（RDS、DMS、自建 MySQL 表）、**图片型**（支持图文检索与 Qwen-VL 解析）；自 2025 年 9 月起，创建流程已按类型分层优化 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多模态能力**：智能体应用支持“多模态回复增强”开关，启用后可解析知识库中的图表内容；工作流应用新增多模态生成节点，支持图像/视频/音频生成 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“建议选择千问-Max 模型”，但文档 2 显示 `qwen-max` 已纳入统一命名体系，且 `qwen-vl-plus-2025-01-25` 等快照版已替代旧版 VL 模型。实际配置时应以控制台当前可用模型列表为准，避免硬编码模型 ID。

## 关键参数

- **Prompt 设计**：System Prompt 定义角色与任务边界，直接影响回答一致性；推荐结合 FewShot 样例库提升效果，样例需包含 Query-Answer 对 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当应用关联多个知识库时，可通过权重参数控制召回优先级，数值越高越优先被检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **检索配置**：在智能体应用中开启“知识检索增强”后，可调整：
  - 初步向量/关键词检索 TopK（影响 [Token](../concepts/token.md) 成本与召回精度）；
  - 是否启用“智能切分”（默认策略，适用于多数文档）；
  - 多模态识别开关（需知识库含图片索引）。
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)（2.0）支持自动信息提取、语义检索与用户画像管理，API 层面需传入 `user_id` 和 `session_id` 实现上下文隔离 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **控制台快速启动**：  
   访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建智能体应用 → 选择模型 → 设置 System Prompt 与欢迎语 → 添加预设问题 → （可选）通过“技能 > 知识库”绑定已有知识库或新建 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用**：  
   - 同步调用：兼容 OpenAI 格式，适用于实时交互场景，参考 [同步调用 API 参考](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)；  
   - 异步调用：设置 `background=true` 返回 Task ID，适用于长耗时任务（如音视频处理），结果通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高级集成**：  
   - MCP 服务可通过 SDK 或一键配置接入第三方系统；  
   - 工作流应用支持 Dify 流程导入、批量节点及条件判断；  
   - 高代码应用支持 Python 项目部署，内置可观测性与日志服务 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库自 2026 年 1 月 4 日起正式商业化，费用 = 规格费 + 模型调用费；支持后付费与资源包两种模式，资源包需单独开通 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **文件限制**：单次上传文档大小上限为 100 MB；音视频文件需先转码为 MP4/MP3 格式，且总时长建议 ≤ 2 小时以保证解析稳定性。
- **调试建议**：知识库调试面板支持在线调整参数并实时验证召回效果，推荐在发布前使用该功能验证检索质量 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列模型暂不支持插件、音视频交互等高级能力，仅适用于纯文本推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


