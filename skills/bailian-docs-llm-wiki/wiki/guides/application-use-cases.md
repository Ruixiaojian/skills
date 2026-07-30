# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的大模型应用落地，核心围绕“低代码集成 + RAG增强 + 多端分发”展开。开发者可基于统一的百炼应用（Application）作为后端推理服务，通过 AppFlow 快速对接网站、微信公众号、企业微信、钉钉等主流渠道；同时支持云端全托管[知识库](../concepts/knowledge-base.md)与本地化RAG两种部署模式，兼顾易用性与私有化需求。所有方案均默认兼容新用户免费额度，按 token 计费。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档1）或 `千问-Plus`（文档2、3、4），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景。`qwen-max`、`qwen-turbo` 亦可在本地RAG方案中按需选用（文档5）。
- **核心能力**：
  - 智能体（Agent）应用：支持角色设定、多轮对话、工具调用（文档1–4）；
  - RAG增强：通过[知识库](../concepts/knowledge-base.md)实现私有文档精准问答（文档1–5）；
  - 多模态支持：文档3明确列出 `.pdf`, `.docx`, `.txt`, `.png`, `.jpg` 等14+格式文件上传能力；
  - 本地RAG：提供完整可运行的 Python 示例工程，支持自定义切分、嵌入模型替换及参数调优（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档1中模型名称写作 `Qwen3.5-Plus`，而文档2–4统一为 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 即千问3.5 Plus），命名差异属文档表述不一致，以控制台实际可用模型列表为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源参考 |
|----------|--------|------|----------|
| **应用凭证** | `App ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取（文档1–4） | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `API Key` | 用于调用百炼 API 的密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建（文档1–4） | |
| **[知识库](../concepts/knowledge-base.md)配置** | `调用方式` | 可选 `必定调用`（强制检索）、`按需调用`（触发关键词时检索）等（文档1–4） | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| | `相似度阈值` / `召回片段数` | 控制RAG检索精度与范围，影响回答相关性与冗余度（文档5） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **生成控制** | `Temperature` / `Max Tokens` / `Context Window` | 影响回复随机性、长度与历史依赖程度（文档5） | |

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**，配置模型（如 `Qwen3.5-Plus`）、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布（文档1–4）。
2. **准备知识数据（可选）**：
   - *云端知识库*：上传文档至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)，创建知识库并绑定至应用（文档1–4）；
   - *本地知识库*：下载并运行 [local_rag.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/odwvrb/local_rag.zip)，通过 Web UI 上传文件、创建知识库（文档5）。
3. **对接渠道**：
   - **网站**：使用 AppFlow 创建 AI 助手 → 配置百炼应用凭证 → 生成悬浮挂件脚本 → 嵌入 HTML（文档1）；
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号 → 绑定百炼应用 → 发布连接流（文档2）；
   - **企业微信/钉钉**：创建对应平台应用 → 获取凭证（CorpID/AgentId/Secret 或 Client ID/Secret）→ 在 AppFlow 中配置连接流与 Webhook → 在平台侧完成消息接收配置（文档3、4）。
4. **验证与日志**：通过渠道端直接交互测试；如需分析对话，可在 AppFlow 连接流中插入 SLS 日志节点（文档2、3、4）。

## 限制和注意事项

- **文件限制**：云端知识库单文件 ≤ 100 MB 或 1000 页，图片 ≤ 20 MB，最多 200 个文件（文档3）；本地RAG不建议上传 > 100 MB 文件（文档5）。
- **认证依赖**：微信公众号若未认证，仅支持被动回复且响应超时限制为 5 秒；建议完成认证以启用客户消息接口（文档2）。
- **可信IP与域名**：企业微信/钉钉要求配置可信IP或自有备案域名，否则可能触发安全拦截（文档3、4）。AppFlow 提供 Nginx 代理或计算巢一键部署方案辅助解决（文档3）。
- **模型响应时效**：微信未认证场景下，若百炼应用响应超时将导致失败；此时应优化 Prompt（如添加“请总是给出简短的回答”）或切换至 `qwen-turbo`（文档2）。
- **本地RAG环境**：Python 版本需 ≥ 3.8 且 ≤ 3.12；Windows 用户需额外安装 `msvc-runtime`（文档5）。

> **注意**：文档1中知识库创建路径指向 `[数据连接] → 默认文件连接器`，而文档2、3、4均指向 `[文件]` 页签。当前百炼控制台已统一入口至 **[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)**，旧路径（数据连接）为历史遗留，应以新路径为准。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


