import re

合作组英文 = {
    "SweetSub": "SweetSub",
    "茉语星梦": "MakariHoshiyume",
    "风之圣殿": "FZSD",
    "千夏字幕组": "Airota",
    "喵萌奶茶屋": "Nekomoe kissaten",
    "诸神字幕组": "Kamigami",
    "天香字幕社": "T.H.X",
    "星空字幕组": "XKsub",
    "白恋字幕组": "Shirokoi",
    "动漫国字幕组": "DMG",
    "悠哈璃羽字幕社": "UHA-WINGS",
}

CJK_PATTERN = r"[\u4E00-\u9FFF\u3400-\u4DBF\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\uAC00-\uD7AF]"
ENG_PATTERN = r"[a-zA-Z0-9]"

def enforce_space(text):
    text = re.sub(f"({CJK_PATTERN})({ENG_PATTERN})", r"\1 \2", text)
    text = re.sub(f"({ENG_PATTERN})({CJK_PATTERN})", r"\1 \2", text)
    return text

def add_br(text):
    return text.replace('\n', '<br>\n')


def format_links(text):
    return '\n\n'.join(
        [f'<a href="{link}" rel="noopener" target="_blank">{link}</a>' for link in text.split('\n') if link != ""])


def del_anchors(text):
    return text.replace('<a', '<del><a').replace('</a>', '</a></del>')


def group_name_eng(names):
    return [合作组英文[name] for name in names]


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
