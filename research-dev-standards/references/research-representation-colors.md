# 按表示类型选择颜色与渲染

这是 [统一科研配色](research-color-standard.md) 的分表示规则。四套参考家族为 CHOIS（默认）、Terra、Any4D、Gaussian Garments；可用的数值/向量编码单独登记在 [JSON](research-color-palettes.json) 的 `encodings`，实际选用见 `representation_defaults`。不是每篇论文都有每一种表示的可核实色板，缺少证据时保留待核实，不补造一整套参数。

## 选择矩阵

| 表示 | 默认/优先参考 | 必须固定的语义 |
| --- | --- | --- |
| 流程图/方法图 | CHOIS 默认；Terra/Any4D 可选 | 功能角色、填充/边框/alpha、深色文字 |
| 深度/逆深度 | SeeClear Depth 定性 LUT | 量定义、单位、近远方向、共同范围、无效值 |
| 法线 | 声明坐标系的方向 RGB；Any4D 仓库 helper 可作特定约定参考 | 坐标系、轴向、分量到 RGB 映射、法线朝向 |
| 点图/pointmap | 明确的 XYZ 编码；不等同点云原始 RGB | 共用坐标系、参考范围、无效点与裁剪 |
| 点云 | 原始 RGB，或明确的 ID/深度/误差/运动属性 | 着色属性、点大小、相机、过滤与采样 |
| 网格/人体/服装 | CHOIS 身份色默认；Gaussian Garments 为候选渲染参考 | 材质、光照、线框/实体模式、身份和几何不变 |
| 3DGS/纹理外观 | 原始 appearance；Gaussian Garments 可作呈现参考 | 原始 RGB/SH、相机、曝光/色调映射、属性完整 |
| 语义/实例分割 | 数据集官方映射优先；否则 CHOIS 起始分类色 | 稳定类别/实例 ID、背景/ignore、统一叠加透明度 |
| 二维光流 | 沿用项目已验证的 UV renderer 并注明来源；Any4D 专用色轮未确认 | UV 正方向、帧对、像素单位、同一色轮与幅值上限 |
| 三维场景流 | Any4D demo 的方向/幅值规则为优先参考 | 坐标系、时间间隔、投影平面、方向色与共同幅值范围 |
| 点轨迹 | Any4D demo 初始位置着色为优先参考 | 参考帧/点 ID、初始位置范围、跨帧身份色 |
| 图表/误差/置信度 | 分类用 CHOIS contrast；标量用适合其量定义的色图 | 方法映射、坐标轴/单位、色标、对照与缺失口径 |

2026-10-21 用户进一步明确喜欢的参考是 Any4D teaser；Figure 1 图注明确它为稀疏显示的三维运动点轨迹。此前将其记作“Any4D 二维光流偏好”的描述已撤回：二维画面中的三维轨迹不等于二维 UV 流。三维箭头、点轨迹和二维光流保持独立编码与证据状态。

## 饱和度不是论文级常数

方法图通常用浅色面积与深色标签，避免背景压过结构；流场需要辨认方向与运动，可使用高饱和色轮。Any4D 三维箭头 demo 的 S/V 随运动幅值变化；点轨迹函数直接采用 `rainbow` RGB，无额外 S/V 重映射，不能声称其 S 恒为 1 或由速度控制。不要为了“全项目统一浅色”而把流图褪色，也不要为了突出某方法而单独增强其饱和度。

饱和度可能本身携带幅值语义，不能把它当成任意美化滑块。数据派生图与生成式概念插图分开；直接比较的传递函数一致。外层标注可用 CHOIS，不要求内部数据颜色也套 CHOIS 蓝绿紫。

## 深度、法线与点图

- 深度定性图可用 SeeClear LUT；正深度、距离、逆深度分别声明，不混用近远方向。方法/帧对照共享参考范围、裁剪和无效掩码；置信度、非负误差与有符号残差分别选择相应色图，不直接沿用深度多色 LUT。
- 法线默认先变到声明的共同坐标系并单位化，再采用明确映射，例如本地 `normal-rgb-v1` 的 `(n+1)/2`。非均匀几何变换用正确的法线变换并重新归一化；无效/零向量另标，不当作合法灰色法线。对照中不得逐方法翻轴、按最小最大值拉伸 RGB 或调整朝向来制造一致。
- Any4D 仓库内 MoGe 的 `colorize_normal` 用 `n*[0.5,-0.5,-0.5]+0.5`，与全部分量正号的约定不同。只有确认输入坐标/轴向后才使用；它是仓库依赖 helper，不保证论文图使用同一路径。
- pointmap 是每像素 XYZ，不是法线、深度或运动向量。若显示 XYZ→RGB，固定参考系和共同 XYZ 范围，不逐图居中/缩放；退化坐标轴须拒绝或显式约定共同常数。坐标编码、原始 RGB 和实例颜色作为不同模式，不混称“点图颜色”。

