import json
from ...main import linkco_path
from ...plugins.llm.main import get_example_chat

with open(linkco_path + 'function/drones/command.txt', 'r', encoding='utf-8') as f:
    tool_list = f.read().split('\n')
    tool_list = [item.split(' - ') for item in tool_list]
f.close()

# 获取回答
def get_response(prompt, history=[], system='', model_nickname=None):

    example_data = {'指令': ['aw.takeoff()', 'aw.land()']}
    rule_list = ['根据提问判断需要使用哪些指令',
                 '根据给定的任务，自动设计功能执行列表',
                 '每个指令()内有需要填的参数，则填入合适的数值',
                 '不需要解释']
    example = ['起飞然后降落', json.dumps(example_data, ensure_ascii=False)]
    # count = 10
    # while count > 0:
    #     try:
    #         response = get_example_chat(prompt=prompt,
    #                                    history=history,
    #                                    system=system,
    #                                    example=example,
    #                                    select=tool_list,
    #                                    rule=rule_list,
    #                                    model_nickname=model_nickname)
    #         response = eval(response)
    #         command_list = response["指令"]
    #         return command_list
    #     except Exception as e:
    #         print(e)
    #         count = count - 1
    #         continue
    response = get_example_chat(prompt=prompt,
                                history=history,
                                system=system,
                                example=example,
                                select=tool_list,
                                rule=rule_list,
                                model_nickname=model_nickname)
    response = eval(response)
    command_list = response["指令"]
    return command_list

    # return example_data["指令"]