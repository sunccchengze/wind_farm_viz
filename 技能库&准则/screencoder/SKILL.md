---
name: screencoder
description: 将网页或应用 UI 截图拆解为可编辑、可继续开发的 HTML/CSS。适用于 screenshot-to-code、设计稿复刻、页面原型还原和已有截图的结构化前端重建；结合 ScreenCoder 的区域规划、UIED 元素检测、多模态代码生成、占位图匹配与真实渲染验证，避免把整张截图伪装成网页。
---

# ScreenCoder：截图转可编辑 HTML/CSS

上游运行时代码位于 `tools/screencoder/`，固定来源与提交见 `catalog/sources.lock.json`。本仓库保留推理主链和 UIED 核心代码；训练栈、示例输入输出和大型媒体未复制，具体见 `tools/screencoder/UPSTREAM.md`。

## 何时使用

- 用户提供 UI 截图，要求还原为 HTML/CSS；
- 需要从图片建立可编辑网页原型；
- 需要提取页面区域、组件边界和图片占位；
- 需要在保持截图视觉关系的前提下继续定制；
- 需要比较生成页面与原图的布局误差。

不适用于只想分析设计风格、只需生成一张静态图片，或没有权利复刻的第三方界面。

## 成功标准

合格结果必须同时满足：

1. 页面由真实 DOM、文字、布局和样式组成；
2. 不用整张截图作为背景冒充实现；
3. 用户能继续编辑文字、颜色、间距、组件和图片；
4. 在约定视口下与原图的结构、位置、层级和视觉权重接近；
5. 真实渲染通过截图对比；
6. 明确区分“忠实复刻”和“基于截图再设计”。

## 第一步：固定任务边界

先确认：

- 截图是必须复刻的 base，还是只提供视觉参考；
- 目标视口宽高和设备像素比；
- 要求像素级复刻、结构近似，还是允许重新设计；
- 是否需要响应式状态、交互、动画和多个页面；
- 截图中的图片、图标和字体能否合法复用；
- 最终需要纯 HTML/CSS、Tailwind，还是接入现有 React/Vue 项目；
- 可编辑性、浏览器范围和验收方式。

这些信息会改变实现时，不要静默猜测。

## 第二步：准备隔离工作区

不要直接在技能仓库中写运行结果。将工具复制到任务工作区，或在目标项目的临时目录运行：

```bash
cp -R tools/screencoder /path/to/work/screencoder
cd /path/to/work/screencoder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
mkdir -p data/input data/output data/tmp
```

依赖包含 OpenCV、Playwright、PaddleOCR、TensorFlow/Keras 和模型 SDK，安装体积较大。先确认环境与 Python 版本兼容。

### 模型凭证

上游代码支持 Doubao、Qwen、GPT 和 Gemini，并读取本地 `*_api.txt` 文件。凭证文件只能存在于本地隔离工作区，不得加入 Git、聊天记录、日志或交付包：

```text
doubao_api.txt
qwen_api.txt
gpt_api.txt
gemini_api.txt
```

运行前检查 `block_parsor.py`、`html_generator.py` 中选择的模型和密钥文件。不要把示例模型名当成长期可用保证。

## 第三步：建立输入

1. 将原图保存到 `data/input/`；
2. 记录原始尺寸，不要先随意拉伸；
3. 去掉浏览器外框、阴影或无关背景时保留原件；
4. 多状态界面分别保存，不从一张截图虚构隐藏交互；
5. 文字、图片和图标若有原始资产，优先使用原始资产。

上游脚本包含 `test1.png` 等硬编码默认路径。运行前统一修改或传入实际路径，确保各阶段读写的是同一组文件。

## 第四步：分阶段执行

上游主流程为：

```text
区域/块规划
  → 组件 HTML 生成
  → HTML 灰色图片占位检测
  → UIED 原图元素检测
  → 占位与原图区域匹配
  → 替换裁剪图片
  → 最终 HTML
```

