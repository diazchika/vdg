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
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = True

    # Convert HTML to Markdown
    md_str = converter.handle(html_str)

    # Split the Markdown content at the last occurrence of '* * *' and append the comparison section
    if comparison_md is not None:
        blocks = md_str.rsplit('* * *', 1)
        md_str = "* * *".join([blocks[0], "\n" + comparison_md])

    return clean_up(md_str)


def generate_drafts(path_to_yaml):
    """Generate drafts based on the provided YAML configuration."""

    # 读取 YAML 配置，送去预处理
    with open(path_to_yaml, "r") as file:
        release_info = preprocess_yaml_dict(yaml.safe_load(file))

    # 生成各种 HTML，主站，Markdown 以及标题
    html_content = generate_draft(release_info, 'templates/html.template')
    main_site_content = generate_draft(release_info, 'templates/main.template')
    titles_content = generate_draft(release_info, 'templates/titles.template')
    markdown_content = html_to_markdown(html_content, release_info["对比图MD"])

    # 设置输出路径
    output_dir = Path(path_to_yaml).parent
    project_name = release_info["filename"] or release_info["ENGLISH"]

    file_paths = {
        "html": output_dir / f"{project_name}.html",
        "markdown": output_dir / f"{project_name}.md",
        "main_html": output_dir / f"{project_name}_main.html",
        "titles": output_dir / f"{project_name}_titles.txt"
    }

    # 写入文件
    with file_paths["html"].open("w") as file:
        file.write(html_content)
    with file_paths["markdown"].open("w") as file:
        file.write(markdown_content)
    with file_paths["main_html"].open("w") as file:
        file.write(main_site_content)
    with file_paths["titles"].open("w") as file:
        file.write(titles_content)

    print(f"稿件 诞生在 {output_dir.absolute()}")


def create_yaml_config(destination_path: Union[str, Path],
                       template_path: Union[str, Path] = 'templates/yaml.template') -> None:
    """
    复制一份 YAML 模版到 destination_path

    Args:
        destination_path (Union[str, Path]): The directory where the config.yaml file will be created.
        template_path (Union[str, Path], optional): The path to the YAML template file. Defaults to 'yaml.template'.
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
