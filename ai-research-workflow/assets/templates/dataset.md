# Datasets

项目用途：<训练/验证/benchmark/诊断；当前数据契约版本>

存放约定：已核验数据盘的 `datasets/<数据集>/<版本或快照>/` 只放原始数据，不加 `raw/` 层；`projects/<项目>/data/<数据集>/<派生版本>/` 放本项目已处理的训练/验证/测试数据。复制/解压与处理暂存放项目工作区，不混入原始库或冒充已就绪版本。

| 数据集 / 版本 | 项目用途与范围 | 原始 datasets 目录 / README / manifest | 项目 data 目录 / 派生版本 | split / 状态 |
| --- | --- | --- | --- | --- |
| <名称、上游版本或快照> | <实际选择范围> | <核验后的 datasets 路径> | <项目 data 路径、派生 manifest> | <固定清单、状态> |

## <数据集名称与版本>

- 存放位置：<已核验的实际路径，直接展示，不放进折叠块>
  - 原始数据：`<verified-data-mount>/datasets/<dataset>/<version-or-snapshot>/`
  - 项目数据：`<verified-data-mount>/projects/<project>/data/<dataset>/<derived-version>/`
- 原始页面：<官方数据集页 / 论文数据页 / Hugging Face 等稳定入口>
- 原始下载链接：<实际使用的文件 URL、仓库地址或官方下载入口；多个分片逐条列出。没有直链时写明从上述页面如何获取>
- 来源与访问条件：<版本、许可证/申请要求>
- 下载/校验：<下载脚本、完成时间、字节数/哈希清单、验证结果及缺失>

数据集结构用默认收起的折叠文本，标题为 `数据集结构`。里面放原始目录和项目派生目录的目录树（代码块），不要把整棵树铺在页面正文里。不要给折叠块加 `open`，写完后也不要展开。目录很大时在折叠块内写明截断深度和省略了什么。

```html
<details>
<summary>数据集结构</summary>

```text
datasets/<dataset>/<version-or-snapshot>/
  README.md
  manifest.json
  ...
projects/<project>/data/<dataset>/<derived-version>/
  ...
```

</details>
```

写入 Notion 时改成默认收起的 toggle，标题仍是 `数据集结构`。写入飞书时改成原生折叠块，同样默认收起。Obsidian 保留上面的 `<details>`，且不能带 `open`。

- 原始格式：<样本单位、文件/字段、标注/GT；CV 任务按需补分辨率、相机/坐标/尺度/单位。目录树放上面的折叠块，不在这里再贴一遍>
- 项目输入与准备：<原始 manifest 路径/哈希、独立复制/解压命令及暂存路径，选择的场景/序列/样本>
- 预处理：<实际脚本 commit、命令、配置、resize/crop/mask/去重/过滤/转换、派生版本及项目 data 输出路径>
- 数量与问题：<处理前后数量、缺失/坏样本、排除清单与影响>
- split：<官方协议或自建分组依据、train/val/test 数量、清单及哈希、泄漏检查>
- 跨方法可比性：<共同输入、方法特有预处理及对指标的影响>
- 关联：<Related Work、Reproduction、Evaluation 和运行报告>
- 项目输入与准备：<原始 manifest 路径/哈希、独立复制/解压命令及暂存路径，选择的场景/序列/样本>
- 预处理：<实际脚本 commit、命令、配置、resize/crop/mask/去重/过滤/转换、派生版本及项目 data 输出路径>
- 数量与问题：<处理前后数量、缺失/坏样本、排除清单与影响>
- split：<官方协议或自建分组依据、train/val/test 数量、清单及哈希、泄漏检查>
- 跨方法可比性：<共同输入、方法特有预处理及对指标的影响>
- 关联：<Related Work、Reproduction、Evaluation 和运行报告>

原始文件保留，不直接在源目录预处理、训练或评测；项目使用独立副本，不能以软链接或硬链接替代。源目录必须有 README.md 和 manifest.json，原始库与派生版规则以 research-dev-standards 的 dataset-storage.md 为准。
