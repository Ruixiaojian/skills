# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括作为可复用组件接入其他AI应用、生成网页UI界面、集成至钉钉/微信等第三方平台，以及启用音视频实时互动能力。所有发布行为均需在统一业务空间下完成，且不同发布渠道对应用版本（Agent 1.0 vs Agent 2.0）有明确兼容性要求。

## 支持的模型/功能

- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体或工作流调用，实现功能复用。组件支持预设系统参数（如 `query`、`imageList`），并可通过别名、描述、可见性、传参方式（业务透传 / 模型识别）精细控制接入逻辑 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI应用**：通过可视化UI设计器构建网页界面，支持拖放式布局、多端适配（PC/H5）、权限管理（匿名访问、OIDC/OAuth 2.0）、数据库与文件存储集成，并一键发布至开发或生产环境 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持将Agent 1.0应用发布至钉钉机器人、微信公众号，需配置API Key、平台凭证（Client ID/Secret、AppID、卡片模板ID等）及回调地址；也支持音视频实时互动（H5/APP扫码体验或SDK集成） [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **模型兼容性**：组件节点、UI应用及第三方渠道均依赖百炼托管模型（如千问-Max-Latest）或MCP服务（如Amap Maps、QuickChart）；音视频互动仅支持图文对话类应用（智能体/工作流），不支持纯语音/视频原生模型。

> **注意**：文档3明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能。**Agent 2.0** 智能体应用仅支持通过 API 调用，不支持上述分享渠道”，而文档1未提及此限制。开发者在选择发布方式前，必须确认目标应用为Agent 1.0版本，否则将无法配置对应渠道。

## 关键参数

| 参数名 | 类型 | 必填 | 用途 | 说明 |
|--------|------|------|------|------|
| `query` | String | 是 | 用户输入文本指令 | 组件默认入参，用于传递自然语言查询（如“查询杭州天气”）；在智能体中启用“模型识别”时由大模型自动填充 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList` | Array<String> | 否 | 图像公网URL列表 | 仅当组件使用图像理解模型时生效；非图像场景需设置“是否可见=否”隐藏该参数 |
| `biz_param` | Object | 否（按需） | 业务透传参数容器 | API调用时传入，用于显式提供`query`等参数值；测试时可在“入参变量配置”中手动填写 |
| API Key | String | 是（UI/第三方渠道必需） | 鉴权凭证 | 必须与应用、UI设计器位于同一业务空间；未正确配置将导致“无法选择API Key”错误 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| 回调地址 / 模板ID / Client ID | String | 是（钉钉/微信必需） | 平台对接凭证 | 钉钉需卡片模板ID + Client ID/Secret；微信需AppID；均需在对应开放平台创建应用后获取 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **发布为组件**  
   - 在应用编辑页点击「发布应用」→ 勾选「发布应用组件」，或进入「组件管理」面板创建；  
   - 配置组件名称、描述、参数别名、传参方式（业务透传/模型识别）及可见性；  
   - 接入智能体：在技能配置中选择组件，大模型根据描述+上下文自动触发；  
   - 接入工作流：拖入「组件节点」，手动连接上游节点输出至`query`等参数。

2. **发布为UI应用**  
   - 方式一：从已有应用发布 → 进入发布渠道 → 选择「UI应用」→ 自动填充基础信息；  
   - 方式二：新建UI → 选模板（如企业AI知识库Lite）→ 配置API Key、智能体、数据库映射 → 拖放组件编辑 → 发布至开发/生产环境；  
   - 开发环境链接24小时失效，生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

3. **分享至第三方平台**  
   - **钉钉/微信**：在应用「发布平台」页签授权计算巢AppFlow → 配置平台凭证 → 获取回调地址/二维码 → 在钉钉群@机器人或微信扫码使用；  
   - **音视频互动**：在「AI实时互动」页签配置API Key → 生成临时体验二维码（24小时有效）→ 发布后支持H5扫码或SDK集成。

## 限制和注意事项

- **版本限制**：仅Agent 1.0支持UI设计器、钉钉/微信发布、组件化及音视频互动；Agent 2.0仅支持API调用，此差异已在文档3中明确，但文档1未警示，开发者务必核验应用版本 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用**：禁止A调用B、B再调用A（循环嵌套），会导致无限递归；A→B→C等三级以上调用易超时，应尽量扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **参数约束**：工作流中即使设置参数为“模型识别”，也不会自动推断值，必须通过上游节点显式传入；智能体中“模型识别”依赖参数描述质量，描述模糊将导致填充失败。
- **环境与计费**：UI开发环境免费但24小时失效；生产环境需付费套餐；模型调用、文件存储（1GB免费）、数据库（0.3GB免费）均按量计费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **业务空间隔离**：API Key、应用、UI设计器必须归属同一业务空间，否则无法关联资源或出现配置项不可见问题。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


