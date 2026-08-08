# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级通信与内容平台的 AI 助手集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + 私有知识库 + AppFlow 低代码连接流实现快速部署，面向开发者提供标准化接入路径和可扩展能力。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在推理效果、响应速度与成本间取得平衡，适用于通用客服问答场景；也可按需选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。  
- **关键能力**：  
  - 多模态文档解析（PDF/DOCX/TXT/XLSX/PPTX/图片等，见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；  
  - RAG 知识增强（支持文件上传 → 向量化 → 知识库绑定 → 应用级调用）；  
  - 低代码连接流（AppFlow 预置模板覆盖微信/企微/钉钉/网页四类入口）；  
  - 自定义 Prompt 引导角色与输出格式（如“请总是给出简短的回答”，见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。  

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`。当前控制台实际可用模型列表以 [阿里云百炼模型中心](https://bailian.console.aliyun.com/?tab=model#/model-center)为准，`Qwen3.5-Plus` 为较新版本，若环境未显示该选项，请优先选用 `qwen-plus`（与 `千问-Plus` 对应）。

## 关键参数

| 参数 | 说明 | 来源示例 |
|------|------|----------|
| **应用 ID** | 百炼应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取，用于连接流配置 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| **API Key** | 百炼服务调用凭证，在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建，需安全存储 | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| **知识库调用方式** | 控制知识检索触发逻辑：`必定调用`（强制检索）、`按需调用`（仅当 query 匹配度高时触发） | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **相似度阈值 & 召回片段数** | 影响 RAG 检索质量的核心参数，可在知识库引用配置或本地 RAG 应用中调整（见文档 5） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `qwen-plus`）→ 配置 Prompt → 发布；  
2. **准备私有知识**：  
   - 云端方案：上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) → 创建知识库 → 在应用中绑定并设为 `必定调用`；  
   - 本地方案：使用 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供的 CLI 工具，支持自定义切分、嵌入模型与向量存储；  
3. **配置连接流**：  
   - 网站：AppFlow → AI助手 → 导入百炼应用 → Web集成 → 获取悬浮挂件脚本 → 插入 HTML；  
   - 微信/企微/钉钉：AppFlow → 选择对应预置模板 → 授权平台凭证（AppID/AgentId/ClientID + Secret）→ 绑定百炼应用 ID → 获取 Webhook URL → 在对应平台后台完成回调配置（含 [Token](../concepts/token.md)、EncodingAESKey、可信 IP 等）；  
4. **验证与评测**：上线前务必执行人工评测（[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)），检查回答准确性、时效性与合规性。

## 限制和注意事项

- **免费额度限制**：新用户享有百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费（文档 1、3、4 均强调此点）；  
- **平台认证要求**：  
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；  
  - 企业微信/钉钉需配置可信 IP 或通过 Nginx 代理解决域名/IP 校验问题（文档 3、4 的常见问题章节详述）；  
- **文件限制**：单文档 ≤ 100 MB 或 1000 页，支持格式包括 PDF/DOCX/TXT/XLSX/PPTX/图片等（文档 3 明确列出）；  
- **调试建议**：  
  - 若连接流无响应，优先检查 AppFlow 运行日志（文档 2 的“配置完成后，与公众号对话没有反应”章节）；  
  - 知识库效果不佳时，应优化文档切分策略、调整相似度阈值或重写 Prompt（文档 5 的“优化回复效果”部分提供系统方法）；  
- **安全要求**：API Key 和应用 ID 属敏感凭证，禁止硬编码于前端或公开仓库；Webhook URL 需启用 HTTPS（文档 3 的“域名主体校验未通过”问题涉及此要求）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