对应脚本：

```bash
python block_parsor.py
python html_generator.py
python image_box_detection.py \
  --html data/output/page_layout.html \
  --screenshot data/input/page.png \
  --out data/tmp \
  --json data/tmp/page_bboxes.json
python UIED/run_single.py
python mapping.py --help
python image_replacer.py --help
```

`main.py` 只是按固定默认值串行调用脚本。第一次接入新截图时优先逐步运行，检查每一步制品，路径全部对齐后再使用一键流程。

### 每一步都检查

| 阶段 | 需要查看的制品 | 失败信号 |
|---|---|---|
| 区域规划 | bbox 树、区域截图 | Header、导航、主内容边界错误 |
| HTML 生成 | 初始 HTML | 文本缺失、层级错误、布局不可编辑 |
| 占位检测 | bbox JSON、调试叠图 | 图片占位漏检或落入错误区域 |
| UIED | 元素 JSON、检测图 | 原图元素被过度切碎或漏检 |
| Mapping | 映射 JSON、overlay | 占位与原图图片错配 |
| Replacement | 最终 HTML、裁剪图 | 图片变形、比例错误、重复替换 |

出错时回到最早出现偏差的阶段，不要只在最终 CSS 上掩盖错误。

## 第五步：整理生成代码

模型生成的代码是初稿。交付前至少完成：

- 删除无效、重复和互相覆盖的样式；
- 把重复颜色、字体、间距抽成适度的变量或 token；
- 保留语义化 HTML 和键盘可访问性；
- 校对截图中的真实文字，不让 OCR 或模型改写内容；
- 将合法资产放到稳定路径，补齐 `alt`；
- 不用大量绝对定位掩盖本可由 Grid/Flex 表达的结构；
- 不引入用户没有要求的框架；
- 接入现有项目时遵守其组件、路由和样式约定。

如果用户要求基于截图再设计，先完成忠实基线，再单独应用设计变更。不要把复刻误差包装成“优化”。

## 第六步：真实渲染验证

至少在目标视口完成一次浏览器截图：

1. 启动本地页面；
2. 用 Playwright 设置与原图一致的 viewport；
3. 截取生成页面；
4. 与原图并排、透明叠加或做像素差；
5. 检查主要区域、文字换行、图片裁剪和溢出；
6. 再检查至少一个窄屏或宽屏状态（若要求响应式）；
7. 检查控制台、网络错误和键盘操作。

优先级：

```text
结构与内容正确
  → 区域和尺寸
  → 字体与换行
  → 色彩和边框
  → 阴影、微动效等细节
```

不要为了降低像素差而破坏 DOM 可编辑性和响应式结构。

## 与其他技能组合

### 忠实截图复刻

```text
主技能：screencoder
支撑：frontend-design（接入现有前端时）
审查：webapp-testing + accessibility
```

### 截图基础上的再设计

```text
第一阶段：screencoder 建立忠实、可编辑基线
第二阶段：victor-design-system 依据任务和人工参考确定新方向
第三阶段：webapp-testing 检查真实页面
```

### 多页面或多状态迁移

可使用 `multi-agent-orchestration`，但各 Worker 必须写不同页面或不同文件；统一组件和 token 由总协调者在合并阶段处理。

## 安全与许可

- 不复刻钓鱼页、登录凭证窃取界面或其他欺骗性页面；
- 不提交模型 API key；
- 不默认拥有截图、Logo、字体、图标和照片的再分发权；
- 涉及第三方产品时，优先抽象结构和交互，不冒充原品牌；
- ScreenCoder 上游使用 Apache-2.0；内含 UIED 代码也保留其许可证。

## 完成交付

交付时说明：

- 源截图和目标视口；
- 采用的技术栈；
- 输出 HTML/CSS/组件和资产路径；
- 运行过的渲染、测试与无障碍检查；
- 哪些视觉差异仍存在；
- 哪些交互因截图没有提供信息而未实现。
