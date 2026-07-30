# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括对外提供 UI 界面、集成至钉钉/微信等第三方平台、作为可复用组件被其他智能体或工作流调用，以及通过音视频实时互动渠道部署。所有发布行为均需基于已创建并发布的应用，且不同发布方式对应用类型（如 Agent 1.0 vs Agent 2.0）有明确兼容性要求。

## 支持的模型/功能

- **适用应用类型**：仅 [Agent 1.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 支持魔笔 UI、钉钉、微信、组件、音视频实时互动等全部发布渠道；[Agent 2.0 智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 仅支持 API 调用，不支持上述 UI 或渠道类发布方式。
- **组件能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）接入使用，实现功能模块化复用。
- **UI 应用**：通过 [UI 设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将已发布的智能体或工作流快速封装为网页应用，支持 PC/H5 多端访问，并内置权限管理、数据库映射与一键发布能力。
- **实时互动**：图文类智能体/工作流应用可发布为语音或视频互动应用，支持扫码体验、H5/APP 分享及 SDK 集成。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 传参方式 |
|--------|------|----------|------|-----------|
| `query` | `String` | 是 | 用户原始输入文本（如“查询杭州天气”） | 支持 `业务透传`（由调用方显式传入）或 `模型识别`（仅在智能体中由大模型自动推断） |
| `imageList` | `Array<String>` | 否 | 图像公网 URL 列表，仅当组件使用图像理解模型时生效 | 仅支持 `业务透传`；`模型识别` 方式在此参数上无效 |
| `biz_param` | `Object` | 否（按需） | API 调用时用于传递 `query` 等业务参数的顶层字段 | 必须在 HTTP 请求 body 中显式构造，例如 `{ "biz_param": { "query": "..." } }` |

> **注意**：文档 1 与文档 2 均指出，当组件接入工作流时，即使参数配置为 `模型识别`，系统也不会自动填充其值——必须通过上游节点显式传入。该行为一致，无矛盾。

## 使用方式

### 发布为组件
1. 在应用编辑页点击 **发布应用** → 勾选 **发布应用组件**，或进入 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 页面手动创建；
2. 配置组件名称、描述及参数（含别名、是否可见、是否必填、传参方式）；
3. 发布后，组件自动随源应用更新（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。

### 接入组件
- **在智能体中**：于技能配置中选择已发布组件；大模型根据组件描述与上下文自动决定是否调用；若含 `业务透传` 参数，测试时需在“入参变量配置”中填写，或 API 调用时通过 `biz_param` 传入。
- **在工作流中**：拖入“组件节点”，选择目标组件，连接上游节点，并在“输入”字段绑定变量（如 `系统变量/query`）。

### 发布为 UI 应用
1. 进入应用发布渠道页，选择 **UI 应用** → **创建**，或直接访问 [UI 设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) 新建；
2. 选择模板（如“AI基础对话”），填写应用名称、API Key、目标智能体/工作流；
3. 编辑界面后，点击 **发布** → 选择 **开发环境**（24 小时有效，免费）或 **生产环境**（需订阅套餐）；
4. 获取 **应用地址** 分享给用户，支持匿名访问配置（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。

### 第三方平台发布
- **钉钉/微信**：需先授权计算巢 AppFlow，配置 API Key、平台凭证（Client ID/Secret、模板 ID 等），生成回调地址或二维码；
- **音视频实时互动**：在应用“AI实时互动”页签配置，生成临时体验二维码或 SDK 集成方案。

## 限制和注意事项

- **版本兼容性**：仅 Agent 1.0 应用支持 UI、钉钉、微信、组件、音视频等发布方式；Agent 2.0 应用仅支持 API 调用，此限制在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确强调。
- **嵌套与多级调用**：禁止 A 调用 B 同时 B 调用 A（循环依赖），否则导致无限递归；A→B→C 等多级调用易触发超时，应尽量扁平化设计（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。
- **环境与配额**：UI 应用开发环境链接 24 小时失效；生产环境需订阅付费套餐；文件存储与数据库超出免费额度（1GB 文件 / 0.3GB 数据库）将按量计费（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **业务空间一致性**：UI 设计器中使用的 API Key、智能体/工作流必须与 UI 所属 **同一业务空间**，否则无法关联（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


