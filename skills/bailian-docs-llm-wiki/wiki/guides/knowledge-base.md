# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。它支持多源数据接入、语义检索、多模态理解及灵活的 API 集成，适用于文档问答、智能客服、知识管理等场景。所有知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持预置与自定义两类模型，覆盖文本、多模态及音视频场景。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义模型需基于上述基座调优后方可使用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
功能上，知识库分为四类：**文档搜索**（支持 PDF/DOCX/图片/音视频等非结构化数据）、**数据查询**（Excel/CSV 表格结构化检索）、**图片问答**（多模态图文理解）、**音视频搜索**（语音识别+帧提取+剧情解析）。其中，「视觉理解」使用场景自动绑定 `qwen3-vl-embedding` 向量模型，不可更改 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
此外，平台提供配套服务：**知识检索**（多知识库联合混排，最多 15 个）、**知识问答**（绑定模型生成自然语言回答，支持极速/多轮智能两种模式）以及**定时数据同步**（OSS/飞书/钉钉/语雀/SharePoint 自动增量同步） [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

> **注意**：文档 2 和文档 6 均声明知识库仅支持华北2（北京）地域，但文档 4 的日志服务示例链接中包含 `cn-beijing` 路径，而文档 8 和 9 的控制台 URL 中部分含 `?tab=app#/knowledge-base/list?activeKey=retrieval`，路径结构不一致。实际部署必须严格遵循地域限制，跨地域调用将失败。

## 关键参数

| 参数类别 | 参数名 | 取值范围/说明 | 关联场景 |
|----------|--------|----------------|----------|
| **索引配置** | Meta信息抽取 | 创建时配置，不可修改；支持常量/正则/字段映射等方式提取 `date`/`filename`/`author` 等元数据 | [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 中明确指出“知识库一旦创建，无法再配置 metadata 抽取” |
| **检索控制** | 相似度阈值 | 0.01–1.0；值越高召回越严格，但可能漏召；默认值未统一（文档 2 提及可设，文档 8/9 默认未说明） | 影响最终返回切片质量，需通过命中测试反复调优 |
| **性能规格** | 检索并发（QPS） | 标准版固定 1 QPS；旗舰版 50–10,000 QPS（对应 1–200 RCU） | [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) 与 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) 均确认该规格 |
| **召回控制** | 初步向量 TopK / 关键词 TopK | 各 1–100；控制向量与关键词双路召回的初始切片数 | 文档 8 和 9 统一规定此范围，且明确“仅基础文档问答与表格库可用” |
| **安全与生成** | 拒答 / 防泄漏 / 引用 | 开关型配置；启用后可自定义话术或触发条件 | [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) 中详细定义其行为逻辑 |

## 使用方式

### 控制台操作
1. **创建知识库**：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面 → 选择标准版/旗舰版 → 填写名称/描述 → 选择类型（如文档搜索）→ 配置数据来源（本地上传或云端导入）→ 设置索引参数（含 Meta 抽取、多轮对话改写等）→ 完成。
2. **集成应用**：
   - *智能体应用*：在应用配置页 → 文档知识库 → + 添加知识库 → 设置相似度阈值与权重。
   - *工作流应用*：拖入「知识库」节点 → 配置输入（如 `query`）、知识库选择方式（固定/动态）、TopK → 连接下游大模型节点 → 在提示词中插入 `{result}` 变量。
3. **高级服务**：在知识库列表页切换至「知识检索」或「知识问答」标签页 → 创建服务 → 绑定多个知识库 → 配置混排模型、路由、标签过滤等参数 → 发布。

### API 集成
需完成前置准备：子账号获取 `AliyunBailianDataFullAccess` 权限并加入业务空间；安装最新版百炼 SDK；配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET` 和 `WORKSPACE_ID` 环境变量 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。核心流程包括：申请文件上传租约 → 上传文件 → 添加文件到类目 → 创建索引 → 提交索引任务 → 等待完成。所有 API 调用均需指定 `workspace_id`，且仅支持文档搜索类知识库 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能强制限定于华北2（北京），其他地域（如新加坡、法兰克福）完全不可用，控制台与 API 均会拒绝请求。
- **存储与配额**：标准版免费额度仅抵扣规格费用（720 小时/用户），不覆盖模型调用费；旗舰版按 RCU 小时计费，变配每日限 1 次；单知识库文件数量无硬上限，但业务空间总文件数上限为 100,000 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **同步与更新**：OSS/飞书/钉钉等同步规则创建后，源文件删除**不会**触发百炼副本自动删除，必须手动清理；同步周期越短（如 1 分钟），钉钉 API 配额消耗越快，需提前评估 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。
- **模型费用独立计费**：向量模型（`text-embedding-v4`/`qwen3-vl-embedding`）、排序模型（`qwen3-rerank`）、路由模型（`qwen-plus`）及问答模型（`qwen3.7-plus`）的 [Token](../concepts/token.md) 消耗单独计费，不包含在知识库规格费用中，且多知识库场景下费用线性叠加 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **调试与监控**：检索日志投递至 SLS，需手动开通并配置 LogStore；日志字段含 `pipeline_id`（知识库 ID）、`latency`、`response_code` 等，可用于用量统计与错误排查 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)


