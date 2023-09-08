import json
import re

extraction_keyword = '[{}]'


def get_select_prompt(select: list or dict or str) -> str:
    """
    获取选择的提示

    Args:
        select (list or dict or str): 选择项

    Returns:
        str: 选择的提示字符串
    """
    if select is None or len(select) == 0:
        return ''

    if isinstance(select, dict):
        return '\n'.join([(extraction_keyword + ' - {}').format(key, value) for key, value in select.items()])

    if isinstance(select, list):
        select_items = [select] if not any(isinstance(item, list) for item in select) else select
        return '\n'.join([(' - '.join([(extraction_keyword).format(item_list[0])] + [item for item in item_list[1:]])) for item_list in select_items])

    return (extraction_keyword + '\n').format(select)


def get_system_prompt(system: str) -> str:
    """
    获取系统信息的提示

    Args:
        system (str): 系统信息

    Returns:
        str: 系统信息的提示字符串
    """
    if system:
        return '【SYSTEM START】\n{}\n【SYSTEM END】\n\n'.format(system)
    return ''


def get_history_prompt(history: list, role: dict = None, if_end_round: bool = False) -> str:
    """
    获取历史对话的提示

    Args:
        history (list): 历史对话记录
        role (dict) : 当前角色替换词典

    Returns:
        str: 历史对话的提示字符串
    """
    if history is None or len(history) == 0:
        return ''

    prompt_str = '[Round 0]\n'
    round_id = 0

    for idx, it in enumerate(history):
        if isinstance(it, dict):
            role_item = it.get('role')
            content_item = it.get('content')

            prompt_str += '[{}]:{}\n'.format(role_item, content_item)

            if role_item == 'assistant' and idx != len(history) - 1:
                round_id += 1
                prompt_str += '[Round {}]\n'.format(round_id)

        elif isinstance(it, list):
            role_item, content_item = it[0], it[1]

            round_id += 1
            prompt_str += '[user]:{}\n[assistant]:{}\n'.format(role_item, content_item)

            if idx != len(history) - 1:
                prompt_str += '[Round {}]\n'.format(round_id)

        else:
            round_id += 1
            prompt_str += '{}\n'.format(it)

            if idx != len(history) - 1:
                prompt_str += '[Round {}]\n'.format(round_id)

    if if_end_round:
        prompt_str += '[Round {}]\n'.format(round_id)

    if role is not None:
        for key in role.keys():
            prompt_str = prompt_str.replace('[{}]'.format(key), '[{}]'.format(role[key]))

    return prompt_str


def get_query_prompt(query: dict or str, response: str = '', role: dict = None) -> str:
    """
    获取当前问题的提示

    Args:
        query (dict or str): 当前问题
        response (str) : 当前回答
        role (dict) : 当前角色替换词典

    Returns:
        str: 当前问题的提示字符串
    """
    if isinstance(query, dict):
        prompt_str = ''
        for item in query.items():
            prompt_str += '[{}]:{}\n'.format(*item)
    else:
        prompt_str = '[user]:{}\n[assistant]:{}'.format(query, response)

    if role is not None:
        for key in role.keys():
            prompt_str = prompt_str.replace('[{}]'.format(key), '[{}]'.format(role[key]))

    return prompt_str


def get_example_prompt(example: list or dict or str, history: list or None = None) -> str:
    """
    获取示例的提示

    Args:
        example (list or dict or str): 示例内容
        history (list or None): 历史对话记录

    Returns:
        str: 示例的提示字符串
    """
    prompt_str = get_history_prompt(history) if history is not None else ''

    if isinstance(example, list):
        for it in example:
            if isinstance(it, list):
                temp_it = [ii for ii in it]
                temp_it[0] = (extraction_keyword).format(temp_it[0])
                prompt_str += ' - '.join(temp_it) + '\n'
            else:
                prompt_str += (extraction_keyword + '\n').format(it)
    elif isinstance(example, dict):
        for key, value in example.items():
            prompt_str += (extraction_keyword + ':{}\n').format(key, value)
    else:
        prompt_str += '{}\n'.format(example)

    return prompt_str


def get_rule_prompt(rule: list or dict or str) -> str:
    """
    获取要求规则的提示

    Args:
        rule (list or dict or str): 要求规则

    Returns:
        str: 要求规则的提示字符串
    """
    if isinstance(rule, list):
        rule_list = ['{}. {}'.format(i + 1, item) for i, item in enumerate(rule)]
        rule_list.append('{}. {}'.format(len(rule) + 1, '按照示例提供的形式输出结果'))
        return '\n'.join(rule_list)
    elif isinstance(rule, dict):
        rule_list = ['{} - {}'.format(key, value) for key, value in rule.items()]
        rule_list.append('直接按照示例提供的形式输出结果')
        return '\n'.join(rule_list)
    else:
        return '{}\n按照示例提供的形式输出结果\n'.format(rule)


def get_chat_prompt(query: dict or str, history: list or None, system: str or None, role: dict or None) -> str:
    """
    获取普通模型对话通用模板的提示

    Args:
        query (dict or str): 当前提问
        history (list or None): 历史对话记录
        system (str or None): 系统信息

    Returns:
        str: 普通模型对话通用模板的提示字符串
    """
    system_str = get_system_prompt(system)
    his_str = get_history_prompt(history, if_end_round=True)
    query_str = get_query_prompt(query)

    prompt_str = system_str + his_str + query_str

    if role is not None:
        for key in role.keys():
            prompt_str = prompt_str.replace('[{}]'.format(key), '[{}]'.format(role[key]))

    return prompt_str