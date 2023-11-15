from linkco import get_chat
from linkco import search_from_vector_database

import time
import json


# 获取回答
def get_response(prompt,
                 history=None,
                 system=None,
                 max_length=2048,
                 top_p=0.9,
                 temperature=0.9,
                 result_num=3,
                 model_nickname=None,
                 database=None
                 ):
    if database is None:
        raise ValueError(f"未发现需要查询的数据库，请输入正确的数据库database")
    # 搜索最相关的文本
    start_time = time.time()
    result = search_from_vector_database(database, prompt, result_num)
    print('【向量库搜索耗时】', time.time() - start_time)
    data_str = '\n'.join([it['content'] for it in result])
    for it in result:
        data_str += it['content']
        print(it['score'])
        print(it['content'])
        print('=========================')

    results = data_str[:1024]
    if history is None:
        history = []

    if len(results) > 0:
        history.append({"role": "observation", "content": json.dumps({"资料": results}, ensure_ascii=False, indent=2)})
        prompt = '根据资料内容，生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字），不可抄袭上文'.format(prompt)
    else:
        prompt = '生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字）'.format(prompt)

    return get_chat(prompt, history, system,
                    max_length=max_length,
                    top_p=top_p,
                    temperature=temperature,
                    model_nickname=model_nickname)