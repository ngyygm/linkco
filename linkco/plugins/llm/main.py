from ...main import llm_module, setting, linkco_module_path
from ..utils.utils_system import load_module
from ..utils.utils_prompt import *


# 获取当前使用的大模型接口
def init_llm_model(model_name='openai',
                   model_nickname=None,
                   model_config=None):
    '''
    model_name: 当前选择的大模型类型，一般开源的有chatglm6b、rwkv、visualglm6b，或者使用openai
    这些必须是plugins.llm里写好的模型加载方法

    model_config: 当前模型的各种设置参数，格式写在config里，如果传入为空，就用对应的默认值

    model_nickname: 如果是一个系统需要多种模型，比如用了不同的微调方案，同时需要运行两三个模型
    那调用的时候就选linkco.get_chat(nickname,prompt,history,system,...)就可以使用不同模型来处理当前问题
    每个模型默认的model_nickname=model_name
    '''


    temp_config = setting['llm'][model_name]
    if model_config is not None:
        for key in model_config:
            temp_config[key] = model_config[key]

    if model_nickname is None:
        model_nickname = model_name

    # print('【当前模型类型】', model_name)
    # print('【当前模型昵称】', model_nickname)
    # print('【当前模型参数】', temp_config)

    if model_nickname not in llm_module.keys():
        llm_module[model_nickname] = {
            'model': '',
            'tokenizer': '',
            'module': ''
        }

    llm_module[model_nickname]['module'] = load_module('{}plugins.llm.llm_{}'.format(linkco_module_path, model_name))
    model, tokenizer = llm_module[model_nickname]['module'].init_model(temp_config)

    llm_module[model_nickname]['model'] = model
    llm_module[model_nickname]['tokenizer'] = tokenizer
    llm_module[model_nickname]['config'] = temp_config
    return model, tokenizer


# 获取大模型结果
def get_chat(prompt,
             history=None,
             system=None,
             image_path=None,
             max_length=2048,
             top_p=1.0,
             temperature=1.0,
             num_beams=1,
             do_sample=True,
             model_nickname=None):

    if model_nickname is None:
        if len(llm_module) > 0:
            # 如果已经有初始化的模型，默认选第一个为回答模型
            model_nickname = list(llm_module.keys())[0]
        else:
            model_nickname = 'openai'

    # 判断当前是否没有初始化任何大模型
    if model_nickname not in llm_module.keys():
        # 默认初始化模型为当前的model_nickname
        init_llm_model(model_name=model_nickname, model_nickname=model_nickname)

    # print('【当前使用的模型昵称】', model_nickname)

    if llm_module[model_nickname]['config']['image']:
        # try:
        response = llm_module[model_nickname]['module'].get_chat(prompt=prompt,
                                                                history=history,
                                                                system=system,
                                                                image_path=image_path,
                                                                max_length=max_length,
                                                                top_p=top_p,
                                                                temperature=temperature,
                                                                num_beams=num_beams,
                                                                do_sample=do_sample)
        # except:
        #     response = '内容读取错误啦~要不换个试试？'
    else:
        if len(prompt) > 0:
            response = llm_module[model_nickname]['module'].get_chat(prompt=prompt,
                                                            history=history,
                                                            system=system,
                                                            max_length=max_length,
                                                            top_p=top_p,
                                                            temperature=temperature,
                                                            num_beams=num_beams,
                                                            do_sample=do_sample)
        else:
            response = '当前模型输入为空'

    # print('【问题】\n', prompt)
    # print('【回答】\n', response)
    # print('======================================================')
    return response


# 获取大模型结果
def get_stream_chat(prompt,
             history=None,
             system=None,
             image_path=None,
             max_length=2048,
             top_p=1.0,
             temperature=1.0,
             num_beams=1,
             do_sample=True,
             model_nickname=None):

    if model_nickname is None:
        if len(llm_module) > 0:
            # 如果已经有初始化的模型，默认选第一个为回答模型
            model_nickname = list(llm_module.keys())[0]
        else:
            model_nickname = 'openai'

    # 判断当前是否没有初始化任何大模型
    if model_nickname not in llm_module.keys():
        # 默认初始化模型为当前的model_nickname
        init_llm_model(model_name=model_nickname, model_nickname=model_nickname)

    # print('【当前使用的模型昵称】', model_nickname)

    if llm_module[model_nickname]['config']['image']:
        # try:
        for response in llm_module[model_nickname]['module'].get_stream_chat(prompt=prompt,
                                                                             history=history,
                                                                             system=system,
                                                                             image_path=image_path,
                                                                             max_length=max_length,
                                                                             top_p=top_p,
                                                                             temperature=temperature,
                                                                             num_beams=num_beams,
                                                                             do_sample=do_sample):
            yield response
        # except:
        #     response = '内容读取错误啦~要不换个试试？'
    else:
        if len(prompt) > 0:
            for response in llm_module[model_nickname]['module'].get_stream_chat(prompt=prompt,
                                                                                 history=history,
                                                                                 system=system,
                                                                                 max_length=max_length,
                                                                                 top_p=top_p,
                                                                                 temperature=temperature,
                                                                                 num_beams=num_beams,
                                                                                 do_sample=do_sample):
                yield response
        else:
            response = '当前模型输入为空'
            yield response


def get_example_chat(prompt,
                    history=None,
                    system=None,
                    example=None,
                    select=None,
                    rule=None,
                    model_nickname=None,
                    max_length=2048,
                    top_p=0.9,
                    temperature=0.95):

    if system is None:
        system = ''

    select_str = get_select_prompt(select)
    if len(select_str) > 0:
        select_str = '【选项】\n' + select_str

    rule_str = '【要求】\n' + get_rule_prompt(rule)

    if isinstance(example, list):
        if len(example) == 2:
            example = {
                'user': example[0],
                'assistant': example[1]
            }

    example_str = '【示例】\n' + get_example_prompt(example)

    temp_system_list = [it for it in [system, select_str, rule_str, example_str] if len(it) > 0]

    temp_system = '\n'.join(temp_system_list)

    temp_prompt = prompt
    if isinstance(example, dict):
        if isinstance(prompt, str):
            temp_prompt = {}
            keys_list = list(example.keys())
            temp_prompt[keys_list[0]] = prompt
            for keys in keys_list[1:]:
                temp_prompt[keys] = ''
        elif isinstance(prompt, dict):
            temp_prompt = {}
            keys_list = list(example.keys())
            temp_prompt[keys_list[0]] = prompt
            for keys in keys_list:
                if keys in prompt.keys():
                    temp_prompt[keys] = prompt[keys]
                else:
                    temp_prompt[keys] = ''
        elif isinstance(prompt, list):
            temp_prompt = {}
            keys_list = list(example.keys())
            temp_prompt[keys_list[0]] = prompt
            for idx, keys in enumerate(keys_list):
                if idx < len(prompt) - 1:
                    temp_prompt[keys] = prompt[idx]
                else:
                    temp_prompt[keys] = ''


    response = get_chat(prompt=temp_prompt,
                        history=history,
                        system=temp_system,
                        max_length=max_length,
                        top_p=top_p,
                        temperature=temperature,
                        model_nickname=model_nickname)

    return response




