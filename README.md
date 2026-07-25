
# 🚀 GitHub Accelerator Pro

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-orange.svg)](https://www.riverbankcomputing.com/technical-support/pyqt5)

一个基于 Python 和 PyQt5 开发的精美桌面应用程序，旨在解决国内用户访问 GitHub 下载速度慢、连接超时等问题。支持 **Cloudflare Workers** 和 **Fastly CDN** 等多种加速策略，提供一键生成加速链接、自动复制和浏览器打开功能。

## ✨ 特性

- **🎨 现代化 UI**：采用深色主题设计，视觉舒适，交互流畅。
- **⚡ 多源加速**：
  - 集成 Cloudflare Workers 代理节点（如 `gh.api.99988866.xyz`）。
  - 支持 Fastly CDN 镜像加速（如 `hub.fastgit.org`）。
- **🛠️ 便捷操作**：
  - 智能解析 GitHub 仓库、Release 及 Raw 文件链接。
  - 一键复制加速链接到剪贴板。
  - 直接在默认浏览器中打开加速后的资源。
- **📦 易于分发**：支持使用 PyInstaller 打包为独立的 `.exe` 可执行文件，无需安装 Python 环境即可运行。

## 📸 界面预览

*(此处建议插入程序运行截图，展示主界面、输入框及生成结果)*

## 🛠️ 技术栈

- **核心语言**: Python 3.8+
- **GUI 框架**: PyQt5
- **网络请求**: Requests
- **打包工具**: PyInstaller

## 🚀 快速开始

### 1. 环境准备

确保你的系统中已安装 Python 3.8 或更高版本。

### 2. 安装依赖

克隆本项目后，在终端中运行以下命令安装所需库：

```bash
pip install -r requirements.txt
```

如果下载速度较慢，可以使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

### 3. 运行程序

```bash
python main.py
```

### 4. 打包为 EXE (可选)

如果你希望将程序分发给没有 Python 环境的用户，可以使用 PyInstaller 进行打包：

```bash
pyinstaller --onefile --windowed --name "GitHubAccelerator" --icon=icon.ico main.py
```

*注意：请自行准备 `icon.ico` 图标文件，或者移除 `--icon` 参数。*

## 📖 使用说明

1. **输入链接**：在“资源链接”输入框中粘贴 GitHub 的 URL（例如：`https://github.com/user/repo/releases/download/v1.0/app.zip`）。
2. **选择策略**：从下拉菜单中选择加速方式：
   - `Cloudflare Workers (ghproxy)`: 适用于大多数通用场景。
   - `Fastly Mirror (hub.fastgit)`: 适用于部分静态资源加速。
3. **生成链接**：点击“生成加速链接”按钮。
4. **获取结果**：
   - 点击“复制链接”将加速后的 URL 存入剪贴板。
   - 点击“在浏览器打开”直接开始下载或访问。

## ⚠️ 注意事项

- **服务稳定性**：本程序使用的加速节点均为公共免费服务，可能会因流量过大或策略调整而出现不稳定情况。如遇失败，请尝试切换其他加速策略。
- **安全性**：请勿通过此代理输入敏感的个人凭证（如 GitHub Token），仅用于公开资源的下载加速。
- **合规性**：请遵守相关法律法规及 GitHub 的使用条款，勿用于恶意爬取或滥用带宽。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果你有更稳定的加速节点推荐，或者想优化 UI 体验，请随时联系。

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [PyQt5](https://www.riverbankcomputing.com/technical-support/pyqt5): 强大的 GUI 框架。
- [gh-proxy](https://github.com/hunshcn/gh-proxy): 灵感来源及部分代理逻辑参考。
- [FastGit](https://fastgit.org/): 提供的快速镜像服务。

---

Made with ❤️ by [Your Name]
