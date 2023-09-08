import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析页面
import os
import re  # 用正则表达式提取url
import json
import time
import random
import threading

from ...main import base_path, headers_list

from ..utils.utils_vector import create_vector_database, search_from_vector_database, load_vector_database
from ..utils.utils_data import get_remove_noun
from ..utils.utils_chat import get_cut_history
from ..utils.utils_time import get_now_datetime
from ..utils.utils_web import get_url_real_content
from ..utils.utils_prompt import get_history_prompt, get_rule_prompt, get_example_prompt

from ..llm.main import get_chat

requests.packages.urllib3.disable_warnings()

quark_data_save_path = base_path + 'quark_search/'

db_name = 'quark_db'
min_score = 400

# 伪装浏览器请求头
headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive",
    "accept-Encoding": "gzip, deflate, br",
    'content-Type': 'text/html;charset=utf-8',
    # 需要更换Cookie
    'cookie': 'sm_uuid=21c12bf0ed95088aa4557c8ec530abf8|||1683785254; sm_diu=21c12bf0ed95088aa4557c8ec530abf8||11eef166754d97370f|1683785254; sm_ruid=8124162926fe07e627edc6f7b1388940|||1683785255; cna=cgCVG9SeICMCAXjtEjlQxc/U; __itrace_wid=1851fadd-9c90-48c0-25cb-68ef64e3ec5c; sm_sid=1ba5642c6b5b5b500fcb0af3f5297120; phid=1ba5642c6b5b5b500fcb0af3f5297120; isg=BHNzJhRpE0Y5Z98Sk2iCtdzfAnedqAdqUirFMCUQyBLJJJPGrXlkutE12hRvhF9i'
   }

wait_time = 3

# 多线程
def run(num, result_list):
    clear_href = ['javascript', 'weibo']
    clear_title = ['图片', '地图']
    global out_data, lock
    for result in result_list:
        temp_data = {}
        try:
            title = result.find('a').text
            href = result.find('a')['href']
            flag_href = True
            for it in clear_href:
                if it in href:
                    flag_href = False
            flag_title = True
            for it in clear_title:
                if it in title[-3:]:
                    flag_title = False
            if flag_href and flag_title:
                # real_url = get_real_url(v_url=href)
                real_url = href
                temp_content = get_url_real_content(real_url)
                if len(temp_content) > 3:
                    temp_data['title'] = "[" + title + "](" + real_url + ")"
                    # temp_data['url'] = real_url
                    temp_data['content'] = temp_content
                    lock.acquire()
                    out_data.append(temp_data)
                    lock.release()
        except Exception as e:
            pass


