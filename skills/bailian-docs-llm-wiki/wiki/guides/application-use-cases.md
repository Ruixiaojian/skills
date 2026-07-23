# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型 + 私有知识”构建 RAG（[检索增强生成](../concepts/rag.md)）能力，覆盖网站、企业微信、微信公众号、钉钉等主流客户触点。所有方案均基于百炼托管的大模型 API 和 AppFlow 低代码集成能力，无需自建推理服务或编写后端逻辑，开发者可快速完成端到端部署。

## 支持的模型/功能

- **基础模型**：统一支持 Qwen 系列商业模型，包括 `qwen-max`、`qwen-plus`（文档 1 中称 Qwen3.5-Plus）、`qwen-turbo`；其中 `qwen-plus` 被多篇文档明确推荐为平衡效果、成本与延迟的默认选择 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 功能**：所有场景均依赖百炼知识库（Knowledge Base）实现私有知识注入，支持 PDF/DOCX/TXT/Excel 等格式上传、自动切分、向量索引（默认 HNSW，可选 ADB-PG 存储）及相似度阈值控制。
- **扩展能力**：除标准问答外，支持日志记录（通过 SLS 日志服务）、卡片消息渲染（钉钉）、深度思考过程展示（[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）、自定义 [Prompt 工程](../concepts/prompt-engineering.md)等。

> **注意**：文档 1 提到模型名为 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`；经核实，`Qwen3.5-Plus` 是 `qwen-plus` 的新版命名，二者为同一模型。实际配置时请以百炼控制台当前可用模型列表为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **认证凭证** | `App ID` + `API Key` | 百炼应用唯一标识与调用密钥，用于 AppFlow 连接百炼服务 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) §1.2 |
| **知识引用** | `调用方式`（必定调用/按需调用）、`相似度阈值`、`召回片段数` | 控制知识库是否强制触发、检索精度及上下文长度 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §5.1 |
| **模型控制** | `temperature`、`max_tokens`、`history_rounds` | 影响生成随机性、输出长度与上下文记忆 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) §优化回复效果 |
| **平台凭证** | 企业微信：`CorpID`/`AgentID`/`Secret`；钉钉：`Client ID`/`Client Secret`；公众号：`AppID`/`AppSecret` | 各平台 OAuth 与 Webhook 认证所需，由对应开放平台提供 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §2.2 |

## 使用方式

1. **创建百炼应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型（推荐 `qwen-plus`），配置 Prompt（如角色设定），发布应用。
2. **准备知识库**（可选但推荐）：
   - 上传文件至百炼数据中心或通过数据连接器导入；
   - 在知识库页面创建标准版知识库，关联文件；
   - 在应用配置中启用知识库，设置调用方式（生产环境建议设为“必定调用”）。
3. **配置目标平台接入**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 配置百炼凭证 → 生成悬浮挂件脚本 → 插入 HTML。
   - **企业微信/钉钉/公众号**：使用 AppFlow 预置模板 → 授权平台账号（扫码或填凭证）→ 绑定百炼应用 → 获取并配置 Webhook URL（企业微信需额外配置可信 IP）。
4. **验证与迭代**：在目标渠道发起对话测试；若效果不佳，优先检查知识库召回质量、Prompt 表达清晰度及模型参数（如 `temperature` 过高导致答案发散）。

## 限制和注意事项

- **免费额度限制**：新用户享有百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费，详见 [新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota) [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **文件限制**：百炼知识库单文档上限 100 MB 或 1000 页，图片单张 ≤20 MB；本地 RAG 方案（文档 5）明确提示“不建议传入超过 100 MB 的文件”。
- **平台特殊约束**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证或选用 `qwen-turbo` 加速响应 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
  - 钉钉机器人必须配置为 HTTP 模式，Stream 模式不兼容 AppFlow [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
  - 企业微信配置 Webhook 时若遇“域名主体校验未通过”，需通过 AppFlow 添加自有域名或部署 Nginx 代理解决。
- **调试建议**：上线前务必执行人工评测（[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)），重点验证知识引用准确性与业务术语一致性；日志记录（SLS）可用于事后分析失败会话。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


