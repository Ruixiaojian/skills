# application [use cases](use-cases.md)

阿里云百炼平台支持多种典型业务场景下的 AI 应用快速落地，涵盖网站嵌入、企业微信、微信公众号、钉钉等主流渠道的智能客服/助手集成，以及基于本地知识库的定制化 RAG 应用。所有方案均以低代码/无代码方式实现，依赖百炼大模型 API 与 AppFlow 连接流编排能力，适用于开发者快速验证和上线生产级应用。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可按需选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及）等变体。  
- **RAG 能力**：所有集成方案均支持知识库增强，通过百炼控制台上传 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.png`, `.jpg` 等格式文件（文档 2 明确列出支持格式及单文件 ≤100MB 限制），自动解析并构建向量索引。  
- **多端交互能力**：  
  - 网站悬浮式 AI 助手（含拖拽、预置问题、主题色自定义）[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；  
  - 企业微信自建应用消息自动回复（支持审批、客服、支付等事件类型）[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
  - 微信公众号智能客服（区分已认证/未认证订阅号，后者受 5 秒响应限制）[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；  
  - 钉钉群机器人（支持卡片消息、HTTP 模式接收）[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)；  
  - 本地部署 RAG 应用（Python + Gradio，支持自定义切分、嵌入模型、提示词）[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中提及模型 `Qwen3.5-Plus`，而文档 2、3、4 均使用 `千问-Plus`。经查证，`千问-Plus` 是 `Qwen3.5-Plus` 的正式商用名称，二者为同一模型，文档表述差异属命名演进，非功能矛盾。

## 关键参数

- **身份凭证**：  
  - 百炼侧：`App ID`（应用管理页获取）与 `API Key`（密钥管理页创建）；  
  - 第三方平台侧：企业微信需 `CorpID`, `AgentID`, `Secret`；微信公众号需 `AppID`（开发接口管理页）；钉钉需 `Client ID`, `Client Secret`；网站集成无需第三方凭证。  
- **知识库配置**：  
  - 调用方式：`必定调用`（强制检索）、`按需调用`（触发关键词时调用）；  
  - 相似度阈值：范围 `0–1`，值越高过滤越严格（文档 2、5 均支持）；  
  - 召回片段数：控制注入 Prompt 的上下文段落数量（文档 5 明确可调）。  
- **模型推理参数**（本地 RAG 场景）：  
  - 温度（`temperature`）、最大输出长度（`max_tokens`）、上下文轮数（`history_rounds`）——详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 使用方式

1. **统一前置步骤**：在百炼控制台创建「智能体应用」→ 配置模型与 Prompt → 获取 `App ID` 和 `API Key` → （可选）上传文件并创建知识库 → 发布应用。  
2. **渠道集成**：  
   - 网站：通过 AppFlow 创建 AI 助手 → 关联百炼应用 → 生成悬浮挂件脚本 → 插入 HTML；  
   - 企业微信/微信公众号/钉钉：使用 AppFlow 预置模板 → 授权第三方平台凭证 → 关联百炼应用 → 获取 Webhook URL → 在对应平台后台配置接收地址与可信 IP/域名；  
3. **本地 RAG**：下载 `local_rag.zip` → 安装依赖 → 配置环境变量 `BAI_LIAN_API_KEY` → 启动服务 → 通过 Gradio UI 或 API 调用。

> **注意**：微信公众号未认证时，必须选择对应模板并接受 5 秒响应限制；若超时，需改用已认证流程或切换至 `qwen-turbo` 模型提速（文档 3 常见问题部分明确说明）。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费（文档 1、2、4 均强调）。  
- **文件限制**：云端知识库单文件 ≤100MB 或 ≤1000 页，图片 ≤20MB，最多 200 个文件（文档 2）；本地 RAG 不建议上传 >100MB 文件（文档 5）。  
- **响应时效**：  
  - 微信公众号未认证：被动回复超 5 秒即失败；  
  - 企业微信/钉钉：需配置可信 IP 白名单（文档 2、4），否则接口调用被拒；  
  - 网站嵌入：无硬性时效限制，但前端体验受网络与模型延迟影响。  
- **安全合规**：  
  - 企业微信/钉钉/微信公众号均需完成主体备案或授权，否则域名校验失败（文档 2 常见问题详述解决方案）；  
  - 日志记录需额外配置 SLS（文档 2、3、4 均提供日志节点添加指南）。  
- **调试与评测**：上线前务必进行人工评测（文档 1、3）或应用评测（文档 2、4），通过优化 Prompt、调整切分策略、补充知识文档提升效果。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


