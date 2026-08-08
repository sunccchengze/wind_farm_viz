# HANDOFF · 风电场偏航优化可视化（孙承泽 · 可视化模块）

> 本文档供**下一个接手 agent** 阅读。最后更新：2026-08-08，分支 `arena/019fe0c0-wind-farm-viz`。

---

## 0. 一句话定位

孙承泽（本科生）的可视化模块。当前交付物是**纯静态、CDN 交互库、可部署 Cloudflare Pages 的网页**（`site/`），用 Plotly.js 恢复了原 Streamlit 版的全部 3D 交互和视觉品质，同时保持零后端。

---

## 1. 已完成的工作

### P0 · 找回丢失的灵魂 ✅
- **3D 尾流曲面**：Plotly.js Surface + 拖拽旋转 + 5 种配色 + 底部投影/风机标记开关
- **3D 体渲染**：Plotly.js Isosurface + 阈值滑块 + 透明度调节 + 轮毂截面 + 风机几何
- **尾流分析**：偏航角滑块 → Plotly Heatmap 流场实时联动 + 4 KPI 实时计算 + 功率曲线分解
- **热力矩阵**：Plotly Heatmap 悬停数值 + 风速/偏航角切片曲线
- **全局视觉**：深空玻璃态 CSS（#020617 + backdrop-blur + 三层阴影 + hover 浮起）

### P1 · 视觉品质统一 ✅
- 全站 14 页统一 Plotly.js 暗色主题（`plotly-theme.js`）
- 着陆页 hero/stat-card/page-card 毛玻璃动效
- 导航自动高亮（`nav.js`）
- 数据总览/风玫瑰/阵列/模型精度全部 Plotly.js 化化

### P2 · 进阶交互 ✅
- **偏航角全场联动**：Dashboard 页风速按钮+偏航角滑块→功率曲线+仪表盘+流场三联动
- **GIF→Canvas 动画**：优化结果页偏航扫描滑块+▶播放/⏸暂停
- **实时仪表盘**：功率跟踪+Dashboard 半圆三色仪表(绿/黄/红)+功率曲线+目标线
- **POD 模态交互**：模态 0/1/2 切换按钮+淡入淡出+说明文字

---

## 2. 技术架构

```
site/  —— 纯静态站点，Cloudflare Pages 直接托管
├── *.html               # 14 个页面
├── css/style.css        # 全局深空玻璃态样式
├── assets/
│   ├── data.js          # 功率/工况数据（build_data.py 生成）
│   ├── data_3d.js       # 流场+热力矩阵数据（build_3d_data.py 生成，871KB）
│   ├── js/
│   │   ├── plotly-theme.js  # 全局 Plotly 暗色主题+ml()/pr()辅助
│   │   ├── nav.js           # 导航自动高亮
│   │   ├── interp.js        # 代理模型接口（predict_power / find_yaw_for_target）
│   │   ├── charts.js        # 旧版 SVG 辅助（保留兼容）
│   │   └── app.js           # 旧遗留
│   └── img/              # 流场图/动画/GIF
├── build_data.py         # CSV/JSON → data.js
├── build_3d_data.py      # npz 流场 → data_3d.js
└── wrangler.toml         # Cloudflare Pages 配置
```

**CDN 依赖**（仅 Plotly.js，按需加载）：
```html
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" defer></script>
```

---

## 3. 数据流向

1. **表格数据**：根目录 CSV/JSON → `python3 site/build_data.py` → `data.js`
2. **流场数据**：`fields/*.npz` + `fields_3d/*.npz` → `python3 site/build_3d_data.py` → `data_3d.js`
3. **前端插值**：`interp.js` 的 `predict_power(yaw, U)` 和 `find_yaw_for_target(target, U)`

> 重建数据：`pip install numpy pandas --break-system-packages && python3 site/build_data.py && python3 site/build_3d_data.py`

---

## 4. 本地预览 / 部署

**本地**：
```bash
git clone https://github.com/sunccchengze/wind_farm_viz.git
cd wind_farm_viz && git checkout arena/019fe0c0-wind-farm-viz
cd site && python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

**部署 Cloudflare Pages**：连 GitHub 仓库，构建命令留空，输出目录 `site`，分支 `arena/019fe0c0-wind-farm-viz`。

---

## 5. 待办（按优先级）

### 下一步
1. **部署 Cloudflare Pages**——获取正式 `*.pages.dev` 网址
2. **接洪祖名 XGBoost**——加载 `final_models/*.json` 到 `interp.js`
3. **接田铭雨 CFD 流场**——替换 `fields/` 后重跑 `build_3d_data.py`

### 再高级
4. 偏航角全局联动扩展到更多页面（不限于 Dashboard）
5. Canvas 动画增加 GSAP 缓动曲线（技能库已有 gsap-skills）
6. 移动端适配检测（3D 页面在移动端降级为静态图）
7. 旧 Streamlit 文件清理（用户确认后删 `app.py` + `pages/`）

---

## 6. 技能库清单

`技能库&准则/` 现在包含：
- boraoztunc-skills（63 个前端设计/CSS/动画技能）
- gsap-skills（GSAP 官方 AI 技能）
- karpathy-skills（编码准则）
- ECC（Agent 性能优化）
- ui-ux-pro-max（50+ 设计风格/161 色板）
- addyosmani-agent-skills（24 个工程技能）
- obra-superpowers（头脑风暴/计划/TDD/调试）
- superpowers-main（原有）
- agent-skills-main、skills-main、nuwa-skill、Research-Paper-Writing 等（原有）
- agent-browser、playwright、browser-use（浏览器自动化/测试）
- frontend-slides（Web PPT）

---

## 7. 已知坑

- Plotly.js ~3.5MB 首次加载，CDN 缓存后 ~1MB gzip
- `data_3d.js` 871KB，真实数据更大时需拆分
- numpy 在沙箱非持久，重装 + 重跑 `build_3d_data.py` 即可
- 沙箱崩溃会丢未提交文件——**频繁提交**
