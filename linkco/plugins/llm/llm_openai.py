import requests
import time
import openai
from .main import setting
from ..utils.utils_prompt import get_query_prompt

from ..utils.utils_data import *
# requests.packages.urllib3.disable_warnings()

wait_time = 3
openai_error = 'openai_error'

model = ''
tokenizer = ''
def init_model(llm_config=setting['llm']['openai']):
    openai.api_key = llm_config['apikey']
    return model, tokenizer


# 转换成openai需要的历史对话形式
def get_chatgpt_his(inp_his):
    out_massages = []
    for item in inp_his:
        user_message = {"role": "user", "content": item[0]}
        robot_message = {"role": "assistant", "content": item[1]}
        out_massages.append(user_message)
        out_massages.append(robot_message)
    return out_massages


def get_chat(prompt,
             history=None,
             system=None,
             max_length=2048,
             top_p=1,
             temperature=1,
             num_beams=1,
             do_sample=True,
             n=1,
             presence_penalty=0,
             frequency_penalty=0,
             stop=None,
             model_name='gpt-3.5-turbo'):

    print('【prompt】\t', prompt)
    print('【history】\t', history)
    print('【system】\t', system)

    his_messages = []
    if history is not None:
        for it in history:
            msg_item = {
                "role": '',
                "content": it['content']
            }
            if it['role'] in ['system', 'user', 'assistant']:
                msg_item['role'] = it['role']
            else:
                msg_item['role'] = 'system'
                msg_item['content'] = '[{}]:{}'.format(it['role'], msg_item['content'])
            his_messages.append(msg_item)

    # messages = get_chatgpt_his(temp_history)
    temp_messages = []

    if system is not None and len(system) > 0:
        system_message = {"role": "system", "content": system}
        # 将用户输入添加到messages中
        temp_messages.append(system_message)

    for item in his_messages:
        temp_messages.append(item)

    if isinstance(prompt, dict):
        user_message = {"role": "user", "content": get_query_prompt(prompt)}
    else:
        user_message = {"role": "user", "content": prompt}
    # 将用户输入添加到messages中
    temp_messages.append(user_message)
    print('【openai调用输入】\t', temp_messages)

    # 创建一个 GPT-3 请求
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=temp_messages,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_length,
        n=n,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        stop=stop,
    )

    robot_message = response.choices[0].message.content
    # 保存生成的数据
    save_data(robot_message, prompt, history, system)
    print('【openai调用结果】\t', robot_message)
    return robot_message


def get_stream_chat(prompt,
                    history=None,
                    system=None,
                    max_length=2048,
                    top_p=1,
                    temperature=1,
                    num_beams=1,
                    do_sample=True,
                    n=1,
                    presence_penalty=0,
                    frequency_penalty=0,
                    stop=None,
                    model_name='gpt-3.5-turbo'):

    print('【prompt】\t', prompt)
    print('【history】\t', history)
    print('【system】\t', system)

    his_messages = []
    if history is not None:
        for it in history:
            msg_item = {
                "role": '',
                "content": it['content']
            }
            if it['role'] in ['system', 'user', 'assistant']:
                msg_item['role'] = it['role']
            else:
                msg_item['role'] = 'system'
                msg_item['content'] = '[{}]:{}'.format(it['role'], msg_item['content'])
            his_messages.append(msg_item)

    # messages = get_chatgpt_his(temp_history)
    temp_messages = []

    if system is not None and len(system) > 0:
        system_message = {"role": "system", "content": system}
        # 将用户输入添加到messages中
        temp_messages.append(system_message)

    for item in his_messages:
        temp_messages.append(item)

    if isinstance(prompt, dict):
        user_message = {"role": "user", "content": get_query_prompt(prompt)}
    else:
        user_message = {"role": "user", "content": prompt}
    # 将用户输入添加到messages中
    temp_messages.append(user_message)
    print('【openai调用输入】\t', temp_messages)

    # 创建一个 GPT-3 请求
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=temp_messages,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_length,
        n=n,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        stop=stop,
        stream=True,
    )
    robot_message = ''
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta'].keys():
            robot_message += chunk['choices'][0]['delta']['content']
            yield robot_message

    # # 保存生成的数据
    # save_data(robot_message, prompt, history, system)
    # print('【openai调用结果】\t', robot_message)
    # return robot_message
