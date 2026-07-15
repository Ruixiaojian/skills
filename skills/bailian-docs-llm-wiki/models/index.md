# 百炼模型市场索引

> 自动生成 · 共 11 个模型家族 · 26 个主干模型 · 更新于 2026-07-15

**机器查询走结构化文件**：

- `index.json` — 全局摘要（统计 + 能力/厂商分布 + 轻量家族列表）
- `families.jsonl` — 每行一个家族（含轻量 `items[]` 摘要），适合按家族筛选
- `models.jsonl` — 每行一个主干模型（含价格/QPM/features），适合跨家族批量查询
- `groups/<slug>.json` — 单家族完整明细（含调用代码、入参 schema）

join：`models.jsonl[].family == families.jsonl[].slug == index.json.families[].slug`。

## 推理 `Reasoning` — 6 个家族

- [DeepSeek](groups/deepseek.json) — DeepSeek是由深度求索提供的开源模型，包含 V3.1、V3、R1以及基于Qwen2.5系列蒸馏的大语言模型。
  - 模型：`deepseek-r1`, `deepseek-r1-0528`, `deepseek-r1-distill-qwen-1.5b`, `deepseek-r1-distill-qwen-14b`, `deepseek-r1-distill-qwen-32b`, `deepseek-r1-distill-qwen-7b`, `deepseek-v3`, `deepseek-v3.1`, `deepseek-v3.2`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, `deepseek-v4-pro`
- [Qwen3.5-Flash](groups/qwen3.5-flash.json) — Qwen3.5原生视觉语言系列Flash模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果在纯文本与多模态方面相较3系列均实现飞跃式进步。
  - 模型：`qwen3.5-flash`
- [Qwen3.6-Flash](groups/qwen3.6-flash.json) — Qwen3.6原生视觉语言系列Flash模型，模型效果相较3.5-Flash显著提升。本模型重点提升agentic coding能力（在多项代码智能体基准上大幅超越前代）、数学推理和代码推理能力；视觉…
  - 模型：`qwen3.6-flash`
- [Qwen3.6-Max](groups/qwen3.6-max.json) — Qwen3.6原生Max模型，相较于此前发布的Qwen3-Max和Qwen3.6-Plus，本模型在vibe coding能力上进一步提升、coding agent执行更加高效、前端编程开发能力显著提…
  - 模型：`qwen3.6-max-preview`
- [Qwen3.6-Plus](groups/qwen3.6-plus.json) — Qwen3.6原生视觉语言系列Plus模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果相较3.5系列显著提升。模型在Agentic coding、前端编程、Vibe coding等代码能力、多…
  - 模型：`qwen3.6-plus`
- [Qwen3.7-Max](groups/qwen3.7-max.json) — Qwen3.7系列中规模最大、综合能力最强的Max模型，当前开放纯文本模型能力供体验。Qwen3.7是面向智能体时代的新一代旗舰模型，核心优势在于智能体能力的广度与深度：在编程、办公与生产力、长周期自…
  - 模型：`qwen3.7-max`, `qwen3.7-max-preview`

## 视频生成 `VG` — 2 个家族

- [HappyHorse-I2V](groups/happyhorse-i2v.json) — HappyHorse系列最新图生视频模型，具备高度还原的动态画面生成能力，能够稳定保持与图像一致性，输出流畅自然、细节丰富的高质量视频。
  - 模型：`happyhorse-1.0-i2v`, `happyhorse-1.1-i2v`
- [HappyHorse-T2V](groups/happyhorse-t2v.json) — HappyHorse系列最新文生视频模型，具备高度还原的动态画面生成能力，能够精准理解文本语义，输出流畅自然、细节丰富的高质量视频。
  - 模型：`happyhorse-1.0-t2v`, `happyhorse-1.1-t2v`

## 文本生成 `TG` — 2 个家族

- [Qwen3.5-Plus](groups/qwen3.5-plus.json) — Qwen3.5原生视觉语言系列Plus模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果在纯文本与多模态方面相较3系列均实现飞跃式进步。
  - 模型：`qwen3.5-plus`
- [Qwen3.7-Plus](groups/qwen3.7-plus.json) — Qwen3.7系列中高性价比Plus模型，在强大文本能力的基础上全面升级了视觉-语言能力，同时保持了在编码、工具使用和生产力工作流方面的完整智能体能力。其核心特色为多模态交互混合智能体能力，能够感知真…
  - 模型：`qwen3.7-plus`

## 视觉理解 `VU` — 1 个家族

- [Qwen3.6开源模型](groups/qwen3.6.json) — Qwen3.6系列开源模型，基于混合架构设计的原生视觉语言模型，模型效果相较于3.5系列同尺寸有大幅提升。
  - 模型：`qwen3.6-27b`, `qwen3.6-35b-a3b`
