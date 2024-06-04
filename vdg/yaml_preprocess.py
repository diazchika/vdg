from typing import Dict, Any

from vdg.utils import wrap_anchor_tags_with_del, wrap_link_with_anchor_tag


def preprocess_yaml_dict(release_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    在这个函数里实现将读取的 YAML 配置预处理的逻辑。
    :param release_info: YAML 配置
    :return: 预处理之后的 YAML 配置
    """

    release_info["BT站链接_HTML"] = '\n\n'.join([
        wrap_link_with_anchor_tag(link) for link in release_info["BT站链接"].split('\n') if link != ''
    ])

    # 标题简写如果没填就填原标题
    for key in release_info["文章标题简写"].keys():
        if release_info["文章标题简写"][key] is None:
            release_info["文章标题简写"][key] = release_info["文章标题"][key]

    for key in release_info.keys():
        if release_info[key] == '' or release_info[key] is None:
            release_info[key] = None
            print(f"WARNING: {key} has no value.")

    # 将（可能是）多行文本中的换行符转换成 <br />
    fields_to_convert = release_info["多行文本关键字"]
    for field in fields_to_convert:
        if release_info[field] is not None:
            release_info[f"{field}_HTML"] = release_info[field].replace("\n", "<br />\n")

    if release_info["旧下载BOX"] is not None:
        release_info["旧下载BOX"] = wrap_anchor_tags_with_del(release_info["旧下载BOX"])

    return release_info
