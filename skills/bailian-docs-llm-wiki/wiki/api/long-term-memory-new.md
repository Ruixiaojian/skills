# long term memory new

[长期记忆](../concepts/memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持将对话内容自动提炼为语义记忆片段，并提供增删改查、语义搜索与用户画像构建等核心功能。其设计面向 Agent 场景，强调低侵入性接入与高语义召回精度。所有接口均基于 RESTful API 实现，需通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`（自动提取）、`SearchMemory`（语义检索）、`ListMemory`（分页查询）、`DeleteMemory`、`UpdateMemory`  
- **用户画像能力**：通过 `CreateProfileSchema` / `GetUserProfile` 等接口支持自定义画像模板与动态画像生成  
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合召回  
- **配套 SDK**：`agentscope-runtime>=1.1.5` 提供 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 的异步封装；`UpdateMemory` 暂未封装，需直接调用 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 PATCH 接口  

> **注意**：原始文档中 `UpdateMemory` 的 Python 示例明确说明“Python SDK 暂未提供此接口的封装”，而其他接口均有对应类封装，该差异需开发者自行处理。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆实体标识符（≤64 字符），所有操作均以此为归属维度 |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（一问一答计 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认记忆库 |
| `top_k`（Search） | integer | 否 | 召回数量，默认 10，范围 1–100 |
| `min_score`（Search） | double | 否 | 相似度阈值，默认 0.3，范围 [0,1] |
| `page_num` / `page_size`（List） | integer | 否 | 分页参数，默认 `page_num=1`, `page_size=10` |

## 使用方式

1. **认证**：在请求 Header 中设置 `Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 获取见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）  
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`  
3. **典型流程**：  
   - 调用 `AddMemory` 提交对话或自定义文本 → 获取 `memory_node_id`  
   - 调用 `SearchMemory` 传入当前对话上下文 → 获取相关记忆片段  
   - （可选）调用 `ListMemory` 或 `GetUserProfile` 进行状态审计  
4. **SDK 快速接入**（推荐）：  
   ```python
   from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
   # 初始化后调用 arun()，详见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 示例
   ```

## 限制和注意事项

- **限流策略（阿里云账号级）**：全部接口总计 ≤3000 QPM；`/add` ≤120 QPM；`/memory_nodes/search` ≤300 QPM  
- **数据时效性**：生成的记忆片段与用户画像**暂无自动失效机制**，需业务层自行管理生命周期  
- **内容长度**：`custom_content` 和 `messages` 提取后的 `content` 字段均 ≤512 字符  
- **字段覆盖逻辑**：`UpdateMemory` 的 `meta_data` 为**增量更新**（非全量替换），而 `custom_content` 会完全覆盖原内容  
- **路径参数安全**：`DeleteMemory` 和 `UpdateMemory` 的 `memory_node_id` 需严格校验合法性，避免越权操作  
- **兼容性提示**：`SearchMemory` 的 `enable_rerank`、`enable_judge`、`enable_rewrite` 均默认 `false`，开启前请确认对应能力已开通，否则可能返回空结果或报错

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)