## 点云、网格、Gaussian 与分割

- 点云可按原 RGB、实体 ID、时间、深度、误差或运动属性着色，先标明展示的属性再选编码。比较固定点大小、投影、相机、可见性、阈值和采样策略。纯展示过滤/稀疏化保留完整源数据并披露，不能伪装成方法输出更干净。
- 网格记录 base color/纹理、shader 空间、材质、flat/smooth/wireframe、灯光、曝光、view transform 和背景。CHOIS 标签色的本地材质适配不等于官方 Blender 复现。比较固定身份色、相机和渲染条件，不增删几何或改 GT。
- Gaussian Garments 的 viewer `adjust_color` 对 `gist_rainbow(t)` 做 `0.3*c/max(c)+0.3`，原调用按 viewer 节点数量取 t。复用时固定实体→t/RGBA 与色图库版本，不依赖插入顺序。这只能证明 viewer 网格配色，不能代替论文服装纹理或全部插图配色。
- 3DGS 保留全部 Gaussian 及其属性；原 appearance/RGB/SH 与独立的几何/ID 诊断着色分开。不能用抽点、统一上色或修改 SH 掩盖重建缺陷；原始结果不变，不用网页接入授权隐含生成新推理。
- 分割优先沿用基准官方类别映射，背景和 ignore 分开。否则登记稳定类/实例映射，可从 CHOIS 开始，类别超过三色时按当前任务扩展并配标签/边界，不能循环取模让不同类别撞色。方法间类别对齐；实例关联须有依据，不能按各图连通域顺序重新编号。mask 重采样用最近邻；叠加 alpha 一致，二值 mask 保留明确正负含义。

## 二维光流、三维场景流和点轨迹

### 二维光流

二维流是 `(u,v)` 的方向与幅值，通常用闭合方向色轮配合幅值到饱和度/亮度的映射。用户指定的 Any4D teaser 不是这类表示。在已核查的官方仓库、官网、官方 HF demo 与 arXiv v1 源码中，尚未确认专用二维 UV 绘制链路；这不证明作者没有其他实现。不得把 `rainbow` 轨迹色表、三维 XZ 箭头编码或 RAFT 的通用色轮标为 Any4D 二维光流复现。

实际出图可先沿用项目已验证的 flow renderer 并说明来源，不为等待参考而伪造映射。记录右/下轴、前向/后向、帧对/时间间隔、像素或像素每秒单位、原分辨率、色轮版本、共同幅值上限及无效/遮挡策略。缩放分辨率时同时正确缩放向量；前后向不是任意取负即可互换。显示方向图例/色轮和幅值说明，直接比较不逐图自动归一化，不随意把 3D XZ 向量当 UV。

### Any4D 三维流 demo：源码确认

固定提交 `aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497` 的 `scripts/demo_inference.py::log_scene_flow_to_rerun`：方向取归一化向量的 XZ 夹角映射到 H，幅值映射到 q 后令 S=`0.3+0.7q`、V=`0.5+0.5q`，再 HSV→RGB；确切公式见 JSON 的 `any4d-scene-flow-xz-v1`。

这只编码 XZ 方向，不能从色相恢复 Y 正负；纯竖直、近零运动/近零 XZ 投影和无效值应单独处理，必要时加三维箭头或 Y 分量图。明确 ego/allo 坐标、轴向、相机与时间间隔；位移和速度不能混称。标注展示的是投影方向，不假装完整球面方向色。

