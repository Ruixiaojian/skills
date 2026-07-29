# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成 API Key 获取、SDK 或 CLI 安装、环境配置等基础准备。这些步骤是所有后续调用的前提，直接影响鉴权有效性、协议兼容性与运行稳定性。本文档结构化梳理关键环节，聚焦可执行的技术细节，避免冗余说明。

## 支持的模型/功能

百炼平台支持多模态模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（如 `qwen-image-2.0`）、视频生成（如 `happyhorse-1.0-t2v`）、语音合成（如 `cosyvoice-v3-flash`）、视觉理解（如 `qwen3-vl-plus`）及向量/排序模型等。模型能力取决于其类型：纯文本模型（如 `qwen3-max`）**不支持** `image_url` 等多模态 `content` 元素；若需处理图片、视频或音频输入，必须选用对应多模态模型（如 `qwen3-vl-plus` 或 `qwen3.5-omni-plus`）。具体支持列表请参见[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)。> **注意**：文档 4 中明确指出，“使用纯文本模型时，若 `messages` 中包含 `image_url` 等多模态元素会触发 `Unexpected item type in content` 错误”，而文档 3 的 CLI 命令（如 `bl omni`）默认启用多模态能力，开发者需根据实际模型类型显式指定 `--model` 参数，避免因隐式默认值导致调用失败。

## 关键参数

调用时需关注以下核心参数及其约束：
- `model`：必须为百炼控制台模型市场中**精确匹配的模型 ID**（如 `qwen3.7-max`），不可混用开源社区命名（如 `Qwen/Qwen3-235B...`）；错误将返回 `Model not exist.` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- `temperature`：取值范围 `[0.0, 2.0)`，超出将报错 `Temperature should be in [0.0, 2.0)`。
- `top_p`：取值范围 `(0.0, 1.0]`，`top_k`、`repetition_penalty`、`presence_penalty` 等均有明确数值边界，详见[错误码文档](../../raw/model-api-reference/preparations/error-code.md)。
- `enable_thinking`：仅部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求为 `true`；开启时必须同时设置 `stream=true` 和 `incremental_output=true`，且禁用 `response_format={"type": "json_object"}`，否则将触发 `Json mode response is not supported when enable_thinking is true` 等错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- `messages` / `prompt`：二者必须且仅存在其一；`messages` 格式需严格符合 JSON Schema（如 `content` 必须为字符串或合法对象数组），非法结构将导致 `Required body invalid` 或 `Input should be a valid dictionary` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### API Key 获取与配置
- **获取**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。新创建的 Key 统一以 `sk-ws` 开头，且**仅创建时可见明文**，关闭弹窗后无法再次查看 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置（Linux/macOS/Windows 均有详细操作指南），避免硬编码泄露风险。CLI 工具也支持 `bl auth login --api-key` 或 `--api-key` 临时传入等方式 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### SDK 与 CLI 安装
- **SDK**：支持 DashScope（Python/Java）和 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 要求 `>=3.8`，Java 要求 `8+`，Go 要求 `1.22+`；Node.js 版本无特殊要求，但百炼 CLI 需 `>=22.12.0` [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：通过 `npm install -g bailian-cli` 安装，认证方式包括浏览器 OAuth 登录（推荐）、API Key 直接登录、环境变量或配置文件持久化。CLI 提供丰富命令（如 `bl text chat`, `bl image generate`）并支持地域切换（`--region cn|us|intl`）和自定义端点（`--base-url`）[原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **地域差异**：美国（弗吉尼亚）地域的 API Key **不支持禁用/重置操作**，且创建后仅显示 Key 值，不提供 `API Host`；其他地域则支持完整生命周期管理 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全升级**：`sk-` 开头的旧 Key 可继续使用，但新 Key 均为 `sk-ws` 格式，长度更长且明文仅一次可见，**强烈建议迁移**。
- **权限隔离**：API Key 权限由其**归属业务空间**决定，同一空间内 Key 权限一致；子业务空间下的 Key 仅能调用该空间已授权的模型 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **IP 白名单**：仅华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域支持配置 IPv4/IPv6 白名单（最多 20 个），美国（弗吉尼亚）地域不支持。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，大小上限 150 MB，页数上限 1500 页；图片类文件需先用 Qwen-VL 提取文本 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


