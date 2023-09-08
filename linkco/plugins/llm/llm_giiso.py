import requests
import time
import random

from ...main import headers_list
from ..utils.utils_prompt import *

requests.packages.urllib3.disable_warnings()


from ..utils.utils_data import *
from .main import setting

wait_time = 3
openai_error = 'openai_error'
api_key = ''

model = ''
tokenizer = ''
def init_model(llm_config=setting['llm']['openai']):
    global api_key
    api_key = llm_config['apikey']
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
             top_p=1, temperature=1,
             num_beams=1, do_sample=True):
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

    temp_messages = []

    if system is not None and len(system) > 0:
        system_message = {"role": "system", "content": system}
        # 将用户输入添加到messages中
        temp_messages.append(system_message)

    temp_messages.extend(his_messages)

    if isinstance(prompt, str):
        user_message = {"role": "user", "content": prompt}
    else:
        user_message = {"role": "user", "content": get_query_prompt(prompt)}
    # 将用户输入添加到messages中
    temp_messages.append(user_message)

    # print('【当前输入到Giiso】')
    # for it in temp_messages:
    #     print('[{}]:{}'.format(it['role'], it['content']))

    # quit()

    # 设置代理服务器的地址和端口
    # ChatGPT API的URL
    url = "http://43.130.153.62:5501/openai"
    data = {'api_key': api_key,
            'model': "gpt-3.5-turbo",
            'text': json.dumps(temp_messages),
            'top_p': top_p,
            'temperature': temperature,
            'max_tokens': max_length
            }
    headers = random.sample(headers_list, 1)[0]
    paras = requests.post(url, headers=headers, data=data, timeout=wait_time*50, verify=False).json()
    robot_message = paras['data']
    # 保存生成的数据
    save_data(robot_message, prompt, history, system)
    return robot_message
