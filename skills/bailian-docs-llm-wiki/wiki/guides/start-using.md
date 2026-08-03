# start using

阿里云百炼平台提供零代码与高代码并存的灵活开发路径，开发者可快速构建私有知识问答、多模态交互、自动化工作流等 AI 应用。本文档聚焦“开始使用”核心路径，涵盖模型与功能选型、关键参数配置、典型使用方式及必须注意的限制项，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型**：智能体应用支持 `qwen-max`（推荐入门）、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等；工作流应用额外支持 DeepSeek 系列模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多模态能力**：自 2025 年 3 月起，智能体应用支持开启“多模态回复增强”，解析知识库中的图表与图像内容；知识库支持上传音视频文件并实现智能检索与问答 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建MySQL）、**图片型**（含图文检索）；非结构化知识库支持自定义 metadata 和标签分类 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/memory.md)**：新版[长期记忆](../concepts/memory.md)（Long-term Memory 2.0）提供自动信息提取、语义检索、用户画像管理等能力，API 全面开放且支持多应用共享 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及的“千问-Max”为旧版命名，当前控制台已统一为 `qwen-max`；且文档 1 未体现 `qwq` 系列、`qwen-vl-plus` 等新模型支持，应以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 为准。

## 关键参数

- **知识库检索参数**：可在智能体应用“检索配置”中调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以控制成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库权重**：当一个智能体应用关联多个知识库时，可为每个知识库设置权重，系统优先召回高权重知识源 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 配置**：System Prompt 定义角色与任务（如“你是一位阿里云百炼手机导购…”），直接影响回答质量；支持 FewShot Prompt 样例库提升准确性 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **多模态识别模型**：导入图片时可显式选择 `qwen-vl-max` 或 `qwen-vl-plus` 模型进行解析，适用于复杂版面识别 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码快速启动**（约 5 分钟）：
   - 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用；
   - 选择 `qwen-max` 模型，配置 System Prompt、欢迎语与预设问题；
   - 创建知识库：上传文档（如 [阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250603/duuuxk/%E9%98%BF%E9%87%8C%E4%BA%91%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)），选择“智能切分”，等待解析完成；
   - 在应用配置中绑定知识库，发布后即可测试问答效果 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

2. **API 调用**：
   - 同步调用：使用 Responses API（兼容 OpenAI 接口），适用于实时交互场景；
   - 异步调用：设置 `background=true`，返回 Task ID 后轮询结果，适用于长耗时任务 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

3. **高级能力集成**：
   - 工作流应用支持 MCP 外部调用、批量节点、音视频实时互动；
   - 高代码应用支持 Python 项目部署，内置可观测性与运维能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用由规格费 + 模型调用费构成；支持后付费与资源包两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型能力边界**：QwQ 系列模型虽具备强推理能力，但不支持插件、流程编排及音视频交互能力（仅限智能体应用基础问答） [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **调试与验证**：知识库编辑时提供在线调试面板，可实时验证检索召回效果；但需注意，文档切分策略（如“智能切分”）直接影响检索精度，不建议在生产环境直接修改默认策略 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **权限与分账**：知识库支持子账号开通与标签分账，适用于多部门/多项目费用隔离，但需提前配置服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`） [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


