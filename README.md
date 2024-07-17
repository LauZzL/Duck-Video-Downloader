<div align="center" >
<img style="display: block; margin: 0 auto; " src="https://s21.ax1x.com/2024/06/30/pkc3qSJ.png" width="200" height="200" />
</div>

<h1 align="center">Duck Video Downloader</h1>

<p align="center">基于 <a href="https://pywebview.flowrl.com/" target="_blank">PyWebview</a> 和 <a href="https://vuejs.org/" target="_blank">Vue3</a> 的视频平台多线程下载器。</p>

<div align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/LauZzL/Duck-Video-Downloader?style=for-the-badge">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/LauZzL/Duck-Video-Downloader?style=for-the-badge">
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/LauZzL/Duck-Video-Downloader?style=for-the-badge">
<img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/LauZzL/Duck-Video-Downloader/total?style=for-the-badge">
</div>

## 免责声明

本项目仅供学习交流，请勿用于非法用途。

## 支持平台

| 平台  | 域名                               | 帖子 | 主页 | 文档                          |
|-----|----------------------------------| --- | --- |-----------------------------|
| 推特  | `x.com` `twitter.com`            | ✅ | ✅ | [Twitter](/wiki/twitter.md) |
| 皮皮虾 | `h5.pipix.com`                   | ✅ | ✅ | [皮皮虾](/wiki/ppx.md)         |
| 抖音  | `v.douyin.com` `www.douyin.com` `www.iesdouyin.com` | ✅ | ❌ | -                           |
| 待添加 | -                                | - | - | -                           |


## 快速开始

[下载](https://github.com/LauZzL/Duck-Video-Downloader/releases)

## Yaml 配置文档

[配置文档](/wiki/yaml.md)


## 参与开发

> [#156](https://github.com/xdlumia/vue3-video-play/issues/156) 由于Vue使用的播放器库`vue3-video-play`的`package.json`中的`module`路径错误，需要在`yarn install`后手动到`node_modules/vue3-video-play/package.json`中将`module`的值修改为`./dist/index.mjs`。

加入该项目同开发者共同维护。

- 你可以通过 [PR](https://github.com/LauZzL/Duck-Video-Downloader/pulls) 对项目代码做出贡献
- 你可以通过 [Issues](https://github.com/LauZzL/Duck-Video-Downloader/issues) 提交问题或提出建议
- 你可以通过 [Discussions](https://github.com/LauZzL/Duck-Video-Downloader/discussions) 讨论项目

### 开发环境

- Node.js
- Vue3
- Vite
- Python 3

下载

```bash
git clone https://github.com/LauZzL/Duck-Video-Downloader.git
```

安装依赖

```bash
# 安装python依赖
pip install -r requirements.txt
# 安装node依赖
cd renderer
yarn install
```

运行

```bash
# 运行ui
cd renderer
yarn dev
# 运行python
cd ..
python app.py
```

## 构建

> 确保打包时ui资源被一同打包，否则无法正常显示

1. 打包ui
    ```bash
    cd renderer
    yarn build
    ```
2. 将`dist`文件夹复制到`根路径`下
3. 修改`app.py`中`RENDERER_URL`修改为`./dist/index.html`
4. 使用第三方python打包工具打包，例如`pyinstaller`

## 预览

### 视频解析

![视频解析](https://s21.ax1x.com/2024/07/01/pkg99aV.png)

### 主页获取

![img.png](https://s21.ax1x.com/2024/07/01/pkg9wi8.png)
![img.png](https://s21.ax1x.com/2024/07/17/pkoV59O.png)

### 播放

![播放器](https://s21.ax1x.com/2024/06/30/pkc8AOI.png)

### 设置

![设置](https://s21.ax1x.com/2024/07/02/pkgUTeJ.png)

### 下载

![下载展示](https://s21.ax1x.com/2024/06/30/pkc8Vmt.png)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LauZzL/Duck-Video-Downloader&type=Date)](https://star-history.com/#LauZzL/Duck-Video-Downloader&Date)