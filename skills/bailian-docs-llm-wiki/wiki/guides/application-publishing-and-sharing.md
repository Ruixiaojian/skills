# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、第三方平台（钉钉/微信）、可复用组件及音视频实时互动渠道。所有发布行为均需基于已创建并发布的应用，且受 Agent 版本、业务空间隔离和权限模型约束。开发者应根据集成场景选择合适方式，并注意各渠道的参数配置要求与运行限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用仅支持 API 调用，不支持上述任何分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：基于魔笔低代码平台构建，支持拖放式页面搭建、数据库映射、多端适配（PC/H5），并可一键发布至开发或生产环境 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持通过钉钉机器人（需配置 Client ID/Secret、卡片模板 ID 及 `Card.Streaming.Write` 权限）和微信公众号（需 AppID 授权）发布，二者均依赖计算巢 AppFlow 自动化集成服务 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件化能力**：智能体或工作流应用可发布为可复用组件，供其他智能体（作为工具）或工作流（作为节点）引用；组件预设 `query` 和 `imageList` 系统参数，支持 `业务透传` 或 `模型识别` 两种传参方式 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种发布路径，需完成 SLR 授权及智能媒体服务开通 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

> **注意**：文档 1 中称“UI 应用”属于“分享渠道”，而文档 2 明确其为独立低代码 UI 开发能力，且支持从已有应用一键生成 UI。二者逻辑一致，但文档 1 未强调 UI 设计器本身可独立创建应用（非仅“分享”已有应用），易引发误解。实际流程中，UI 应用既可通过“从已有应用发布”快速生成，也可完全独立于智能体/工作流新建 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 调用百炼服务的身份凭证，必须与应用、UI 设计器位于同一业务空间 | 必填；跨业务空间不可见 |
| **钉钉配置** | Client ID / Client Secret / 卡片模板 ID | 钉钉开放平台应用凭证，用于身份鉴权与消息渲染 | 均需在钉钉开放平台获取；`Card.Streaming.Write` 权限必须申请 |
| **微信配置** | AppID（开发者ID） | 微信公众号唯一标识，用于 OAuth 授权 | 必填；需在微信公众号后台「开发接口管理」中获取 |
| **组件参数** | `query`（String, 必填）<br>`imageList`（Array<String>, 非必填） | 预设系统参数，分别承载文本输入与图像 URL 列表 | 不可删除；可通过“是否可见”控制暴露；`imageList` 仅在启用视觉模型时生效 |
| **UI 发布** | 环境（开发/生产） | 开发环境链接 24 小时失效，免费；生产环境需订阅付费套餐并绑定自定义域名 | 生产环境发布前必须完成域名配置与套餐订阅 |

## 使用方式

1. **UI 应用发布**  
   - 进入 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)，选择模板或空白画布 → 配置 API Key 与目标智能体/工作流 → 拖放组件编辑界面 → 点击右上角 **发布** → 选择环境（开发/生产）→ 获取应用地址分享。

2. **第三方平台发布**  
   - 在应用「发布平台」页签，点击对应渠道（钉钉/微信）卡片的 **创建** → 完成 API Key 选择 → 填写平台凭证（Client ID/Secret/模板 ID 或 AppID）→ 提交后获取回调地址（钉钉）或二维码（微信）→ 在对应平台完成机器人配置或扫码接入。

3. **组件发布与引用**  
   - 在应用「发布渠道」页签 → 点击 **组件** 区域的 **+ 创建** → 填写组件名称、描述 → 配置 `query`/`imageList` 等参数的别名、可见性、传参方式（`业务透传` 或 `模型识别`）→ **确定发布**。  
   - 引用时：智能体在「技能」中选择组件；工作流在画布中拖入「组件节点」并选择目标组件 → 按需配置输入（如 `系统变量/query`）。

4. **音视频实时互动**  
   - 在应用「AI 实时互动」页签 → 点击「语音/视频互动」→ 选择 API Key → 生成临时体验二维码（24 小时）→ 测试通过后点击 **发布** → 完成 SLR 授权与智能媒体服务开通 → 选择「H5/APP 扫码」或「SDK 集成」发布。

## 限制和注意事项

- **Agent 版本硬性限制**：所有非 API 方式（UI、钉钉、微信、组件、音视频）均**仅支持 Agent 1.0**；Agent 2.0 应用无法使用这些功能 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **业务空间隔离**：API Key、智能体/工作流应用、UI 设计器必须归属同一业务空间，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发超时（默认最长运行时间限制），建议扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 环境时效性**：开发环境发布的 UI 链接**24 小时后自动失效**，需重新发布；生产环境需订阅付费套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费**：  
  - UI 应用默认仅限阿里云用户访问，可配置匿名访问权限；  
  - 所有调用产生的模型费用由应用创建者 UID 承担；  
  - UI 数据存储（文件/数据库）超出免费额度后按量计费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


