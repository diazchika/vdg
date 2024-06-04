import re
from pathlib import Path
from typing import Union, Dict, Any

import jinja2


def read_template(template_path: Union[str, Path]) -> str:
    abs_template_path = Path(__file__).parent.absolute() / template_path
    with open(abs_template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_from_template_str(template_str: str, **kwargs) -> str:
    """
    Render a string template with the given context.
    :param template_str: The string template to render.
    :param kwargs: The context to render the template with.
    :return: The rendered template as a string.
    """

    template = jinja2.Template(template_str, trim_blocks=True, lstrip_blocks=True)
    return template.render(**kwargs)


def clean_up(s: str) -> str:
    s = re.sub(r'^\n+', '', s)
    s = re.sub(r'[ \t]+$', '', s, flags=re.MULTILINE)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s


def generate_draft(release_info: Dict[str, Any], template_path: Union[str, Path]) -> str:
    """
    生成 *** 发布稿。
    :param release_info: The context dictionary with release information.
    :param template_path: The path to the template file.
    :return: The generated string.
    """

    # 读取 HTML 模版
    template_str = read_template(template_path)

    # 生成发布稿
    draft_str = render_from_template_str(template_str, **release_info)

    # 去除重复空行、多余缩进。
    return clean_up(draft_str)


def wrap_anchor_tags_with_del(html_string):
    # Regular expression to match <a> tags
    pattern = re.compile(r'(<a.*?>.*?</a>)', re.IGNORECASE)

    # Function to wrap found matches with <del> tags
    def wrap_with_del(match):
        return f"<del>{match.group(1)}</del>"

    # Replace <a> tags with wrapped version
    result = pattern.sub(wrap_with_del, html_string)
    return result


def wrap_link_with_anchor_tag(link):
    return f'<a href="{link}" target="_blank" rel="noopener">{link}</a>'
