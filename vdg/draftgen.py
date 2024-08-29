import os
import inspect
from pathlib import Path
import re
import html2text
from jinja2 import Environment, FileSystemLoader
import vdg.filters as filters
from vdg.utils import read_from_file, write_to_file, create_file


class DraftGenerator:
    CJK_PATTERN = r"[\u4E00-\u9FFF\u3400-\u4DBF\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\uAC00-\uD7AF]"
    ENG_PATTERN = r"[a-zA-Z0-9]"

    def __init__(self, release_info):
        self.release_info = release_info

    def __format_text(self, text):
        """Format text by adding spaces between CJK and English characters."""
        text = re.sub(f"({self.CJK_PATTERN})({self.ENG_PATTERN})", r"\1 \2", text)
        text = re.sub(f"({self.ENG_PATTERN})({self.CJK_PATTERN})", r"\1 \2", text)
        text = re.sub(r"^\n+", "", text)
        text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
        text = re.sub(r"\n{3,}", "\n", text)
        return text

    def __generate_draft(self, template_name):
        """Generate drafts using the specified Jinja2 template."""
        env = Environment(
            loader=FileSystemLoader(Path(__file__).parent.absolute() / "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        for name, func in inspect.getmembers(filters, inspect.isfunction):
            env.filters[name] = func

        # Load and render the template
        template = env.get_template(template_name)
        content = self.__format_text(template.render(**self.release_info))
        return content

    def __generate_bangumi_draft(self):
        """Generate the Bangumi draft."""
        return self.__generate_draft("bangumi.html.jinja")

    def __generate_bangumi_title(self):
        """Generate the Bangumi title."""
        return self.__generate_draft("bangumi.title.txt.jinja")

    def __generate_nyaa_draft(self):
        """Generate the Nyaa draft by converting the Bangumi draft to markdown."""
        bangumi_draft = self.__generate_bangumi_draft()
        converter = html2text.HTML2Text(bodywidth=0)
        md_str = converter.handle(bangumi_draft)

        # Append comparison images in markdown format if available
        comparison_md = read_from_file( self.release_info["对比图"]["MD"] )
        if comparison_md:
            md_str = "* * *".join([md_str.rsplit("* * *", 1)[0], "\n" + comparison_md])
        return md_str

    def __generate_vcb_s_draft(self):
        """Generate the VCB-S.com draft."""
        return self.__generate_draft("vcb-s.html.jinja")

    def __generate_vcb_s_title(self):
        """Generate the VCB-S.com title."""
        return self.__generate_draft("vcb-s.title.txt.jinja")

    def generate(self, site, content):
        if site == 'bangumi' and content == "draft":
            return self.__generate_bangumi_draft()
        elif site == 'bangumi' and content == "title":
            return self.__generate_bangumi_title()
        elif site == 'nyaa' and content == "draft":
            return self.__generate_nyaa_draft()
        elif site == 'nyaa' and content == "title":
            return self.__generate_bangumi_title()
        elif site == 'vcb-s' and content == "draft":
            return self.__generate_vcb_s_draft()
        elif site == 'vcb-s' and content == "title":
            return self.__generate_vcb_s_title()
        else:
            raise ValueError("Invalid site or content type.")

    @staticmethod
    def __get_empty_config():
        return read_from_file( Path(__file__).parent.absolute() / "templates/form.yml" )

    @staticmethod
    def generate_configs():
        if os.path.exists("./config.yml"):
            print("WARNING: Config already exists. Override? (y/n) ", end='')
            if input().lower() != "y":
                return
        write_to_file("./config.yml", DraftGenerator.__get_empty_config())
        for filename in ["./url.html", "./url.md", "./mediainfo.txt"]:
            create_file(filename)
