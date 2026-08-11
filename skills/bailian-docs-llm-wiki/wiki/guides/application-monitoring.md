# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪和分析智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、[Token](../concepts/token.md) 消耗、模型思考过程、节点状态等关键指标，并提供数据筛选、标注、导出与评测集集成等功能。所有观测数据以分钟级频率同步至可观测链路 OpenTelemetry 服务，**当前不提供 API 接口**，仅支持控制台交互式使用 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `FullCodeApp` 根节点，**不支持内部链路追踪**）  
- **支持的节点类型**（按应用类型区分）：
  - *智能体应用*：`CHAIN`（如 `AgentApp`）、`AGENT`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`REWRITER`、`EMBEDDING`、`RERANKER`、`LLM`、`TOOL`、`GUARDRAIL`  
  - *工作流应用*：除上述节点外，额外支持 `START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`  
  - *高代码应用*：仅 `CHAIN` 类型下的 `FullCodeApp` 节点，**无子节点展开能力**  
- **核心功能**：调用链追踪（Root/All/Model Span 三种视图）、多维筛选（状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签）、数据标注（布尔/分类/数字/文本）、导出（JSONL/Excel）、监控统计（调用次数、失败率、[Token](../concepts/token.md) 趋势、首 Token 耗时）、添加至评测集（支持字段映射与导入策略）  

> **注意**：[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确说明“暂不支持通过 Assistant API 创建的智能体应用”，该限制未在其他文档中被覆盖或更新，需严格遵守。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或节点；可通过节点详情页「查看 ID」获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `延时`（调用时长） | LLM 节点延时包含流式响应全过程；平均首 Token 耗时专用于流式场景 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token总量` | = 输入 Token + 输出 Token；`EMBEDDING` 节点 Token 量指向量化输入长度 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `标签` | 支持布尔、分类、数字、文本四类标注类型，与评测系统共享标签管理 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（一次性）
1. 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」  
2. 完成三步开通：① 授权可观测链路 OpenTelemetry 服务角色；② 开通 OpenTelemetry 服务；③ 初始化 LogStore 存储  
   > 子账号需额外配置 `AliyunBailianFullAccess` + 页面权限 + `CreateServiceLinkedRole` 策略，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中「常见问题」章节  

### 日常使用流程
1. **添加应用**：在应用观测列表点击「添加」→ 选择已发布且归属当前业务空间的应用  
2. **查看数据**：  
   - 在 Span 列表页使用过滤器（状态、关键词、延时范围、标签等）快速筛选  
   - 切换 Span 视图模式（Root/All/Model）聚焦不同分析粒度  
   - 点击节点名称展开详情，查看原始输入/输出、标注记录、嵌套子节点  
3. **导出与评测**：  
   - 在 Trace 列表页右上角「导出数据」支持 JSONL/Excel  
   - 批量选中 Span → 「添加到评测集」→ 配置目标集、导入方式、字段映射（最多 50 字段）  

## 限制和注意事项

- **功能限制**：  
  - ❌ 不支持 Assistant API 创建的智能体应用  
  - ❌ 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测  
  - ❌ 高代码应用无法观测内部节点，仅显示 `FullCodeApp` 根节点  
  - ❌ 无公开 API，全部操作依赖控制台界面  

- **技术限制**：  
  - 数据同步延迟为分钟级，不支持实时查询  
  - `TextRetriever`/`VectorRetriever` 默认返回 100 个切片，**不可配置数量**  
  - `EMBEDDING` 和 `LLM` 节点的 Token 统计口径不同（前者仅输入，后者为输入+输出）  

- **权限与计费**：  
  - 应用观测功能本身免费，但底层依赖 OpenTelemetry 服务，**存储与查询费用需单独承担**  
  - 子账号开通需主账号预配置 RAM 权限，否则将提示权限不足（参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的「常见问题」）  

> **注意**：高代码应用若开启观测后无统计数据，需确认两点：① 代码中已集成 AgentScope-AI 的 `Tracing` 模块；② 部署时显式启用 `--telemetry enable` 参数 —— 此要求在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 末尾「常见问题」中明确指出，是唯一权威依据。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)


