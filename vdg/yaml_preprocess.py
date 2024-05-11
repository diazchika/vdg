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
    for key in ["中文", "ENGLISH", "日本語"]:
        if release_info[f"{key}_s"] is None:
            release_info[f"{key}_s"] = release_info[key]

    return release_info
