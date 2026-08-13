# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保持可用推理能力的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/#73749f1ee5634)之后、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-1/#3bc53b23c7shc)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成微调训练的自定义模型**，不支持基础模型（如原始 Qwen 系列）或第三方导入模型。
- 当前明确支持的模型示例：`qwen3.5-flash-2026-02-23`（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“量化与剪枝、蒸馏有什么区别？”章节）。
- 压缩任务本身限时免费，但压缩后模型的部署费用按 MU 规格单独计费（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “计费说明”部分）。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号，便于追踪。 |
| **选择源模型** | 是 | 仅展示当前工作空间中已完成且状态为“成功”的微调模型；切换源模型会自动清空已选量化模板。 |
| **量化产出模型名后缀** | 是 | 仅限小写字母和数字，≤8 位；将拼接至源模型名后形成新模型标识（如 `my-model-quant8`）。 |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加；须先选定源模型才可加载对应模板列表。 |
| **校准数据** | 条件选填 | 仅当所选模板需校准输入时显示；最多选 5 个已在数据管理中**发布**的数据集；不支持 OSS 挂载数据集。 |

> **注意**：文档中“校准数据”字段描述为“条件选填”，但实际 UI 行为依赖模板配置；若模板未声明校准需求，则该字段不出现——此逻辑与 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“创建压缩任务”章节一致，无矛盾。

## 使用方式

1. **前提**：确保已有状态为“成功”的微调模型（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “前提条件”）。
2. 控制台路径：**模型 > 模型训练 > 模型压缩** → 单击**创建压缩任务**。
3. 完成参数配置（含任务名、源模型、后缀、量化模板、校准数据），确认无误后单击**开始压缩**。
   - 创建后配置不可修改，请务必在提交前核对量化模板。
4. 任务提交后进入列表页，可点击任务名称查看**详情**（含状态、配置、错误信息）或**日志**（支持按级别着色、下载全量日志、自动刷新等）。
5. 任务状态共 7 种：`PENDING` → `QUEUING` → `RUNNING` → `{SUCCEEDED/FAILED}`；`CANCELING`/`CANCELED` 为用户主动终止路径。

## 限制和注意事项

- **地域限制**：仅华北2（北京）可用。
- **模型来源限制**：仅支持百炼平台内微调产出的自定义模型；基础模型或外部上传模型不可压缩。
- **不可逆性**：
  - 压缩后模型**不支持继续微调**；
  - **不支持二次压缩**；
  - 如需调整，必须从上游全精度微调模型重新发起压缩任务。
- **失败排查**：优先查看详情页错误信息，再搜索日志中 `ERROR` 级别条目；必要时下载全量日志并附任务 ID 提交工单。
- **停止与删除**：
  - 仅 `PENDING` 和 `RUNNING` 状态可**停止**（不可恢复）；
  - 仅终态（`SUCCEEDED`/`FAILED`/`CANCELED`）可**删除**；删除任务记录不影响已产出模型。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


