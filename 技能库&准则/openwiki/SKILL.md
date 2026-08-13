---
name: openwiki
description: 使用仓库内固定版本的 LangChain OpenWiki CLI，为代码库生成和持续维护面向 Agent 的 Markdown Wiki、AGENTS/CLAUDE 入口、Mermaid 图与 OKF 文档。适用于代码库理解、架构文档、持续文档更新和 CI 文档任务。
---

# OpenWiki

工具源码固定在 `tools/openwiki/`。完整行为、提供商和连接器说明见 `tools/openwiki/README.md`，不要凭本入口猜测当前 CLI 参数。

## 适用任务

- 第一次为代码库建立 Agent 可读的结构化文档；
- 在代码变化后更新已有 `openwiki/`；
- 维护架构、CLI、集成、运行与评估说明；
- 生成 OKF 兼容 Markdown 和基于源码的 Mermaid 图；
- 在 GitHub Actions、GitLab CI 或 Bitbucket Pipelines 中定期更新文档。

不用于替代用户明确要求的单篇 README 改稿，也不应覆盖人工维护的项目事实。

## 本地准备

```bash
cd tools/openwiki
corepack enable
pnpm install
pnpm build
```

开发运行以该目录 `package.json` 中的 scripts 和上游 README 为准。模型凭证放在 OpenWiki 指定的用户环境文件或 CI secrets 中，绝不能提交到本仓库。

## 工作流

1. 阅读目标代码库的 `AGENTS.md`、README 和现有文档约束；
2. 明确 wiki 的读者、范围、重点和禁止内容；
3. 在目标仓库初始化 OpenWiki，并把项目要求写入 `openwiki/INSTRUCTIONS.md`；
4. 运行生成或 update；
5. 查看真实 diff，核对架构事实、路径、链接和 Mermaid；
6. 运行目标项目测试或文档检查；
7. 只提交 OpenWiki 管理的区块和经过审阅的 wiki 变化。

## 约束

- OpenWiki 生成内容仍需人工/Agent 事实审查；
- 连接器配置只引用环境变量名，不写入原始 secret；
- 不删除现有文档中不由 OpenWiki 管理的内容；
- 更新时以当前源码为依据，不把旧 wiki 当成事实源；
- CI 使用固定版本，升级时先看上游 changelog 并重新验证。
