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
