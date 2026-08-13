# 孙承泽通用技能仓库

这是一个面向所有方向的 Agent 技能底座。它不预设风电、叶轮机械、公益、软件工程或任何单一专业；接入项目的 Agent 先理解本项目，再从仓库中检索、组合和本地化技能，形成自己的专家团与执行链。

## 已整合内容

### 三个历史技能库的语义并集

已汇总以下分支中的 `技能库&准则`：

- `sunccchengze/turbine-blade-ai-platform@arena/019feb03-turbine-blade-ai-platform`
- `sunccchengze/wind_farm_viz@arena/019feb53-wind-farm-viz`
- `sunccchengze/-@arena/019ff697-repo`

历史目录中含有大量相同副本、不同 Agent 框架的生成版、压缩包、测试夹具和大体积展示素材。本仓库采用**紧凑语义并集**：

- 每个逻辑技能名保留一个带 references、scripts、templates 等资源的主版本；
- 同名但内容不同的 `SKILL.md` 全部保留为 variants；
- 字节完全相同的副本只记录别名，不重复占空间；
- 去掉 zip、字体、音视频、大图、测试夹具和完整应用源码等非技能核心制品；
- 专业项目中的规则只作为可选技能，不再成为全库默认立场。

当前历史并集包含 **1,556 个主技能**与 **697 个内容不同的同名变体**。准确数字与逐项来源见 [`catalog/import-report.json`](catalog/import-report.json)。

### 新装载项目

| 项目 | 本仓库位置 | 用途 |
|---|---|---|
| [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing) | [`skills/human-writing/`](skills/human-writing/) | 中文创作、改稿、现实/虚构边界与活人感审校 |
| [victorzhang016-code/victor-design](https://github.com/victorzhang016-code/victor-design) | [`skills/victor-design/`](skills/victor-design/) | 证据驱动的海报、演示、产品 UI 与跨载体视觉生产 |
| [langchain-ai/openwiki](https://github.com/langchain-ai/openwiki) | [`tools/openwiki/`](tools/openwiki/) | 为代码库生成并持续维护 Agent 文档；配套入口见 [`skills/openwiki/`](skills/openwiki/) |
| [leigest519/ScreenCoder](https://github.com/leigest519/ScreenCoder) | [`tools/screencoder/`](tools/screencoder/) | 将 UI 截图重建为可编辑 HTML/CSS；配套入口见 [`skills/screencoder/`](skills/screencoder/) |

四者均固定到 [`catalog/sources.lock.json`](catalog/sources.lock.json) 中的提交，并保留原许可证与上游说明。

## Agent 从这里开始

1. 阅读 [`AGENTS.md`](AGENTS.md) 与根 [`SKILL.md`](SKILL.md)。
2. 把当前项目的目标、事实、约束和交付物写成任务简报。
3. 搜索技能，不要一次加载整个仓库：

   ```bash
   python scripts/search_skills.py "你的任务关键词" --limit 12
   ```

4. 选择一个主技能，按需增加研究、制作、审查技能；通常不超过四个。
5. 按 [`governance/QUALITY_GATES.md`](governance/QUALITY_GATES.md) 验证，再交付。

完整流程见 [`guides/USAGE.md`](guides/USAGE.md)，跨领域消化方法见 [`guides/DOMAIN_ADAPTATION.md`](guides/DOMAIN_ADAPTATION.md)。

## 目录

```text
AGENTS.md                    Agent 入口与指令层级
SKILL.md                     通用技能路由器
governance/                  宪法、内阁、多 Agent 与质量门禁
guides/                      使用和领域适配指南
skills/
  community/                 历史并集中的资源完整主技能
  variants/                  同名但内容不同的轻量变体
  human-writing/             上游完整技能包
  victor-design/             上游完整技能包
  openwiki/                  OpenWiki 使用技能
  screencoder/               ScreenCoder 截图转代码技能
catalog/                     可搜索目录、导入报告和来源锁
scripts/                     搜索、安装、校验、重建目录与重新导入
tools/openwiki/              OpenWiki 固定版本源码
tools/screencoder/           ScreenCoder 紧凑运行时源码
third_party/                 上游 README、许可证和归属说明
```

## 常用命令

```bash
# 重建可搜索目录
python scripts/build_catalog.py

# 搜索技能
python scripts/search_skills.py "literature review statistics"

# 将技能复制到某个 Agent 的技能目录
python scripts/install_skills.py --name human-writing --target /path/to/skills

# 验证目录、来源锁、入口和导入边界
python scripts/validate_repository.py

# OpenWiki 本地开发/运行
cd tools/openwiki
corepack enable
pnpm install
pnpm build
```

第三方技能各自遵循原许可证。本仓库的整理、路由和通用准则不改变任何上游项目的权利声明。详见 [`third_party/NOTICE.md`](third_party/NOTICE.md)。