class Tool():
    def __init__(self):
        self.name = '网络搜索'
        self.desc = '如果涉及到一些专业知识和实时性信息，需要查阅一些资料或者与资讯，可以使用该功能进行网络搜索。'

    # 做数据切分
    def cut_data(self, inp_str, split_len=384, split_step=3):
        out_put = []
        count = 0
        while count + split_len < len(inp_str):
            out_put.append(inp_str[count: count + split_len])
            count += int(split_len / split_step)
        out_put.append(inp_str[count:])

        return out_put

    # 拼接list
    def concat_data(self, inp_list, data_len=0):
        if len(inp_list) == 0:
            return inp_list
        temp_sentence_list = [inp_list[0]]
        for i in range(1, len(inp_list)):
            for j in range(len(temp_sentence_list)):
                prefix = os.path.commonprefix([temp_sentence_list[j], inp_list[i]])
                if temp_sentence_list[j].index(prefix) == 0:
                    temp_sentence_list[j] = inp_list[i].replace(prefix, '') + temp_sentence_list[j].replace(prefix, '')
                elif inp_list[i].index(prefix) == 0:
                    temp_sentence_list[j] = temp_sentence_list[j].replace(prefix, '') + inp_list[i].replace(prefix, '')
                else:
                    temp_sentence_list.append(inp_list[i])
        if data_len == len(temp_sentence_list):
            return inp_list
        else:
            return self.concat_data(temp_sentence_list, len(temp_sentence_list))

    def get_response(self,
                     prompt,
                     history=None,
                     system=None,
                     out_count=2,
                     news_len=768,
                     if_query=True,
                     model_nickname=None):

        prompts = [prompt]

        if not if_query:
            # 如果当前传入的内容是一段聊天，需要二次提取问题，则进行问题提取

            if history is not None:
                temp_history = [it for it in get_cut_history(history, 256, 3)]
            else:
                temp_history = []
            example_data = {'问题': ['', '']}

            rule_list = ['根据当前提问和历史对话，提取出需要进行网络搜索的问题列表',
                         '需要进行网络搜索的内容可能存在多个，都要写出来',
                         '每个问题都要求信息完整，内容明确'
                         ]

            temp_history.append({'role': 'data', 'content': '当前时间:{}'.format(get_now_datetime())})
            role_dict = {
                'user': '问',
                'assistant': '答'
            }
            history_prompt = get_history_prompt(temp_history, role_dict)
            rule_prompt = get_rule_prompt(rule_list)
            example_prompt = get_example_prompt(json.dumps(example_data, ensure_ascii=False))

            temp_prompt = '历史对话:' \
                          '\n{}' \
                          '\n当前提问:{}' \
                          '\n\n要求:' \
                          '\n{}' \
                          '\n示例:' \
                          '\n{}'.format(history_prompt,
                                        prompt,
                                        rule_prompt,
                                        example_prompt)

            # print('【temp_prompt】', temp_prompt)
            # quit()
            count = 5
            while count > 0:
                try:
                    response = get_chat(prompt=temp_prompt,
                                        model_nickname=model_nickname)
                    response = eval(response)
                    prompts = response['问题']
                    break
                except Exception as e:
                    print(e)
                    count = count - 1
                    time.sleep(wait_time)

        out_results = ''
        for prompt_item in prompts[:3]:
            # print('【相似度搜问题】', prompt_item)
            response_d = []
            try:
                response_d = search_from_vector_database(db_name, prompt_item, out_count, min_score)
            except Exception as e:
                print(e)
            if len(response_d) == 0:
                dict_url = {
                    'from': 'kkframenew',
                    'predict': '1',
                    'search_id': 'AAPBzJ1CaZFx2dd3XIbnp6R%2FLWvCQv98%2BoR2I9e5pWcKAg%3D%3D_1683739677820',
                    'round_id': '-1',
                    'pdtt': '1683739678',
                    'uc_param_str': 'dnntnwvepffrbijbprsvchgputdemennosstodcaaapcgidsdieini',
                    'q': prompt_item,
                    'hid': 'baab53e0a589438df41d09c0f3d7e28e',
                    'extra_params': 'AAMplgqv4M50rgwSUug44KAhyR0xzLyTyYJmt4JFwQQ7zA%3D%3D',
                    'qshare_entry': 'clipboard'
                }
                url = 'https://quark.sm.cn/s?'
                for item in dict_url.keys():
                    url += item + '={}&'.format(dict_url[item])
                url = url[:-1]
                temp_headers = random.sample(headers_list, 1)[0]
                headers['user-agent'] = temp_headers['user-agent']

                html = ''
                count = 5
                while count > 0:
                    try:
                        r = requests.get(url,
                                         headers=headers,
                                         timeout=wait_time,
                                         verify=False)
                        break
                    except Exception as e:
                        print(e)
                        count = count - 1
                        time.sleep(wait_time)

                html = r.text
                soup = BeautifulSoup(html, 'html.parser')
                result_list = []
                result_list.extend(soup.find_all(class_='c-container'))
                result_list.extend(soup.find_all(class_='c-theme-olympic c-theme-quark'))
                result_list.extend(soup.find_all(class_='c-flex c-flex-bottom'))

                global out_data, lock
                out_data = []

                thread_list = []
                thread_num = 8
                lock = threading.Lock()

                content_datas_list = []
                for i in range(thread_num):
                    content_datas_list.append(result_list[int((i) * (len(result_list) / thread_num)): int(
                        (i + 1) * (len(result_list) / thread_num))])

                for i in range(thread_num):
                    thread = threading.Thread(target=run, args=[i, content_datas_list[i]])

                    thread.start()
                    thread_list.append(thread)

                for t in thread_list:
                    t.join()

                weibo_list = []
                weibo_list.extend(soup.find_all(class_='M_Other_Weibo_strong_Dilu_weibo_strong'))
                for weibo in weibo_list:
                    temp_data = {}
                    url_list = weibo.find_all(
                        class_='c-paragraph--v1_0_0 c-flex c-flex-center-y c-font-darkest c-font-m c-font-normal c-margin-top-s c-weibo-expression c-font-l')
                    url_list = [it['href'] for it in url_list]

                    dice_list = weibo.find_all(class_='js-c-paragraph-text')
                    dice_list = [it.text for it in dice_list]

                    for i in range(len(dice_list)):
                        temp_content = dice_list[i]
                        title = '【来源微博】:{}'.format(temp_content[:16])
                        real_url = ''
                        if i < len(url_list) - 1:
                            real_url = url_list[i]
                        temp_data['title'] = "[" + title + "](" + real_url + ")"
                        temp_data['content'] = temp_content
                        out_data.append(temp_data)

                # print('【out_data】', len(out_data))
                # 这里会创建一个文件夹quark_search，用来保存所有搜索到的数据
                if not os.path.exists(quark_data_save_path):
                    os.makedirs(quark_data_save_path)
                # 保存数据
                file_list = []
                for it in out_data:
                    if '(http' in it['title']:
                        temp_title = it['title'].split('(http')[0]
                    else:
                        temp_title = it['title']
                    temp_title = get_remove_noun(temp_title)
                    save_path = quark_data_save_path + temp_title
                    if os.path.exists(save_path):
                        with open(save_path, 'r', encoding='utf-8') as f:
                            temp_data = f.read()
                        f.close()
                        temp_content = it['content'].split('\n')
                        for it_content in temp_content:
                            if it_content not in temp_data:
                                with open(save_path, 'a', encoding='utf-8') as f:
                                    f.write('\n' + it_content)
                                f.close()
                    else:
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(it['content'])
                        f.close()
                    file_list.append(save_path)

                # 把下载来的数据，保存到向量数据库中
                create_vector_database(db_name, file_list, split_len=768)

                # 判断检索到的知识是否与当前问题相关
                response_d = search_from_vector_database(db_name, prompt_item, out_count, min_score+100)

            # for item in response_d:
            #     print('{}\t{}'.format(item['score'], item['content'][:128].replace('\n', '')))
            results = ''.join([re.sub('\n', '', it['content']) for it in response_d])
            out_results += '{}\n{}\n\n'.format(prompt_item, results[:news_len])

        return out_results