# 原始 datasets、项目 data 与元数据

## 存放与保留

先按主 skill 核验数据盘挂载、空间和缓存位置，再下载。原始库按数据集/版本区分：上游提供什么格式就保留什么格式，包括压缩包、分片、原图、标注、相机和 split 文件。`.part` 及未校验下载保持未就绪状态；完整性检查后才标为可用。保留原始下载件，不因已解压、缓存整理、另一方法需要新格式或磁盘紧张删除、覆盖或修改它们。替换上游版本使用新版本目录；源数据删除/替换须用户另行明确授权。

目录职责按用户确认的约定区分：**`datasets/` 放上游原始数据集，不增设 `raw/` 层；`projects/<project>/data/` 放该项目已处理、可用于训练/验证/测试的数据集。** 不把项目生成的 mask、裁剪图、转换标注等写入 `datasets/`，也不将项目 `data/` 当作共享原始库。预处理所需的独立复制/解压暂存放项目工作区，与原始库及已就绪的 `data/` 版本分开。

```text
<verified-data-mount>/datasets/<dataset>/<version-or-snapshot>/
  README.md
  manifest.json
  archives-or-original-files/
<verified-data-mount>/projects/<project>/data/<dataset>/<derived-version>/
  README.md
  manifest.json
  <项目所需的训练/验证/测试数据及标注结构>
  splits/       # 如需独立保存划分清单
```

示例路径中的 data mount 必须实际核验；不凭名称判断。上游无版本号时，用访问日期与文件哈希定义本地 snapshot，说明“上游未提供版本”，不捏造 release。

`data/` 内保持项目实际读取的格式，不强制再套一层 `processed/` 或固定的 train/val/test 目录；划分也可由清单表达。不同方法的预处理不兼容时采用不同派生版本，不能互相覆盖。未完成处理或验证的版本保持未就绪状态，不能作为已处理可用数据供训练/评测读取。

原始目录只作为校验、独立复制/解压和生成派生数据的读取来源，不能直接作为项目训练、评测或原地预处理的工作目录。禁止用软链接、硬链接或把原始目录直接挂成项目工作目录来代替副本；不同方法会原地写入 mask、resize、缓存或标注，必须隔离。无需设置只读权限或强制只读挂载。复制完成后核对文件数/大小/清单和必要校验，所有变换及临时产物写项目副本，保留预处理版本；不允许路径参数出错时写回原始库。

已有项目若混用原始/派生文件，先检查文件和既有记录，标注当前状态；不能将处理过的数据回标为原始，也不能未经授权清理或替换现有文件。依据官方版本/哈希恢复原始来源后再建立可追溯派生版本。

## 原始目录必须同时提供 README 和 JSON

每个数据集版本的根目录在下载开始时创建 `README.md` 与 `manifest.json`，记录进行中状态，完成后更新实际文件和验证结果。不能只在聊天/项目报告中写来源，或只保留两个文件中的一个。

README 至少写明数据集名、上游来源/下载途径、版本或快照、许可证/访问条件、下载时间、原始目录/文件格式、大小、完整性验证方式/结果、可用范围与已知缺失，以及“保留源文件；项目用独立副本”的使用约定。JSON 记录对应机器可读信息；字段未知写 `null` 并解释原因，不能伪造哈希、完成时间或 verified 状态。来源 URL 记录稳定入口，不保存令牌、cookie 或带凭据的临时下载链接。

最小 JSON 结构示例（此处是待填写模板，不代表已下载资源）：

```json
{
  "schema_version": 1,
  "dataset_id": "<dataset-id>",
  "upstream_version": null,
  "snapshot_id": "<local-snapshot-id>",
  "source": {
    "homepage_url": "<official-source-url>",
    "download_url": "<stable-download-entry>",
    "resolved_revision": null,
    "license": "<license-or-access-terms>"
  },
  "download": {
    "completed_at": null,
    "tool": "<tool-and-version>",
    "command_or_script": "<reproducible-command-without-credentials>"
  },
  "raw_root": "<verified-data-mount>/datasets/<dataset>/<version-or-snapshot>",
  "files": [
    {
      "path": "<relative-original-file>",
      "size_bytes": null,
      "sha256": null,
      "upstream_sha256": null
    }
  ],
  "verification": {
    "status": "pending",
    "checks": [],
    "limitations": []
  }
}
```

下载后计算本地 SHA256 并记录实际字节数；上游哈希存在时独立对比。只有本地哈希不能证明上游真实性；无上游哈希时还需压缩包完整性、文件结构、数量、随机读取/最小 batch 等检查，记录降级验证。大规模清单可放单独的 checksums/JSONL 文件，由 manifest 记录路径及其 SHA256；不用为每次 dry-run 重新遍历所有大文件。上游来源/内容变化时新建快照并重新校验。

## 项目数据说明与派生记录

项目 `dataset.md` 记录数据用途、选择范围、原始 manifest、项目副本、格式、样本单位、相机/坐标/标注语义、预处理步骤、过滤前后数量、固定 split 和已知问题。参照 [`dataset.md` 模板](../../ai-research-workflow/assets/templates/dataset.md)。

每个派生版本的 manifest 关联 `raw_manifest_path`、`raw_manifest_sha256`、数据版本、方法/项目、预处理脚本 commit、命令/配置、样本数、split 清单/哈希与验证结果。README 说明如何从独立复制/解压重建该版本。代码或参数改变会影响数据时生成新派生版本，不能悄悄覆盖旧实验所用数据；每个 run 引用实际派生版本及评价协议版本。
