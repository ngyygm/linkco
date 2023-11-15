from linkco import get_chat
from linkco import tool_search_quark

import json

# 获取回答
def get_response(prompt, history=None, system=None, model_nickname=None):
    tool = tool_search_quark.Tool()
    results = tool.get_response(prompt, history, system, out_count=3, news_len=512)
    print('【资料】\n', results)
    results = results[:1024]

    if history is None:
        history = []

    if len(results) > 0:
        history.append({"role": "observation", "content": json.dumps({"资料": results}, ensure_ascii=False, indent=2)})
        prompt = '根据资料内容，生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字），不可抄袭上文'.format(prompt)
    else:
        prompt = '生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字）'.format(prompt)


    return get_chat(prompt, history, system, model_nickname=model_nickname)