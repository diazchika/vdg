from pathlib import Path
from typing import Union

import html2text
import yaml

from vdg.utils import read_template, clean_up, generate_draft
from vdg.yaml_preprocess import preprocess_yaml_dict


def html_to_markdown(html_str: str, comparison_md: str) -> str:
    """
    Generate Markdown release draft.
    :param html_str: HTML 字符串
    :param comparison_md: Markdown格式的对比图字符串
    :return:
    """
    # Convert HTML to Markdown
    converter = html2text.HTML2Text(bodywidth=0)

    # Convert HTML to Markdown
    md_str = converter.handle(html_str)

    # Split the Markdown content at the last occurrence of '* * *' and append the comparison section
    if comparison_md is not None:
        blocks = md_str.rsplit('* * *', 1)
        md_str = "* * *".join([blocks[0], "\n" + comparison_md])

    return md_str


def generate_drafts(path_to_yaml):
    """Generate drafts based on the provided YAML configuration."""

    # 读取 YAML 配置，送去预处理
    with open(path_to_yaml, "r") as file:
        release_info = preprocess_yaml_dict(yaml.safe_load(file))

    output_dir = Path(path_to_yaml).parent
    project_name = release_info["filename"] or release_info["ENGLISH"]
    use_v2 = release_info["use_v2"]

    html_config = {
        "template_path": "templates/html_v2.tmpl" if use_v2 else "templates/html.tmpl",
        "output_dir": output_dir / (f"{project_name}_v2.html" if use_v2 else f"{project_name}.html")
    }
    main_config = {
        "template_path": "templates/main.tmpl",
        "output_dir": output_dir / f"{project_name}_main.html"
    }
    configs = [
        html_config, main_config
    ]

    for config in configs:
        content = generate_draft(release_info, config["template_path"])
        with config["output_dir"].open("w") as file:
            file.write(content)

    html_content = generate_draft(release_info, html_config["template_path"])
    markdown_content = html_to_markdown(html_content, release_info["对比图MD"])
    with (output_dir / f"{project_name}.md").open("w") as file:
        file.write(markdown_content)

    print(f"稿件 诞生在 {output_dir.absolute()}")


def create_yaml_config(destination_path: Union[str, Path],
                       template_path: Union[str, Path] = 'templates/yaml.tmpl') -> None:
    """
    复制一份 YAML 模版到 destination_path

    Args:
        destination_path (Union[str, Path]): The directory where the config.yaml file will be created.
        template_path (Union[str, Path], optional): The path to the YAML template file. Defaults to 'yaml.tmpl'.
    """

    # 读取 YAML 模版
    yaml_str = read_template(template_path)

    # 写入文件
    output_path = Path(destination_path)
    with open(output_path, "w") as f:
        f.write(yaml_str)

    # User Prompt
    print(f"config.yaml 诞生在 {output_path.absolute()}")


def generate_links(path_to_yaml) -> None:
    """Generate drafts based on the provided YAML configuration."""
    with open(path_to_yaml, "r") as file:
        release_info = yaml.safe_load(file)

    links = release_info.get("BT站链接")

    for link in links.split('\n'):
        if link != "":
            print(f'<a href="{link}" rel="noopener" target="_blank">{link}</a>\n')
