# bailian-docs-llm-wiki

> [中文版 / Chinese →](README.zh.md)

Technical documentation knowledge base for **Alibaba Cloud Model Studio (Bailian)** — enables your agent to look up model specs, API references, error codes, pricing, SDK usage, and platform guides instantly.

## What it does

This skill provides a structured, offline-first knowledge base that your agent reads to answer Bailian-related questions:

1. **Model specs** — context window, QPM limits, pricing, sample code for every foundation model
2. **API reference** — request/response formats, parameters, error codes
3. **Platform guides** — agents, RAG, knowledge base, memory, plugins, multimodal capabilities
4. **Comparisons** — structured side-by-side analysis of similar models or approaches

## When to use

- Looking up a specific model's specs, pricing, or rate limits
- Checking API parameters, error codes, or request formats
- Learning about Bailian features (RAG, agents, knowledge base, memory, plugins)
- Understanding SDK / OpenAI-compatible interface usage
- Comparing models or capabilities
- Token billing, free quotas, and pricing questions

**Not for this skill:**
- Other cloud providers (OpenAI, Anthropic, Google)
- General programming / framework questions
- `bl` CLI command usage → use `bailian-cli` skill
- Non-Bailian Alibaba Cloud products (OSS, ECS, RDS)

## Directory structure

| Directory | Content | Trust level |
|-----------|---------|-------------|
| `models/` | Model marketplace structured data (from console gateway) | Highest — most up-to-date |
| `raw/` | Official documentation (crawled from help.aliyun.com) | High — authoritative source |
| `wiki/` | LLM-synthesized wiki (topic / concept / comparison pages) | Medium — may lag behind |

**Trust priority:** `models/` > `raw/` > `wiki/`

## How to look things up

| Question type | Start here |
|--------------|------------|
| Model specs, pricing, QPM, context window | `models/index.md` |
| API docs, guides, concepts | `wiki/index.md` |
| Deep-dive into a specific topic | Follow links from wiki pages to `raw/` sources |

## Prerequisites

This skill requires Alibaba Cloud Model Studio CLI (`bl`). Before using this skill, check if `bl` is installed:

```bash
bl --version
```

If not installed or the command is not found, follow the install guide:

> https://bailian.aliyun.com/cli/install.md

## License

Apache-2.0
