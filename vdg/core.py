import re
from pathlib import Path
from typing import Union, Dict, Any

import html2text
import jinja2
import yaml


def newline_to_html_break(text: str) -> str:
    """
    Convert newlines in the text to HTML <br> tags.
    :param text: The string to be converted.
    :return: The converted string.
    """

    return text.replace("\n", "<br />\n")


def apply_html_conversion_to_fields(context: Dict[str, Any], fields: list) -> None:
    """
    在多行文本的换行符之前加上 <br />
    :param context: The context dictionary containing the fields.
    :param fields: List of field names to convert.
    :return:
    """

    for field in fields:
        if field in context:
            context[f"{field}_HTML"] = newline_to_html_break(context[field])
        else:
            print(f"Warning: Field '{field}' not found in context.")


def render_from_template_str(template_str: str, **kwargs: Any) -> str:
    """
    Render a string template with the given context.
    :param template_str: The string template to render.
    :param kwargs: The context to render the template with.
    :return: The rendered template as a string.
    """

    template = jinja2.Template(template_str)
    return template.render(**kwargs)


def generate_html_draft(release_info: Dict[str, Any],
                        template_path: Union[str, Path] = 'templates/html.template') -> str:
    """
    生成 HTML 发布稿。
    :param release_info: The context dictionary with release information.
    :param template_path: The path to the HTML template file.
    :return: The generated HTML string.
    """

    # 以下键值对应文本中可能会出现换行符
    fields_to_convert = release_info["多行文本关键字"]

    # 将换行符转换成 <br />
    apply_html_conversion_to_fields(release_info, fields_to_convert)

    # 读取 HTML 模版
    abs_template_path = Path(__file__).parent.absolute() / template_path
    with open(abs_template_path, "r", encoding="utf-8") as f:
        html_template_str = f.read()

    # 生成发布稿
    html_str = render_from_template_str(html_template_str, **release_info)

    # 去除重复空行、多余缩进。
    cleaned_html_str = re.sub(r'\s*\n\s*', '\n', html_str)
    return cleaned_html_str.strip()


def generate_main_draft(release_info: Dict[str, Any],
                        template_path: Union[str, Path] = 'templates/main.template') -> str:
    """
    生成主站发布稿。
    :param release_info: The context dictionary with release information.
    :param template_path: The path to the HTML template file.
    :return: The generated HTML string.
    """

    # 读取 主站发布稿 模版
    abs_template_path = Path(__file__).parent.absolute() / template_path
    with open(abs_template_path, "r", encoding="utf-8") as f:
        main_template_str = f.read()

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
    # 读取标题模版
    abs_template_path = Path(__file__).parent.absolute() / template_path
    with open(abs_template_path, "r", encoding="utf-8") as f:
        titles_template_str = f.read()

    # 生成标题
    titles_str = render_from_template_str(titles_template_str, **release_info)

    return titles_str


def generate_drafts(path_to_yaml):
    """Generate drafts based on the provided YAML configuration."""
    try:
        with open(path_to_yaml, "r") as file:
            release_info = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: The file {path_to_yaml} does not exist.")
        return
    except yaml.YAMLError as exc:
        print(f"Error loading YAML file: {exc}")
        return

    project_name = release_info.get("filename")
    if not project_name:
        print("Error: 'filename' key is missing in the YAML file.")
        return

    try:
        html_content = generate_html_draft(release_info)
        markdown_content = generate_markdown_draft(html_content, release_info["对比图MD"])
        main_site_content = generate_main_draft(release_info)
        titles_content = generate_titles(release_info)
    except KeyError as exc:
        print(f"Error: Missing required YAML key: {exc}")
        return

    output_dir = Path(path_to_yaml).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    file_paths = {
        "html": output_dir / f"{project_name}.html",
        "markdown": output_dir / f"{project_name}.md",
        "main_html": output_dir / f"{project_name}_main.html",
        "titles": output_dir / f"{project_name}_titles.txt"
    }

    try:
        with file_paths["html"].open("w") as file:
            file.write(html_content)
        with file_paths["markdown"].open("w") as file:
            file.write(markdown_content)
        with file_paths["main_html"].open("w") as file:
            file.write(main_site_content)
        with file_paths["titles"].open("w") as file:
            file.write(titles_content)
    except IOError as exc:
        print(f"Error writing to file: {exc}")

    print(f"稿件 诞生在 {output_dir}")


def create_yaml_config(destination_path: Union[str, Path],
                       template_path: Union[str, Path] = 'templates/yaml.template') -> None:
    """
    复制一份 YAML 模版到 destination_path

    Args:
        destination_path (Union[str, Path]): The directory where the config.yaml file will be created.
        template_path (Union[str, Path], optional): The path to the YAML template file. Defaults to 'yaml.template'.
    """
    # 读取 YAML 模版
    abs_template_path = Path(__file__).parent.absolute() / template_path
    with open(abs_template_path, "r") as file:
        yaml_str = file.read()

    output_path = Path(destination_path)
    with open(output_path, "w") as f:
        f.write(yaml_str)

    # User Prompt
    print(f"config.yaml 诞生在 {output_path}")


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
