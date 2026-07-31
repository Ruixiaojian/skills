# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保持推理能力基本稳定的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节（微调 → 压缩 → 部署），仅作用于平台内微调产出的自定义模型，不支持结构剪枝或知识蒸馏等其他压缩范式。详细背景请参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 支持的模型与功能

- **支持范围**：仅限通过百炼平台完成微调训练的自定义模型（如 `qwen3.5-flash-2026-02-23`），不支持基础模型、第三方模型或非百炼微调产出的模型。
- **当前支持系列**：Qwen 系列（具体以控制台实时列表为准）；其他模型支持计划请关注 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的更新说明。
- **核心功能**：仅提供量化（Quantization），包括 INT4/INT8 等精度档位，通过校准数据优化量化误差；不提供剪枝、蒸馏、权重稀疏化等能力 —— 这一限定在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中已明确强调。

> **注意**：文档中“压缩前部署规格 MU1\*2 → 压缩后 MU8\*1”的示例存在表述歧义：MU8\*1 并非更低规格，而是指单卡 8MU 实例（对比双卡 1MU）。实际部署资源总量可能变化，需以控制台显示的 MU 总量（如 8MU vs 2MU）和单价综合判断成本。详情请核对 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中的计费说明章节。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号（如 `qwen35f-int4-v1`） |
| **选择源模型** | 是 | 仅展示当前工作空间中状态为“成功”的微调模型；切换模型将自动清空已选模板 |
| **量化产出模型名后缀** | 是 | 仅小写字母+数字，≤8 位；将拼接至源模型名后（如源模型 `my-qwen-ft` + 后缀 `int4` → `my-qwen-ft-int4`） |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，代表部署所需单卡算力越高（如 MU8 > MU4），但总 MU 成本未必更低；须先选源模型才可加载对应模板列表 |
| **校准数据** | 条件必填 | 仅当所选模板要求校准时出现；最多选 5 个已发布数据集（不支持 OSS 挂载）；推荐使用与目标场景语义一致的样本 |

## 使用方式

1. **前提**：确保工作空间中存在状态为“成功”的微调模型（参见 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/#73749f1ee5634)）。
2. **入口**：控制台 → **模型** > **模型训练** > **模型压缩** → **创建压缩任务**。
3. **配置**：按上述关键参数完成填写；特别注意：**配置提交后不可修改**，务必确认量化模板与校准数据无误。
4. **启动**：点击**开始压缩**（所有必填项校验通过后按钮才可用）。
5. **监控**：在任务列表页点击任务名进入详情页，通过**详情**页查看状态与配置，通过**日志**页查看实时运行日志（支持 ERROR 搜索、全量下载等）。

任务状态共 7 种：`PENDING` → `QUEUING` → `RUNNING` → `{SUCCEEDED/FAILED}`；`CANCELING`/`CANCELED` 为人工干预态。仅 `PENDING` 和 `RUNNING` 可停止；仅终态任务（`SUCCEEDED`/`FAILED`/`CANCELED`）可删除。

## 限制和注意事项

- **地域限制**：仅华北2（北京）可用。
- **不可逆性**：压缩后的模型**不支持继续微调**，也**不支持二次压缩**；若需调整，必须回退至原始微调模型重新发起任务（详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）。
- **数据依赖**：校准数据必须已在[数据管理](https://help.aliyun.com/zh/model-studio/manage-data/#9d2f7039bfo1a)中创建并发布；OSS 数据集不可用。
- **免费策略**：压缩任务本身限时免费（截止时间以控制台公告为准），但压缩后模型的部署费用始终按 MU 规格实时计费，不受免费期影响。
- **失败排查**：优先查看详情页错误信息 → 日志页搜索 `ERROR` → 下载全量日志分析 → 提交工单（附任务 ID 与日志）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


