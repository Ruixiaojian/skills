# API Key 与鉴权

API Key 是阿里云百炼平台访问模型与应用 API 的核心凭证，所有调用通过 HTTP 请求头 `Authorization: Bearer <API_KEY>` 完成鉴权。Key 的权限由其归属的**业务空间**决定，并按使用场景细分为永久 Key、临时 Key、套餐专属 Key 等多种形态。

## API Key 的形态与归属

百炼平台目前存在三种格式的 API Key，互不相通，混用会触发 `401 Invalid API-key` 或 `401 invalid access token`：

| 格式前缀 | 用途 | 获取入口 |
| --- | --- | --- |
| `sk-xxxxx` | 通用永久 API Key，调用模型 API / 应用 API | 百炼控制台 → API Key（华北 2 北京）或工作台 → API Key（其他地域） |
| `sk-sp-xxxxx` | Token Plan 团队版 / Coding Plan 专属 Key | Token Plan 管理后台或 Coding Plan 个人控制台 |
| `st-xxxxx` | 临时 API Key（短期凭证） | 由永久 Key 调用 `POST /api/v1/tokens` 接口换取 |

**归属规则**（适用于永久 Key）：

- 单个 Key 只能归属**一个地域 + 一个业务空间 + 一个用户**，不可转移。
- Key 的可调用模型、限流配额与归属业务空间一致，**不受用户控制台权限影响**。
- 同一业务空间内的所有 API Key 权限相同，无需为文生文 / 文生图 / 语音等不同模型分别建 Key。
- 调优后的模型只能用其所在业务空间的 API Key 调用。

## 创建与配额

创建 API Key 必须由**主账号**或拥有「API-Key 管理」页面权限的 RAM 子账号操作。创建成功后弹窗仅展示一次完整 Key，**关闭后无法再次查看明文**，必须立即复制保存。

各地域配额：

| 地域 | 每主账号最大 Key 数 | IP 白名单 |
| --- | --- | --- |
| 华北 2（北京）、新加坡、德国（法兰克福） | 50 | 仅华北 2 支持，最多 20 个 IPv4/IPv6 地址或网段 |
| 美国（弗吉尼亚） | 20 | 不支持 |

> 自 2026 年 3 月 25 日起，华北 2（北京）地域所有**新创建**的 API Key 均归属主账号。

**生命周期**：

| 操作 | 主账号 API Key | RAM 账号 API Key |
| --- | --- | --- |
| 主动删除 | 失效，不可恢复 | 失效，不可恢复 |
| RAM 账号被移出业务空间 | — | 失效（重新加入后恢复） |
| RAM 控制台删除该账号 | — | 失效，不可恢复 |

## 配置环境变量 `DASHSCOPE_API_KEY`

强烈建议把永久 Key 写入环境变量 `DASHSCOPE_API_KEY`，避免硬编码进代码。

### Linux / macOS

| 类型 | Linux | macOS (Zsh) | macOS (Bash) |
| --- | --- | --- | --- |
| 永久 | 写入 `~/.bashrc` | 写入 `~/.zshrc` | 写入 `~/.bash_profile` |
| 临时 | `export DASHSCOPE_API_KEY="..."` | 同左 | 同左 |
| 生效 | `source ~/.bashrc` | `source ~/.zshrc` | `source ~/.bash_profile` |
| 验证 | `echo $DASHSCOPE_API_KEY` | 同左 | 同左 |

