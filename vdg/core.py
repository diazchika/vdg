import re
from pathlib import Path
from typing import Union, Dict, Any

import html2text
import yaml

from vdg.utils import render_from_template_str, read_template
from vdg.yaml_preprocess import preprocess_yaml_dict


def generate_html_draft(release_info: Dict[str, Any],
                        template_path: Union[str, Path] = 'templates/html.template') -> str:
    """
    生成 HTML 发布稿。
    :param release_info: The context dictionary with release information.
    :param template_path: The path to the HTML template file.
    :return: The generated HTML string.
    """

    # 读取 HTML 模版
    html_template_str = read_template(template_path)

    # 生成发布稿
    html_str = render_from_template_str(html_template_str, **release_info)

    # 去除重复空行、多余缩进。
    cleaned_html_str = re.sub(r'\s*\n\s*', '\n', html_str)
    return cleaned_html_str.strip()


def generate_main_draft(release_info: Dict[str, Any],
                        template_path: Union[str, Path] = 'templates/main.template') -> str:

    # 读取 主站发布稿 模版
    main_template_str = read_template(template_path)

    # 生成发布稿
    main_str = render_from_template_str(main_template_str, **release_info)

    # 将连续两个以上的换行符减少为两个
    cleaned_str = re.sub(r'\n{3,}', '\n\n', main_str)
    return cleaned_str.strip()


def generate_markdown_draft(html_draft_str: str, comparison_md: str) -> str:
    """
    Generate Markdown release draft.
    :param html_draft_str: HTML 发布稿字符串
    :param comparison_md: Markdown格式的对比图字符串
    :return:
    """
    # Initialize the HTML to Markdown converter
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = True

    # Convert HTML to Markdown
    markdown_content = converter.handle(html_draft_str)

    # Split the Markdown content at the last occurrence of '* * *' and append the comparison section
    blocks = markdown_content.rsplit('* * *', 1)
    markdown_content = "* * *".join([blocks[0], "\n" + comparison_md])

    return markdown_content


def generate_titles(release_info: Dict[str, Any], template_path: Union[str, Path] = 'templates/titles.template') -> str:
    """
    生成标题。
    :param release_info: The context dictionary with release information.
    :param template_path: The path to the titles template file.
    :return: The generated titles string.
    """

    titles_template_str = read_template(template_path)
    titles_str = render_from_template_str(titles_template_str, **release_info)
    return titles_str


def generate_drafts(path_to_yaml):
    """Generate drafts based on the provided YAML configuration."""

    # 读取 YAML 配置，送去预处理
    with open(path_to_yaml, "r") as file:
        release_info = preprocess_yaml_dict(yaml.safe_load(file))

    # 生成各种 HTML，主站，Markdown 以及标题
    html_content = generate_html_draft(release_info)
    markdown_content = generate_markdown_draft(html_content, release_info["对比图MD"])
    main_site_content = generate_main_draft(release_info)
    titles_content = generate_titles(release_info)

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

    # project_name = release_info.get("filename")
    links = release_info.get("BT站链接")

    # output_dir = Path(path_to_yaml).parent
    # output_dir.mkdir(parents=True, exist_ok=True)

    # file_paths = output_dir / f"{project_name}_links.txt"

    # with file_paths.open("w") as file:
    for link in links.split('\n'):
        if link != "":
            print(f'<a href="{link}" rel="noopener" target="_blank">{link}</a>\n')

    # print(f"Links 诞生在 {output_dir}")
