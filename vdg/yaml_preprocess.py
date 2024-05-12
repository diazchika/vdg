from typing import Dict, Any


def preprocess_yaml_dict(release_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    在这个函数里实现将读取的 YAML 配置预处理的逻辑。
    :param release_info: YAML 配置
    :return: 预处理之后的 YAML 配置
    """

    # 将（可能是）多行文本中的换行符转换成 <br />
    fields_to_convert = release_info["多行文本关键字"]
    for field in fields_to_convert:
        if field in release_info:
            release_info[f"{field}_HTML"] = release_info[field].replace("\n", "<br />\n")

    # 标题简写如果没填就填原标题
    for key in release_info["文章标题简写"]:
        if release_info["文章标题简写"][key] is None:
            release_info["文章标题简写"][key] = release_info["文章标题"][key]

    return release_info
