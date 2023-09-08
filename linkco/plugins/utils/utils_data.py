import re
import json
import hashlib

from ...main import llm_response_path


def save_data(response: str, prompt: str, history: str, system: str, save_path: str = llm_response_path) -> None:
    """
    保存数据到指定路径的JSON文件中
    Args:
        response (str): 生成的回复内容
        prompt (str): 输入的提示内容
        history (str): 对话的历史记录
        system (str): 系统名称
        save_path (str): 保存文件的路径，默认为llm_response_path
    Returns:
        None
    """
    if history is None:
        history = []
    if system is None:
        system = ''
    out_json = {
        'system': system,
        'prompt': prompt,
        'response': response,
        'history': history
    }
    # 保存数据
    with open(save_path, 'a', encoding='utf-8') as f2:
        json.dump(out_json, f2, ensure_ascii=False)
        f2.write('\n')


def get_remove_noun(inp_data: str) -> str:
    """
    去除输入数据中的所有标点符号
    Args:
        inp_data (str): 输入的数据
    Returns:
        str: 去除标点符号后的结果
    """
    return re.sub('\W*', '', inp_data)


def get_hash(inp_data: str) -> str:
    """
    计算输入数据的哈希值
    Args:
        inp_data (str): 输入的数据
    Returns:
        str: 哈希值
    """
    md5 = hashlib.md5()  # 应用MD5算法
    md5.update(inp_data.encode('utf-8'))
    return md5.hexdigest()


def get_text_split(text: str, split_len: int = 384, win_len: int = 64, split_icon: str = '\n\n') -> list:
    """
    将文本进行分割处理

    Args:
        text (str): 要分割的文本
        split_len (int, optional): 分割长度。默认为384。
        win_len (int, optional): 重叠长度。默认为64。
        split_icon (str, optional): 分割标志。默认为'\n\n'。

    Returns:
        List[str]: 分割后的文本列表
    """

    if len(text) <= split_len:
        return [text]

    output = text.split(split_icon)
    if all(len(item) <= split_len for item in output):
        return output

    sub_output = []
    for item in output:
        if len(item) <= split_len:
            sub_output.append(item)
        else:
            start = 0
            while start < len(item):
                sub_output.append(item[start: start + split_len])
                start = start + split_len - win_len

    merged_output = []
    merged_item = sub_output[0]
    for item in sub_output[1:]:
        if len(merged_item) + len(item) <= split_len:
            merged_item += item
        else:
            merged_output.append(merged_item)
            merged_item = item
    if len(merged_item) > win_len:
        merged_output.append(merged_item)

    return merged_output