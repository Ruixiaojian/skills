# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括对外分发为 UI 应用、集成至钉钉/微信等第三方平台、封装为可复用组件，以及接入音视频实时互动场景。所有发布行为均基于已创建并发布的应用，且需注意 Agent 版本兼容性与环境依赖约束。

## 支持的模型/功能

- **适用应用类型**：仅支持 **Agent 1.0 智能体应用** 和 **工作流应用**；Agent 2.0 应用不支持魔笔分享、钉钉/微信发布、UI 应用及组件发布等渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件能力**：智能体或工作流均可发布为模块化组件，供其他智能体或工作流作为工具节点或技能接入，实现跨应用功能复用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将智能体或工作流封装为网页级交互界面，支持拖放式低代码构建、权限配置与一键发布至开发/生产环境。
- **第三方平台集成**：支持发布至钉钉机器人、微信公众号（需 API Key 与对应平台凭证）、音视频实时互动（H5/APP 扫码或 SDK 集成）。

> **注意**：文档 2 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能”，而文档 1 中未限定 Agent 版本即默认按此执行；若开发者尝试在 Agent 2.0 应用中操作组件发布或 UI 发布，将失败或无响应，该限制需严格遵守。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 传参方式 |
|--------|------|------|------|-----------|
| `query` | `String` | 是 | 用户原始输入文本（如“查询杭州天气”） | 支持 `业务透传`（上游显式传入）或 `模型识别`（仅智能体中由大模型自动推断） |
| `imageList` | `Array<String>` | 否 | 图像公网 URL 列表，仅当组件使用视觉模型时生效 | 仅支持 `业务透传`；`模型识别` 方式对图像参数无效 |
| `biz_param` | `Object` | 否（API 场景） | API 调用时传递业务透传参数的顶层字段，用于覆盖组件配置中的 `业务透传` 参数 | 仅适用于 HTTP API 调用，不适用于 UI 或工作流节点配置 |

- **别名（Alias）**：必须为每个入参设置唯一别名，调用方仅可见别名，不可见原始参数名（如 `query` → `userQuery`）。
- **是否可见**：控制参数是否在调用方界面透出，建议对非目标模型使用的参数（如文本组件隐藏 `imageList`）设为“否”。
- **默认值**：仅在 `业务透传` 模式下生效，用于兜底填充；`模型识别` 模式下忽略默认值。

## 使用方式

### 1. 发布为组件
- 进入应用编辑页 → 点击 **发布应用** → 勾选 **发布应用组件** → 在弹窗中点击 **立即发布**；或进入 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) → **+ 创建** → 选择已有应用。
- 配置组件名称、描述（影响智能体自动调用决策）、参数别名与传参方式后确认发布 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

### 2. 接入组件
- **智能体中**：在“技能”区域添加已发布组件，大模型根据 `query` 描述与上下文自动触发调用；含 `业务透传` 参数时，需在测试页手动填入 `入参变量配置` 或 API 调用时传 `biz_param`。
- **工作流中**：拖入 **组件节点** → 选择目标组件 → 在“输入”字段绑定上游变量（如 `系统变量/query`）→ 输出结果通过 `组件1/result` 传递至下游节点。

### 3. 发布为 UI 应用
- 从应用发布页选择 **UI 应用** → **创建**，系统自动填充 API Key 与智能体；或直接进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → **创建UI** → 选择模板 → 绑定百炼 API Key 与已发布应用 → 编辑页面 → **发布** 至开发/生产环境 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

### 4. 第三方平台发布
- **钉钉/微信**：在应用 **发布平台** 页签授权计算巢 AppFlow → 配置对应平台凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码 → 在目标平台完成机器人配置与发布。
- **音视频互动**：在 **AI实时互动** 页签配置 API Key → 生成临时体验二维码（24 小时有效）→ 发布后开通智能媒体服务并完成 SLR 授权。

## 限制和注意事项

- **Agent 版本限制**：所有分享渠道（魔笔、钉钉、微信、UI、组件、音视频）仅支持 Agent 1.0；Agent 2.0 仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件调用限制**：
  - **禁止嵌套调用**：A 调用 B 且 B 调用 A 会导致无限循环，功能不可用。
  - **慎用多级调用**：A→B→C 等链路受最长运行时间限制，易超时失败。
  - **工作流中 `模型识别` 无效**：即使参数设为 `模型识别`，工作流仍需上游显式传参，否则报错 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用时效性**：开发环境发布的 UI 链接 **24 小时后失效**，需重新发布；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **业务空间一致性**：UI 设计器、API Key、智能体/工作流应用必须归属于同一 [业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **费用归属**：所有通过分享链接产生的模型调用、存储等费用，均由应用创建者 UID 账号承担 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


