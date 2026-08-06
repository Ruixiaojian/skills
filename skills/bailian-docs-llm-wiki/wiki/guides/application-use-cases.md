# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到多种主流业务渠道中，实现开箱即用的智能交互场景。典型用例包括在网站、钉钉、微信公众号、企业微信等平台嵌入AI助手或机器人，通过RAG（[检索增强生成](../concepts/rag.md)）技术结合私有知识库，提供7×24小时专业问答服务。所有方案均基于统一的百炼应用API调用，无需自建模型服务，开发者只需配置连接流与知识库即可完成端到端部署。

## 支持的模型/功能

- **核心模型**：默认推荐 `qwen-plus`（即文档中多次提及的“千问-Plus”），其在效果、速度与成本间取得平衡，适用于客服问答、产品咨询等通用任务；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `Qwen3.5-Plus`（见[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。  
- **关键能力**：  
  - 基于Prompt的角色设定（如“你叫小助，可以帮助用户解答产品选购、使用等方面的问题”）；  
  - RAG知识增强：支持上传PDF/DOCX/TXT等格式文档，自动切分、向量化并关联至应用；  
  - [多模态](../concepts/multimodal.md)支持：企业微信场景明确支持图片（PNG/JPG/BMP/GIF）、PPTX、XLSX等格式上传 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
  - 本地RAG扩展：提供`local_rag`开源示例，支持本地文档管理、自定义切分策略及嵌入模型替换（如GTE中文-large）[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档1中指定模型为`Qwen3.5-Plus`，而文档2、4、5均使用`千问-Plus`（即`qwen-plus`），二者为不同版本。实际部署时应以百炼控制台当前可用模型列表为准，`Qwen3.5-Plus`属于较新迭代，若控制台未列出则需降级至`qwen-plus`。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置性 |
|----------|--------|------|----------|
| **模型层** | 温度（temperature） | 控制输出随机性，值越高越发散 | 仅本地RAG方案支持调整 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | 最大回复长度 | 限制生成token数 | 同上 |
| | 携带上下文轮数 | 决定历史对话参考深度 | 同上 |
| **RAG层** | 召回片段数 | 检索返回的最相关文本段数量 | 同上 |
| | 相似度阈值 | 过滤低于该阈值的检索结果 | 同上；企业微信场景还支持为单个知识文档配置权重和阈值 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **集成层** | 调用方式 | 知识库调用策略：`必定调用`/`按需调用`/`不调用` | 全场景支持，推荐生产环境设为`必定调用` |

## 使用方式

1. **创建百炼应用**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建“智能体应用”，配置模型、Prompt及知识库引用；  
2. **获取凭证**：从[API Key](https://bailian.console.aliyun.com/?tab=app#/api-key)页面获取API Key，从应用详情页复制Application ID；  
3. **选择集成通道**：  
   - **网站嵌入**：通过AppFlow创建AI助手 → 配置Web集成 → 获取悬浮挂件脚本插入HTML [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；  
   - **钉钉/企业微信/微信公众号**：在对应平台创建应用（需管理员权限）→ 获取平台凭证（Client ID/Secret、AppID、AgentId等）→ 在AppFlow中使用预置模板创建连接流 → 绑定百炼应用ID与API Key → 发布并配置Webhook；  
4. **注入私有知识**：  
   - 云端方式：上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) → 创建知识库 → 在应用中引用；  
   - 本地方式：运行`local_rag`示例，通过Gradio界面上传文件或创建持久化知识库。

## 限制和注意事项

- **知识库文件限制**：  
  - 云端上传单文件≤100MB或1000页，图片≤20MB，总文件数≤200个 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
  - 本地RAG方案受限于Embedding API限流，不建议上传>100MB文件 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)；  
- **认证依赖**：  
  - 微信公众号未认证时，消息响应必须≤5秒，超时即失败；建议完成认证或选用`qwen-turbo`模型提速 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；  
- **安全配置**：  
  - 企业微信要求配置可信IP白名单，且同一IP不可复用于多个企业；若IP被识别为第三方服务商，需通过ECS/Nginx代理解决 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
- **调试与日志**：  
  - 所有AppFlow连接流均支持添加SLS日志节点记录对话，便于问题排查与效果分析（各文档均提供详细步骤）；  
  - 生产上线前务必进行[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)或[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-application/)，验证回答准确性。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)


