from ...plugins.llm.main import get_chat
from ...plugins.utils.utils_vector import load_vector_database, search_from_vector_database

import time


# 获取回答
def get_response(db_name,
                 prompt,
                 history=None,
                 system=None,
                 max_length=2048,
                 top_p=0.9,
                 temperature=0.9,
                 result_num=3,
                 model_nickname=None,
                 db_path=None,
                 ):
    print('【加载向量库】', db_name)
    load_vector_database(db_name, db_path)
    # 搜索最相关的文本
    start_time = time.time()
    result = search_from_vector_database(db_name, prompt, result_num)
    print('【向量库搜索耗时】', time.time() - start_time)
    data_str = '\n'.join([it['content'] for it in result])
    for it in result:
        data_str += it['content']
        print(it['score'])
        print(it['content'])
        print('=========================')
    results = data_str[:1024]
    if len(results) > 0:
        prompt = '{}\n\n根据上文内容，生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字），不可抄袭上文'.format(results, prompt)
    else:
        prompt = '生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字）'.format(results, prompt)
    return get_chat(prompt, history, system,
                    max_length=max_length,
                    top_p=top_p,
                    temperature=temperature,
                    model_nickname=model_nickname)