# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业通讯与业务平台中，实现开箱即用的智能问答、客服与助手服务。核心路径为：创建百炼智能体应用 → 通过 AppFlow 连接目标平台（如企业微信、钉钉、微信公众号、网站）→ 可选配置私有知识库（RAG）。所有方案均无需编码，依赖统一的 API Key 与应用 ID 配置，且新用户可使用免费额度完成端到端验证。

## 支持的模型/功能

- **基础模型**：所有用例均支持通义千问系列模型，包括 `qwen-plus`（文档 1、3、4 中明确指定为默认或推荐）、`qwen-turbo`（文档 3 提及用于提速）、`qwen-max`（文档 5 列为可选项）及 `qwen3.5-plus`（文档 2 明确指定）。模型选择直接影响响应质量、延迟与成本，需按场景权衡。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定（Prompt）、多轮对话、工具调用（当前文档未展开，但为百炼基础能力）。
  - RAG 知识增强：所有用例均支持通过上传文件（PDF/DOCX/TXT 等）创建知识库，并在应用中启用“必定调用”等策略 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
  - 多平台消息交互：支持文本、卡片（钉钉）、富媒体消息（企业微信/公众号）等格式，具体能力取决于目标平台接口限制（如未认证公众号仅支持 5 秒内被动回复）[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **本地部署选项**：除云端 SaaS 方式外，还提供基于 Python 的本地 RAG 应用框架，支持自定义文档切分、本地嵌入模型（如 GTE）及灵活参数调优 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1、3、4 均以 `qwen-plus` 为默认模型，而文档 2 明确使用 `qwen3.5-plus`，文档 5 则列出 `qwen-max`/`plus`/`turbo` 三者供选。实际部署时应以百炼控制台当前可用模型列表为准，`qwen3.5-plus` 属于较新版本，若控制台未显示则需选用 `qwen-plus` 作为兼容替代。

## 关键参数

- **身份凭证**：
  - `App ID`：百炼应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取。
  - `API Key`：用于 AppFlow 或前端 SDK 调用百炼 API 的密钥，在 [API Key](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建。
- **平台凭证**（依目标平台而异）：
  - 企业微信：`CorpID`、`AgentID`、`Secret`（文档 1）。
  - 微信公众号：`AppID`（文档 3），认证状态决定连接流模板选择。
  - 钉钉：`Client ID`、`Client Secret`（文档 4）。
  - 网站：无需平台凭证，依赖前端 SDK 注入（文档 2）。
- **RAG 相关参数**：
  - `召回片段数`、`相似度阈值`：控制知识检索精度，可在本地 RAG 应用中直接调整 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
  - `调用方式`（必定调用/按需调用）、`权重`、`文件处理方式`（全文引用/切片检索）：在百炼应用配置界面设置（文档 1、2、3、4）。

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型、配置 Prompt → 发布。
2. **配置目标平台连接**：
   - **企业微信/钉钉/公众号**：使用 AppFlow 预置模板（文档 1、3、4 提供具体 URL），通过向导配置平台凭证与百炼凭证，生成 Webhook URL 或完成 OAuth 授权。
   - **网站**：在 AppFlow 创建 AI 助手 → 导入百炼应用 → 配置 Web 集成（悬浮挂件）→ 将生成的 JS 脚本嵌入 HTML（文档 2）。
3. **启用知识增强（可选）**：
   - 上传文件至百炼 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center) 或使用 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)（文档 2、4）。
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建知识库并关联至应用。
4. **平台侧配置**：
   - 企业微信：配置 API 接收消息（填入 Webhook URL、[Token](../concepts/token.md)、EncodingAESKey）及可信 IP（文档 1）。
   - 公众号：开启服务器配置（需认证）或使用被动回复（文档 3）。
   - 钉钉：在应用后台启用 HTTP 模式机器人并填入 Webhook URL（文档 4）。
   - 网站：部署 JS 脚本后即可生效（文档 2）。

## 限制和注意事项

- **平台能力限制**：
  - 未认证微信公众号仅支持 5 秒内被动回复，超时将失败；建议完成认证或选用 `qwen-turbo` 降低延迟（文档 3）。
  - 钉钉机器人必须选择 **HTTP 模式**，Stream 模式不被 AppFlow 支持（文档 4）。
  - 企业微信需配置可信 IP 与域名主体校验，否则 API 接收失败；若无备案域名，需通过 AppFlow 内网代理或 Nginx 转发解决（文档 1）。
- **文件与知识库限制**：
  - 百炼云端知识库：单文件 ≤ 100MB 或 1000 页，支持格式详见各文档（PDF/DOCX/TXT 等）；解析耗时 1–6 分钟（文档 1、2、3、4）。
  - 本地 RAG 应用：不建议上传 >100MB 文件，受限于 Embedding API 限流（文档 5）。
- **调试与监控**：
  - 所有 AppFlow 连接流均支持查看 **运行日志** 排查失败原因（文档 3）。
  - 可通过添加 SLS 日志节点记录完整对话（文档 1、3、4），用于效果分析与合规审计。
- **安全要求**：
  - 钉钉应用需显式开通 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限（文档 4）。
  - 企业微信/钉钉的凭证（Secret/Client Secret）须严格保密，不可硬编码于前端。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


