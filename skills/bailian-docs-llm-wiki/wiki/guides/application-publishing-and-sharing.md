# application publishing and sharing

百炼平台提供多种应用发布与共享能力，支持将智能体、工作流等 AI 应用以 UI 网页、钉钉/微信机器人、可复用组件、音视频实时互动等形式对外交付。所有发布行为均需在统一业务空间内完成，且依赖已发布的应用和有效的 API Key。发布后的应用默认由创建者承担全部调用费用。

## 支持的模型/功能

- **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可视化构建网页界面，支持 PC/H5 多端适配，集成智能体、工作流、数据库、HTTP 服务等资源。
- **渠道分享**：支持魔笔（即 UI 应用）、钉钉机器人、微信公众号三种外部平台分发方式，**仅限 Agent 1.0 智能体应用**；Agent 2.0 不支持此类渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件化复用**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：支持图文类智能体/工作流接入语音或视频通话场景，提供 H5/APP 扫码体验及 SDK 集成路径，适用于客服、培训等实时交互场景。

> **注意**：文档 2 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能”，而文档 3 中“发布应用为组件”未限定 Agent 版本，但实际组件发布入口与调用逻辑均基于 Agent 1.0 的技能体系。若尝试对 Agent 2.0 应用执行组件发布操作，控制台将不可见或报错——此为隐含限制，开发者应以文档 2 的版本约束为准。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `API Key` | 调用百炼服务的认证凭证，**必须与应用、UI 设计器同属一个业务空间** | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 强调“百炼应用、API Key 和 UI 设计需要归属于**同一**业务空间” |
| `query`（系统参数） | 组件默认接收的文本输入参数，类型为 `String`，建议设为必填 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 规定其为预设参数，不可删除 |
| `imageList`（系统参数） | 组件默认接收的图像 URL 列表参数，类型为 `Array<String>`，仅在启用多模态模型时生效，可设为非必填并隐藏 | 同上文档，明确说明“预设的系统参数无法删除”，需通过“是否可见”控制暴露 |
| `传参方式`（业务透传 / 模型识别） | 决定参数值由上游显式传递（业务透传）还是由大模型自动推断（模型识别）；**工作流中即使设为模型识别，也必须显式传入值** | [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 与 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 均强调该差异 |

## 使用方式

1. **UI 应用发布流程**  
   - 进入应用详情页 → 发布渠道 → 选择 **UI 应用** → 创建（自动填充基础信息）或从零开始使用 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；  
   - 编辑完成后，点击右上角 **发布** → 选择 **开发环境**（24 小时有效，免费）或 **生产环境**（需订阅团队版套餐，支持自定义域名）；  
   - 发布后获取 **应用地址**，可直接分享给阿里云用户访问。

2. **第三方平台分享**  
   - 在应用 **发布渠道** 页签，选择对应平台（钉钉/微信/音视频）→ 完成授权（SLR + API Key 加密传输）→ 配置平台凭证（如钉钉 Client ID/Secret、微信 AppID）→ 获取回调地址或二维码；  
   - 钉钉需额外配置机器人消息接收模式为 **HTTP 模式**（Stream 模式不兼容），微信需生成并分发客服二维码。

3. **组件发布与引用**  
   - 发布：在应用编辑页点击 **发布应用** → 勾选 **发布应用组件**，或进入 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 页面手动创建；  
   - 引用：  
     - *智能体中*：在“技能”中选择组件，大模型根据组件描述与上下文自动触发；  
     - *工作流中*：拖入“组件节点”，手动连接上游节点并指定输入变量（如 `系统变量/query`）。

## 限制和注意事项

- **业务空间强绑定**：API Key、智能体/工作流应用、UI 设计器操作必须位于同一业务空间，跨空间操作将导致资源不可见或配置失败 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **环境有效期**：开发环境发布的 UI 应用 **24 小时后自动失效**，需重新发布；生产环境长期有效但需付费订阅 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：  
  - 禁止 A 调用 B、B 又调用 A 的**嵌套调用**，会导致死循环；  
  - 多级调用（A→B→C）易触发运行超时，应尽量扁平化设计 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 与 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 均明确警示。
- **文件参数特殊处理**：若工作流应用含文件类自定义参数，需在 UI 设计器中显式配置 `{{{file_name:files[0]}}}`（`file_name` 替换为实际变量名），否则 UI 上传文件无法被正确解析 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