原 demo 默认在掩码与可能的最多一万箭头抽样之后计算幅值 min/max；显式提供 `scene_bounds` 时采用该范围。抽样通常按运动幅值加权，近零幅值时均匀随机；相等幅值上限加 `1e-6`。函数签名的 `colormap_name='rainbow'` 未在函数体使用，实际颜色来自 HSV→RGB，不能按参数名推断为 rainbow 查表。正式比较预先确定共同范围，固定相同参考点/箭头位置、seed、长度比例及采样策略，不逐方法突出大运动点；保留完整预测。这里只规范着色，不自动授权推理、筛选或抽样重写数据；3DGS 的全量要求不受箭头展示策略影响。无效/近零方向处理与共享范围是本地适配，不能冒充原函数原样行为。

### Any4D 点轨迹 demo：另一种颜色语义

同文件 `log_point_tracks` 取 `point_tracks[0][:, 0]`，即传入轨迹数组第 0 时刻的三维 x 分量，而非像素 u，也不保证是原始视频帧 0。用 `mpl.colors.Normalize(vmin=x_min, vmax=x_max)` 归一化后取 `cm.get_cmap('rainbow')(normalized_x)[:, :3]`，每条轨迹以一个固定 RGB 传给 `rr.LineStrips3D`。这是线性位置色表，不是闭合方向色轮；无额外 HSV 饱和度/亮度调整，也不按位移、速度或时间分色。CLI、Gradio 与官方 HF demo 的该函数 AST 一致。

比较采用共同参考点/稳定 ID、共同三维参考 x 范围及相同色图库版本；退化范围/无效值显式处理是本地适配，原函数没有自定义保护逻辑。不要每个方法重新按自己的预测位置分色。

### Teaser 证据边界

| 结论 | 状态与依据 |
| --- | --- |
| Figure 1 表示三维运动点轨迹 | 论文图注明确确认 |
| 公开轨迹函数是 `rainbow + 第 0 时刻三维 x 的 min–max`，同轨迹同色，无额外 S/V 调整 | 三个官方端点源码确认 |
| 上述函数就是 teaser 全部面板的确切生成链路 | 待核实；TeX 仅引入 `figures/cvpr_teaser.pdf`，未找到完整绘制/渲染/导出脚本 |
| Any4D 专用二维 UV 色轮、饱和度和归一化 | 未确认；不得由 teaser 或三维箭头推导，也不以 RAFT 替代 |

核查固定在 GitHub `aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497`、HF `ee9a56bacb830fac7e3fe41118e29a699d7c899c` 和 arXiv `2512.10935v1`。来源：[Figure 1](https://arxiv.org/html/2512.10935v1#S0.F1)、[CLI 轨迹函数](https://github.com/Any-4D/Any4D/blob/aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497/scripts/demo_inference.py#L208-L232)、[Gradio](https://github.com/Any-4D/Any4D/blob/aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497/scripts/any4d_gradio.py#L97-L120)、[官方 HF 源码](https://huggingface.co/spaces/theairlabcmu/Any4D/blob/ee9a56bacb830fac7e3fe41118e29a699d7c899c/app.py)、[TeX 包](https://arxiv.org/src/2512.10935v1)。项目选用公开 demo 机制时可称“采用 Any4D demo 轨迹编码”，不能声称 teaser 已精确复现。

## 图表与统一验收

方法图/图表的类别色、连续量的数值色、向量方向色、实例身份色和网页状态色分别登记，不因外观相似而混用。分类图表用 CHOIS contrast 并配线型/标记；连续热图标单位、范围与色标；不能默认绿色就是最好。统一的是语义、来源与可复现条件，而不是把所有媒体压成同样的低饱和度。

项目记录 `palette_id/version`、`representation`、`encoding_id`、source commit/函数、角色/ID 映射、颜色空间/alpha；数值/向量另记坐标、方向、单位、传递函数、共同范围、无效/遮挡与时间；3D 另记完整 renderer/material/camera。按实际尺寸检查图例、灰度/色觉缺陷、文字对比度，以及真实来源和身份一致；保留原资产与派生输出边界。

来源：[Any4D demo](https://github.com/Any-4D/Any4D/blob/aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497/scripts/demo_inference.py#L103)、[Any4D 所附 MoGe helper](https://github.com/Any-4D/Any4D/blob/aa9f1b0d7ecdf44a6ef8cef93387be0093bdd497/any4d/external/MoGe/moge/utils/vis.py)、[Gaussian Garments viewer](https://github.com/eth-ait/Gaussian-Garments/blob/ceb66fc36598da05b3b3391f4562cdc54d2a2ed2/inference.py#L77)。这些源码分别证实函数/展示路径，不是所有论文图片的通用生成证据。
