import json
from ...main import linkco_path
from ...plugins.llm.main import get_chat
from ...plugins.utils.utils_prompt import get_select_prompt, get_example_prompt

with open(linkco_path + 'function/drones/command.txt', 'r', encoding='utf-8') as f:
    tool_list = f.read().split('\n')
    tool_list = [item.split(' - ') for item in tool_list]
f.close()

# 获取回答
def get_response(prompt, history=[], system='', model_nickname=None):
    example_data = {'指令': ['aw.takeoff()']}
    rule_list = ['根据提问判断需要使用哪些指令',
                 '根据给定的任务，自动设计功能执行列表',
                 '每个指令()内有需要填的参数，则填入合适的数值',
                 '不需要解释']
    example = json.dumps(example_data, ensure_ascii=False)

    select_str = get_select_prompt(tool_list)
    # rule_str = get_rule_prompt(rule_list)

    rule_str = '请根据上文内容，判断需要使用中哪些指令？' \
               '\n根据给定的任务，自动设计功能执行列表。' \
               '\n每个指令()内有需要填的参数，则填入合适的数值。' \
               '\n不需要解释。\n'

    example_str = '示例：\n' + get_example_prompt(example)

    inp_prompt = system + '\n以下是一些无人机指令：\n{}' \
                          '\n{}' \
                          '\n问：{}' \
                          '\n\n用以下格式输出。' \
                          '\n{}'.format(select_str, rule_str, prompt, example_str)

    response = get_chat(prompt=inp_prompt,
                        model_nickname=model_nickname)
    response = eval(response)
    command_list = response["指令"]
    return command_list