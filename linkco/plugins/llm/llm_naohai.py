import requests
import time
from .main import setting
from ..utils.utils_prompt import get_chat_prompt

from ..utils.utils_data import *
# requests.packages.urllib3.disable_warnings()

url = "http://192.168.202.124:6878/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headers['Host'] = '192.169.202.124:8000'

wait_time = 3

model = ''
tokenizer = ''
def init_model(llm_config=setting['llm']['naohai']):

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


def client_ip(index="dialog", input_data_dict=None):
    '''
    params=""
    if input_data_dict:
        params="?"
        for key in input_data_dict:
            params = params + key + "=" + str(input_data_dict[key]) + "&"
    '''
    print('【input_prompt】', input_data_dict['content_list'][0])
    in_data = json.dumps(input_data_dict)
    url_http_addr_token = url + index
    response = requests.post(url_http_addr_token,  data=in_data, headers=headers)
    print('【脑海】', response.text)
    response = eval(response.text)['response_list'][0]
    return response

def get_chat(prompt,
             history=None,
             system=None,
             max_length=2048,
             top_p=1, temperature=1,
             num_beams=1, do_sample=True, num_keys=0):

    # 将用户输入添加到messages中
    print('【prompt】', prompt)
    if isinstance(prompt, dict):
        prompt = prompt['content']

    messages = [prompt]

    input_data_dict = {'request_type': 0, 'sessionId': "2022092603", 'content_list': messages}

    return client_ip(index="dialog", input_data_dict=input_data_dict)
