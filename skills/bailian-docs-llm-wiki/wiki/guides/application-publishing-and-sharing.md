# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种形态发布与共享，包括作为可复用的模块化组件、嵌入式 UI 应用、第三方平台（钉钉/微信）机器人、以及音视频实时互动服务。所有发布行为均基于已创建并发布的应用，且需注意 Agent 1.0 与 Agent 2.0 在分享能力上的关键差异。核心目标是实现 AI 能力的标准化封装、安全可控分发与跨场景集成。

## 支持的模型/功能

- **支持的应用类型**：仅 [Agent 1.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 支持全部发布渠道（UI 应用、钉钉、微信、组件、音视频互动）；[Agent 2.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 仅支持 API 调用，**不支持任何 UI 或第三方平台分享渠道**。
- **组件能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）接入复用。组件支持预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），并可通过别名、描述、可见性及传参方式（业务透传 / 模型识别）精细化配置。
- **UI 应用能力**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将智能体或工作流快速封装为网页应用，支持拖放式低代码构建、多端适配（PC/H5）、权限管理（含匿名访问）及一键发布至开发/生产环境。
- **第三方集成**：支持发布为钉钉机器人（需配置 Client ID/Secret、卡片模板 ID）、微信公众号客服（需 AppID 授权）及音视频实时互动（H5/APP 扫码或 SDK 集成）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源约束 |
|------|------|------|------|----------|
| `query` | String | 是 | 用户原始输入文本，用于触发组件逻辑（如“查询杭州天气”） | 所有组件默认预设，不可删除；在 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中明确定义 |
| `imageList` | Array<String> | 否 | 用户上传图像的公网 URL 列表，仅当组件使用视觉模型时生效 | 同上，预设但可隐藏 |
| `biz_param` | Object | 否（按需） | API 调用时传递业务透传参数的顶层字段，例如 `{"userQuery": "杭州天气"}` | 仅在 API 场景下使用，见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 测试说明 |
| `callback_url` | String | 是（钉钉/微信） | 百炼生成的回调地址，用于接收钉钉/微信平台的用户消息 | 由 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 发布流程自动生成 |

> **注意**：文档 1 与文档 2 均指出工作流中设置为“模型识别”的参数**不会被自动推断**，必须显式传入；但文档 1 的示例配置中未体现该强制要求，而文档 2 明确强调“您**必须**像业务透传一样……明确地为该参数提供输入值”。此处以文档 2 的表述为准，开发者需在工作流节点配置中手动绑定上游变量。

## 使用方式

1. **发布为组件**  
   - 进入应用编辑页 → 点击**发布应用** → 勾选**发布应用组件** → 配置组件名称、描述、参数别名/描述/可见性/传参方式 → 确认发布。  
   - 或进入 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) → **+ 创建** → 选择已有应用。  
   - 组件发布后自动随原应用更新（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 注意事项）。

2. **发布为 UI 应用**  
   - 方式一（从应用发布）：应用发布页 → **UI 应用** → **创建** → 自动填充基础信息（API Key、智能体等）→ **立即创建**。  
   - 方式二（UI 设计器新建）：[UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → **创建UI** → 选模板 → 填写应用名/API Key/智能体 → 编辑组件 → **发布**至开发/生产环境（开发环境链接 24 小时失效）。

3. **发布至第三方平台**  
   - **钉钉/微信**：应用发布页 → 对应卡片 → **创建** → 完成授权（SLR + API Key）→ 配置平台凭证（Client ID/Secret/模板 ID 或 AppID）→ 获取回调地址/二维码 → 在钉钉/微信侧完成机器人配置。  
   - **音视频互动**：应用发布页 → **AI实时互动** → 选语音/视频 → 配置 API Key → 生成体验二维码（24 小时）→ **发布**后开通智能媒体服务并授权 SLR。

## 限制和注意事项

- **Agent 版本限制**：仅 Agent 1.0 支持 UI、钉钉、微信、组件、音视频等发布方式；Agent 2.0 仅支持 API，此限制在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确声明。
- **组件调用风险**：  
  - **禁止嵌套调用**（A→B→A）：导致无限循环，功能不可用；  
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时失败（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 注意事项）。
- **环境与权限**：UI 设计器、API Key、智能体/工作流应用**必须归属同一业务空间**，否则无法关联（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 准备工作）。
- **开发环境时效性**：UI 应用发布至开发环境后，链接**24 小时后自动失效**，需重新发布；生产环境需订阅付费套餐并绑定自定义域名（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 发布说明）。
- **计费责任**：所有通过分享链接产生的模型调用、存储等费用，均由应用创建者 UID 账号承担（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 访问权限说明）。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


