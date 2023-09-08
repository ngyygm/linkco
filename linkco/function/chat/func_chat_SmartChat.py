from ...plugins.llm.main import get_chat
from ...plugins.tools.main import get_switch_tool
from ...main import llm_module
from ...plugins.utils.utils_data import save_data


# 获取回答
def get_response(prompt,
                 history=None,
                 system=None,
                 max_length=1024,
                 top_p=0.95, temperature=1,
                 image_path=None,
                 model_nickname=None):
    # print('【prompt】', prompt)
    # print('【history】', history)
    # print('【system】', system)
    # print('【model_nickname】', model_nickname)
    query = prompt
    temp_response= ''
    if len(system) == 0:

        tools = get_switch_tool(prompt, history, '')
        tool_result = ''

        if len(tools) > 0:
            tool = tools[0]
            yield '使用{}中...'.format(tool.name), []
            tool_result = tool.get_response(prompt, history, '')
            print('【工具】{}'.format(tool.name))
            temp_response = temp_response + '{}: \n{}\n\n'.format(tool.name, tool_result[:256] + '...')
            yield temp_response, []
            if len(tool_result) > 0:
                history.append({'role': 'data', 'content': tool_result})
                # query = '{}的结果：\n{}\n\n请结合上述内容回答：\n{}'.format(tool.name, tool_result[:512], prompt)

            # if tool.name == '网络搜索':
            #     print('【网络搜索 问题】\n', query)
            #
            #     response = get_chat(query,
            #                         history,
            #                         system,
            #                         max_length=max_length,
            #                         top_p=top_p,
            #                         temperature=temperature,
            #                         model_nickname='linkco')
            #
            #     # new_history = history + [{'role': 'data', 'content': tool_result[:512]}, {'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]
            #     # save_data(response, prompt, new_history, system)
            #     new_history = history + [{'role': 'user', 'content': prompt},
            #                              {'role': 'assistant', 'content': response}]
            #
            #     yield response, new_history
            #     return response, new_history


    print('【其他回答 问题】\n', query)

    for response in llm_module[model_nickname]['module'].stream_chat(query,
                                                                     history,
                                                                     system,
                                                                     max_length=max_length,
                                                                     top_p=top_p,
                                                                     temperature=temperature):
        new_history = history + [{'role': 'user', 'content': query},
                                 {'role': 'assistant', 'content': response}]

        yield temp_response + response, new_history