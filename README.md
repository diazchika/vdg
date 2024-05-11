# VDG (VCB-S Draft Gen)

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

## Introduction

主要是使用 Jinja2 对 HTML 模版进行填充以达到生成发布稿的效果。只需要把发布信息填写在 YAML 文件里就可以轻松生成三分发布稿（并不是终稿）✌️。

[生成样品](https://github.com/diazchika/vdg/tree/main/test)

## Installation
`pip install vdg`

## Usage

### 生成新 YAML 文件

`vdg new --path <path>`

会在`<path>`路径下生成 `config.yaml`，里面很多空要填...

`<path>` 默认为 `config.yaml`

YAML 里具体有什么看[这里](https://github.com/diazchika/vdg/blob/main/vdg/templates/yaml.template)。

### 生成发布稿件

`vdg gen --path <path-to-yaml>`

会读取`<path-to-yaml>`指定的 yaml 文件，并根据它生成发布稿。

`<path>` 默认为 `config.yaml`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
