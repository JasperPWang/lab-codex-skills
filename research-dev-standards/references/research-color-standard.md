# 科研配色与渲染表示：四套参考，默认 CHOIS

用户于 2026-10-21 确认。适用于新科研图、定性渲染与实验网页的配色选择，不自动改写已确认项目或历史结果。项目明确配置、本次指定风格与期刊硬性要求优先；保留已有映射，迁移需作为明确变更记录。

## 选择与单一权威源

精确色值、透明度、变体、数据编码与固定来源保存在同目录 [research-color-palettes.json](research-color-palettes.json)。不要在各 Skill 另建默认色表；项目从此表读取或复制所需配置，并记录参考家族、表示类型、编码 ID/版本与角色映射。没有代码读取器时，直接读取 JSON，不凭记忆填色。深度、法线、点图/点云、网格、分割、光流/场景流/轨迹及图表，按 [分表示规范](research-representation-colors.md) 选择；不是只有流程图需要配色规范。

| 方案 ID | 用途 | 默认行为 |
| --- | --- | --- |
| `chois-v1` | 交互组、人体/物体、轨迹、通用分类、图表与网页辅助色 | 未指定时选此方案；面积用 `soft`，细线/小字/控件用本地 `contrast` 适配 |
| `terra-v1` | 多阶段方法表达，以及有明确证据的渲染表示参考 | 当前确认的是方法图矢量色；其他表示不能据此推断 |
| `any4d-v1` | 方法图、三维流箭头、点轨迹及其他 CV 表示参考 | 用户指定的 teaser 是三维运动点轨迹，不是二维 UV 光流；公开轨迹函数已确认，teaser 完整生成链路待核实 |
| `gaussian-garments-v1` | 服装/人体、网格、Gaussian 外观与论文插图参考 | 已确认 viewer 网格着色机制；论文整套精确色板仍为部分证据，不虚构 HEX |

四套是参考家族，不是四组覆盖所有物理量的通用 HEX。CHOIS 的 soft/contrast 是同一方案适配；SeeClear Depth 独立放在 `encodings` 中，不占家族名额；数值误差色图也属于编码选择。v2 保留 `seeclear-depth-v1` ID 与 LUT，但从 `schemes` 移至 `encodings`，读取旧 JSON 结构的项目应显式迁移。Vid2World 等仍可作附加参考。

颜色饱和度按表示目的设定，不按论文名一刀切：流程图的浅色填充承托结构与文字；流场的方向/幅值可用更鲜艳的色轮。Any4D 的三维箭头 demo 明确令饱和度随幅值从 0.3 升至 1、亮度从 0.5 升至 1；点轨迹函数则直接取 Matplotlib `rainbow` RGB，没有额外 HSV 调整。前者不适用于 teaser 轨迹，二者均不能证明二维 UV 色轮。直接对照时共享编码、范围和饱和度/亮度传递函数，不能逐方法调鲜艳程度。

## CHOIS 的语义与使用

- 原始 teaser 标签的蓝/绿/紫分别为 `#879BD9`、`#A9CEA9`、`#B991D2`，由 TeX 包 `figures/Figure_teaser.pdf` 的不透明矢量填充确认，与先前 PNG 标签取样相符。辅助灰、画布及 contrast 变体是本地约定，不冒充作者原色。
- 交互组可让人和其交互物同色，用标签/轮廓区分两者；单人体默认蓝，多组按蓝/绿/紫稳定分配。需要实体分色时可用人体蓝、物体紫，但必须给图例。这是本地角色约定，不是作者统一规则。
- 定量曲线可用 contrast 蓝表示 Ours、灰表示主要对照，其余按注册表分配。绿色不是“最好”的通用标志。GT/预测/优化前后优先用栏位、标签、线型和标记区别，保持同一实体身份色。
- 网页保持中性界面，交互色与实验类别色分开。成功、失败、缺失采用独立状态语义并配文字/图标，不与方法图例混用。浅色块不直接当白底小字颜色。

## 原始依据与复现边界

