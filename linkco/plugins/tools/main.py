import os
import json

from ...main import linkco_module_path, linkco_path
from ..utils.utils_system import load_module
from ..utils.utils_chat import get_cut_history
from ..llm.main import get_example_chat


def get_tool_dict(tool_list: list = None) -> dict:
    """
    获取工具字典

    Args:
        tool_list (list): 工具列表

    Returns:
        dict: 工具字典
    """
    tool_dict = {}
    file_list = os.listdir(linkco_path + '/plugins/tools/')
    file_list = [f[:-3] for f in file_list if 'tool_' in f and 'demo' not in f]

    for item in file_list:
        temp_tool = load_module('{}plugins.tools.{}'.format(linkco_module_path, item)).Tool()
        if tool_list is not None and isinstance(tool_list, list):
            if temp_tool.name in tool_list:
                tool_dict[temp_tool.name] = temp_tool
        else:
            tool_dict[temp_tool.name] = temp_tool
    return tool_dict


def get_switch_tool(prompt: str,
                    history: str = None,
                    system: str = None,
                    tool_dict_list: list = None,
                    model_nickname: str = None) -> list:
    """
    判断使用哪个工具

    Args:
        prompt (str): 输入的提示内容
        history (str): 对话的历史记录
        system (str): 系统名称
        tool_dict_list (list): 工具字典列表
        model_nickname (str): 模型昵称

    Returns:
        list: 工具列表
    """
    temp_history = get_cut_history(history, 64, 2)
    tool_dict = get_tool_dict(tool_dict_list)
    select_dict = {}
    for key in tool_dict.keys():
        select_dict[key] = tool_dict[key].desc
    example = json.dumps({'工具': ['天气搜索']}, ensure_ascii=False)

    temp_prompt = prompt

    rule_list = ['判断需要使用哪些工具',
                 '可以使用多种工具，按顺序排列',
                 '如果历史对话中已经有当前问题所需的内容，就选聊天对话',
                 '不需要使用工具，就选聊天对话',
                 '只能输出选项中有的选项，不允许捏造']
    count = 5
    while count > 0:
        try:
            response = get_example_chat(temp_prompt, temp_history, system, example, select_dict, rule_list, model_nickname)
            response = eval(response)
            tool_names = response["工具"]

            temp_tool_names = []
            for i in range(len(tool_names)):
                tool_name = tool_names[i]
                if tool_name not in tool_dict.keys():
                    for it in tool_dict.keys():
                        if tool_name[:3] in it:
                            temp_tool_names.append(it)
                else:
                    temp_tool_names.append(tool_name)
            tool_names = list(set(temp_tool_names))

            output = [tool_dict[item] for item in tool_names]
            return output
        except Exception as e:
            print(e)
            count = count - 1
            continue
    output = [tool_dict[item] for item in ['聊天对话']]
    return output
