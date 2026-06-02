# t7oolkit (Tauri)

基于 Tauri v2 + React/TypeScript 的桌面工具箱，功能与 [`../python`](../python) 版对齐。

## 功能

- 工具栏：可插拔工具卡片网格
- 基础配置：线程数量、默认导出目录（与 Python 版共用 `~/.config/t7oolkit/config.json`）
- 内置工具：
  - **文本处理**：字符数统计与大写转换演示
  - **图片缩放**：批量将文件夹内图片等比缩放至指定边长以内（Rust + `image` crate）

## 项目结构

```
app/tauri/
├── src/                 # React 前端
│   ├── components/      # 壳层 UI 组件
│   ├── tools/           # 工具页面
│   ├── registry/        # 工具注册
│   └── api/             # Tauri invoke 封装
├── src-tauri/           # Rust 后端
│   └── src/
│       ├── config.rs    # 共享配置读写
│       └── tools/       # 工具后端逻辑
│           ├── mod.rs
│           └── img_rect640.rs
└── package.json
```

## 环境要求

- Node.js 18+
- Rust 1.77+（含 Cargo）
- macOS / Windows / Linux 桌面开发工具链（见 [Tauri 前置依赖](https://v2.tauri.app/start/prerequisites/)）

## 开发

```bash
cd app/tauri
npm install
npm run tauri dev
```

## 构建

```bash
cd app/tauri
npm run tauri build
```

产物位于 `src-tauri/target/release/bundle/`。

## 发布

推送 `v*` 标签时，GitHub Actions 会同时构建 Python 与 Tauri 安装包并发布到 GitHub Release：

```bash
git tag v0.1.0
git push origin v0.1.0
```

Release 资产包括：

| 版本 | Windows | macOS |
|------|---------|-------|
| Python | `t7oolkit-*-windows.zip` | `t7oolkit-*-macos.zip` |
| Tauri | `t7oolkit_*-setup.exe` | `t7oolkit_*_aarch64.dmg` |
| Tauri 便携版 (Windows) | `t7oolkit-*-windows-portable.zip`（解压后直接运行 `t7oolkit.exe`） | — |

CI 工作流见 [`.github/workflows/tauri-ci.yml`](../../.github/workflows/tauri-ci.yml) 与 [`.github/workflows/release.yml`](../../.github/workflows/release.yml)。

### Windows 便携版（本地构建）

无需安装程序，解压 zip 后双击 `t7oolkit.exe` 即可运行（系统需已安装 [WebView2 运行时](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)）：

```powershell
cd app/tauri
npm install
npm run build:portable
npm run package:portable
```

产物：`dist/release/t7oolkit-<version>-windows-portable.zip`

## 配置格式

与 Python 版共用配置文件，顶层字段互通，各框架特有字段放在嵌套对象中：

```json
{
  "thread_count": 4,
  "export_dir": "/Users/you/Downloads",
  "python": {},
  "tauri": {}
}
```

## 添加新工具

1. 在 `src/tools/` 新建 React 组件，实现 `ToolProps` 接口
2. 在 `src/registry/tools.ts` 的 `registerAllTools()` 中注册

如需 Rust 能力，在 `src-tauri/src/tools/` 新建模块并在 `tools/mod.rs` 与 `lib.rs` 中注册 command。