- **CHOIS**：`2312.03913v1` 的矢量 teaser 确认标签三色。[官方 Blender 代码](https://github.com/lijiaman/chois_release/blob/8ec585aa0200fd2a890ffb12897bcf69ae719463/manip/vis/blender_vis_utils.py)中的人体/物体 BSDF base color 则是 `(10/255,30/255,225/255,1)` / `(153/255,51/255,1)`，不是上述标签色或最终受光像素，不能混为一个官方色板。
- **Terra**：`2510.14977v1` 的 `figures/pipeline.pdf` 矢量参数，包含不透明浅桃、主箭头与外框，及约 0.4 透明度的条件/生成填充。TeX 引入现成 PDF，没有证据表明它由公开 TikZ 色表生成。选定色值与 alpha 见 JSON；原图还有其他局部颜色，不全量迁移。
- **Any4D**：`2512.10935v1` 的 `figures/any4d_architecture_v3.pdf` 矢量参数。模块/token 的 alpha 约 0.623529，输入区域约 0.992157；基础 RGB 不等于合成后的 PNG 色值。TeX 中的作者/网页蓝紫色也不能冒充模块颜色。
- **Any4D 运动/几何表示**：[论文 Figure 1](https://arxiv.org/html/2512.10935v1#S0.F1) 明确 teaser 为三维运动点轨迹。[官方 demo 固定提交](https://github.com/Any-4D/Any4D/blob/aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497/scripts/demo_inference.py) 确认三维箭头与轨迹采用不同着色机制；轨迹按传入数组第 0 时刻的三维 x 做 min–max 后查 `rainbow`。TeX 只引入成图 `figures/cvpr_teaser.pdf`，尚未找到完整导出脚本，不能宣称 teaser 参数已逐项复现。专用二维 UV 色轮仍未确认，禁止用 RAFT 通用实现冒充。仓库内 MoGe helper 另定义法线、深度等编码；函数存在不等于论文图调用证据。详见分表示规范。
- **Gaussian Garments**：[官方 viewer 固定提交](https://github.com/eth-ait/Gaussian-Garments/blob/ceb66fc36598da05b3b3391f4562cdc54d2a2ed2/inference.py#L77) 确认网格用 `gist_rainbow` 后归一化并缩放/偏移 RGB；不把 viewer 节点插入顺序带到正式身份色映射，不声称该公式就是所有论文插图的配色。
- **SeeClear**：[固定提交的官方 demo](https://github.com/YumengHe/SeeClear/blob/f7508f28ace7d0219b365b2274ff3e6f47c9bc05/demo/visualization.py#L8) 明确给出五色数组、均匀锚点和逐 RGB 通道线性插值。只确认该 demo 的实现，不保证原论文 teaser 每幅图都使用此脚本。TeX 表格的 OursColor/Palette5 是行/最佳结果强调色，不是深度 LUT，不自动混入本标准。

JSON 中 PDF HEX 是提取 RGB 四舍五入到 8-bit 的复用表示，以 sRGB 作为本地 2D 约定，不声称验证了作者完整 ICC/打印流程。透明填充同时保存 alpha 与白底；画面像素还受合成、色彩管理与抗锯齿影响。不同用途的原始代码值、矢量参数、屏幕取样和本地适配必须分别标注。模板超链接色、未使用的 TeX 宏、相机随机色都不是论文方法图的配色证据。

## 连续量与证据完整性

- SeeClear LUT 从红经浅黄、绿、蓝到紫；原 demo 默认每图有限值 p2/p98 归一化，退化时回退 min/max。复用颜色不意味着复用其逐图范围策略。直接比较必须共享单位、vmin/vmax、裁剪、无效值和方向，范围由 GT、评测协议或明确的共同参考确定，不能各方法独立拉伸。
- 正深度与逆深度的近远方向不同，须说明量定义；逐图/逐实例归一化只作明确标注的定性检查，不根据颜色比较绝对深度。LUT 不保证感知亮度单调，定量非负误差优先 viridis/cividis，有符号残差用零中心发散色图。
- 同一项目的角色映射跨帧、样本、方法和视频稳定；一张分类图通常只用一套风格的少量主色。类别过多时先分组/分面，补充直接标签、线型与标记，不把多套色板拼成无语义彩虹。
- 原始 RGB、纹理、3DGS 外观、WorldModel 帧和归档资产保持不变。展示性重着色只改独立派生输出或浏览器显示状态，明确标注；不以换色暗示精度提升。
- 三维另记录 shader 输入空间、材质、灯光、曝光、view transform 和输出空间。按引擎要求从 sRGB 转换，不重复转换；同一 HEX 不保证 Blender/Three.js 像素一致。已有 `#6EA8FE` 是项目历史选择，不标为 CHOIS 原色，不自动覆盖。

## 验证与项目记录

记录 `palette_id`、`palette_version`、`variant`、`representation`、`encoding_id`、角色映射与颜色空间；连续量另记 LUT/色轮、单位、方向、共享范围、归一化/裁剪和无效值；向量另记坐标系、投影平面、时间间隔、饱和度/亮度函数；3D 另记渲染配置与源资产版本。新风格使用独立输出/缓存键，保留历史可回放性。

按实际论文版宽/网页尺寸检查，类别配标签、线型、形状或轮廓，检查灰度与色觉缺陷模拟；尚未检查的组合不宣称色盲安全。普通网页文字对比度目标至少 4.5:1，逐个实际前景/背景组合验证，不能因采用 contrast 变体就免检。真实结果验收同时检查身份、范围与源数据未变。

## 可重新获取的来源

- [CHOIS TeX v1](https://arxiv.org/src/2312.03913v1)
- [Terra TeX v1](https://arxiv.org/src/2510.14977v1)
- [Any4D TeX v1](https://arxiv.org/src/2512.10935v1)
- [SeeClear TeX v1](https://arxiv.org/src/2603.19547v1) 与上述固定提交代码
- [Matplotlib 连续色图选择](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- [WCAG 普通文字对比度](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
