from ...plugins import *

# 获取回答
def get_response(prompt, history=[], system=''):
    results = tool_search_quark.get_response(prompt, out_count=3, news_len=512, if_query=False)
    print('【资料】\n', results)
    results = results[:1024]
    if len(results) > 0:
        prompt = '{}\n\n根据上文内容，生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字），不可抄袭上文'.format(results, prompt)
    else:
        prompt = '生成一篇关于{}的资讯新闻，要求内容丰富，字数多（800字）'.format(results, prompt)
    return get_chat(prompt, history, system)