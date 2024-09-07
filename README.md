# VDG

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
[![Deploy to PyPI](https://github.com/diazchika/vdg/actions/workflows/python-publish.yml/badge.svg)](https://github.com/diazchika/vdg/actions/workflows/python-publish.yml)

## 简介

使用 Jinja2 填充 VCB-Studio 发布稿 YAML 模版。使用 Selenium Webdriver 半自动上传稿件。

## 安装

`pip install vdg`

## 使用方法

### 1. 运行 `vdg new`

会在当前目录下生成四个文件:

- `config.yml`: 用于填写发布信息;
- `url.html`: 填写 HTML 格式的总监截图;
- `url.md`: 填写 Markdown 格式的总监截图;
- `mediainfo.txt`: 填写 MediaInfo.

### 2. 填写发布信息

填写完毕后运行 `vdg gen`, 生成发布稿件 (预览).

### 3. 运行 `vdg publish`

若生成的稿件预览没有问题, 在公网发布时运行 `vdg publish`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
