from pathlib import Path
from typing import Union

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

    template = jinja2.Template(template_str)
    return template.render(**kwargs)