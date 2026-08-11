# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保持可用推理能力的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/#73749f1ee5634)之后、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-1/#3bc53b23c7shc)之前。压缩操作不可逆，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成微调训练的自定义模型**，不支持基础模型（如原始 Qwen 系列）或第三方导入模型。  
- 当前明确支持的模型示例包括 `qwen3.5-flash-2026-02-23`（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。实际可用模型以控制台动态列表为准。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“功能概述”章节说明）。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式和版本号，便于追踪管理。 |
| **选择源模型** | 是 | 仅展示当前工作空间中状态为“成功”的微调模型；切换源模型将自动清空已选量化模板。 |
| **量化产出模型名后缀** | 是 | 仅支持小写字母+数字，≤8 位；将拼接至源模型名后形成新模型标识（如 `my-model-quant8`）。 |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加（参考 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“量化模板怎么选？”说明）。 |
| **校准数据** | 条件必填 | 仅当所选模板需校准输入时显示；最多选 5 个已发布数据集（不支持 OSS 挂载），应与目标推理场景语义一致。 |

> **注意**：文档中“压缩前部署规格”示例为 `MU1*2`、“压缩后为 `MU8*1`”，但 MU 编号逻辑易引发歧义（MU8 并非指更高算力，而是更低规格的轻量级单元）。请以控制台模板卡片标注的实际部署规格（如 `MU8×1` 表示 8 个轻量单元）为准，避免按数字大小直觉推断性能。

## 使用方式

1. **前提**：确保已有状态为“成功”的微调模型（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “前提条件”章节）。
2. 控制台路径：**模型 > 模型训练 > 模型压缩** → 单击**创建压缩任务**。
3. 完成参数配置（含任务名称、源模型、后缀、量化模板、校准数据），确认无误后单击**开始压缩**。
4. 创建后不可修改配置；任务状态可在列表页实时查看，详情页含**详情**与**日志**两个页签，支持下载全量日志、ERROR 日志搜索等调试能力。
5. 任务成功（`SUCCEEDED`）后，压缩模型将出现在模型中心，可直接用于部署。

## 限制和注意事项

- **地域限制**：仅华北2（北京）地域可用。  
- **模型来源限制**：仅支持百炼平台内微调产出的模型；基础模型或外部上传模型不可压缩。  
- **不可逆性**：压缩后的模型**不支持继续微调，也不支持二次压缩**（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）。  
- **任务管理**：仅 `PENDING` 和 `RUNNING` 状态可停止；仅终态（`SUCCEEDED`/`FAILED`/`CANCELED`）可删除；删除任务不影响已产出模型。  
- **计费**：压缩任务当前限时免费（截止时间以控制台公告为准）；压缩后模型的部署费用按实际 MU 规格单独计费，不受免费期影响。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


