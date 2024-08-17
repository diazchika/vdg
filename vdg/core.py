import inspect
import os
from pathlib import Path
import re
from typing import Union

import yaml
import html2text
from jinja2 import Environment, FileSystemLoader

import vdg.filters


def log(message: str):
    print(message)


def read_from_file(file_path: str) -> str:
    file_path = Path(__file__).parent.absolute() / file_path
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"Written to {Path(file_path).absolute()}")

def enforce_space(text):
    cjk_pattern = r'[\u4E00-\u9FFF\u3400-\u4DBF\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\uAC00-\uD7AF]'
    eng_pattern = r'[a-zA-Z0-9]'

    og_text = text
    text = re.sub(f'({cjk_pattern})({eng_pattern})', r'\1 \2', text)
    text = re.sub(f'({eng_pattern})({cjk_pattern})', r'\1 \2', text)

    if og_text != text:
        log("WARNING: Added spaces between CJK and English characters.")
    return text

def html_to_markdown(html_str: str, comparison_md: str) -> str:
    converter = html2text.HTML2Text(bodywidth=0)
    md_str = converter.handle(html_str)

    # Split the Markdown content at the last occurrence of '* * *' and append the comparison section
    if comparison_md is not None:
        with open(comparison_md, "r", encoding="utf-8") as f:
            comparison_md = f.read()
        blocks = md_str.rsplit('* * *', 1)
        md_str = "* * *".join([blocks[0], "\n" + comparison_md])

    return md_str


def clean_up(s: str) -> str:
    s = re.sub(r'^\n+', '', s)
    s = re.sub(r'[ \t]+$', '', s, flags=re.MULTILINE)
    s = re.sub(r'\n{3, }', '\n', s)
    return s


def generate_drafts(path):
    """Generate drafts based on the provided YAML configuration."""

    with open(path, "r") as file:
        release_info = yaml.safe_load(file)

    output_dir = Path(path).parent
    filename = release_info["filename"]

    html_config = {
        "template_name": "html.jinja",
        "output_dir": output_dir / f"{filename}.html",
        "markdown": True
    }
    main_config = {
        "template_name": "main.jinja",
        "output_dir": output_dir / f"{filename}.main.html"
    }
    txt_config = {
        "template_name": "txt.jinja",
        "output_dir": output_dir / f"{filename}.txt"
    }
    configs = [
        html_config, main_config, txt_config
    ]

    # Create a Jinja Environment
    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent.absolute() / "templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    for name, func in inspect.getmembers(vdg.filters, inspect.isfunction):
        env.filters[name] = func

    for config in configs:
        template = env.get_template(config["template_name"])
        content = template.render(**release_info)
        content = enforce_space(content)
        write_to_file(config["output_dir"], clean_up(content))
        if config.get("markdown"):
            markdown_content = html_to_markdown(content, release_info["对比图"]["MD"])
            write_to_file(output_dir / f"{filename}.md", clean_up(markdown_content))


def create_form() -> None:
    if os.path.exists("./config.yml"):
        log(f"Config already exists. Override? (y/n)")
        if input().lower() != "y":
            return

    yaml_str = read_from_file('templates/form.yml')
    write_to_file("./config.yml", yaml_str)

    for filename in ["./url.html", "./url.md", "./mediainfo.txt"]:
        write_to_file(filename, "")
