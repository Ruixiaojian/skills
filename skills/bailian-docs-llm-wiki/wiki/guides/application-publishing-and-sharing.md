# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信渠道、可复用组件及音视频实时互动等形态，便于集成至业务系统或面向终端用户分发。所有发布行为均需基于已发布的应用，并受 Agent 版本、权限空间和计费模型约束。开发者应根据目标场景选择适配的发布路径，并严格遵循参数配置与调用规范。

## 支持的模型/功能

- **Agent 1.0 智能体应用**：完整支持全部发布渠道，包括魔笔 UI 应用、钉钉机器人、微信公众号、组件化封装、音视频实时互动（H5/APP/SDK）。  
- **Agent 2.0 智能体应用**：**仅支持 API 调用**，不支持 UI 应用、钉钉、微信、组件、音视频等任何前端分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **工作流应用**：支持发布为组件、UI 应用、音视频实时互动；但**不支持**直接发布为钉钉或微信机器人（仅 Agent 1.0 支持）[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **UI 设计器能力**：依托魔笔低代码平台，支持拖放式界面搭建、多端适配（PC/H5）、OIDC/OAuth 2.0 登录集成及数据库映射，适用于智能体与工作流的前端封装 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 2 中“步骤二：发布应用为组件”提到“对于已经发布的应用，您也可以在**组件管理**面板将其发布为组件”，但实际控制台当前仅支持从应用编辑页的「发布渠道」→「组件」入口创建组件，**无独立「组件管理」页面入口**；该描述与当前控制台 UI 不一致，应以 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中的「发布渠道」操作路径为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定有效 API Key，且必须与应用、UI 同属**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 不可跨空间复用；需提前在「我的 API-KEY」中创建并授权 |
| **钉钉配置** | 钉钉 Client ID / Client Secret / 模板 ID | 用于对接钉钉开放平台；模板 ID 必须关联已申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限的应用 | 模板类型必须为「AI卡片」，消息接收模式必须为「HTTP模式」（Stream 模式不兼容） |
| **微信配置** | AppID（开发者ID） | 微信公众号后台「基本配置」页获取；需完成微信侧 OAuth 授权流程 | 仅支持服务号/企业微信（未明确支持订阅号），且需通过微信审核 |
| **组件参数** | `query`（String, 必填）、`imageList`（Array<String>, 可选） | 预设系统参数，不可删除；`query` 传递用户文本输入，`imageList` 传递图像公网地址列表 | 若组件不使用图像模型，应将 `imageList` 的「是否可见」设为否 |
| **UI 应用** | 开发环境地址 / 生产环境域名 | 开发环境链接有效期为 **24 小时**，生产环境需绑定自定义域名并订阅付费套餐 | 开发环境免费，生产环境需团队版及以上套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **前置条件**：确保目标应用（Agent 1.0 或工作流）已完成构建并**已发布**；确认 API Key、应用、UI 均位于**同一业务空间**。  
2. **入口统一**：所有发布操作均从应用详情页的「发布渠道」页签发起（部分场景如 UI 应用亦支持从 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 页面独立创建）。  
3. **按渠道操作**：
   - **UI 应用**：在「UI 应用」卡片点击「创建」→ 自动填充基础信息 → 编辑 UI → 发布至开发/生产环境 → 获取「应用地址」分享。  
   - **钉钉/微信**：在对应卡片点击「创建」→ 完成 API Key 选择与平台凭证配置（Client ID/Secret/AppID/模板 ID）→ 获取回调地址或二维码 → 在钉钉/微信侧完成机器人配置或扫码接入。  
   - **组件**：在「组件」卡片点击「创建」→ 填写组件名称、描述 → 配置 `query`/`imageList` 等参数（别名、是否必填、传参方式、是否可见）→ 「确定发布」→ 在其他智能体/工作流中通过「技能」或「组件节点」引用。  
   - **音视频实时互动**：在「AI实时互动」页签点击「语音/视频互动」→ 选择 API Key → 生成临时体验二维码（24小时）→ 测试通过后「发布」→ 开通智能媒体服务并授权 SLR → 选择 H5/APP 分享或 SDK 集成。  

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**完全不支持**除 API 外的任何分享渠道，此为平台级限制，无法绕过 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环与服务不可用；  
  - 避免深度多级调用（A→B→C→D），因总运行时间受限，易触发超时错误。  
- **UI 应用时效性**：开发环境发布的 UI 地址**24 小时后自动失效**，需重新发布；生产环境需付费订阅且必须配置自定义域名。  
- **权限与计费归属**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由**应用创建者 UID 账号承担**，与访问者身份无关。  
- **工作流组件传参强制性**：当组件参数设置为「模型识别」时，在**工作流中引用必须显式提供输入值**（不能依赖大模型推断），否则运行失败；该行为与智能体场景不同，需特别注意配置一致性。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


