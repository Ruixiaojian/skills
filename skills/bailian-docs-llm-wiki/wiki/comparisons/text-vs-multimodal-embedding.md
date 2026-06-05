# 文本向量与多模态向量对比

百炼平台同时提供**通用文本向量**（[general text embedding](../api/general-text-embedding.md)）和**多模态向量**（[multimodal vector](../api/multimodal-vector.md)）两套向量化能力，分别面向纯文本场景与跨模态语义场景。两者的模型系列、调用接口、计费方式与适用任务都存在明显差异，本文从开发者技术选型的角度做横向对比，帮助快速决定"用哪一套、用哪个模型"。

## 能力定位

- **通用文本向量**：将纯文本转为高维向量，覆盖中英及 100+ 主流语种与多种编程语言，典型用途为语义检索、聚类、分类、推荐召回等下游 NLP 任务。提供**同步**与**异步批处理**两类接口。
- **多模态向量**：将文本、图像、视频映射到**同一语义空间**，支持以文搜图、以图搜视频、跨模态相似度计算等，并可生成"图文/视文/图视文"融合向量做综合表征。仅提供同步 HTTP 调用方式。

## 关键维度对比

| 维度 | 通用文本向量（[general text embedding](../api/general-text-embedding.md)） | 多模态向量（[multimodal vector](../api/multimodal-vector.md)） |
| --- | --- | --- |
| 输入模态 | 仅文本（字符串、字符串列表、文本文件） | 文本 / 图像 / 视频 / 多图，可混合 |
| 代表模型 | `text-embedding-v4`、`v3`、`v2`、`v1`；批处理 `text-embedding-async-v2/v1` | `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus/flash`（含 `2026-03-06` 版本）、`multimodal-embedding-v1` |
| 向量维度 | v4：64–2048 多档可选；v3：64–1024；v2/v1 与批处理：固定 1536 | 64–2560，按模型不同档位可选；部分模型维度固定（如 `multimodal-embedding-v1` 固定 1024） |
| 向量生成模式 | 单模态文本向量 | **独立向量**（每个输入一个）或**融合向量**（多模态合一） |
| 调用方式 | 同步：OpenAI 兼容 + DashScope 原生；批处理：DashScope 异步任务 | 同步 HTTP（DashScope 原生） |
| API 端点 | 同步：`POST /compatible-mode/v1/embeddings`<br>异步：`POST /api/v1/services/embeddings/text-embedding/text-embedding` + `GET /api/v1/tasks/{task_id}` | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| 输入限制 | 同步 v3/v4：单串/单行 ≤ 8,192 Token，列表/文件 ≤ 10 行；v1/v2：≤ 2,048 Token、≤ 25 行；异步：单文件 ≤ 200MB、≤ 100,000 行、每行 ≤ 2,048 Token | 文本 ≤ 32K Token（部分模型仅 1K/512 Token）；图片单张 ≤ 3–10MB；视频 ≤ 10–50MB；多图最多 8 或 64 张（按模型不同） |
| 关键参数 | `model`、`input`、`dimensions`（仅 v3/v4）、`encoding_format`（仅 `float`）；异步还有 `parameters.text_type=document/query` | `model`、`input.contents`、`parameters.dimension`、`enable_fusion`（仅 `qwen3-vl-embedding`）、`fps`、`instruct`、`res_level`、`max_video_frames` |
| 异步/批处理 | 提供异步批处理接口（结果 URL 仅保留 24 小时） | 不提供异步批处理 |
| SDK 支持 | DashScope Python/Java；同步兼容模式可用 OpenAI SDK | DashScope SDK 与 HTTP 直调 |
| 计费方式 | 按 Token 计费：v3/v4 0.0005 元/千 Token（Batch 0.00025）；v1/v2 0.0007 元/千 Token | 按调用与媒体内容计量（图片/视频按时长或分辨率档位计费），具体以模型详情为准 |
| 区域可用性 | 北京区为主；OpenAI 兼容模式与 DashScope 均可 | 北京区全量；新加坡区仅 `tongyi-embedding-vision-plus` / `flash` |
| 典型下游任务 | 文本语义检索 / RAG 召回、聚类、分类、推荐 | 跨模态检索（文搜图、图搜视频）、内容打标与聚类、商品图文融合表征、相似图/相似视频 |
| 是否跨模态对齐 | 否（仅文本空间） | 是（文本、图像、视频共享语义空间） |

