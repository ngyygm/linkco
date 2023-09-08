from ..llm.main import get_chat


def get_cut_history(history, cut_len: int = 8192, his_len: int = 8192, max_length: int = 8192):
    """
    缩减历史对话内容，减少字数消耗

    Args:
        history (list): 历史对话列表
        cut_len (int): 截断每个对话内容的长度，默认为-1
        his_len (int): 历史对话长度，默认为-1
        max_length (int): 最大总长度，默认为8192

    Returns:
        list or None: 缩减后的历史对话列表，如果输入的历史对话为None，则返回None
    """
    if history is not None:
        temp_his = [it for it in history]
        temp_his.reverse()

        now_str = ''
        out_his = []
        for it in temp_his:
            out_his.append({'role': it['role'], 'content': it['content'][:cut_len]})
            now_str += '[{}]:{}'.format(it['role'], it['content'][:cut_len])
            if his_len == 0 and len(now_str) < max_length:
                break
            if it['role'] == 'assistant':
                his_len = his_len - 1

        out_his.reverse()
        return out_his
    else:
        return None


def get_relate_history(prompt: str, history_data_list: list):
    """
    判断与问题有关的历史对话，截取history_data_list中与当前的prompt相关的历史对话信息

    Args:
        prompt (str): 当前的问题
        history_data_list (list): 历史对话列表

    Returns:
        list: 与当前问题相关的历史对话信息
    """
    now_sentence = prompt
    for j in range(len(history_data_list)):
        i = len(history_data_list) - j - 1
        temp_sentence = '问:{}\n答:{}\n'.format(history_data_list[i][0][:128].replace('\n', ''),
                                                history_data_list[i][1][:128].replace('\n', ''))

        temp_q = '历史对话:\n{}\n当前提问：“{}”\n请判断当前提问是否满足：'\
                 '\n1. 是不是需要用到历史对话中的内容作为补充或者指代？'\
                 '\n2. 是不是在发表对历史对话内容的疑惑或肯定？'\
                 '\n3. 是不是与历史对话内容处于同一个话题？'\
                 '\n若以上判断有一个为“是”，则直接回复“是”。'\
                 '\n若以上判断都“不是”，则直接回复“不是”。'.format(temp_sentence, now_sentence)

        if '继续' in prompt:
            panduan = '是。'
        else:
            panduan = get_chat(temp_q, [], '')

        if '不是' in panduan:
            return history_data_list[i+1:]
        else:
            now_sentence = history_data_list[i][0][:128]
    return history_data_list


def get_item_history(query: str, response: str):
    """
    获取一问一答的历史对话形式

    Args:
        query (str): 用户提问
        response (str): 机器人回答

    Returns:
        list: 历史对话列表
    """
    out_data = [
        {'role': 'user', 'content': query},
        {'role': 'assistant', 'content': response}
    ]
    return out_data


def get_update_history(query: str, response: str, history: list):
    """
    获取更新的历史对话

    Args:
        query (str): 用户提问
        response (str): 机器人回答
        history (list): 历史对话列表

    Returns:
        None
    """
    history.extend(get_item_history(query, response))
    return history

