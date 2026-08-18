# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信渠道、可复用组件及音视频实时互动等形态，便于集成至业务系统或面向终端用户交付。所有发布行为均需基于已创建并发布的应用，且不同发布方式对应用类型、模型能力及权限配置有明确约束。开发者应根据目标场景选择适配的发布路径，并注意各渠道的计费主体与运行限制。

## 支持的模型/功能

- **仅限 Agent 1.0 应用**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何 UI 或渠道类发布方式，仅可通过 API 调用接入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用兼容性更广**：UI 设计器不仅支持接入 Agent 1.0，也支持接入已发布的**工作流应用**，但需确保二者与 UI 所属业务空间一致 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件来源双轨制**：智能体应用和工作流应用均可发布为组件，且组件可在智能体或工作流中被引用——该能力在 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中有完整说明。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 3 在“准备工作”中强调“智能体应用或工作流应用”均可集成至 UI，但未限定 Agent 版本；结合文档 1 的强约束，实际开发中若选用 Agent 2.0，则无法使用 UI、钉钉、微信等所有非 API 发布方式，此为关键兼容性边界，不可忽略。

## 关键参数

| 参数 | 说明 | 使用场景 | 约束 |
|------|------|----------|------|
| `query`（系统预设） | 用户输入的文本指令，类型为 `String`，默认必填 | 所有组件接入场景（智能体/工作流） | 不可删除；如不需使用，须设为“是否可见=否” |
| `imageList`（系统预设） | 用户上传的图像公网地址列表，类型为 `Array<String>`，默认非必填 | 组件调用图像理解模型时生效 | 仅当组件底层模型支持多模态时有效 |
| `biz_param`（API 调用专用） | 用于透传业务参数的 JSON 对象，在 API 请求体中传递 | 智能体组件需“业务透传”参数时的 API 调用方式 | 仅适用于 HTTP API 调用，UI/钉钉/微信等渠道不支持该字段 |
| 回调地址 / Token / 分享链接 | 各渠道唯一访问入口，含时效性与权限控制 | 钉钉机器人、微信公众号、H5/APP 体验、SDK 集成 | UI 开发环境链接有效期为 24 小时；生产环境链接长期有效 |

## 使用方式

1. **统一入口**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面的目标应用卡片进入，点击 **发布** 或切换至对应页签（如“发布平台”、“AI实时互动”、“组件”）。
2. **四类主流发布路径**：
   - **UI 应用**：通过“UI 应用”卡片创建，自动关联已有智能体/工作流，经 UI 设计器编辑后发布至开发/生产环境，生成可分享的网页链接 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；
   - **钉钉/微信渠道**：需先完成第三方平台授权（SLR + API-KEY），再配置钉钉 Client ID/Secret/模板 ID 或微信 AppID，最终获取回调地址或客服二维码；
   - **组件发布**：在“组件”卡片中创建，需明确定义组件名称、描述、参数别名、传参方式（`业务透传` 或 `模型识别`）及可见性，发布后可在其他智能体/工作流中作为节点或工具引用；
   - **音视频实时互动**：仅支持图文类应用（智能体/工作流），需配置 API-KEY 后生成临时体验二维码或正式发布至 H5/APP/SDK 渠道。
3. **组件接入差异**：
   - 在**智能体中引用组件**时，若参数设为 `模型识别`，大模型会基于上下文与参数描述自动填充值；
   - 在**工作流中引用组件**时，无论传参方式如何，**必须由上游节点显式提供输入值**，`模型识别` 不生效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 限制和注意事项

- **Agent 版本硬限制**：所有非 API 类发布方式（UI、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**，Agent 2.0 应用无法出现在对应发布页签中，强行尝试将失败。
- **组件调用风险**：
  - 禁止 A → B → A 的**嵌套调用**，会导致无限循环与服务不可用；
  - A → B → C 的**三级及以上调用链**易触发超时（默认最长运行时间受限），建议扁平化设计；
  - 组件发布后，其底层应用若重新发布，组件将**自动更新**，需确保变更向后兼容。
- **环境与权限约束**：
  - UI 应用开发环境链接**24 小时失效**，生产环境需订阅付费套餐并绑定自定义域名；
  - 所有分享链接（UI、钉钉、微信）的访问者产生的模型调用费用，**均由应用创建者 UID 账号承担**；
  - UI、钉钉、微信等渠道均要求应用、API-KEY、UI 设计器三者处于**同一业务空间**，跨空间将导致资源不可见。
- **计费提示**：UI 设计器本身免费，但模型调用、文件存储（1GB 免费）、数据库（0.3GB 免费）及生产环境发布均按量计费，详情见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 计费说明。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


