from importlib import import_module


def load_module(module_path):
    """
    加载模块方法

    Args:
        module_path (str): 模块路径

    Returns:
        module: 加载的模块对象
    """
    return import_module(module_path)


def merge_dicts(dict1: dict, dict2: dict = None) -> dict:
    """
    合并两个字典并返回结果

    Args:
        dict1 (dict): 第一个字典
        dict2 (dict): 第二个字典

    Returns:
        dict: 合并后的字典
    """
    if dict2 is not None:
        merged_dict = dict1.copy()
        merged_dict.update(dict2)
        return merged_dict
    else:
        return dict1


