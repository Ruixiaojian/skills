# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括生成可访问的 UI 网页、集成至钉钉/微信等第三方平台、封装为可复用组件、以及接入音视频实时互动场景。所有发布行为均基于已创建并发布的应用实例，且需注意 Agent 1.0 与 Agent 2.0 在分享能力上的根本差异。

## 支持的模型/功能

- **适用应用类型**：仅 `Agent 1.0` 智能体应用支持魔笔 UI 分享、钉钉/微信发布、组件化、音视频实时互动；`Agent 2.0` 应用**仅支持 API 调用**，不支持任何 UI 或渠道类分享功能 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将智能体或工作流应用快速封装为网页界面，支持拖放式低代码编辑、数据库集成与多端适配（PC/H5）。
- **第三方渠道**：
  - 钉钉：需创建钉钉应用、配置机器人、申请 `Card.Streaming.Write` 等权限，并填入模板 ID、Client ID/Secret；
  - 微信公众号：需提供 AppID 并完成授权，生成客服二维码供扫码体验。
- **组件化能力**：智能体或工作流应用均可发布为组件，预设系统参数 `query`（String）和 `imageList`（Array<String>），支持在其他智能体或工作流中作为工具节点或组件节点引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 2 在“步骤一：创建应用”示例中直接使用 `千问-Max-Latest` 模型并提及 MCP 服务，但未说明该模型是否仅限 Agent 1.0。结合文档 1 的强约束性声明，应以文档 1 为准：**所有非 API 类发布方式（含组件）仅适用于 Agent 1.0 应用**。若在 Agent 2.0 中尝试发布组件，控制台将不可见对应入口。

## 关键参数

| 参数 | 说明 | 适用场景 |
|------|------|----------|
| `query` | 系统预设文本输入参数，必填，用于传递用户自然语言指令（如“查询杭州天气”） | 所有组件接入场景 |
| `imageList` | 系统预设图像输入参数，非必填，为公网可访问的图片 URL 数组 | 组件启用多模态能力时有效 |
| `biz_param` | API 调用时传入业务参数的字段名，用于透传 `query` 等参数值 | 智能体测试或 API 集成时手动填入 |
| `Token 有效时间` | 音视频实时互动 H5/APP 分享链接的时效控制参数，单位为小时 | 音视频互动发布环节 |
| `传参方式`（业务透传 / 模型识别） | 决定参数由上游显式提供，还是由大模型根据 `参数描述` 自动填充 | 智能体中启用模型识别；工作流中**必须使用业务透传** |

## 使用方式

1. **UI 应用发布**：  
   进入应用管理 → 目标应用卡片 → **发布** → 选择 **UI 应用** → 创建后跳转至 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)，可编辑界面并发布至开发环境（24 小时有效期）或生产环境（需订阅套餐）。

2. **钉钉/微信发布**：  
   在应用 **发布平台** 页签，分别点击对应渠道卡片的 **创建** → 完成第三方平台授权（首次需 SLR + API-KEY 授权）→ 填写凭证（钉钉：模板 ID/Client ID/Secret；微信：AppID）→ 获取回调地址或二维码 → 在钉钉群/微信公众号中配置机器人或客服。

3. **组件发布与引用**：  
   - 发布：在应用 **发布渠道** 页签 → **组件** 区域点击 **+ 创建** → 填写组件名称、描述及参数（注意 `是否可见` 和 `传参方式` 设置）→ **确定发布**；  
   - 引用：  
     - 智能体中：在 **技能** 配置里选择已发布组件，大模型依据描述自动触发；  
     - 工作流中：拖入 **组件节点** → 选择组件 → 显式连接上游节点输出至 `query` 等参数（模型识别在此场景**无效**）。

4. **音视频实时互动**：  
   进入应用 **AI 实时互动** 页签 → 配置 API-KEY → 生成临时体验二维码（24 小时）→ 测试通过后发布 → 开通智能媒体服务并授权 SLR → 选择 H5/APP 分享或 SDK 集成。

## 限制和注意事项

- **Agent 版本限制**：所有 UI、渠道、组件、音视频发布能力**仅限 Agent 1.0**；Agent 2.0 仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发超时，建议单层深度优先；  
  - 工作流中组件参数**必须显式传入**，`模型识别` 方式被忽略 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与计费**：  
  - UI 开发环境链接 24 小时失效，生产环境需订阅团队版及以上套餐；  
  - 所有分享产生的模型调用费用均由应用创建者 UID 承担，与访问者身份无关 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
  - UI 数据（文件/数据库）超出免费额度后按量计费。
- **权限与空间一致性**：UI 设计器、API-KEY、目标智能体/工作流**必须归属同一业务空间**，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


