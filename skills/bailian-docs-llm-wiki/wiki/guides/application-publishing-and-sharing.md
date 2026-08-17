# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括对外提供 UI 界面、集成至钉钉/微信等第三方平台、作为可复用组件被其他智能体或工作流调用，以及接入音视频实时互动场景。所有发布行为均基于已创建并发布的应用，且需注意 Agent 版本兼容性与运行时约束。

## 支持的模型/功能

- **支持的应用类型**：仅 [Agent 1.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 支持全部发布渠道（UI 应用、钉钉、微信、组件、音视频互动）；[Agent 2.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 仅支持 API 调用，不支持上述分享渠道。
- **组件能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）接入使用，实现功能复用。组件支持预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），详见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用能力**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将智能体或工作流快速封装为网页应用，支持拖放式低代码搭建、多端适配（PC/H5）、权限控制及一键发布至开发/生产环境。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 传参方式 |
|--------|------|----------|------|-----------|
| `query` | String | 是 | 用户输入的自然语言指令（如“查询杭州天气”） | 支持 `业务透传`（由调用方显式传入）或 `模型识别`（仅在智能体中生效，由大模型从上下文推断） |
| `imageList` | Array<String> | 否 | 图像公网 URL 列表，仅当组件内部使用图像理解模型时有效 | 仅支持 `业务透传`；`模型识别` 方式下该参数不可用 |
| `biz_param` | Object | 否（按需） | API 调用时用于传递业务透传参数的顶层字段，结构为 `{ "param_name": "value" }` | 仅适用于 API 调用场景，不适用于 UI 或工作流节点配置 |

> **注意**：文档 1 与文档 2 均指出“工作流中即使设置 `模型识别`，也不会自动填充参数”，但文档 1 在“步骤三：配置组件名称和参数”中未明确强调此限制，而文档 2 在“发布应用为组件”小节中重复强调该行为，应以文档 2 的表述为准。

## 使用方式

### 发布为组件
1. 进入智能体或工作流应用编辑页 → 点击 **发布** → 在 **发布渠道** 页签点击 **组件** 区域的 **创建**；
2. 配置组件名称、描述，并为 `query` 和 `imageList` 设置别名、参数描述、是否可见、是否必填及传参方式；
3. 发布后，可在其他智能体的 **技能** 中选择该组件，或在工作流画布中拖入 **组件节点** 并关联。

### 发布为 UI 应用
1. 在应用发布渠道页签选择 **UI 应用** → **创建**，系统自动填充基础信息（API Key、智能体、图标等）；
2. 或前往 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → **创建UI** → 选择模板 → 绑定百炼应用与 API Key → 编辑界面 → **发布**；
3. 发布后获取 **应用地址**（开发环境链接有效期 24 小时），可直接分享给阿里云用户访问。

### 集成至第三方平台
- **钉钉/微信**：需先授权计算巢 AppFlow，配置对应平台的 Client ID/Secret、模板 ID（钉钉）或 AppID（微信），再生成回调地址或客服二维码；
- **音视频实时互动**：仅支持图文类应用（智能体/工作流），需配置 API Key，生成临时体验二维码或 SDK 集成方案。

## 限制和注意事项

- **版本限制**：Agent 2.0 不支持除 API 外的任何发布渠道，强行尝试将导致配置不可见或失败 —— 此限制在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确声明。
- **嵌套与多级调用**：组件间禁止 A→B→A 的循环调用，否则导致无限递归；A→B→C 的三级及以上调用易触发超时（默认最长运行时间受限），建议控制在两层以内。
- **组件自动更新**：应用重新发布后，其已发布的组件将**自动同步更新**，无需手动重发 —— 此特性在 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中说明，开发者需确保更新不影响下游依赖。
- **环境隔离**：UI 应用的开发环境链接 24 小时失效，生产环境需订阅付费套餐并绑定自定义域名；所有分享链接产生的费用均由应用创建者 UID 账号承担。
- **业务空间一致性**：UI 设计器、API Key 与目标智能体/工作流必须归属于同一 [业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)，否则无法在 UI 创建流程中选中对应资源 —— 此要求在 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 的“准备工作”中强调。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


