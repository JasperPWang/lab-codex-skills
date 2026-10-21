# 三维重建结果渲染与对照

本参考整合用户 GRAFT 实验页下的《Threejs快捷渲染规范》和《Blender高质量渲染规范》（读取于 2026-10-12）。适用于人体/场景重建的定性图、旋转视频及优化前后对照。两份原文描述的是当时的 GRAFT/PhySIC 工作区：`paper_fast_v1` 与 `physic-paper-v2-graft-orbit45` 是项目配置名，以下数值是该项目的固定配置快照。执行时先读取当前项目 `Phy-SIC/render_pipeline/preset.json`、共享相机/运镜契约和实际渲染入口；与本快照不同时核实变更，不盲目覆盖。其他项目保留共享真实性要求，再按其相机、材质、任务与预算设定参数。

## 共享约束

- 新项目的分类/实体展示配色默认按 [四套配色规范](research-color-standard.md) 选 CHOIS；Terra/Any4D 用于方法图，SeeClear 用于定性深度。已有项目配置（包括下面的 `#6EA8FE`）是历史快照，不因默认变化自动覆盖。三维记录颜色空间与完整渲染条件，不能将 CHOIS 标签 HEX 当作其官方 BSDF 或最终像素。

- 渲染是对已生成重建的展示，不运行推理、优化姿态、修补网格、改评测分数或伪造 GT。保留原始 GLB/数组的顶点、面、场景缺口、预测地面、人体姿态、场景颜色来源和实际尺度。禁止为了好看添加代理地板、补全场景、消除穿插、减面、平滑修改几何或重画接触区域。人体可平滑着色，场景可平面着色；展示色改动只写入独立颜色缓冲，不修改归档源资产。
- 同一案例的前后状态来自同一次推理；固定人体身份、原始场景、完整相机内参 `fx/fy/cx/cy`、共享运镜时序及初始化人体的旋转中心。不要对各阶段独立居中、缩放或改焦距。benchmark GT 使用其真实标定，不把预测内参强加给 GT；野外图没有 GT 时不设 GT 占位，也不计算需要 GT 的指标。
- 原始照片淡出、起止原视角、绕 Y 轴 ±45° 的轨迹属于当前 GRAFT/PhySIC 对照契约；迁移到其他坐标系前验证轴向和投影。该项目相机坐标转换为 `(x,-y,-z)`，必须用非对称内参和轨迹极值检查，而非仅凭画面居中判断正确。
- 样本筛选依据事先固定的同一次逐帧评估，PA-MPJPE 和接触 F1 分开排序并保留最好/最差组；标明指标方向、数据集、帧身份和重复帧。该项目目标展示量是每指标每组十例，两例上下同屏，每对五秒，整组二十五秒；已有六例视频仍标六例。失败组只能用于失败分析，不能代表全数据集平均收益；不按改善幅度重新挑选样本。
- Benchmark 对照为 GT｜优化前｜优化后三栏；野外为优化前｜优化后两栏。仅对照同一方法自己的输出及来源明确的 GT，不把别的方法重建、去人场景或原图冒充本方法结果。不要为展示修改 GT 或源几何。静态接触图若使用当前项目约定，则正面及背面脚底朝镜头两视角、同一模板/颜色/相机/光照；接触标签在实际姿态下计算，再按顶点编号映射至 T-pose，最好/最差组采用同一次评估的精确标签。
- 保留输入资产、配置/代码版本和哈希、相机/运镜契约、状态参数、无损帧、可编辑场景（如 Blender）、视频与解码/渲染日志。新风格使用独立缓存键和输出名，不覆盖已发布历史视频；旧风格回放须显式选择。服务器长任务遵循主 skill 的 tmux、Docker 与数据盘规则。

## Three.js 快捷路径：`paper_fast_v1`

用途：新快捷抓帧的项目默认风格，接近当前 Blender 的视觉表达，不声称与 Cycles 像素级相同。项目使用 Three.js `0.158.0`、GLTFLoader、浏览器离屏抓帧和 FFmpeg 编码。GRAFT 官方交互查看器只提供 GLB 展示依据；本地离屏脚本、精确相机投影、原图淡出和比较排版并非作者公开的顶部演示视频生成器。

| 项目 | 当前项目配置 | 边界 |
| --- | --- | --- |
| 人体 | `#6EA8FE`，roughness `0.65`，metalness `0`，specular intensity `0.5`，clearcoat `0` | 哑光蓝是本地选择；specular intensity 不等同 Blender IOR Level `0.25` |
| 场景 | 原始顶点 RGB；已知 sRGB 字节先转线性，再只在展示缓冲做线性空间 HSV 饱和度 `0.85`；roughness `0.9`，flat shading | 已线性化的 GLB 不可再次套用 sRGB 转换；不改存档源色 |
| 色彩与背景 | ACES Filmic，exposure `1.0`，sRGB 输出；白底 `#ffffff` | 固定 Three.js 版本没有 AgX，不能宣称与 Blender 色调映射相同 |
| 环境与光源 | 白色 AmbientLight `0.5`；矩形面光源 `4x4`，key/fill/rim 强度 `20/7.5/6`，相对共享中心偏移 `(3,4,5)/(-4,2,3)/(1,3,-4)` | 光向与相对比例近似 Blender；强度单位不是瓦数，光源形状也不同 |
| 阴影 | 不启用 shadow map，不补 AO 几何 | 快捷路径不复刻 Cycles 的软阴影、间接光或多次反弹 |