一行写入示例：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc
```

### Windows

- **系统属性**：`Win+Q` 搜索"编辑系统环境变量" → **环境变量 → 新建**，变量名 `DASHSCOPE_API_KEY`。
- **CMD 永久**：`setx DASHSCOPE_API_KEY "YOUR_KEY"`，验证 `echo %DASHSCOPE_API_KEY%`。
- **PowerShell 永久**：`[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_KEY", [EnvironmentVariableTarget]::User)`，验证 `echo $env:DASHSCOPE_API_KEY`。
- **临时**：CMD 用 `set DASHSCOPE_API_KEY=...`，PowerShell 用 `$env:DASHSCOPE_API_KEY = "..."`。

> 环境变量生效后**不会**自动注入到已经启动的 IDE / 命令行 / 服务进程。常见失败原因：未重启 IDE；使用 `sudo` 时未带 `-E` 继承环境；`systemd` / `supervisord` 启动的进程需在服务配置中显式声明。

## 临时 API Key（`st-` 开头）

用于浏览器、移动 App 等**不可信前端环境**：由可信后端用永久 Key 兑换临时 Key 下发，避免长期凭证外泄。

调用接口：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `token` | String | 临时 API Key，前缀固定为 `st-` |
| `expires_at` | Number | UNIX 时间戳（秒），到期后自动失效 |

关键约束：

- **权限继承**：临时 Key 完全继承永久 Key 的权限（模型 / 知识库白名单等）。生成前应先把永久 Key 配置为最小权限。
- **有效期**：默认 60 秒，通过 `expire_in_seconds` 指定，范围 `[1, 1800]` 秒。
- **不可提前撤销**：一旦生成只能等 TTL 过期，**不支持手动删除**。
- **地域隔离**：北京、新加坡、弗吉尼亚的永久 Key 互相独立，临时 Key 也必须在对应地域接口调用。
- **RAM 联动**：RAM 用户在 RAM 控制台被禁用或删除后，其名下所有 API Key（包括用其换出的临时 Key）立即失效。

## 套餐专属 API Key（`sk-sp-` 开头）

Token Plan 团队版与 Coding Plan 都使用 `sk-sp-` 前缀，但**互不相通**。

| 套餐 | API Key 获取入口 | Base URL（OpenAI 兼容） | Base URL（Anthropic 兼容） |
| --- | --- | --- | --- |
| Token Plan 团队版 | 管理后台由管理员分配席位后生成 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | 个人控制台获取 | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

> Coding Plan 必须使用专属 `sk-sp-xxxxx` Key，不能与通用 `sk-xxxxx` 混用；把 Token Plan 的 Base URL 用到 Coding Plan 工具上（或反之）会得到 `400 url error` / `404 status code`。

## OpenAPI 调用与 RAM 授权

RAM 用户默认**无权**调用百炼应用的数据、知识库、Prompt 工程、长期记忆等 OpenAPI，需由主账号在 RAM 控制台单独授权：

- **`AliyunBailianFullAccess`**：跨地域、跨空间的超级管理员权限（不含 OpenAPI 接口权限）。
- **`AliyunBailianDataFullAccess`**：调用应用 API 目录下所有 API。
- **`AliyunBailianDataReadOnlyAccess`**：仅调用只读类 API。

## 鉴权调用范式

所有支持 API Key 鉴权的接口（包括模型推理、应用调用、异步任务管理、临时 Key 换取等）统一使用 HTTP Bearer Token：

```
Authorization: Bearer ${DASHSCOPE_API_KEY}
```

请求失败时返回标准错误体：

```json
{
  "code": "InvalidApiKey",
  "message": "...",
  "request_id": "..."
}
```

常见鉴权类错误码：

| 错误码 / HTTP | 含义 | 排查方向 |
| --- | --- | --- |
| `401 InvalidApiKey` | Key 不存在、被删除或被禁用 | 检查 Key 是否复制完整、所属 RAM 账号是否还在；Token Plan / Coding Plan / 通用 Key 是否混用 |
| `401 invalid access token` | 套餐 Key 与 Base URL 不匹配 | 比对 `sk-sp-` Key 的来源套餐与请求的 Base URL 是否一致 |
| `400 url error` / `404` | Base URL 路径错误 | OpenAI 兼容路径以 `/v1` / `/compatible-mode/v1` 结尾；Anthropic 兼容路径以 `/apps/anthropic` 结尾 |
| `403 Forbidden` | IP 不在白名单或业务空间未开通模型 | 检查华北 2 Key 的 IP 白名单、目标模型是否在业务空间已授权 |

## 最佳实践

- **永远不要把永久 Key 嵌入前端代码或客户端 App**。前端调用必须经由后端换取临时 Key。
- **按环境隔离**：为开发、测试、生产分别创建业务空间（如 `project-dev-workspace` / `project-prod-workspace`），用各空间的独立 Key 调用，便于限流、审计与停用。
- **遵循最小权限**：永久 Key 应限定模型 / 知识库白名单（华北 2 还可加 IP 白名单），避免临时 Key 继承到过大权限。
- **轮换与撤销**：Key 泄露时立即在控制台删除（不可恢复），重新签发；不要为同一职责长期复用同一 Key。
- **代码中通过环境变量读取**：始终用 `os.environ["DASHSCOPE_API_KEY"]` 等方式读取，不要把 Key 写入版本控制。

## 关联主题页

- [preparations](../api/preparations.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [application permission management](../guides/application-permission-management.md)
- [token plan guide](../guides/token-plan-guide.md)