## 适用场景建议

### 优先选择 **通用文本向量** 的情况

- 数据源完全是文本（文章、对话、代码、日志、商品标题/描述等）。
- 需要**最高的语言覆盖**或多语种检索：选 `text-embedding-v4`（Qwen3-Embedding 家族，100+ 语种 + 编程语言）。
- 需要灵活调整向量维度以平衡存储与精度：选 v3/v4，使用 `dimensions` 参数（64–2048）。
- 大文件 / 离线批量向量化（百万级行），对延迟不敏感、希望省一半费用：使用 `text-embedding-async-v2` + DashScope 异步任务，记得 24 小时内下载结果文件。
- 直接接入 OpenAI 生态（已有 `openai` SDK 代码）：使用同步接口的 OpenAI 兼容模式，仅替换 `base_url` 与模型名即可。
- 非对称检索（query → document）：异步接口可通过 `parameters.text_type=query` 区分查询侧编码。

### 优先选择 **多模态向量** 的情况

- 检索/匹配涉及**至少两种模态**（以文搜图、以图搜视频、图文混合相似度等）。
- 需要把"图片 + 描述"或"视频 + 文案"融合成**单一表征向量**入库：选 `qwen3-vl-embedding`（设 `enable_fusion=true`）或 `qwen2.5-vl-embedding`（始终融合）；若需要图、视频、文本三模态混合融合，选 `tongyi-embedding-vision-plus/flash-2026-03-06`。
- 视频帧级语义匹配场景：选支持 `fps`、`max_video_frames` 与 `res_level` 的 `2026-03-06` 版本，按算力/效果取舍。
- 需要在新加坡区部署：仅 `tongyi-embedding-vision-plus` 与 `tongyi-embedding-vision-flash` 可用。
- 想以最小成本验证多模态检索 PoC：选 `tongyi-embedding-vision-flash` 或 `multimodal-embedding-v1`（维度固定，简单稳定）。

### 混合场景的搭配建议

- **图文电商搜索**：商品图与描述使用多模态融合向量入库；纯关键词/长文搜索通道仍可叠加 `text-embedding-v4` 做文本召回，再做跨模态融合排序。
- **跨语言文档 + 截图知识库**：长文本走 `text-embedding-v4`（多语种覆盖广、维度灵活）；截图/示意图走多模态向量；两路召回后再做融合重排。
- **离线大批量预处理 + 在线交互**：离线侧用 `text-embedding-async-v2` 处理历史语料；在线新增数据用同步 `text-embedding-v4` 或多模态模型即时向量化。

## 技术选型速查

- 输入只有文本 → **通用文本向量**（默认 `text-embedding-v4`，多语种/多维度首选）。
- 输入含图/视频，或需要"图文一起编码" → **多模态向量**（`qwen3-vl-embedding` 优先，融合可关可开）。
- 单次请求 ≤ 25 行、对维度无要求且只用经典模型 → `text-embedding-v2/v1`。
- 单文件几万到十万行的离线场景 → 通用文本向量的**批处理接口**。
- 新加坡区域调用 → 多模态侧只能用 `tongyi-embedding-vision-plus` / `flash`；文本侧无此限制。
- 想要 OpenAI 接口零成本迁移 → 通用文本向量的同步 OpenAI 兼容模式。

总体原则：**模态决定路线，规模与延迟决定接口，模型版本决定维度与上下文长度**。先按模态二选一定下技术栈，再按数据量与延迟在"同步 / 异步"之间挑接口，最后基于上下文长度、维度档位与计费选择具体模型版本即可。

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [multimodal vector](../api/multimodal-vector.md)