当前比较排版：benchmark 上下两例、三栏，画幅 `3840x1520`；野外上下两例、两栏，画幅 `2560x1520`；每个视图 `1280x720`，另加行标签。两例同屏五秒、`30 FPS`，前后共用相机和运镜。`render_style.mjs` 是共享风格模块，`render_style_profile.mjs` 提供纯配置/颜色逻辑；三个调用方分别是 `graft/tools/render_iteration_comparison.mjs`、`render_gt_comparison.mjs`、`Phy-SIC/tools/render_standard.mjs`。这些路径是原工作区入口，运行前先核对项目文件及固定依赖。

```bash
node --loader ./graft/tools/three_runtime_loader.mjs --test graft/tools/render_style.test.mjs
bash graft/tools/render_iteration_comparison.sh \
  --manifest graft/outputs_iteration_comparison_20261011/comparison.json \
  --style paper_fast_v1
```

以上命令依赖已安装的固定版本 Node 模块目录及原项目清单；输出须使用新路径。`--style legacy` 只用于明确重放旧版。历史肤色人体视频不能作为新蓝色风格验收证据。当前记录的抓帧环境为 CPU 软件 WebGL，“快捷”不保证 GPU 渲染或固定倍率加速。

先用同一已存在 GLB 做原视角及左右极值的小样本：顶点/索引数组不变、相机契约测试通过、四角度预览非空、无浏览器/着色器错误、profile 元数据正确、最终视频完整解码。原文记录三项风格测试、九项相机/排版测试和三项跨项目默认值测试通过；这不是对未来新资产或新环境的免检证明。

## Blender 高质量路径：`physic-paper-v2-graft-orbit45`

用途：精选展示案例。当前项目记录的参数权威源为 `Phy-SIC/render_pipeline/preset.json`；此处是原文快照。渲染器 Blender `4.5.0`、Cycles `CUDA`，必须有 GPU；`128` samples、seed `0`、降噪与 persistent data，颜色管理 AgX。透明 RGBA PNG 最终合成白底。

| 项目 | 当前项目配置 |
| --- | --- |
| 人体 | `#6EA8FE`，roughness `0.65`，Specular IOR Level `0.25`，metallic `0`，Coat Weight `0` |
| 场景 | 原顶点 RGB；sRGB 转线性、HSV 饱和度 `0.85`，roughness `0.9` |
| 环境光 | 白色 world，strength `0.5` |
| 三盏灯 | 圆盘面光源 size `4`；key/fill/rim `1200/450/350 W`；相对人体中心偏移 `(3,4,5)/(-4,2,3)/(1,3,-4)` |
| 单视图输出 | `1920x1080`，`30 FPS`，五秒，最终完整解码 `150` 帧 |
| 编码 | H.264、CRF `18`、`yuv420p`、BT.709、faststart、无音轨 |

从现有 GLB 无损拆出网格数组；保留顶点、面、原色和预测地面。单例轨迹从原图视角开始和结束，Y 轴 ±45°，原照片淡出；原工作区用 `240` 个内部相位重定时到 `150` 个输出帧。与 Three.js 对照时共享源相机、初始人体中心和比较时序。当前 `Phy-SIC/render_pipeline/run.py` 只实现 PhySIC 单例，不可声称它已有 GRAFT 多阶段批量适配；新增适配先做单例验证。

```bash
cd Phy-SIC
python3 render_pipeline/run.py --case yoga_man --preview \
  --out outputs/blender_quality_preview_new
python3 render_pipeline/run.py --case yoga_man \
  --out outputs/blender_quality_single_new
```

仅在对应项目目录、现有 `physic:local` 镜像及已校验 Blender 安装可用时使用这些原文命令；不要隐式拉新镜像或改共享 Docker 服务。保留 `.blend`、无损 PNG 与视频。GPU 不可用时停止，不静默退回 CPU。验收包括：原视角、非对称相机和轨迹的投影误差均 `<0.001 px`；顶点/面数量不变、坐标误差 `<=1e-5`；无缺帧且视频完整解码 `150` 帧。已有样例坐标误差为零，但不能推断所有资产转换必然为零。

原文记录的 yoga 案例 `128` samples 单帧渲染中位数约 `8.2 s`、`157` 张唯一图像累计约 `21.4 min`；这只是历史单例测量，不是与 Three.js 的受控速度比较。

## 来源与复用边界

- [GRAFT 官方项目页](https://pradyumnaym.github.io/graft/)：确认交互 GLB 查看器及 Three.js/GLTFLoader；不能据此推断顶部预录视频的制作流程。[官方仓库](https://github.com/pradyumnaym/graft)提供 `graft/export.py` 导出与模型/数据集相机输出，不应为展示改重建或评测配置。
- [Three.js r158](https://github.com/mrdoob/three/tree/r158)提供图形库接口；本地抓帧、FFmpeg 编码和风格适配属于项目实现。
- [PhySIC 官方仓库](https://github.com/YuxuanSnow/Phy-SIC)提供重建与 `get_scene` 派生的几何；Blender 场景组装和相机验证是本地实现。
- [CHOIS 固定版本渲染脚本](https://github.com/lijiaman/chois_release/blob/8ec585aa0200fd2a890ffb12897bcf69ae719463/manip/vis/blender_vis_utils.py)只作模板载入、人体/物体材质分离、GPU Cycles 与逐帧输出的结构参考；没有复制 CHOIS 的模板、网格或渲染源码。[Blender v4.5.0](https://github.com/blender/blender/tree/v4.5.0)提供引擎和材质/色彩管理接口。
- 哑光蓝 `#6EA8FE`、具体灯光和上述两套比较配置是本地实验选择，不是 GRAFT、PhySIC 或 CHOIS 论文参数。Three.js 与 Blender 的光源单位、色调映射、阴影、间接光和反射模型不同，只比较同一资产的表达效果，不声称像素一致。
