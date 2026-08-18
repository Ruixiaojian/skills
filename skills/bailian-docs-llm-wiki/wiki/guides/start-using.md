# start using

阿里云百炼平台提供零代码与高代码双路径，支持开发者快速构建、测试并发布智能体应用、工作流应用及高代码应用。核心流程围绕模型选择、Prompt 设计、知识库集成与发布部署展开，适用于私有知识问答、多模态交互、自动化业务流程等场景。本文档聚焦“开始使用”阶段的关键能力与实操要点，面向开发者提炼结构化指引。

## 支持的模型/功能

- **智能体应用（Agent 2.0）**：支持千问-Max、QwQ系列（qwq-plus、qwq-32b）、DeepSeek 系列、qwen-vl-plus-latest 等模型；具备知识库/MCP 自主调用规划、多模态回复增强、文件问答（全文引用/切片检索/自定义处理）等能力 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **工作流应用**：支持 DeepSeek、QwQ、qwen-vl-plus 等模型；提供多模态生成节点、批量节点、异步运行模式、Dify 工作流一键导入等功能；知识库节点支持必定调用/智能调用/旧版调用三种方式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：分为**文档**、**数据**（结构化，支持 RDS/MySQL/DMS）、**图片**三类；非结构化知识库支持 DOCX、PDF、Excel、HTML、音视频（MP4、MP3、WAV）等多种格式；结构化知识库支持图文混合索引与图片上传检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **新增能力**：[长期记忆](../concepts/long-term-memory.md)（新）API（支持多应用共享、自动信息提取、语义检索）、Responses API（同步/异步调用）、高代码应用（Python 项目部署）、MCP 市场与外部调用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及的“Assistant API（下线中）”已明确废弃，不应作为新项目开发路径；当前推荐使用 Responses API 或工作流/智能体应用标准调用接口 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- **知识库检索配置**：可在智能体应用中设置“初步向量检索 TopK”和“初步关键词检索 TopK”，降低送入排序模型的 Token 量以控制成本；多知识库场景支持按权重分配召回优先级 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Embedding 模型**：知识库默认使用 `text-embedding-v4`（推荐），亦支持 `v3`；图片解析可选 `qwen-vl-max` 或 `qwen-vl-plus` 模型 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **Prompt 相关**：System Prompt 定义角色与任务（如“你是一位阿里云百炼手机导购…”）；支持 FewShot Prompt 样例库，通过 Query-Answer 对提升回答准确性 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)参数**：新版[长期记忆](../concepts/long-term-memory.md)支持自动提取关键信息、用户画像字段自定义、语义检索阈值调节等 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **创建应用**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”或“工作流应用” → 命名 → 选择模型（如千问-Max）→ 配置 System Prompt 与欢迎语/预设问题 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
2. **构建知识库**：
   - *非结构化*：直接在知识库创建页上传文件（DOCX/PDF/MP4 等），选择“智能切分”；支持离线 HTML、Excel 导入及自定义 metadata [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
   - *结构化*：选择 DMS、RDS 或自建 MySQL 数据源，指定表与字段映射 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
3. **关联与调试**：在应用配置页 → “技能” → “知识库” → 添加知识库；启用“调试面板”可实时验证检索召回效果 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
4. **发布与调用**：
   - 控制台点击“发布”后，应用即上线；
   - 调用方式包括：控制台内测、H5/APP SDK、微信/钉钉机器人、Responses API（同步/异步）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式计费，费用 = 规格费 + 模型调用费；支持后付费与 RAG 资源包（标准版/旗舰版）两种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程、音视频交互能力**；仅限纯文本推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **权限与分账**：知识库支持子账号开通与标签分账，需提前配置业务空间标签以实现费用归属 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **调试依赖**：知识库解析耗时因文档大小而异（通常 1–6 分钟），上传后需等待“解析完成”状态再测试；音视频解析可能额外增加处理时间 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


